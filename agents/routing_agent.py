
import os
import json
import httpx
import asyncio
from typing import Dict, Any
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from a2a.client import A2ACardResolver

from remote.remote_agent_connection import RemoteAgentConnection   
from agents.planning_agent import PlanningAgent
from agents.validation_agent import ValidationAgent

class RoutingAgent:
    def __init__(self):
        self.remote_agent_connections: Dict[str, RemoteAgentConnection] = {}
        self.cards: Dict[str, Any] = {}
        self.agents_client = AgentsClient(
            endpoint="https://hack25-aifoundry.services.ai.azure.com/api/projects/BlueprintAI",
            credential=DefaultAzureCredential(),
        )
        self.azure_agent = None
        self.current_thread = None

    async def initialize(self, remote_agent_addresses: list[str]):
        async with httpx.AsyncClient(timeout=30) as client:
            for address in remote_agent_addresses:
                try:
                    card_resolver = A2ACardResolver(client, address)
                    card = await card_resolver.get_agent_card()
                    remote_connection = RemoteAgentConnection(card, address)
                    self.remote_agent_connections[card.name] = remote_connection
                    self.cards[card.name] = card
                except Exception as e:
                    print(f"Failed to connect to agent at {address}: {e}")

        await self._create_azure_agent()

    async def _create_azure_agent(self):
        instructions = self._get_routing_instructions()
        tools = [{
            "type": "function",
            "function": {
                "name": "send_message",
                "description": "Delegate task to specialized remote agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_name": {"type": "string"},
                        "task": {"type": "string"}
                    },
                    "required": ["agent_name", "task"]
                }
            }
        }]

        model_name = os.environ.get("AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME", "gpt-4")
        self.azure_agent = self.agents_client.create_agent(
            model=model_name,
            name="routing-agent",
            instructions=instructions,
            tools=tools
        )
        self.current_thread = self.agents_client.threads.create()
        print(f"Routing agent initialized: {self.azure_agent.id}")

    def _get_routing_instructions(self) -> str:
        agent_info = [
            {'name': card.name, 'description': card.description}
            for card in self.cards.values()
        ]
        return f"""You are an intelligent routing agent for a multi-agent system.

        Available Specialist Agents:
        {json.dumps(agent_info, indent=2)}"""
