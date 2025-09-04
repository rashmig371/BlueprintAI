import os
from agents.agent import Agent
from typing import Dict, Any

class PlanningAgent(Agent):
    def __init__(self):
        super().__init__(
            name="PlanningAgent",
            instructions=(
                "You are a project planning assistant. Given project requirements, timeline, and team size, "
                "generate a milestone-based execution plan and suggest a suitable architecture. "
                "Use best practices from agile, DevOps, and cloud-native design."
            )
        )

    def plan(self, project_details: Dict[str, Any]) -> str:
        return self.run(str(project_details))
