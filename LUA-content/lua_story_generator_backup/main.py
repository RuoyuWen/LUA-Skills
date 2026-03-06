"""FastAPI backend for LUA Story Generator."""
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import config
from orchestrator import run_full_pipeline

app = FastAPI(title="LUA Story to Script Generator")
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


class GenerateResponse(BaseModel):
    expanded_story: str
    plan_output: str
    steps: list
    generated_files: dict


@app.get("/")
def root():
    """Serve frontend or API info."""
    from fastapi.responses import FileResponse
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"status": "ok", "app": "LUA Story Generator"}


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

    try:
        result = run_full_pipeline(
            story_input=req.story_input.strip(),
            api_key=req.api_key.strip(),
            story_model=req.story_model,
            planning_model=req.planning_model,
            coding_model=req.coding_model,
        )
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
