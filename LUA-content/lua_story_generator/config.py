"""Configuration for LUA Story Generator."""
import os
from pathlib import Path

# Model identifiers - 若 API 模型名不同可替换为 gpt-4o、gpt-4-turbo 等
STORY_MODELS = ["gpt-4.1", "gpt-5.1"]
PLANNING_MODELS = ["gpt-4.1", "gpt-5.1"]
CODING_MODELS = ["gpt-4.1", "gpt-5.1", "gpt-5.1-codex-max", "gpt-5.2-codex"]  # Codex 使用 Responses API

# Document paths (relative to project root, used by skills_loader)
LUA_API_DOC = "lua_atomic_modules_call_guide.md"
RULE_DOC = "rule.md"

# Project root (parent of lua_story_generator)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DataTable CSV 路径：素材库 NPC/Enemy/Prop/Item 从此读取，启动时加载
# 通过环境变量 DATATABLE_DIR 覆盖，以适配不同部署路径
_PROJECT_ROOT_PATH = Path(PROJECT_ROOT).resolve()
# LUA-Skills -> LLM_AI -> ChronicleForge，2 级至 ChronicleForge/Doc/DataTable
_DEFAULT_DATATABLE = _PROJECT_ROOT_PATH / ".." / ".." / "Doc" / "DataTable"
DATATABLE_DIR = Path(os.environ.get("DATATABLE_DIR", str(_DEFAULT_DATATABLE.resolve())))

# 地图地面高度与玩家出生区域（玩家落地后约 X=11536, Y=11963, Z=90）
GROUND_Z = 90
# 奇遇基准坐标：靠近玩家落地位置，确保触发盒子在地面层级
ENCOUNTER_BASE_X = 11600
ENCOUNTER_BASE_Y = 12000
