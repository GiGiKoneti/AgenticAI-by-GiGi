from typing import Dict, Any, List
from agents.document_agent import DocumentAgent
from agents.notification_agent import NotificationAgent
from agents.planner_agent import PlannerAgent
from agents.reflection_agent import ReflectionAgent

AGENT_REGISTRY = {
    "document": DocumentAgent(),
    "notification": NotificationAgent(),
    "planner": PlannerAgent(),
    "reflection": ReflectionAgent(),
}

def route_and_execute(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Executes each agent in sequence.
    Each agent receives:
        - details from the decomposer
        - previous agent outputs (context)
    """

    results = []
    route = []
    shared_context = {}  # NEW: accumulate output here

    for task in tasks:
        agent_name = task.get("agent")
        agent = AGENT_REGISTRY.get(agent_name)

        if not agent:
            results.append({"agent": agent_name, "error": "Unknown agent"})
            continue

        # Merge context into agent details
        details = task.get("details", {})
        details["context"] = shared_context  # << ADD CONTEXT

        output = agent.run(details)

        # Save output into shared context for next agent
        shared_context[agent_name] = output

        results.append({
            "agent": agent_name,
            "input": details,
            "output": output
        })
        route.append(agent_name)

    return {
        "results": results,
        "route": route,
        "shared_context": shared_context
    }