from typing import Dict, Any
from .decomposer import decompose_task
from .router import route_and_execute
from agents.reflection_agent import ReflectionAgent

reflection_agent = ReflectionAgent()

def run_orchestration(user_message: str) -> Dict[str, Any]:
    decomposition = decompose_task(user_message)
    tasks = decomposition.get("tasks", [])

    agent_result = route_and_execute(tasks)

    # Give reflection ALL context
    reflection_output = reflection_agent.run({
        "combined": {
            "decomposition": decomposition,
            "agent_result": agent_result,
        }
    })

    return {
        "decomposition": decomposition,
        "agent_result": agent_result,
        "reflection": reflection_output,
        "route": agent_result.get("route", []),
    }