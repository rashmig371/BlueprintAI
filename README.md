# Intelligent Project Execution Agent

This project simulates a multi-agent system using Azure AI Foundry to generate and validate project execution plans.

## Structure
- `agents/`: Contains specialized agent classes.
- `remote/`: Manages remote agent connections.
- `config/`: Stores environment variables.
- `main.py`: Entry point to run the system.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure `.env` with your Azure Foundry details.
3. Run the system:
   ```bash
   python main.py
