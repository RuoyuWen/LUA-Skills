"""NPC 实时互动：根据 UE 传入的 PropTag、Personality、Goal 生成 LUA 表演脚本。"""
import json
from openai import OpenAI


def generate_npc_interaction_lua(
    api_key: str,
    prop_tag: str = "",
    prop_pos: dict | None = None,
    personality: dict | None = None,
    goal: dict | None = None,
    animations: list[str] | None = None,
) -> str:
    """
    根据 UE 传入的上下文生成 NPC 互动 LUA。
    返回包含 _self_:Say() 和 _self_:PlayAnimLoop() 的 LUA 脚本。
    """
    pers = personality if isinstance(personality, dict) else {}
    goal_data = goal if isinstance(goal, dict) else {}

    extraversion = pers.get("Extraversion", pers.get("extraversion", 50))
    try:
        extraversion = int(extraversion)
    except (TypeError, ValueError):
        extraversion = 50

    current_goal = str(goal_data.get("CurrentGoal", goal_data.get("current_goal", "")) or "")

    # 完整 personality 供模型参考（排除已单独展示的）
    pers_str = json.dumps(pers, ensure_ascii=False) if pers else "未指定"

    anims = animations or [
        "Happy", "Frustrated", "Wave", "Scared", "Shy", "Dance", "Drink", "Eat",
        "Idle", "Sit", "Sleep", "Sing", "PickUp", "Dialogue", "Admiring",
    ]
    anim_str = ", ".join(anims[:30])

    client = OpenAI(api_key=api_key)
    prompt = f"""你是一个游戏 NPC 表演脚本生成器。**生成的台词和行为必须与以下三项强相关**：NPC 看到的道具、NPC 性格、NPC 当前目标。不得输出与此无关的通用台词。

**1. PropTag（NPC 当前看到的物体）**  
{prop_tag.strip() or "无"}  
→ 台词必须针对这个物体有感而发（如看到酒聊酒、看到椅子想坐、看到食物想吃喝等）。若为空则 NPC 处于无特定关注对象的状态。

**2. Personality（性格）**  
{pers_str}  
Extraversion 外向性 0-100：高(≥70)=开朗直接、易兴奋；低(≤40)=沉稳内敛、少言。  
→ 台词口吻、情绪强度必须符合性格。

**3. Goal（当前目标）**  
{current_goal or "无"}  
→ 行为需服务于该目标。例如：Relax→放松类动作(Drink/Happy/Idle/Sit)；Work→专注(Admiring/Idle)；社交→Wave/ Dialogue。

**可用动画**（仅使用以下）：{anim_str}

**生成规则**（三者缺一不可）：
- 台词要对 PropTag 做出反应；口吻由 Personality 决定；动作选择由 Goal 驱动。
- PropTag=drink/food/chair 等 → 选对应 Drink/Eat/Sit 等；无明确物体 → Idle/Admiring 等。
- 输出 2~4 行 LUA，必须用 _self_ 指代 NPC，格式：_self_:Say("...") 和 _self_:PlayAnimLoop("AnimName", 0)。

**输出**：仅 LUA 代码，无 markdown 包裹。
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
    )
    text = (response.choices[0].message.content or "").strip()
    if text.startswith("```"):
        import re
        m = re.search(r"```(?:lua)?\s*\n([\s\S]*?)```", text)
        if m:
            text = m.group(1).strip()
    # 确保使用 _self_ 指代 NPC，替换可能误写的 npc:
    text = text.replace("npc:Say(", "_self_:Say(").replace("npc:PlayAnimLoop(", "_self_:PlayAnimLoop(")
    return text
