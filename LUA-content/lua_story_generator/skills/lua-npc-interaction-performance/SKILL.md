---
name: lua-npc-interaction-performance
description: Generates LUA for NPC 思考 (表演/演绎). Use when UE/Web sends Type=NPC_Think_Begin, Code={NPCInfo, TagList} - generate Say/PlayAnim/PlayAnimLoop based on Favorability, MoralTendency, Personality, Goals, TagList.
---

# LUA NPC 思考 / 表演 Skill

## 何时加载

当 UE/Web 端传入 `Type=NPC_Think_Begin`、`Code={NPCInfo, TagList}` 时，根据 NPC 信息与周围可互动对象生成表演 LUA。NPCInfo 含 Favorability、MoralTendency、Personality（大五）、Goals（长期/中期/短期）、Memory。

## 可用 API（LUA 表演库）

使用 **`_self_`** 作为指代当前 NPC，所有调用格式为 `_self_:函数名(...)`。

| 函数 | 说明 | 适用场景 |
|------|------|----------|
| _self_:PlayAnim(AnimName) | 播放**一次性蒙太奇**动画（如攻击、挥手、点头、摆手）。边说话边做的短暂手势，播完即止。 | 高兴时摇头摆手、打招呼挥手、喝酒举杯动作等 |
| _self_:PlayAnimLoop(AnimName, Time) | 播放动画并**持续指定时间**（循环或保持）。如站岗、躺地、坐着休息。 | 站岗、躺地下死了、坐着喝酒、趴着睡觉等 |
| _self_:Say(Text) | 头顶显示气泡对话。脚本挂起直到显示时间结束，默认 3 秒 | 任意台词 |

## 生成原则

生成的台词和行为**必须同时反映**：TagList（周围可互动对象）、Personality（性格）、Goals（尤其是 ShortTerm 当下行为）。

- **TagList（周围对象）**：台词须对某对象有感而发。drink→喝酒+Drink；food→Eat；chair→Sit
- **Personality（大五）**：口吻、情绪由 Extraversion 等决定。高=开朗；低=沉稳
- **Goals**：LongTerm=人生信念，MediumTerm=阶段性规划，ShortTerm=当下行为 → 动作服务于目标
- **Favorability / MoralTendency**：影响对玩家态度与道德相关台词
- **PlayAnim vs PlayAnimLoop**：短暂手势→PlayAnim；持续状态→PlayAnimLoop

## 动画库（来自 DT_AnimStartTable / DT_MontageTable）

常用：Happy, Frustrated, Wave, Scared, Shy, Dance, Drink, Eat, Idle, Sit, Sleep, Sing, PickUp, PointTo, Admiring, Dialogue 等。仅使用 DataTable 中列出的 AnimName。

## 输出格式

```lua
_self_:Say("生成的台词")
_self_:PlayAnim("Wave")           -- 一次性手势，边说话边做
_self_:PlayAnimLoop("Idle", 0)    -- 持续状态（站岗、躺死、坐着等）
```

- **PlayAnim**：选一次性手势（Wave、Drink、PointTo 等），配合 Say 做「边说话边做动作」。
- **PlayAnimLoop**：选持续/循环状态（Idle、Sit、Sleep、躺死等），Time 建议 0（持续至下一动作）或 2.0~5.0 秒。
