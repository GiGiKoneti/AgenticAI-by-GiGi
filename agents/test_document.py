import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from document_agent import DocumentAgent

agent = DocumentAgent()

sample = {
    "text": "Your internal exam is on 5 Dec 2025. Submit lab records by 3rd Dec."
}

print(agent.run(sample))