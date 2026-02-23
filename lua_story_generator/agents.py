"""Multi-agent system: Story Expert, Planner, Coding Agent with Skills + TPA + Feedback."""
import json
import re
from typing import Optional

from openai import OpenAI

import config
from skills_loader import get_full_docs, get_skill_for_step


def _call_chat(
    client: OpenAI,
    model: str,
    messages: list,
) -> str:
    """Call Chat Completions API (for GPT 4.1, 5.1)."""
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content or ""


def _call_responses(
    client: OpenAI,
    model: str,
    input_text: str,
) -> str:
    """Call Responses API (for Codex). client.responses.create()"""
    result = client.responses.create(
        model=model,
        input=input_text,
        reasoning={"effort": "high"},
    )
    if hasattr(result, "output_text") and result.output_text:
        return result.output_text
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
) -> str:
    """Agent 1: Story Expert - expand natural language into full 奇遇."""
    system_prompt = """你是一位专业的游戏剧情设计师。将玩家输入的简短故事梗概扩写为完整的、可用于LUA脚本实现的「奇遇」剧本。

**重要**：
1. 若故事涉及对弈、比赛、赌局、棋类、猜拳等，获胜/失败有不同结果，必须标注「需调用 UI.PlayMiniGame」，并写明赢/输分支。
2. **单一事件**（对弈、赌局、当场对话分支等）应**合并为一个 encounter**，一个 NPC 一个地点讲完；仅当故事**明确需要换场景**（如接任务→去别处→再回来交任务）时才拆成多步。

输出格式 TPA：
## Thinking - 分析核心要素、角色、冲突，是否含 MiniGame，是否为单一地点（不拆步）
## Planning - 设计起承转合、分支、奖励；若为单一事件则明确「一个 encounter 完成」
## Action - 完整剧本，包含：奇遇ID/名称、触发位置、参与NPC、剧情流程、道具ID，若含 MiniGame 则标注 gameType 建议
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"请将以下故事扩写为完整的奇遇剧本：\n\n{story_input}"},
    ]
    return _call_chat(client, model, messages)


def run_planner(
    client: OpenAI,
    expanded_story: str,
    model: str,
    assets: dict | None = None,
) -> str:
    """Agent 2: Planner - 仅规划 Encounter 步骤（Setup 固定不生成）"""
    planning_skill = """
## 输出 JSON 步骤列表（仅 type=encounter，不要 setup）

**核心原则：一个故事一个 NPC 一个地点**
- 对弈、赌局、MiniGame、对话分支等**当场完成**的剧情 → **只生成 1 个 encounter**，一个 NPC 在一个地点讲完，禁止拆成「下棋 encounter」+「领奖 encounter」
- **连续奇遇 (chain)** 仅当故事**明确需要换场景**（如接任务→去森林→回酒馆交任务）时才拆成多步

**关键**：必须判断是「独立奇遇」还是「连续奇遇」：
- **独立奇遇**：每个故事互不关联，**一个 NPC 一个地点**完成 → chain 为 null
- **连续奇遇**：需换场景的多步任务 → 同 chain 设 chainOrder、isFinal

**MiniGame**：对弈/赌局等，在**同一 encounter 内**完成 PlayMiniGame 并当场发放奖励/惩罚，description 含「PlayMiniGame」「对弈」等关键词。

{
  "steps": [
    {"id": 1, "name": "SpawnEncounter_xxx", "type": "encounter", "description": "...", "chain": null},
    {"id": 2, "name": "SpawnEncounter_yyy", "type": "encounter", "description": "...", "chain": "quest_name", "chainOrder": 2, "isFinal": true}
  ]
}
"""
    asset_note = ""
    if assets:
        npcs = ", ".join(assets.get("npcs", [])) or "无"
        enemies = ", ".join(assets.get("enemies", [])) or "无"
        asset_note = f"\n素材库限制：NPC 仅可用 [{npcs}]，Enemy 仅可用 [{enemies}]。"
    full_docs = get_full_docs()
    system_prompt = f"""你是一位LUA奇遇系统开发规划师。Setup 和路人NPC 已固定，只需规划奇遇(Encounter)步骤。
{asset_note}

输出格式：仅 encounter 类型步骤的 JSON。
{planning_skill}
"""
    user_msg = f"规则与API：\n{full_docs[:12000]}\n\n---\n扩写故事：\n{expanded_story}\n\n请输出步骤JSON。"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]
    return _call_chat(client, model, messages)


def run_coding_agent(
    client: OpenAI,
    step: dict,
    expanded_story: str,
    previous_code: str,
    model: str,
    validation_errors: Optional[list] = None,
    assets: dict | None = None,
    all_steps: Optional[list] = None,
    step_index: int = 0,
) -> str:
    """
    Agent 3: Coding Agent - generate LUA using Skills.
    仅使用素材库内的 NPC/Enemy/Prop，禁止库外 ID。
    """
    step_name = step.get("name", "unknown")
    step_desc = step.get("description", "")
    step_type = step.get("type", "general")

    skill_content = get_skill_for_step(step_type, step_name)

    asset_constraint = ""
    if assets:
        npcs = assets.get("npcs", [])
        enemies = assets.get("enemies", [])
        props = assets.get("props", [])
        minigames = assets.get("minigames", []) or []
        asset_constraint = f"""
=== 【强制】素材库约束（禁止使用库外 ID）===
- npcData 中的 NPC 类型仅可使用: {", ".join(npcs) if npcs else "（无）"}
- World.SpawnEnemy / AddEnemySpawn 仅可用 Enemy: {", ".join(enemies) if enemies else "（无）"}
- Env.AddProp / placeProp 仅可用 Prop: {", ".join(props) if props else "（无）"}
- **UI.PlayMiniGame(gameType, lv)** 的 gameType 仅可使用: {", ".join(minigames) if minigames else "（无，禁止使用 PlayMiniGame）"}
- 不得使用以上列表之外的任何 ID。
"""

    use_codex = "codex" in model.lower()
    base_prompt = f"""你是一位精通LUA和CineText/Narrative API的资深程序员。根据以下 Skill 规范生成**绝对正确**的LUA脚本。
{asset_constraint}

=== Skill 规范（必须遵循）===
{skill_content}

=== 输出要求 ===
1. 只输出可运行的LUA代码，不要 markdown 包裹
2. 严格遵循 Skill 中的 Checklist 和模板
3. FVector 格式 {{X=..., Y=..., Z=...}}
4. NPC ID：encXX_RoleName
5. 仅使用素材库中列出的 NPC/Enemy/Prop ID
6. **UI.Ask**（2选项）：比较用选项文案，如 if r == "答应" then，禁止 r == "A" 或 r == true
7. **UI.AskMany**（3+选项）：比较用选项文案，如 if choice == "血量偏低" then
8. **奇遇位置**：奇遇间至少 1000 单位；先发生的故事离玩家更近，后发生的更远。第 1 步最近（如 12100,13500），第 2 步 1000+ 外，第 3 步再 1000+ 外。禁止返回 {{X=0,Y=0,Z=0}}
9. **敌人生成**：剧情中若需敌人，必须用 World.SpawnEnemy(id, loc, count) 或 World.SpawnEnemyAtPlayer(id, count)，禁止把 Enemy ID 放入 npcData 或使用 World.SpawnNPC
10. **API 规范**：仅使用 lua_atomic_modules_call_guide.md 中列出的 API（World/UI/Entity/Performer），FVector/FRotator 格式严格遵循
11. **事件节奏**：台词/动作之间插入 World.Wait(0.8~1.5)，避免剧情同一帧执行完
12. **动画动作**：说话与演绎中适当加入 npc:PlayAnimLoop（Happy/Frustrated/Wave/Scared/Shy/Dance 等）或 npc:PlayAnim("Drink")，根据情绪选动作
13. **NPC 离场**：若剧情需 NPC 离开，可调用 World.DestroyByID("encXX_npc") 或 npc:SetVisible(false)
14. **MiniGame**：若描述含对弈、比赛、赌局、棋类，赢/输有不同结果，必须用 UI.PlayMiniGame(gameType, lv)，**gameType 仅可用素材库 minigames 中的 ID**（如 TTT），**在同一 encounter 内**根据 result == "Success" 当场分支处理奖励/惩罚，禁止拆成两个 encounter
"""

    # 连续奇遇上下文
    chain = step.get("chain")
    chain_order = step.get("chainOrder")
    is_final = step.get("isFinal", False)
    chain_context = ""
    if chain and all_steps:
        chain_steps = [s for s in all_steps if s.get("chain") == chain]
        chain_context = f"""
=== 【连续奇遇】本步骤属于 chain="{chain}"，chainOrder={chain_order}，isFinal={is_final} ===
- 使用 _G.{chain.replace("-", "_")}_* 共享状态（如 _G.drunkard_ring_agreed, _G.drunkard_ring_hasRing）
- **谢礼（GiveWeapon/GiveEquip/金钱）仅能在 isFinal=true 的最后一环发放**；中间环可发放任务道具（GiveItem）供最后一环判定
- 前一环设置状态供后一环读取；最后一环检查状态后发放谢礼
- 每环仍有自己的 _G.encXX_done 防重复
"""
        if is_final and len(chain_steps) > 1:
            chain_context += f"- 本步骤为 chain 最后一环，在此发放奖励。前面 {len(chain_steps)-1} 环不得发奖。\n"

    # 奇遇位置：根据步骤顺序，先发生的近、后发生的远，间距至少 1000
    total_steps = len(all_steps) if all_steps else 1
    order = step_index + 1  # 1-based
    loc_hint = ""
    if order == 1:
        loc_hint = "\n=== 【奇遇位置】本步骤为第 1 步（最先发生），应离玩家最近，如 {X=12100, Y=13500, Z=4797} ==="
    else:
        base_x, base_y = 12100, 13500
        offset = (order - 1) * 1100  # 每步 +1100
        loc_hint = f"\n=== 【奇遇位置】本步骤为第 {order} 步（共 {total_steps} 步），应距第 1 步至少 {(order-1)*1000} 单位，如 {{X={base_x + offset}, Y={base_y}, Z=4797}} 或 {{X={base_x - offset}, Y={base_y - offset}, Z=4797}} ==="

    if validation_errors:
        fix_prompt = f"""
=== 上一版代码未通过校验，请修正以下问题后重新输出 ===
{chr(10).join('- ' + e for e in validation_errors)}

请输出修正后的完整代码。
"""
    else:
        fix_prompt = ""

    user_msg = f"""步骤: {step_name} (type={step_type})
描述: {step_desc}
{chain_context}{loc_hint}{fix_prompt}

扩写故事（剧情参考）:
{expanded_story[:2500]}

已生成前序代码:
{previous_code[:2000] if previous_code else "（无）"}

请生成本步骤的LUA代码。"""

    full_input = f"{base_prompt}\n\n{user_msg}"

    if use_codex:
        return _call_responses(client, model, full_input)
    messages = [
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": user_msg},
    ]
    return _call_chat(client, model, messages)


def extract_steps_from_planner_output(plan_output: str) -> list:
    """Parse planner output to get step list."""
    match = re.search(r"\{[\s\S]*\"steps\"[\s\S]*\}", plan_output)
    if match:
        try:
            data = json.loads(match.group(0))
            return data.get("steps", [])
        except json.JSONDecodeError:
            pass
    steps = []
    for m in re.finditer(r"Step\s+(\d+):\s*(\w+)[\s\-]+(.+?)(?=Step\s+\d+:|$)", plan_output, re.DOTALL):
        steps.append({
            "id": int(m.group(1)),
            "name": m.group(2).strip(),
            "description": m.group(3).strip()[:200],
            "type": "encounter" if "enc" in m.group(2).lower() else "setup",
        })
    return steps if steps else [
        {"id": 1, "name": "SpawnEncounter_main", "type": "encounter", "description": "Main encounter from story"}
    ]
