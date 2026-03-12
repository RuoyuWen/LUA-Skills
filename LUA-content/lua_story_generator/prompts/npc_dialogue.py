# -*- coding: utf-8 -*-
"""
NPC 对话功能 - Prompt 定义
便于策划/开发者直接修改调整。

输入格式（UE/Web 通用）：
{
    "Type": "NPC_Dialogue_Request",
    "Code": {
        "NPCInfo": {
            "Gender": "", "Name": "", "Title": "", "BackgroundStory": "",
            "Favorability": 0, "MoralTendency": 0,
            "Personality": {}, "Goals": {},
            "ShortTermMemory": "", "MediumTermMemory": "", "LongTermMemory": ""
        },
        "CurrentDialogue": ""   # 当前对话内容
    }
}

输出格式：{"Type": "NPC_Dialogue_Reply", "Code": "<lua string>"}

注：具体生成逻辑待后续定义。
"""

# 主 Prompt 模板。占位符：{npc_info_json}, {current_dialogue}
NPC_DIALOGUE_MAIN_PROMPT = """你是一个游戏 NPC 对话回复生成器。根据 NPC 的完整信息与当前对话内容，生成 NPC 的回复 LUA 代码。

**1. NPC 信息（NPCInfo）**
{npc_info_json}

**2. 当前对话（CurrentDialogue）**
{current_dialogue}

**输出要求**：
- 根据 NPC 性格、目标、记忆、对玩家好感，生成符合人设的回复
- 使用 _self_:Say("...") 输出台词，可配合 _self_:PlayAnim / _self_:PlayAnimLoop
- 仅输出 LUA 代码，无 markdown 包裹
"""
