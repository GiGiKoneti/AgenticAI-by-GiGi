from typing import Dict, Any
from .decomposer import decompose_task
from .router import route_and_execute
from agents.reflection_agent import ReflectionAgent

reflection_agent = ReflectionAgent()

def run_orchestration(user_message: str) -> Dict[str, Any]:
    """
    High-level orchestration:
    1. Decompose user message into tasks.
    2. Route tasks to agents.
    3. Run reflection on combined output.
    """
    decomposition = decompose_task(user_message)
    tasks = decomposition.get("tasks", [])

    agent_result = route_and_execute(tasks)
    route = agent_result.get("route", [])
    print("[AURA] Route taken:", route)  # 👈 small debug print

    combined = {
        "decomposition": decomposition,
        "agent_result": agent_result,
    }

    # Reflection: improve final answer
    reflection_output = reflection_agent.run({"combined": combined})

    return {
        "combined": combined,
        "reflection": reflection_output,
        "route": route,
    }