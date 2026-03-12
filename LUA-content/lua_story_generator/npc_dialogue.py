"""NPC 对话功能：根据 Type=NPC_Dialogue_Request、Code={NPCInfo, CurrentDialogue} 生成回复 LUA。"""
import json
import re
from openai import OpenAI

from prompts.npc_dialogue import NPC_DIALOGUE_MAIN_PROMPT


def _safe_str(v, default=""):
    if v is None:
        return default
    return str(v).strip() or default


def _parse_dialogue_code(code: dict | None) -> tuple[dict, str]:
    """从 Code 中解析 NPCInfo 和 CurrentDialogue。"""
    if not isinstance(code, dict):
        return {}, ""
    npc_info = code.get("NPCInfo") or code.get("npc_info") or {}
    current = code.get("CurrentDialogue") or code.get("current_dialogue") or ""
    if not isinstance(npc_info, dict):
        npc_info = {}
    return npc_info, _safe_str(current)


def generate_npc_dialogue_reply_lua(
    api_key: str,
    code: dict | None = None,
    animations: list[str] | None = None,
) -> str:
    """
    根据 Type=NPC_Dialogue_Request 的 Code 生成 NPC 对话回复 LUA。
    Code 包含 NPCInfo 与 CurrentDialogue。
    返回包含 _self_:Say() 等的 LUA 脚本。
    """
    npc_info, current_dialogue = _parse_dialogue_code(code)

    info_parts = []
    info_parts.append(f"Name: {_safe_str(npc_info.get('Name'))} | Title: {_safe_str(npc_info.get('Title'))} | Gender: {_safe_str(npc_info.get('Gender'))}")
    info_parts.append(f"BackgroundStory: {_safe_str(npc_info.get('BackgroundStory'), '未提供')}")
    info_parts.append(f"Favorability（对玩家好感）: {npc_info.get('Favorability', '未提供')}")
    info_parts.append(f"MoralTendency（道德倾向）: {npc_info.get('MoralTendency', '未提供')}")

    pers = npc_info.get("Personality") or npc_info.get("personality")
    if isinstance(pers, dict):
        info_parts.append(f"Personality（大五人格）: {json.dumps(pers, ensure_ascii=False)}")
    else:
        info_parts.append("Personality: 未提供")

    goals = npc_info.get("Goals") or npc_info.get("goals")
    if isinstance(goals, dict):
        info_parts.append(f"Goals - LongTerm: {_safe_str(goals.get('LongTerm') or goals.get('long_term'))}")
        info_parts.append(f"Goals - MediumTerm: {_safe_str(goals.get('MediumTerm') or goals.get('medium_term'))}")
        info_parts.append(f"Goals - ShortTerm: {_safe_str(goals.get('ShortTerm') or goals.get('short_term'))}")

    for key in ["ShortTermMemory", "MediumTermMemory", "LongTermMemory"]:
        v = npc_info.get(key) or npc_info.get(key[0].lower() + key[1:])
        if v:
            info_parts.append(f"{key}: {_safe_str(v)}")

    npc_info_str = "\n".join(info_parts) if info_parts else "未提供"
    current_str = current_dialogue or "（无）"

    prompt = NPC_DIALOGUE_MAIN_PROMPT.format(
        npc_info_json=npc_info_str,
        current_dialogue=current_str,
    )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
    )
    text = (response.choices[0].message.content or "").strip()
    if text.startswith("```"):
        m = re.search(r"```(?:lua)?\s*\n([\s\S]*?)```", text)
        if m:
            text = m.group(1).strip()
    text = (
        text.replace("npc:Say(", "_self_:Say(")
        .replace("npc:PlayAnim(", "_self_:PlayAnim(")
        .replace("npc:PlayAnimLoop(", "_self_:PlayAnimLoop(")
    )
    return text
