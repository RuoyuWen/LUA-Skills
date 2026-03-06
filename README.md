# LUA 项目

LUA（Lua Unreal Adventure）—— 基于多 Agent AI 的奇遇脚本生成系统，将自然语言故事转换为符合 Unreal 引擎规范的 Lua 奇遇脚本。

## 项目结构

```
LUA/
├── LUA-Skills/                    # 核心项目（多 Agent + Skills 架构）
│   ├── LUA-content/               # 内容与规范
│   │   ├── rule.md                # Encounter 开发规范
│   │   ├── lua_atomic_modules_call_guide.md  # Lua API 文档
│   │   └── lua_story_generator/   # 故事 → Lua 脚本生成器
│   ├── start.bat                  # 启动脚本
│   ├── 点击开始.bat
│   └── deploy.ps1
└── README.md
```

## 快速开始

### 1. 启动 LUA 奇遇脚本生成器

**方式一：双击启动**
```
双击 点击开始.bat 或 LUA-Skills\start.bat
```

**方式二：命令行**
```bash
cd LUA-Skills\LUA-content\lua_story_generator
pip install -r requirements.txt
python main.py
```

服务默认监听 `http://localhost:9000`。

### 2. 使用流程

1. 打开浏览器访问 `http://localhost:9000`
2. 输入 OpenAI API Key
3. 输入故事梗概，点击「生成 LUA 脚本」
4. 复制或下载生成的 `Full_Script.lua` 用于 Unreal 集成

## 核心功能

- **多 Agent 流水线**：故事扩写 → 规划拆解 → 代码生成 → 校验反馈
- **Skills 架构**：Progressive Disclosure、Checklist、Feedback Loop
- **DataTable 素材库**：自动加载 NPC、Enemy、Prop、Item 等
- **TCP 服务**：支持 Unreal 客户端直接调用（端口 9010）

## 环境要求

- Python 3.10+
- OpenAI API Key（或兼容接口）

## 更多文档

- [lua_story_generator 详细说明](LUA-Skills/LUA-content/lua_story_generator/README.md)
- [Unreal 集成指南](LUA-Skills/LUA-content/lua_story_generator/UNREAL_INTEGRATION.md)
- [Encounter 开发规范](LUA-Skills/LUA-content/rule.md)
- [Lua API 参考](LUA-Skills/LUA-content/lua_atomic_modules_call_guide.md)
