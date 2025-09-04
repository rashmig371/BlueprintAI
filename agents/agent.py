from azure.ai.agents.models import AgentThreadCreationOptions, ThreadMessageOptions, ListSortOrder
from utils.utility_functions import get_agent_id_by_name
from utils.utility_functions import get_agents_client


class Agent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions
        self.client = get_agents_client()
        self.agent = None
        self.agent_id = get_agent_id_by_name(name)

    def create(self, model: str = "gpt-4o-mini"):
        # if agent_id is provided, we will fetch the existing agent
        if self.agent_id:
            self.agent = self.client.get_agent(self.agent_id)
        else:
            self.agent = self.client.create_agent(
                model=model,
                name=self.name,
                instructions=self.instructions
            )
            self.agent_id = self.agent.id
        return self.agent

    def run(self, user_input: str) -> str:
        if not self.agent:
            raise ValueError("Agent must be created before running.")

        run = self.client.create_thread_and_process_run(
            agent_id=self.agent.id,
            thread=AgentThreadCreationOptions(
                messages=[ThreadMessageOptions(role="user", content=user_input)]
            )
        )

        if run.status == "failed":
            return f"Run failed: {run.last_error}"

        messages = self.client.messages.list(thread_id=run.thread_id, order=ListSortOrder.ASCENDING)
        # Find the last assistant message with text content
        assistant_response = None
        for msg in reversed(list(messages)):
            if msg.role == "assistant" and msg.content:
                for content in msg.content:
                    if content["type"] == "text" and "text" in content and "value" in content["text"]:
                        assistant_response = content["text"]["value"]
                        break
            if assistant_response:
                break
        return assistant_response or "No assistant response received."

