"""Multi-agent system: Story Expert, Planner, Coding Agent with TPA format."""
from typing import Optional

from openai import OpenAI

import config
from rag import get_full_docs, get_rag_context_for_step


def _call_chat(
    client: OpenAI,
    model: str,
    messages: list,
    api_key: Optional[str] = None,
) -> str:
    """Call Chat Completions API (for GPT 4.1, 5.1)."""
    kwargs = {"model": model, "messages": messages}
    if api_key:
        kwargs["api_key"] = api_key
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content or ""


def _call_responses(
    client: OpenAI,
    model: str,
    input_text: str,
    api_key: Optional[str] = None,
) -> str:
    """Call Responses API (for Codex). client.responses.create()"""
    kwargs = {
        "model": model,
        "input": input_text,
        "reasoning": {"effort": "high"},
    }
    result = client.responses.create(**kwargs)
    # response.output_text is the primary output
    if hasattr(result, "output_text") and result.output_text:
        return result.output_text
    # Fallback: traverse output items
    if hasattr(result, "output") and result.output:
        texts = []
        for item in result.output:
            if hasattr(item, "content") and item.content:
                for block in item.content:
                    if hasattr(block, "text") and block.text:
                        texts.append(block.text)
        if texts:
            return "\n".join(texts)
    return str(result) if result else ""


def run_story_expert(
    client: OpenAI,
    story_input: str,
    model: str,
    api_key: Optional[str] = None,
) -> str:
    """
    Agent 1: Story Expert - expand natural language into full 奇遇 (encounter) story.
    TPA: Thinking (analyze) -> Planning (structure) -> Action (write).
    """
    system_prompt = """你是一位专业的游戏剧情设计师和故事专家。你的任务是将玩家输入的简短故事梗概，扩写为一个完整的、可用于LUA脚本实现的「奇遇」剧本。

请按照以下 TPA 格式输出：

## Thinking (思考)
- 分析用户输入的故事核心要素
- 识别关键角色、地点、冲突、奖励

## Planning (规划)
- 设计奇遇的起承转合
- 明确NPC行为、玩家选择分支、奖励发放逻辑

## Action (输出)
输出扩写后的完整奇遇故事，包含：
1. 奇遇ID与名称
2. 触发位置与范围描述
3. 参与NPC及其角色
4. 详细剧情流程（对话、选择、战斗、奖励）
5. 使用的道具/装备ID（从DT_Items等表中选择：TestSword, FireSword, Helmet, Money 等）
"""

    user_msg = f"请将以下故事扩写为完整的奇遇剧本：\n\n{story_input}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]

    return _call_chat(client, model, messages, api_key)


def run_planner(
    client: OpenAI,
    expanded_story: str,
    model: str,
    api_key: Optional[str] = None,
) -> str:
    """
    Agent 2: Planner - break down into steps following rule.md workflow.
    TPA format output with step list.
    """
    full_rules = get_full_docs()

    system_prompt = """你是一位LUA奇遇系统开发规划师。根据 rule.md 的设计规则，将扩写后的奇遇故事分解为可执行的开发步骤。

规则中的标准流程：
1. Setup 初始化地图
2. Build 世界
3. 生成常驻 NPC（可选）
4. 注册多个 Encounter
5. StartGame + Resume Time

请按 TPA 格式输出：

## Thinking
- 分析故事需要哪些组件（Setup/Encounter/等）
- 确定每个Encounter的参数

## Planning
列出具体步骤，每步格式：
Step N: [步骤名] - [简述] - 需查资料: [lua_api/rule_section]

例如：
Step 1: Setup_World - 创建地图、Block、建筑 - 需查: Env API, Setup规范
Step 2: SpawnEncounter_XXX - 奇遇XXX - 需查: World.SpawnEncounter, Encounter规范

## Action
输出结构化的步骤JSON（供后续Coding Agent使用）：
{
  "steps": [
    {"id": 1, "name": "Setup_World", "type": "setup", "description": "..."},
    {"id": 2, "name": "SpawnEncounter_xxx", "type": "encounter", "description": "..."}
  ]
}
"""

    user_msg = f"""规则文档：
{full_rules[:15000]}

---
扩写后的奇遇故事：
{expanded_story}

请按上述TPA格式规划开发步骤。"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]

    return _call_chat(client, model, messages, api_key)


def run_coding_agent(
    client: OpenAI,
    step: dict,
    expanded_story: str,
    previous_code: str,
    model: str,
    api_key: Optional[str] = None,
) -> str:
    """
    Agent 3: Coding Agent - generate LUA code for each step.
    Uses RAG to inject relevant docs. TPA format.
    """
    step_name = step.get("name", "unknown")
    step_desc = step.get("description", "")
    step_type = step.get("type", "general")

    rag_context = get_rag_context_for_step(step_name, f"{step_desc} {step_type}")

    use_codex = "codex" in model.lower()
    system_prompt = f"""你是一位精通LUA和CineText/Narrative API的资深程序员。根据提供的规则和API文档，为当前步骤生成**绝对正确**的LUA脚本。

## Thinking (思考)
- 分析本步骤需要使用的API
- 检查是否符合 rule.md 中的硬性规则（防重复触发、合法性检查、奖励必须GiveItem/GiveWeapon/GiveEquip等）

## Planning (规划)
- 列出将调用的API及参数
- 确认命名规范（encXX_角色名）

## Action (输出)
**只输出可运行的LUA代码**，不要输出思考过程。代码必须：
1. 严格遵循 lua_atomic_modules_call_guide.md 中的API用法
2. 遵循 rule.md 中的 Encounter/Setup 规范
3. 使用正确的 FVector 格式 {{X=..., Y=..., Z=...}}
4. Encounter 必须有 _G.encXX_done 防重复
5. 必须对 player 和 NPC 做 IsValid 检查
"""

    user_msg = f"""=== 本步骤 RAG 资料 ===
{rag_context[:12000]}

=== 当前步骤 ===
名称: {step_name}
类型: {step_type}
描述: {step_desc}

=== 扩写故事（剧情参考）===
{expanded_story[:3000]}

=== 已生成的前序代码（如有）===
{previous_code[:2000] if previous_code else "（无）"}

请生成本步骤的LUA代码。只输出代码，不要markdown包裹。"""

    if use_codex:
        full_input = f"{system_prompt}\n\n{user_msg}"
        return _call_responses(client, model, full_input, api_key)
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ]
        return _call_chat(client, model, messages, api_key)


def extract_steps_from_planner_output(plan_output: str) -> list:
    """Parse planner output to get step list."""
    import json
    import re

    # Try to find JSON block
    match = re.search(r"\{[\s\S]*\"steps\"[\s\S]*\}", plan_output)
    if match:
        try:
            data = json.loads(match.group(0))
            return data.get("steps", [])
        except json.JSONDecodeError:
            pass

    # Fallback: infer from text
    steps = []
    for m in re.finditer(r"Step\s+(\d+):\s*(\w+)[\s\-]+(.+?)(?=Step\s+\d+:|$)", plan_output, re.DOTALL):
        steps.append({
            "id": int(m.group(1)),
            "name": m.group(2).strip(),
            "description": m.group(3).strip()[:200],
            "type": "encounter" if "enc" in m.group(2).lower() else "setup",
        })
    return steps if steps else [{"id": 1, "name": "SpawnEncounter_main", "type": "encounter", "description": "Main encounter from story"}]
