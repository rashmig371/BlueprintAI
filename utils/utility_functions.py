import os
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential

_client_instance = None

def write_env_variable(key: str, value: str, env_path: str = "config/.env"):
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break
    if not found:
        lines.append(f"{key}={value}\n")
    with open(env_path, "w") as f:
        f.writelines(lines)

def read_env_variable(key: str) -> str | None:
    return os.getenv(key)

def get_agents_client():
    global _client_instance
    if _client_instance is None:
        _client_instance = AgentsClient(
            endpoint=read_env_variable("AZURE_AI_AGENT_ENDPOINT"),
            credential=DefaultAzureCredential()
        )
    return _client_instance

def get_agent_id_by_name(name: str) -> str:
    client = get_agents_client()
    agents = client.list_agents()
    for agent in agents:
        if agent.name == name:
            return agent.id
    return None