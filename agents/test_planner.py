from agents.planner_agent import PlannerAgent

agent = PlannerAgent()

output = agent.run({"text": "Help me prepare for my AI exam tonight."})
print(output)