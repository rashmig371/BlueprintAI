import os
from dotenv import load_dotenv
from agents.planning_agent import PlanningAgent
from agents.validation_agent import ValidationAgent
from utils.utility_functions import read_env_variable

print("Loading environment variables from .env file...")
load_dotenv(dotenv_path=os.path.join("config", ".env"))

def main():
    # Sample project input
    print("Starting Intelligent Project Execution...\n")
    project_details = {
        "name": "AI-Powered CRM",
        "requirements": "Build a scalable CRM with AI features like lead scoring and sentiment analysis.",
        "timeline_weeks": 12,
        "team_size": 5
    }

    # Initialize and create Planning Agent
    planning_agent = PlanningAgent()
    planning_agent.create(
        model=read_env_variable("MODEL_DEPLOYMENT_NAME") or "gpt-4o-mini"
    )

    planning_prompt = (
        f"Create a detailed execution plan for the following project:"
        f"Name: {project_details['name']}"
        f"Requirements: {project_details['requirements']}"
        f"Timeline: {project_details['timeline_weeks']} weeks"
        f"Team Size: {project_details['team_size']}"
    )

    # Generate execution plan
    execution_plan = planning_agent.plan(planning_prompt)
    print("Execution Plan ---")
    print(execution_plan)

    # Initialize and create Validation Agent
    validation_agent = ValidationAgent()
    validation_agent.create(
        model=read_env_variable("MODEL_DEPLOYMENT_NAME") or "gpt-4o-mini"
    )

    # Validate the execution plan
    validation_report = validation_agent.validate(execution_plan)
    print("Validation Report ---")
    print(validation_report)

if __name__ == "__main__":
    main()