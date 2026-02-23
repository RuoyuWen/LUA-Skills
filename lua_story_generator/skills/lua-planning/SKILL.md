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

## 核心原则：一个故事一个 NPC 一个地点

**单一事件**（对弈、赌局、对话分支、当场给奖励）：**只生成 1 个 encounter**，一个 NPC 在一个地点把故事讲完。禁止拆成多个 encounter、多个 NPC。

**连续奇遇 (chain)**：仅当故事**明确需要换场景或延后**时才拆分，例如「接任务（酒馆）→ 去森林打狼 → 回酒馆交任务」需 3 个不同地点。

## 两种奇遇模式（必须正确标注）

### 独立奇遇（无 chain）
每个奇遇是**完整独立**的故事，**一个 NPC 一个地点**讲完。对弈、赌局、MiniGame 等当场分出胜负并发放奖励的，**全部合并为一个 encounter**。

### 连续奇遇（有 chain）
仅当故事需要**换场景**（如去森林、再回酒馆）时才拆分为多步。同一 chain 的多步对应不同地点或不同阶段。

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

## MiniGame 奇遇（对弈/比赛/赌局）

若故事涉及**与 NPC 对弈、棋类、赌局、比赛**，赢/输有不同结果：**只生成 1 个 encounter**，在该 encounter 内完成邀请→PlayMiniGame→当场发放奖励/惩罚。**禁止拆成「下棋 encounter」+「领奖 encounter」两个步骤**。

```json
{"id": 1, "name": "SpawnEncounter_OldManChess", "type": "encounter", "description": "酒吧门口老人邀玩家下棋，PlayMiniGame 获胜得 TestSword，失败被骂。同一 NPC 同一地点完成。", "chain": null}
```

## step.type 取值

- `setup` → 加载 lua-setup-world Skill
- `encounter` → 加载 lua-encounter Skill
