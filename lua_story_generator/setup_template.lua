local CELL = 200
local MAP_W = 220
local MAP_H = 220
Time.Pause()
local seed = 20260211
local map = Env.CreateMap(MAP_W, MAP_H, CELL)
Env.SetMapName(map, "StoneRing_Village")
Env.SetMapTheme(map, "Medieval_CentralPlaza")

for y = 0, MAP_H - 1 do
    for x = 0, MAP_W - 1 do
        local n1 = Math.PerlinNoise2D(x * 0.045, y * 0.045) * 110
        local n2 = Math.PerlinNoise2D((x + 137) * 0.016, (y + 71) * 0.016) * 85
        Env.SetTerrainHeight(map, x, y, 4700 + n1 + n2)
    end
end

Env.FlattenTerrain(map, { X = 95, Y = 108 }, 34, 4820)
Env.FlattenTerrain(map, { X = 145, Y = 108 }, 34, 4820)
Env.RaiseTerrain(map, { X = 160, Y = 138 }, 17, 760, 0.58)
Env.GenMountainRange(map, { X = 12, Y = 195 }, { X = 208, Y = 210 }, 920, 6)
Env.GenMountainRange(map, { X = 194, Y = 14 }, { X = 210, Y = 186 }, 820, 5)
Env.GenMountainRange(map, { X = 18, Y = 18 }, { X = 34, Y = 160 }, 560, 4)
Env.PaintTerrain(map, 112, 108, 26, "sand")
Env.PaintTerrain(map, 164, 136, 18, "stone")

local village = Env.AddBlock(map, "StoneRingVillage", { X = 45, Y = 58 }, { X = 100, Y = 100 })
Env.SetBlockType(village, "Village")
Env.SetBlockRotation(village, 0, true)
Env.SetBlockProperty(village, "Core", "FountainRing")
Env.SetBlockProperty(village, "Layout", "SingleBlockCluster")

local function BlockGridToLocal(gx, gy, z)
    local p = Env.BlockGridToBlockLocalPos(village, { X = gx, Y = gy })
    return { X = p.X, Y = p.Y, Z = z or 0 }
end

local propSizeCache = {}

local buildDefs = {
    { P = { X = 71, Y = 86 }, S = { X = 10, Y = 8 },  Y = 45.0 },
    { P = { X = 17, Y = 81 }, S = { X = 12, Y = 10 }, Y = 67.5 },
    { P = { X = 64, Y = 77 }, S = { X = 8,  Y = 6 },  Y = 67.5 },
    { P = { X = 30, Y = 74 }, S = { X = 10, Y = 10 }, Y = 45.0 },
    { P = { X = 77, Y = 72 }, S = { X = 10, Y = 14 }, Y = 22.5 },
    { P = { X = 60, Y = 67 }, S = { X = 8,  Y = 8 },  Y = 67.5 },
    { P = { X = 37, Y = 68 }, S = { X = 10, Y = 6 },  Y = 45.0 },
    { P = { X = 28, Y = 65 }, S = { X = 2,  Y = 2 },  Y = 67.5 },
    { P = { X = 85, Y = 62 }, S = { X = 6,  Y = 10 }, Y = 0.0 },
    { P = { X = 70, Y = 60 }, S = { X = 2,  Y = 2 },  Y = 90.0 },
    { P = { X = 7,  Y = 62 }, S = { X = 18, Y = 12 }, Y = 67.5 },
    { P = { X = 35, Y = 56 }, S = { X = 2,  Y = 2 },  Y = 67.5 },
    { P = { X = 42, Y = 55 }, S = { X = 2,  Y = 2 },  Y = 67.5 },
    { P = { X = 24, Y = 53 }, S = { X = 8,  Y = 12 }, Y = 67.5 },
    { P = { X = 66, Y = 55 }, S = { X = 6,  Y = 2 },  Y = 90.0 },
    { P = { X = 34, Y = 53 }, S = { X = 2,  Y = 2 },  Y = 67.5 },
    { P = { X = 71, Y = 52 }, S = { X = 6,  Y = 10 }, Y = 90.0 },
    { P = { X = 25, Y = 36 }, S = { X = 10, Y = 8 },  Y = 22.5 },
    { P = { X = 12, Y = 27 }, S = { X = 12, Y = 10 }, Y = 22.5 },
    { P = { X = 36, Y = 25 }, S = { X = 10, Y = 8 },  Y = 67.5 },
    { P = { X = 7,  Y = 19 }, S = { X = 8,  Y = 12 }, Y = 22.5 },
    { P = { X = 14, Y = 9 },  S = { X = 6,  Y = 10 }, Y = 45.0 },
    { P = { X = 24, Y = 10 }, S = { X = 18, Y = 10 }, Y = 45.0 }
}

local built = {}
for i = 1, #buildDefs do
    local d = buildDefs[i]
    local snapYaw = math.floor(d.Y / 22.5 + 0.5) * 22.5 % 360
    local b = Env.AddBuilding(village, d.P, d.S, "Medieval", { Pitch = 0, Yaw = snapYaw, Roll = 0 })
    built[#built + 1] = b
    if b then
        Env.SetBuildingType(b, "House")
    end
end
if built[3] then Env.AddBuildingFloor(built[3], 380) end
if built[6] then Env.AddBuildingFloor(built[6], 380) end
if built[11] then Env.AddBuildingFloor(built[11], 380) end

local eastAnchors = {}
local windAnchors = {}
local northAnchors = {}

local ok, pos
local sz, snapYaw, rot
local ok0, empty0, okSize, blockSize, maxX, maxY, tryPos, ok1, empty1, okFind, freePos, p, ok2, empty2

local function placeProp(propId, prefX, prefY, prefZ, yaw)
    snapYaw = math.floor((yaw or 0) / 22.5 + 0.5) * 22.5 % 360
    rot = { Pitch = 0, Yaw = snapYaw, Roll = 0 }

    sz = propSizeCache[propId]
    if sz == nil then
        local okG, grid = pcall(Env.GetPropGridSize, map, propId)
        if okG and grid and grid.X and grid.Y then
            sz = { X = math.max(1, grid.X) * CELL, Y = math.max(1, grid.Y) * CELL }
        else
            sz = { X = CELL, Y = CELL }
        end
        propSizeCache[propId] = sz
    end

    local preferredPos = { X = prefX, Y = prefY, Z = prefZ or 0 }

    ok0, empty0 = pcall(Env.IsSpaceEmpty, village, preferredPos, sz)
    if ok0 and empty0 then
        Env.AddProp(village, propId, preferredPos, rot)
        return true, { X = prefX, Y = prefY, Z = prefZ or 0 }
    end

    okSize, blockSize = pcall(Env.GetBlockSize, village)
    if okSize and blockSize and blockSize.X and blockSize.Y then
        maxX = blockSize.X * CELL - sz.X - 20
        maxY = blockSize.Y * CELL - sz.Y - 20
        if maxX > 0 and maxY > 0 then
            for _ = 1, 56 do
                tryPos = {
                    X = Math.RandFloat(10, maxX),
                    Y = Math.RandFloat(10, maxY),
                    Z = prefZ or 0
                }
                ok1, empty1 = pcall(Env.IsSpaceEmpty, village, tryPos, sz)
                if ok1 and empty1 then
                    Env.AddProp(village, propId, tryPos, rot)
                    return true, { X = tryPos.X, Y = tryPos.Y, Z = tryPos.Z or 0 }
                end
            end
        end
    end

    okFind, freePos = pcall(Env.FindEmptySpace, village, sz)
    if okFind and type(freePos) == "table" and freePos.X and freePos.Y then
        p = { X = freePos.X, Y = freePos.Y, Z = prefZ or 0 }
        ok2, empty2 = pcall(Env.IsSpaceEmpty, village, p, sz)
        if ok2 and empty2 then
            Env.AddProp(village, propId, p, rot)
            return true, { X = p.X, Y = p.Y, Z = p.Z or 0 }
        end
    end

    print("[StoneRing.PropMissing] " .. tostring(propId))
    return false, nil
end

Env.AddProp(village, "Prop_Fountain", BlockGridToLocal(48, 47, 0), { Pitch = 0, Yaw = 0, Roll = 0 })
Env.AddProp(village, "Prop_Stage",    BlockGridToLocal(47, 55, 0), { Pitch = 0, Yaw = 0, Roll = 0 })
Env.AddProp(village, "Prop_Bar",      BlockGridToLocal(47, 41, 0), { Pitch = 0, Yaw = 0, Roll = 0 })
Env.AddProp(village, "Prop_Market",   BlockGridToLocal(42, 49, 0), { Pitch = 0, Yaw = 180, Roll = 0 })
Env.AddProp(village, "Prop_Market",   BlockGridToLocal(42, 45, 0), { Pitch = 0, Yaw = 180, Roll = 0 })
Env.AddProp(village, "Prop_Market",   BlockGridToLocal(54, 49, 0), { Pitch = 0, Yaw = 180, Roll = 0 })
Env.AddProp(village, "Prop_Market",   BlockGridToLocal(54, 45, 0), { Pitch = 0, Yaw = 180, Roll = 0 })

placeProp("Prop_Tent1",   12 * CELL + CELL * 0.5, 53 * CELL + CELL * 0.5, 0, 22.5)
placeProp("Prop_Tent2",   40 * CELL + CELL * 0.5, 54 * CELL + CELL * 0.5, 0, 337.5)
placeProp("Prop_Market",  28 * CELL + CELL * 0.5, 82 * CELL + CELL * 0.5, 0, 45)

placeProp("Prop_Tent5",   14 * CELL + CELL * 0.5, 20 * CELL + CELL * 0.5, 0, 337.5)
placeProp("Prop_Tent2",   42 * CELL + CELL * 0.5, 22 * CELL + CELL * 0.5, 0, 22.5)
placeProp("Prop_Market",  26 * CELL + CELL * 0.5, 46 * CELL + CELL * 0.5, 0, 337.5)

placeProp("Prop_Tent1",   70 * CELL + CELL * 0.5, 22 * CELL + CELL * 0.5, 0, 22.5)
placeProp("Prop_Tent5",   98 * CELL + CELL * 0.5, 24 * CELL + CELL * 0.5, 0, 337.5)
placeProp("Prop_FlowerShop", 83 * CELL + CELL * 0.5, 48 * CELL + CELL * 0.5, 0, 22.5)

placeProp("Prop_Hachiko",  48 * CELL + CELL * 0.5, 46 * CELL + CELL * 0.5, 0, 22.5)
placeProp("Prop_Armory",   56 * CELL + CELL * 0.5, 55 * CELL + CELL * 0.5, 0, 180)
placeProp("Prop_Gambling", 65 * CELL + CELL * 0.5, 55 * CELL + CELL * 0.5, 0, 90)

ok, pos = placeProp("Prop_Tent5", 61 * CELL + CELL * 0.5, 68 * CELL + CELL * 0.5, 0, 315)
if ok and pos then eastAnchors[#eastAnchors + 1] = pos end
ok, pos = placeProp("Prop_Tent1", 74 * CELL + CELL * 0.5, 64 * CELL + CELL * 0.5, 0, 0)
if ok and pos then eastAnchors[#eastAnchors + 1] = pos end
ok, pos = placeProp("Prop_Tent2", 81 * CELL + CELL * 0.5, 60 * CELL + CELL * 0.5, 0, 0)
if ok and pos then eastAnchors[#eastAnchors + 1] = pos end
ok, pos = placeProp("Prop_Camp",  80 * CELL + CELL * 0.5, 71 * CELL + CELL * 0.5, 0, 45)
if ok and pos then eastAnchors[#eastAnchors + 1] = pos end
ok, pos = placeProp("Prop_Fires", 78 * CELL + CELL * 0.5, 68 * CELL + CELL * 0.5, 0, 0)
if ok and pos then eastAnchors[#eastAnchors + 1] = pos end

ok, pos = placeProp("Prop_Windmill", 100 * CELL + CELL * 0.5, 66 * CELL + CELL * 0.5, 0, 22.5)
if ok and pos then windAnchors[#windAnchors + 1] = pos end
ok, pos = placeProp("Prop_Windmill", 118 * CELL + CELL * 0.5, 64 * CELL + CELL * 0.5, 0, 337.5)
if ok and pos then windAnchors[#windAnchors + 1] = pos end
ok, pos = placeProp("Prop_Farm", 108 * CELL + CELL * 0.5, 56 * CELL + CELL * 0.5, 0, 0)
if ok and pos then windAnchors[#windAnchors + 1] = pos end
ok, pos = placeProp("Prop_Farm", 116 * CELL + CELL * 0.5, 56 * CELL + CELL * 0.5, 0, 0)
if ok and pos then windAnchors[#windAnchors + 1] = pos end

for r = 0, 1 do
    for c = 0, 2 do
        local cx = (58 + c * 7) * CELL + CELL * 0.5
        local cy = (50 + r * 7) * CELL + CELL * 0.5
        ok, pos = placeProp("Prop_Market", cx, cy, 0, 0)
        if ok and pos then eastAnchors[#eastAnchors + 1] = pos end
    end
end
for r = 0, 1 do
    for c = 0, 1 do
        local cx = (92 + c * 8) * CELL + CELL * 0.5
        local cy = (56 + r * 6) * CELL + CELL * 0.5
        ok, pos = placeProp("Prop_Market", cx, cy, 0, 90)
        if ok and pos then windAnchors[#windAnchors + 1] = pos end
    end
end
local treeIds = { "Prop_Tree1", "Prop_Tree2", "Prop_Tree3" }
local treeYaw = { 0, 90, 180, 270 }

for i = 1, 34 do
    local base = eastAnchors[Math.RandInt(1, math.max(1, #eastAnchors))]
    if base == nil then
        base = { X = 66 * CELL + CELL * 0.5, Y = 62 * CELL + CELL * 0.5, Z = 0 }
    end
    placeProp(
        treeIds[Math.RandInt(1, #treeIds)],
        base.X + Math.RandFloat(-560, 560),
        base.Y + Math.RandFloat(-560, 560),
        0,
        treeYaw[Math.RandInt(1, #treeYaw)]
    )
end

for i = 1, 30 do
    local base = windAnchors[Math.RandInt(1, math.max(1, #windAnchors))]
    if base == nil then
        base = { X = 106 * CELL + CELL * 0.5, Y = 62 * CELL + CELL * 0.5, Z = 0 }
    end
    placeProp(
        treeIds[Math.RandInt(1, #treeIds)],
        base.X + Math.RandFloat(-520, 520),
        base.Y + Math.RandFloat(-460, 460),
        0,
        treeYaw[Math.RandInt(1, #treeYaw)]
    )
end

for i = 1, 46 do
    local px = Math.RandInt(72, 118) * CELL + CELL * 0.5
    local py = Math.RandInt(6, 20) * CELL + CELL * 0.5
    ok, pos = placeProp(treeIds[Math.RandInt(1, #treeIds)], px, py, 0, treeYaw[Math.RandInt(1, #treeYaw)])
    if ok and pos then northAnchors[#northAnchors + 1] = pos end
end

Env.AddSpawnPoint(village, "PlayerStart", { X = 56 * CELL + CELL * 0.5, Y = 46 * CELL + CELL * 0.5, Z = 0 })
Env.AddNPCSpawn(village, "NPC_Bartender",  { X = 76 * CELL + CELL * 0.5, Y = 44 * CELL + CELL * 0.5, Z = 0 }, { Pitch = 0, Yaw = 180, Roll = 0 })
Env.AddNPCSpawn(village, "NPC_Blacksmith", { X = 50 * CELL + CELL * 0.5, Y = 62 * CELL + CELL * 0.5, Z = 0 }, { Pitch = 0, Yaw = 180, Roll = 0 })
Env.AddNPCSpawn(village, "NPC_Camper",     { X = 86 * CELL + CELL * 0.5, Y = 74 * CELL + CELL * 0.5, Z = 0 }, { Pitch = 0, Yaw = 90, Roll = 0 })
Env.AddEnemySpawn(village, "Enemy_Wolf",   { X = 122 * CELL + CELL * 0.5, Y = 16 * CELL + CELL * 0.5, Z = 0 }, 900)

Env.ValidateMap(map)
Env.BuildAsync(map)

-- ============ 放置路人NPC（间距加大，避免扎堆）============
World.SpawnNPC("Merchant_Male","stranger",{X=17800,Y=21800,Z=4801.29})
World.SpawnNPC("Merchant_Male","stranger",{X=17800,Y=20500,Z=4801.29})
World.SpawnNPC("Hunter_Male","fountain",{X=18800,Y=20800,Z=4801.29})
World.SpawnNPC("Ironworker_Male","fountain",{X=19500,Y=21200,Z=4801.29})
World.SpawnNPC("Merchant_Male","stranger",{X=20200,Y=20400,Z=4801.29})
World.SpawnNPC("Merchant_Male","stranger",{X=20200,Y=22200,Z=4801.29})
World.SpawnNPC("Ironworker_Male","blacksmith",{X=18600,Y=24400,Z=4801.29})
World.SpawnNPC("Hunter_Male","stranger",{X=18200,Y=16800,Z=4781.83})
World.SpawnNPC("Hunter_Male","stranger",{X=14800,Y=18600,Z=4794.21})
World.SpawnNPC("Merchant_Male","stranger",{X=23200,Y=19800,Z=4801.27})
World.SpawnNPC("Merchant_Male","stranger",{X=20400,Y=21600,Z=4801.27})
World.SpawnNPC("Assassin_Male","stranger",{X=18800,Y=22600,Z=4801.29})
World.SpawnNPC("Assassin_Male","stranger",{X=15800,Y=19600,Z=4781.67})
World.SpawnNPC("Ironworker_Male","stranger",{X=17200,Y=15200,Z=4770.66})
