from typing import Dict, Any
from agents.agent import Agent

class ValidationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ValidationAgent",
            instructions=(
                "You are a validation agent. Given a project execution plan, assess it for risks including scalability, "
                "security, feasibility, and alignment with best practices. Provide a detailed validation report."
            )
        )

    def validate(self, execution_plan: Dict[str, Any]) -> str:
        return self.run(str(execution_plan))
