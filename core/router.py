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
    Given a list of tasks from the decomposer, call the right agents.
    """
    results = []
    route = []

    for task in tasks:
        agent_name = task.get("agent")
        agent = AGENT_REGISTRY.get(agent_name)

        if not agent:
            results.append({"agent": agent_name, "error": "Unknown agent"})
            continue

        output = agent.run(task.get("details", {}))
        results.append({"agent": agent_name, "output": output})
        route.append(agent_name)

    return {"results": results, "route": route}