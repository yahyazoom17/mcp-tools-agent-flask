from agent_config.my_agent.agent import run_agent_with_query

async def run_agent(agent_data:dict):
    try:
        agent_name = agent_data.get('agent_name')
        model_name = agent_data.get('model_name')
        tools = agent_data.get('tools', [])
        instruction = agent_data.get('instruction', '')
        user_id = agent_data.get('user_id')
        query = agent_data.get('query')

        # Optionally validate required fields
        if not all([agent_name, model_name, instruction, user_id]):
            raise ValueError("Missing one or more required fields: 'agent_name', 'model_name', 'instruction', 'user_id'")

        return await configure_agent(
            user_id=user_id,
            query=query,
            agent_data=agent_data
        )

    except Exception as e:
        print(f"[ERROR] run_agent failed: {e}")
        return {"error": str(e)}
