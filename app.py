from flask import Flask, request, jsonify
from agent_config.my_agent.agent import process_query, current_event_loop

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/create_agent', methods=['POST'])
def create_agent():
    data = request.json

@app.route("/ask_agent", methods=["POST"])
def ask():
    data = request.json
    agent_data = data.get("agent_data")
    user = data.get("user")
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        result = current_event_loop.run_until_complete(process_query(user, agent_data, query))
        return jsonify({"response": result})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
