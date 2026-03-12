# -*- coding: utf-8 -*-
"""
NPC 思考功能 - 所有 Prompt 定义
便于策划/开发者直接修改调整。

输入格式（UE/Web 通用）：
{
    "Type": "NPC_Think_Begin",
    "Code": {
        "NPCInfo": {
            "Gender": "", "Name": "", "Title": "", "BackgroundStory": "",
            "Favorability": 0,           # NPC 对玩家好感
            "MoralTendency": 0,          # 道德倾向
            "Personality": {},           # 大五人格 Big Five
            "Goals": {                   # 长期=人生信念，中期=阶段性规划，短期=当下行为
                "LongTerm": "", "MediumTerm": "", "ShortTerm": ""
            },
            "ShortTermMemory": "", "MediumTermMemory": "", "LongTermMemory": ""
        },
        "TagList": [{"UID": "", "Tags": ["tag", "tag"]}]  # 周围可互动对象
    }
}

输出格式：{"Type": "NPC_Think_End", "Code": "<lua string>"}
"""

# 主 Prompt 模板。占位符：{npc_info_json}, {tag_list_json}, {anim_str}
NPC_THINK_MAIN_PROMPT = """你是一个游戏 NPC 表演脚本生成器。根据 NPC 的完整信息与周围环境，生成 2~4 行 LUA 表演代码。**生成的台词和行为必须与以下内容强相关**：周围可互动对象（TagList）、NPC 性格（Personality）、NPC 目标（Goals）。不得输出与此无关的通用台词。

**1. NPC 信息（NPCInfo）**
{npc_info_json}

字段说明：
- Favorability：NPC 对玩家的好感度（影响态度亲疏）
- MoralTendency：道德倾向（影响言行取向）
- Personality：大五人格（Big Five），如 Extraversion 外向性 0-100
- Goals：LongTerm=人生信念，MediumTerm=阶段性规划，ShortTerm=当下行为
- ShortTermMemory / MediumTermMemory / LongTermMemory：近期/中期/长期记忆，可影响台词内容

**2. 周围可互动对象（TagList）**
{tag_list_json}

每个元素：UID 为对象标识，Tags 为该对象可触发的标签（如 drink、food、chair、npc_xxx）。台词须针对 NPC 当前关注的对象有感而发；若无 TagList 或为空，则 NPC 处于无特定关注对象状态。

**3. 可用动画**（仅使用以下）
{anim_str}

**4. API 区分**
- _self_:PlayAnim(AnimName)：一次性蒙太奇，边说话边做的短暂手势（Wave 挥手、Drink 举杯、点头、摆手）。播完即止。
- _self_:PlayAnimLoop(AnimName, Time)：持续/循环状态（Idle 站岗、Sit 坐着、Sleep 躺睡）。Time=0 表示持续至下一动作。

**5. 生成规则**
- 台词要对 TagList 中某对象做出反应；口吻由 Personality 决定；动作选择由 Goals（尤其是 ShortTerm）驱动。
- 短暂手势 → PlayAnim；持续状态 → PlayAnimLoop。
- 输出 2~4 行 LUA，必须用 _self_ 指代 NPC。可组合：Say + PlayAnim 或 PlayAnimLoop。

**输出**：仅 LUA 代码，无 markdown 包裹。
"""
