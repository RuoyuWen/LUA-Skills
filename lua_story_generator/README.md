# LUA 奇遇脚本生成器（Skills 版）

多 Agent AI 系统，将自然语言故事转换为符合 `rule.md` 规范的 LUA 奇遇脚本。采用 **Skills 思维**：Progressive Disclosure、Checklist、Feedback Loop。

## 流程

1. **故事专家 AI**：将简短故事扩写为完整奇遇剧本（TPA 格式）
2. **规划 AI**：按 `lua-planning` Skill + rule.md 拆解为开发步骤
3. **代码 AI**：每步按类型加载对应 Skill（lua-encounter / lua-setup-world），生成 LUA 代码
4. **校验反馈**：Encounter 代码通过 `validate_lua.py` 校验，不通过则自动修正（最多 2 轮）

## Skills 目录

```
skills/
├── lua-encounter/      # 奇遇脚本 Skill
│   ├── SKILL.md       # Checklist、模板、功能模块
│   └── reference.md   # API 参考
├── lua-setup-world/   # 地图 Setup Skill
│   ├── SKILL.md
│   └── reference.md
└── lua-planning/      # 规划 Skill
    └── SKILL.md
```

## 模型选择

- **故事/规划**：GPT 4.1、GPT 5.1
- **代码生成**：GPT 4.1、GPT 5.1、**Codex (gpt-5.1-codex-max)**

## 安装与运行

```bash
cd lua_story_generator
pip install -r requirements.txt
python main.py
```

访问 http://localhost:8000

## 目录结构

```
lua_story_generator/
├── main.py           # FastAPI 入口
├── config.py
├── skills_loader.py  # Progressive disclosure 加载 Skills
├── agents.py         # Story / Planner / Coding
├── orchestrator.py   # 流水线 + 校验反馈循环
├── validate_lua.py   # Encounter 规则校验
├── skills/           # Skill 定义
├── static/
│   └── index.html
└── requirements.txt
```

## 备份

改造前版本备份于 `lua_story_generator_backup/`。
