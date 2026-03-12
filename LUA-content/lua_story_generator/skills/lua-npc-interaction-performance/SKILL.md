---
name: lua-npc-interaction-performance
description: Generates LUA for NPC real-time interaction (表演/演绎). Use when UE sends PropTag, Personality, Goal - generate Say dialogue, PlayAnim (one-shot), and PlayAnimLoop (sustained) based on context.
---

# LUA NPC Interaction Performance Skill

## 何时加载

当 UE 端传入 NPC 互动上下文（PropTag、Personality、Goal）时，根据大五人格、目标、所见物体生成表演 LUA。

## 可用 API（LUA 表演库）

使用 **`_self_`** 作为指代当前 NPC，所有调用格式为 `_self_:函数名(...)`。

| 函数 | 说明 | 适用场景 |
|------|------|----------|
| _self_:PlayAnim(AnimName) | 播放**一次性蒙太奇**动画（如攻击、挥手、点头、摆手）。边说话边做的短暂手势，播完即止。 | 高兴时摇头摆手、打招呼挥手、喝酒举杯动作等 |
| _self_:PlayAnimLoop(AnimName, Time) | 播放动画并**持续指定时间**（循环或保持）。如站岗、躺地、坐着休息。 | 站岗、躺地下死了、坐着喝酒、趴着睡觉等 |
| _self_:Say(Text) | 头顶显示气泡对话。脚本挂起直到显示时间结束，默认 3 秒 | 任意台词 |

## 生成原则（三者缺一不可）

生成的台词和行为**必须同时反映**：NPC 看到的道具、NPC 性格、NPC 当前目标。

- **PropTag（所见物体）**：台词须对该物体有感而发。drink→喝酒台词+Drink；food→Eat；chair→Sit；无物体→无特定关注
- **Personality（性格）**：口吻、情绪强度由 Extraversion 等决定。高=开朗直接；低=沉稳内敛
- **Goal（当前目标）**：动作服务于目标。Relax→Drink/Happy/Idle/Sit；Work→Admiring/Idle；Social→Wave/Dialogue
- **PlayAnim vs PlayAnimLoop**：短暂手势（挥手、举杯、点头）→ PlayAnim；持续状态（站岗、坐着、躺着）→ PlayAnimLoop

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
