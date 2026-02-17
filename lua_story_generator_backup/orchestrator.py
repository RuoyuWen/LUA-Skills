"""Orchestrator: runs full pipeline Story -> Plan -> Code."""
from typing import Optional

from openai import OpenAI

from agents import (
    extract_steps_from_planner_output,
    run_coding_agent,
    run_planner,
    run_story_expert,
)
import config


def run_full_pipeline(
    story_input: str,
    api_key: str,
    story_model: str = "gpt-4.1",
    planning_model: str = "gpt-4.1",
    coding_model: str = "gpt-5.1-codex-max",
) -> dict:
    """
    Execute: Story Expert -> Planner -> Coding Agent (per step).
    Returns { expanded_story, plan, steps, generated_files: { filename: code } }
    """
    client = OpenAI(api_key=api_key)

    # Phase 1: Story Expert
    expanded_story = run_story_expert(
        client, story_input, story_model, api_key=None
    )

    # Phase 2: Planner
    plan_output = run_planner(
        client, expanded_story, planning_model, api_key=None
    )
    steps = extract_steps_from_planner_output(plan_output)
    if not steps:
        steps = [
            {
                "id": 1,
                "name": "SpawnEncounter_main",
                "type": "encounter",
                "description": "Main encounter from expanded story",
            }
        ]

    # Phase 3: Coding Agent (per step)
    generated_files = {}
    previous_code = ""

    for i, step in enumerate(steps):
        code = run_coding_agent(
            client,
            step,
            expanded_story,
            previous_code,
            coding_model,
            api_key=None,
        )
        # Clean code: remove markdown code blocks if present
        code = _clean_code_output(code)

        step_name = step.get("name", f"step_{i+1}")
        if step.get("type") == "setup":
            filename = "Setup_World.lua"
        elif step.get("type") == "encounter":
            filename = f"Encounters/enc_{step_name.replace('SpawnEncounter_', '').lower()}.lua"
        else:
            filename = f"{step_name}.lua"

        generated_files[filename] = code
        previous_code += "\n\n" + code

    # Generate Main.lua
    main_code = _generate_main_lua(generated_files)
    generated_files["Main.lua"] = main_code

    return {
        "expanded_story": expanded_story,
        "plan_output": plan_output,
        "steps": steps,
        "generated_files": generated_files,
    }


def _clean_code_output(text: str) -> str:
    """Remove markdown code blocks if present."""
    import re
    text = text.strip()
    # ```lua ... ``` or ``` ... ```
    m = re.search(r"```(?:lua)?\s*\n([\s\S]*?)```", text)
    if m:
        return m.group(1).strip()
    return text


def _generate_main_lua(files: dict) -> str:
    """Generate Main.lua that requires all modules in correct order."""
    setup_lines = []
    enc_lines = []

    if "Setup_World.lua" in files:
        setup_lines.append('require("Setup_World")')
    if "Spawn_AmbientNPC.lua" in files:
        setup_lines.append('require("Spawn_AmbientNPC")')

    for k in sorted(files.keys()):
        if k.startswith("Encounters/") and k.endswith(".lua"):
            mod = k.replace("Encounters/", "").replace(".lua", "")
            enc_lines.append(f'require("Encounters.{mod}")')

    if not setup_lines:
        setup_lines.append('-- require("Setup_World")  -- add if you have Setup')
    if not enc_lines:
        enc_lines.append('-- require("Encounters.enc_main")  -- add encounter')

    main = """Time.Pause()

-- 1) build world
"""
    main += "\n".join(setup_lines)
    main += """

-- 2) register encounters
"""
    main += "\n".join(enc_lines)
    main += """

World.StartGame()
Time.Resume()
UI.Toast("游戏开始")
"""
    return main
