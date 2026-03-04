local map = Env.CreateMap(256, 256, 200.0)
Env.SetMapName(map, "StoneRingVillage")
Env.SetMapTheme(map, "Village")

local block = Env.AddBlock(map, "StoneRingVillage", { X = 45, Y = 58 }, { X = 100, Y = 50 })
Env.SetBlockType(block, "Village")

Env.AddBuilding(block, { X = 26, Y = 18 }, { X = 8,  Y = 14 }, "Chapel", { Pitch = 0.0, Yaw = 90.0,  Roll = 0.0 })

Env.AddBuilding(block, { X = 15, Y = 4  }, { X = 10, Y = 6 }, "House", { Pitch = 0.0, Yaw = -22.5, Roll = 0.0 })
Env.AddBuilding(block, { X = 18, Y = 9  }, { X = 8,  Y = 6 }, "House", { Pitch = 0.0, Yaw = 0.0,   Roll = 0.0 })
Env.AddBuilding(block, { X = 22, Y = 12 }, { X = 6,  Y = 6 }, "House", { Pitch = 0.0, Yaw = 22.5,  Roll = 0.0 })

Env.AddBuilding(block, { X = 40, Y = 8  }, { X = 10, Y = 8 }, "House", { Pitch = 0.0, Yaw = 0.0,   Roll = 0.0 })
Env.AddBuilding(block, { X = 46, Y = 11 }, { X = 6,  Y = 4 }, "House", { Pitch = 0.0, Yaw = 0.0,   Roll = 0.0 })

Env.AddBuilding(block, { X = 64, Y = 2  }, { X = 10, Y = 6 }, "House", { Pitch = 0.0, Yaw = -22.5, Roll = 0.0 })
Env.AddBuilding(block, { X = 71, Y = 5  }, { X = 10, Y = 6 }, "House", { Pitch = 0.0, Yaw = -22.5, Roll = 0.0 })
Env.AddBuilding(block, { X = 78, Y = 9  }, { X = 10, Y = 6 }, "House", { Pitch = 0.0, Yaw = -22.5, Roll = 0.0 })
Env.AddBuilding(block, { X = 86, Y = 13 }, { X = 10, Y = 6 }, "House", { Pitch = 0.0, Yaw = -22.5, Roll = 0.0 })

Env.AddBuilding(block, { X = 5,  Y = 25 }, { X = 10, Y = 6 }, "House", { Pitch = 0.0, Yaw = 90.0,  Roll = 0.0 })
Env.AddBuilding(block, { X = 8,  Y = 30 }, { X = 8,  Y = 6 }, "House", { Pitch = 0.0, Yaw = 112.5, Roll = 0.0 })

Env.AddBuilding(block, { X = 22, Y = 22 }, { X = 6,  Y = 6 }, "House", { Pitch = 0.0, Yaw = 45.0,  Roll = 0.0 })
Env.AddBuilding(block, { X = 58, Y = 32 }, { X = 6,  Y = 4 }, "House", { Pitch = 0.0, Yaw = 22.5,  Roll = 0.0 })

Env.AddBuilding(block, { X = 14, Y = 40 }, { X = 10, Y = 6 }, "House", { Pitch = 0.0, Yaw = 0.0,   Roll = 0.0 })
Env.AddBuilding(block, { X = 10, Y = 46 }, { X = 8,  Y = 6 }, "House", { Pitch = 0.0, Yaw = -22.5, Roll = 0.0 })

Env.AddBuilding(block, { X = 43, Y = 39 }, { X = 12, Y = 6 }, "House", { Pitch = 0.0, Yaw = 0.0,   Roll = 0.0 })
Env.AddBuilding(block, { X = 51, Y = 42 }, { X = 10, Y = 6 }, "House", { Pitch = 0.0, Yaw = 0.0,   Roll = 0.0 })
Env.AddBuilding(block, { X = 59, Y = 45 }, { X = 8,  Y = 6 }, "House", { Pitch = 0.0, Yaw = 22.5,  Roll = 0.0 })

Env.AddBuilding(block, { X = 83, Y = 37 }, { X = 12, Y = 6 }, "House", { Pitch = 0.0, Yaw = 67.5,  Roll = 0.0 })
Env.AddBuilding(block, { X = 87, Y = 43 }, { X = 10, Y = 6 }, "House", { Pitch = 0.0, Yaw = 90.0,  Roll = 0.0 })

Env.AddProp(block, "Prop_Fountain", { X = 9900.0, Y = 4300.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 0.0, Roll = 0.0 })
if Env.IsSpaceEmpty(block, { X = 10800.0, Y = 4300.0, Z = 0.0 }, { X = 1000.0, Y = 800.0 }) then Env.AddProp(block, "Prop_Bar", { X = 10800.0, Y = 4300.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 90.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 8600.0, Y = 3800.0, Z = 0.0 }, { X = 800.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Market", { X = 8600.0, Y = 3800.0, Z = 0.0 }, { Pitch = 0.0, Yaw = -45.0, Roll = 0.0 }) end
do
    local placed = false
    local stageSize = { X = 1100.0, Y = 800.0 }
    local candidates = {
        { X = 8800.0, Y = 4300.0, Z = 0.0 },
        { X = 9900.0, Y = 3200.0, Z = 0.0 },
        { X = 10800.0, Y = 4300.0, Z = 0.0 },
        { X = 9900.0, Y = 5400.0, Z = 0.0 },
        { X = 7800.0, Y = 4300.0, Z = 0.0 },
        { X = 9900.0, Y = 2100.0, Z = 0.0 },
        { X = 12000.0, Y = 4300.0, Z = 0.0 },
        { X = 9900.0, Y = 6500.0, Z = 0.0 }
    }
    for i = 1, #candidates do
        local p = candidates[i]
        if Env.IsSpaceEmpty(block, p, stageSize) then
            Env.AddProp(block, "Prop_Stage", p, { Pitch = 0.0, Yaw = 0.0, Roll = 0.0 })
            placed = true
            break
        end
    end
    if not placed then
        Env.AddProp(block, "Prop_Stage", { X = 9900.0, Y = 4300.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 0.0, Roll = 0.0 })
    end
end

Env.PaintTerrain(map, 75, 83, 10.0, "Grass")
Env.PaintTerrain(map, 65, 68, 8.0, "Grass")
Env.PaintTerrain(map, 89, 68, 7.0, "Grass")
Env.PaintTerrain(map, 115, 64, 8.0, "Grass")
Env.PaintTerrain(map, 130, 70, 8.0, "Grass")
Env.PaintTerrain(map, 55, 90, 9.0, "Grass")
Env.PaintTerrain(map, 67, 80, 4.0, "Grass")
Env.PaintTerrain(map, 60, 103, 7.0, "Grass")
Env.PaintTerrain(map, 93, 102, 8.0, "Grass")
Env.PaintTerrain(map, 105, 105, 5.0, "Grass")
Env.PaintTerrain(map, 133, 100, 9.0, "Grass")

if Env.IsSpaceEmpty(block, { X = 1200.0, Y = 1000.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 1200.0, Y = 1000.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 15.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 2600.0, Y = 800.0,  Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 2600.0, Y = 800.0,  Z = 0.0 }, { Pitch = 0.0, Yaw = 40.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 4200.0, Y = 900.0,  Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 4200.0, Y = 900.0,  Z = 0.0 }, { Pitch = 0.0, Yaw = 85.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 6200.0, Y = 900.0,  Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 6200.0, Y = 900.0,  Z = 0.0 }, { Pitch = 0.0, Yaw = 120.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 8200.0, Y = 900.0,  Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 8200.0, Y = 900.0,  Z = 0.0 }, { Pitch = 0.0, Yaw = 160.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 10400.0, Y = 900.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 10400.0, Y = 900.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 205.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 12800.0, Y = 900.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 12800.0, Y = 900.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 250.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 15200.0, Y = 900.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 15200.0, Y = 900.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 300.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 17600.0, Y = 900.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 17600.0, Y = 900.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 340.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 19400.0, Y = 1200.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 19400.0, Y = 1200.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 20.0, Roll = 0.0 }) end

if Env.IsSpaceEmpty(block, { X = 900.0,  Y = 1800.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 900.0,  Y = 1800.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 35.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 900.0,  Y = 3600.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 900.0,  Y = 3600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 90.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 900.0,  Y = 5600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 900.0,  Y = 5600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 150.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 900.0,  Y = 7600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 900.0,  Y = 7600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 210.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 1000.0, Y = 9300.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 1000.0, Y = 9300.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 270.0, Roll = 0.0 }) end

if Env.IsSpaceEmpty(block, { X = 19400.0, Y = 1800.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 19400.0, Y = 1800.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 30.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 19400.0, Y = 3600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 19400.0, Y = 3600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 95.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 19400.0, Y = 5600.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 19400.0, Y = 5600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 155.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 19400.0, Y = 7600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 19400.0, Y = 7600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 235.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 19200.0, Y = 9300.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 19200.0, Y = 9300.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 320.0, Roll = 0.0 }) end

if Env.IsSpaceEmpty(block, { X = 1800.0, Y = 9600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 1800.0, Y = 9600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 25.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 3800.0, Y = 9600.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 3800.0, Y = 9600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 70.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 6000.0, Y = 9600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 6000.0, Y = 9600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 120.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 8200.0, Y = 9600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 8200.0, Y = 9600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 165.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 10400.0, Y = 9600.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 10400.0, Y = 9600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 210.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 12600.0, Y = 9600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 12600.0, Y = 9600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 255.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 14800.0, Y = 9600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 14800.0, Y = 9600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 300.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 17000.0, Y = 9600.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 17000.0, Y = 9600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 345.0, Roll = 0.0 }) end

if Env.IsSpaceEmpty(block, { X = 2500.0, Y = 2100.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 2500.0, Y = 2100.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 20.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 3700.0, Y = 2900.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 3700.0, Y = 2900.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 65.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 5200.0, Y = 2300.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 5200.0, Y = 2300.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 110.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 6500.0, Y = 3100.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 6500.0, Y = 3100.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 165.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 5600.0, Y = 4600.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 5600.0, Y = 4600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 220.0, Roll = 0.0 }) end

if Env.IsSpaceEmpty(block, { X = 7600.0, Y = 2100.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 7600.0, Y = 2100.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 15.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 9200.0, Y = 2100.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 9200.0, Y = 2100.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 60.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 10800.0, Y = 2100.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 10800.0, Y = 2100.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 120.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 12200.0, Y = 3200.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 12200.0, Y = 3200.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 180.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 11000.0, Y = 4700.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 11000.0, Y = 4700.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 240.0, Roll = 0.0 }) end

if Env.IsSpaceEmpty(block, { X = 12600.0, Y = 1800.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 12600.0, Y = 1800.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 10.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 14200.0, Y = 2400.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 14200.0, Y = 2400.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 55.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 15800.0, Y = 3000.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 15800.0, Y = 3000.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 110.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 17400.0, Y = 3600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 17400.0, Y = 3600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 165.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 18600.0, Y = 4700.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 18600.0, Y = 4700.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 230.0, Roll = 0.0 }) end

if Env.IsSpaceEmpty(block, { X = 2400.0, Y = 5400.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 2400.0, Y = 5400.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 30.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 3600.0, Y = 6200.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 3600.0, Y = 6200.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 90.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 2500.0, Y = 7300.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 2500.0, Y = 7300.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 140.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 4200.0, Y = 8200.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 4200.0, Y = 8200.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 220.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 5200.0, Y = 9100.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 5200.0, Y = 9100.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 300.0, Roll = 0.0 }) end

if Env.IsSpaceEmpty(block, { X = 6100.0, Y = 6100.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 6100.0, Y = 6100.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 20.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 7600.0, Y = 6900.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 7600.0, Y = 6900.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 85.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 9300.0, Y = 6400.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 9300.0, Y = 6400.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 140.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 11100.0, Y = 7100.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 11100.0, Y = 7100.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 200.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 12600.0, Y = 6400.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 12600.0, Y = 6400.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 260.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 14500.0, Y = 7000.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 14500.0, Y = 7000.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 320.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 16100.0, Y = 7800.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 16100.0, Y = 7800.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 20.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 17700.0, Y = 8500.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 17700.0, Y = 8500.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 90.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 18800.0, Y = 9100.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 18800.0, Y = 9100.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 160.0, Roll = 0.0 }) end

if Env.IsSpaceEmpty(block, { X = 5600.0, Y = 2400.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 5600.0, Y = 2400.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 35.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 7000.0, Y = 3600.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 7000.0, Y = 3600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 100.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 8600.0, Y = 4800.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 8600.0, Y = 4800.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 160.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 11400.0, Y = 5000.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 11400.0, Y = 5000.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 220.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 13800.0, Y = 5000.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 13800.0, Y = 5000.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 285.0, Roll = 0.0 }) end

if Env.IsSpaceEmpty(block, { X = 4800.0, Y = 1600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 4800.0, Y = 1600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 10.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 5800.0, Y = 1600.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 5800.0, Y = 1600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 50.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 12400.0, Y = 1600.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree1", { X = 12400.0, Y = 1600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 95.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 16800.0, Y = 2600.0, Z = 0.0 }, { X = 200.0, Y = 200.0 }) then Env.AddProp(block, "Prop_Tree3", { X = 16800.0, Y = 2600.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 150.0, Roll = 0.0 }) end
if Env.IsSpaceEmpty(block, { X = 18400.0, Y = 6200.0, Z = 0.0 }, { X = 600.0, Y = 600.0 }) then Env.AddProp(block, "Prop_Tree2", { X = 18400.0, Y = 6200.0, Z = 0.0 }, { Pitch = 0.0, Yaw = 210.0, Roll = 0.0 }) end

Env.ValidateMap(map)
local levelRoot = Env.BuildAsync(map)