"""Configuration for LUA Story Generator."""
import os

# Model identifiers - 若 API 模型名不同可替换为 gpt-4o、gpt-4-turbo 等
STORY_MODELS = ["gpt-4.1", "gpt-5.1"]
PLANNING_MODELS = ["gpt-4.1", "gpt-5.1"]
CODING_MODELS = ["gpt-4.1", "gpt-5.1", "gpt-5.1-codex-max"]  # Codex 使用 Responses API

# RAG document paths (relative to project root)
LUA_API_DOC = "lua_atomic_modules_call_guide.md"
RULE_DOC = "rule.md"

# Project root (parent of lua_story_generator)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
