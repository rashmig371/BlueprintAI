from flask import Flask, request, jsonify
import asyncio
from agents.routing_agent import RoutingAgent

app = Flask(__name__)
routing_agent = RoutingAgent()

@app.route('/route', methods=['POST'])
def route():
    data = request.json
    remote_agents = data.get('remote_agents', [])
    # Initialize and run the routing agent asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(routing_agent.initialize(remote_agents))
    # You can add more logic to handle requests and return results
    return jsonify({"status": "initialized", "agents": list(routing_agent.cards.keys())})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)