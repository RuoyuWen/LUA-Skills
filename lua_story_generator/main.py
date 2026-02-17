"""FastAPI backend for LUA Story Generator."""
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import config
from orchestrator import run_full_pipeline

app = FastAPI(title="LUA Story to Script Generator")
APP_DIR = Path(__file__).parent
ASSETS_FILE = APP_DIR / "assets.json"
DEFAULT_ASSETS = APP_DIR / "assets_default.json"
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    story_input: str
    api_key: str
    story_model: str = "gpt-4.1"
    planning_model: str = "gpt-4.1"
    coding_model: str = "gpt-5.1-codex-max"
    assets: dict | None = None  # {npcs:[], enemies:[], props:[]}


class AssetsModel(BaseModel):
    npcs: list[str] = []
    enemies: list[str] = []
    props: list[str] = []


class GenerateResponse(BaseModel):
    expanded_story: str
    plan_output: str
    steps: list
    generated_files: dict
    full_script: str  # 拼装好的完整 LUA 脚本


@app.get("/")
def root():
    """Serve frontend or API info."""
    from fastapi.responses import FileResponse
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"status": "ok", "app": "LUA Story Generator"}


def _load_assets() -> dict:
    if ASSETS_FILE.exists():
        try:
            return json.loads(ASSETS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    if DEFAULT_ASSETS.exists():
        return json.loads(DEFAULT_ASSETS.read_text(encoding="utf-8"))
    return {"npcs": [], "enemies": [], "props": []}


def _save_assets(data: dict) -> None:
    with open(ASSETS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/api/assets")
def get_assets():
    """获取素材库"""
    return _load_assets()


@app.post("/api/assets")
def save_assets(data: AssetsModel):
    """保存素材库"""
    _save_assets({"npcs": data.npcs, "enemies": data.enemies, "props": data.props})
    return {"ok": True}


@app.get("/models")
def get_models():
    """Return available models for each phase."""
    return {
        "story": config.STORY_MODELS,
        "planning": config.PLANNING_MODELS,
        "coding": config.CODING_MODELS,
    }


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    """Run full pipeline: story expansion -> planning -> code generation."""
    if not req.api_key or not req.api_key.strip():
        raise HTTPException(status_code=400, detail="API Key is required")

    if not req.story_input or not req.story_input.strip():
        raise HTTPException(status_code=400, detail="Story input is required")

    if req.story_model not in config.STORY_MODELS:
        req.story_model = config.STORY_MODELS[0]
    if req.planning_model not in config.PLANNING_MODELS:
        req.planning_model = config.PLANNING_MODELS[0]
    if req.coding_model not in config.CODING_MODELS:
        req.coding_model = config.CODING_MODELS[0]

    assets = req.assets or _load_assets()
    if not assets.get("npcs") and not assets.get("enemies") and not assets.get("props"):
        assets = _load_assets()

    try:
        result = run_full_pipeline(
            story_input=req.story_input.strip(),
            api_key=req.api_key.strip(),
            story_model=req.story_model,
            planning_model=req.planning_model,
            coding_model=req.coding_model,
            assets=assets,
        )
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
