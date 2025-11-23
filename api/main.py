from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from core.orchestrator import run_orchestration  # 👈 NEW IMPORT

app = FastAPI(
    title="AURA Agentic System",
    description="Multi-agent AI framework with local LLMs via Ollama",
    version="0.1.0",
)

# ---------- Schemas ----------

class ChatRequest(BaseModel):
    user_id: Optional[str] = "demo-user"
    message: str

class ChatResponse(BaseModel):
    reply: str
    route: Optional[List[str]] = None        # which agents ran
    raw: Optional[Dict[str, Any]] = None     # full internal structure (for debugging)


# ---------- Basic Routes ----------

@app.get("/")
def root():
    return {"status": "ok", "message": "AURA backend is running 🚀"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """
    Main chat endpoint.
    1. Runs orchestration (decompose -> route agents -> reflection).
    2. Extracts a user-friendly reply.
    3. Returns both reply + route + optional raw debug.
    """
    orchestration_result = run_orchestration(req.message)

    # Extract route (which agents were called)
    route = orchestration_result.get("route", [])

    # For now, build a simple user-facing reply from planner + reflection
    combined = orchestration_result.get("combined", {})
    agent_result = combined.get("agent_result", {})
    results = agent_result.get("results", [])

    # Try to find planner output if exists
    planner_output = None
    for r in results:
        if r.get("agent") == "planner":
            planner_output = r.get("output")
            break

    reflection = orchestration_result.get("reflection", {})

    # Build a simple readable reply
    lines = []

    if planner_output:
        plan = planner_output.get("plan", [])
        if isinstance(plan, list):
            lines.append("Here is your suggested plan:\n")
            for step in plan:
                lines.append(f"- {step}")
        else:
            lines.append(str(plan))

    # Add reflection note if available
    if reflection:
        ref_text = reflection.get("reflection")
        if ref_text:
            lines.append("\n\nReflection:\n" + ref_text)

    # Fallback if nothing else
    if not lines:
        lines.append("AURA processed your request, but has no detailed reply yet.")

    reply_text = "\n".join(lines)

    return ChatResponse(
        reply=reply_text,
        route=route,
        raw=orchestration_result,  # you can hide this later
    )