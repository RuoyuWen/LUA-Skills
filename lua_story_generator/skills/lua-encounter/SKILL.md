---
name: lua-encounter
description: Generates LUA Encounter scripts for CineText/Narrative. Use when generating encounter (奇遇) code, World.SpawnEncounter, NPC dialogue, UI.Ask, rewards. Enforces rule.md hard rules via checklist.
---

# LUA Encounter Skill

## 何时加载

当步骤类型为 `encounter` 或名称包含 `SpawnEncounter`、`奇遇` 时应用本 Skill。

## 输出 Checklist（生成后必须自检，全部通过）

- [ ] 有 `if _G.encXX_done then return end` 和 `_G.encXX_done = true`
- [ ] 对 player 和所有 NPC 做了 `if not obj or not obj:IsValid() then return end`
- [ ] 奖励使用 `npc:GiveItem(id,count)` / `GiveWeapon` / `GiveEquip`，不能用 Toast 代替
- [ ] UI.Ask / UI.AskMany 返回值必须用**选项的实际文案**比较，禁止用 "A"、"B" 或 true
- [ ] 仅使用 lua_atomic_modules_call_guide.md 中存在的 API
- [ ] NPC ID 命名：`encXX_RoleName`（如 enc07_smith）
- [ ] 台词/动作间适当插入 World.Wait(0.8~1.5) 控制节奏

## 奇遇位置与敌人生成

- **玩家出生点**：X=12016.59, Y=13372.98, Z=4797.61
- **距离规则**：奇遇之间相距至少 **1000** 单位；**先发生的故事离玩家更近，后发生的更远**
- **ResolveEncounterLoc()** 根据本步骤在故事中的顺序返回坐标，Z 保持约 4797：
  - 第 1 步（最先发生）：最近，如 `{X=12100, Y=13500, Z=4797}`
  - 第 2 步：距第 1 步至少 1000，如 `{X=13200, Y=13500, Z=4797}` 或 `{X=11100, Y=12300, Z=4797}`
  - 第 3 步：距第 2 步至少 1000，如 `{X=14300, Y=13500, Z=4797}` 或 `{X=10100, Y=11300, Z=4797}`
- **敌人生成**：必须用 `World.SpawnEnemy(id, loc, count)` 或 `World.SpawnEnemyAtPlayer(id, count)`，禁止用 World.SpawnNPC 或把 Enemy ID 放入 npcData。npcData 仅用于 NPC。

## 强制模板结构

```lua
local function ResolveEncounterLoc()
    return {X=12100, Y=13500, Z=4797}  -- 靠近玩家出生点 (12016, 13372, 4797)
end

function SpawnEncounter_XXX()
    local npcData = { encXX_npc = "Default" }
    local code = [[
        if _G.encXX_done then return end
        _G.encXX_done = true
        local player = World.GetByID("Player")
        local npc = World.GetByID("encXX_npc")
        if not player or not player:IsValid() then return end
        if not npc or not npc:IsValid() then return end
        -- 剧情逻辑
    ]]
    local loc = ResolveEncounterLoc()
    return World.SpawnEncounter(loc, 200.0, npcData, "EnterVolume", code)
end
SpawnEncounter_XXX()
```

**range 推荐值（rule 12.3）**：单人对话 100~200，2 NPC+分支 200~300，战斗/多 NPC 300~450。

## 可用功能模块

| 模块 | API | 示例 |
|------|-----|------|
| 剧情 | UI.Toast, npc:ApproachAndSay, UI.ShowDialogue | npc:ApproachAndSay(player, "你好") |
| 选择 | UI.Ask（2选项）, UI.AskMany（3+选项） | 见下方规范 |
| 动画 | npc:PlayAnim, npc:PlayAnimLoop, World.Wait | World.Wait(1.0) |
| 战斗 | npc:SetAsHostile（NPC 变敌）, World.SpawnEnemy（生成敌人） | World.SpawnEnemy("Enemy_Wolf", loc, 1) |
| 奖励 | npc:GiveItem, GiveWeapon, GiveEquip | npc:GiveWeapon("FireSword", 1) |
| 销毁/隐藏 | World.DestroyByID, World.Destroy, obj:Destroy, obj:SetVisible | World.DestroyByID("enc07_drunk") |

## 事件节奏（rule 9.3）

每段台词/动作之间建议插入 `World.Wait(0.8 ~ 1.5)`，避免剧情在同一帧执行完、体验生硬。示例：
```lua
npc:ApproachAndSay(player, "谢谢你。")
World.Wait(1.0)
npc:GiveWeapon("TestSword", 1)
```

## 演绎后 NPC 处理（rule 13.7）

若剧情需要 NPC 离开场景，可调用：
- `World.DestroyByID("encXX_npc")` — 按 ID 销毁
- `npc:Destroy()` 或 `World.Destroy(npc)` — 按对象销毁
- `npc:SetVisible(false)` — 仅隐藏，不销毁

## UI.Ask / UI.AskMany 规范（强制）

- **两个选项**：用 `UI.Ask("问题", "选项A文案", "选项B文案")`，返回值比较 `if r == "选项A文案" then`，禁止用 `r == "A"` 或 `r == true`
- **三个及以上选项**：用 `UI.AskMany("问题", {"选项1", "选项2", "选项3"})`，返回值比较 `if choice == "选项1" then` 等
- 示例：
```lua
local r = UI.Ask("帮忙找戒指吗？", "答应", "拒绝")
if r == "答应" then
    ...
else
    ...
end

local choice = UI.AskMany("你的状态如何？", {"血量偏低", "缺乏装备", "质问为何在战场摆摊"})
if choice == "血量偏低" then
    ...
elseif choice == "缺乏装备" then
    ...
elseif choice == "质问为何在战场摆摊" then
    ...
end
```

## 连续奇遇（chain）规范

当 Planner 标注本步骤属于 `chain` 且 `isFinal=false` 时：

- **共享状态**：使用 `_G.questName_flag` 格式，如 `_G.drunkard_ring_agreed`、`_G.drunkard_ring_hasRing`
- **禁止发谢礼**：中间环节不得发放报酬类奖励（GiveWeapon/GiveEquip/金钱）；可发放任务道具 GiveItem(id,1)（id 须在 DT_Items 中），或用 `_G.questName_hasRing = true` 标记进度
- **防重复**：每环仍有 `_G.encXX_done`，但可读取前一环的 `_G.questName_*` 判断进度

当 `isFinal=true`（最后一环）时：

- **检查状态**：根据 `_G.questName_hasRing` 或玩家是否拥有任务道具，判断是否完成前置
- **奖励一次**：仅在归还戒指/完成任务时调用一次 GiveWeapon 等作为谢礼

示例（醉汉戒指 chain，第 1 环）：
```lua
if r == "答应" then
    _G.drunkard_ring_agreed = true
    UI.Toast("你决定去北边森林寻找戒指。")
    -- 不发放奖励
end
```

示例（第 3 环，最后一环）：
```lua
if _G.drunkard_ring_hasRing and r == "递交戒指" then
    drunk:GiveWeapon("TestSword", 1)
    UI.Toast("你获得了 TestSword。")
end
```

## 敌人生成示例

剧情中如需出现敌人，在 encounter 代码内调用：

```lua
local loc = player:GetPos()  -- 或固定坐标
local enemies = World.SpawnEnemy("Enemy_Wolf", loc, 1)
-- 或直接在玩家附近生成：
local enemies = World.SpawnEnemyAtPlayer("Enemy_Wolf", 1)
```

禁止：把 `Enemy_Wolf` 等放入 npcData，或使用 World.SpawnNPC 生成敌人。

## 参考（严格遵守 lua_atomic_modules_call_guide.md）

- 仅使用该文档中列出的 API，禁止使用未列出的函数
- 数据类型：FVector `{X=0,Y=0,Z=0}`，FRotator `{Pitch=0,Yaw=0,Roll=0}`
- GiveItem/GiveWeapon/GiveEquip 的 id 必须来自 DT_Items（如 TestSword, FireSword, Helmet, Money）
- 连续奇遇任务道具：若 DT_Items 无对应项，用 `_G.questName_hasRing = true` 等标志代替 GiveItem("LostRing",1），最后一环检查该标志
