"""RAG module for retrieving relevant LUA API and rule documentation."""
import os
import re
from pathlib import Path
from typing import List, Tuple

import config


def load_document(path: str) -> str:
    """Load a document from the project root."""
    full_path = Path(config.PROJECT_ROOT) / path
    if not full_path.exists():
        return ""
    return full_path.read_text(encoding="utf-8")


def chunk_by_sections(text: str) -> List[Tuple[str, str]]:
    """Split document into sections (heading, content)."""
    chunks = []
    lines = text.split("\n")
    current_heading = ""
    current_content: List[str] = []

    for line in lines:
        if line.startswith("#") or line.startswith("##") or line.startswith("###"):
            if current_content:
                chunks.append((current_heading, "\n".join(current_content)))
            current_heading = line.strip()
            current_content = [line]
        else:
            current_content.append(line)

    if current_content:
        chunks.append((current_heading, "\n".join(current_content)))
    return chunks


def extract_api_sections(lua_doc: str) -> List[str]:
    """Extract API-related sections for coding context."""
    chunks = chunk_by_sections(lua_doc)
    relevant = []
    for heading, content in chunks:
        if any(
            kw in heading.lower() or kw in content.lower()
            for kw in ["api", "event", "world", "ui", "time", "entity", "performer", "math", "env"]
        ):
            relevant.append(f"{heading}\n{content}")
    return relevant


def get_rag_context_for_step(
    step_name: str,
    step_description: str,
) -> str:
    """
    Retrieve relevant documentation for a given generation step.
    Uses keyword matching (simple RAG) to select sections.
    """
    lua_doc = load_document(config.LUA_API_DOC)
    rule_doc = load_document(config.RULE_DOC)

    # Build keyword set from step
    step_lower = f"{step_name} {step_description}".lower()
    keywords = set(re.findall(r"\w+", step_lower))

    context_parts = []

    # For Encounter steps: need Encounter rules, World API, UI API, Performer API
    if "encounter" in step_lower or "奇遇" in step_lower:
        context_parts.append("=== ENCOUNTER DESIGN RULES (rule.md) ===\n")
        # Extract encounter-related from rule
        for match in re.finditer(
            r"(#+\s+.*?Encounter.*?)(?=#+\s|\Z)",
            rule_doc,
            re.DOTALL | re.IGNORECASE,
        ):
            context_parts.append(match.group(1)[:8000])

        context_parts.append("\n\n=== LUA API RELEVANT TO ENCOUNTERS ===\n")
        lua_chunks = extract_api_sections(lua_doc)
        for c in lua_chunks[:15]:  # Limit size
            context_parts.append(c[:3000])
            context_parts.append("\n---\n")

    # For Setup steps: need Env API, World setup
    elif "setup" in step_lower or "世界" in step_lower or "地图" in step_lower:
        context_parts.append("=== SETUP RULES (rule.md) ===\n")
        for match in re.finditer(
            r"(#+\s+.*?Setup.*?)(?=#+\s|\Z)",
            rule_doc,
            re.DOTALL | re.IGNORECASE,
        ):
            context_parts.append(match.group(1)[:6000])

        context_parts.append("\n\n=== ENV API (lua_atomic_modules_call_guide.md) ===\n")
        if "3.8" in lua_doc or "Env" in lua_doc:
            idx = lua_doc.find("### 3.8 `Env`")
            if idx >= 0:
                context_parts.append(lua_doc[idx : idx + 12000])

    # For Main.lua or general: full rule structure + API overview
    else:
        context_parts.append("=== RULE STRUCTURE ===\n")
        context_parts.append(rule_doc[:12000])
        context_parts.append("\n\n=== LUA API OVERVIEW ===\n")
        context_parts.append(lua_doc[:15000])

    return "\n".join(context_parts)


def get_full_docs() -> str:
    """Get full documentation for comprehensive context."""
    lua_doc = load_document(config.LUA_API_DOC)
    rule_doc = load_document(config.RULE_DOC)
    return f"""# RULE DOCUMENT (rule.md)
{rule_doc}

# LUA API DOCUMENT (lua_atomic_modules_call_guide.md)
{lua_doc}
"""
