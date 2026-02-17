---
name: lua-planning
description: Plans LUA encounter development steps from expanded story. Use when decomposing story into Setup/Encounter steps. Outputs JSON step list for Coding Agent.
---

# LUA Planning Skill

## 标准流程（rule.md）

1. Setup 初始化地图
2. Build 世界
3. 生成常驻 NPC（可选）
4. 注册 Encounter（1~N）
5. StartGame + Time.Resume

## 两种奇遇模式（必须正确标注）

### 独立奇遇（无 chain）
每个奇遇是**完整独立**的故事，各有自己的结局和奖励。互不关联。

### 连续奇遇（有 chain）
多个步骤属于**同一个大任务**，剧情前后衔接，奖励仅在**最后一环**发放。中间环节不发放奖励。

- 同一 chain 的 steps 共享 `chain` 名称（如 `"drunkard_ring"`）
- `chainOrder`：在该 chain 中的顺序 1,2,3...
- `isFinal`：是否为该 chain 的最后一环（**只有最后一环可发放奖励**）

## 输出格式

```json
{
  "steps": [
    {"id": 1, "name": "SpawnEncounter_xxx", "type": "encounter", "description": "...", "chain": null},
    {"id": 2, "name": "SpawnEncounter_yyy", "type": "encounter", "description": "...", "chain": null}
  ]
}
```

**独立奇遇示例**（三个互不相关的故事）：
```json
{
  "steps": [
    {"id": 1, "name": "SpawnEncounter_Blacksmith", "type": "encounter", "description": "铁匠委托，完成后得剑", "chain": null},
    {"id": 2, "name": "SpawnEncounter_Merchant", "type": "encounter", "description": "商人讨价还价，完成后得金币", "chain": null}
  ]
}
```

**连续奇遇示例**（醉汉戒指：接任务→打狼得戒指→归还得奖励）：
```json
{
  "steps": [
    {"id": 1, "name": "SpawnEncounter_DrunkardOffer", "type": "encounter", "description": "酒馆门口醉汉请求找戒指，玩家答应/拒绝", "chain": "drunkard_ring", "chainOrder": 1, "isFinal": false},
    {"id": 2, "name": "SpawnEncounter_ForestWolf", "type": "encounter", "description": "北边森林击败野狼获得戒指", "chain": "drunkard_ring", "chainOrder": 2, "isFinal": false},
    {"id": 3, "name": "SpawnEncounter_DrunkardReturn", "type": "encounter", "description": "归还戒指给醉汉，获得 TestSword 奖励", "chain": "drunkard_ring", "chainOrder": 3, "isFinal": true}
  ]
}
```

## step.type 取值

- `setup` → 加载 lua-setup-world Skill
- `encounter` → 加载 lua-encounter Skill
