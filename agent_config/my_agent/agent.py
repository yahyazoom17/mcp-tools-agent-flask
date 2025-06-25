from dotenv import load_dotenv

import warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

load_dotenv()
import os
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

from google.genai import types
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, SseServerParams
from google.adk.agents.llm_agent import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
import asyncio

current_event_loop = asyncio.get_event_loop()

async def process_query(user, agent_data, query):
    all_tools = []
    try:
        for tool in agent_data["tools"]:
            print(tool)
            if tool["connection_type"] == "sse":
                sse_tool = MCPToolset(
                    connection_params=SseServerParams(
                    url=tool["url"],
                    headers=tool["headers"],
                    )
                )
                sse_tool_data = await sse_tool.get_tools()
                all_tools += sse_tool_data
            else:
                stdio_tool = MCPToolset(
                    connection_params=StdioServerParameters(
                    command=tool["command"],
                    args=tool["args"],
                    )
                )
                stdio_tool_data = await stdio_tool.get_tools()
                all_tools += stdio_tool_data
    except Exception as e:
        print(e)

    agent = LlmAgent(
        name=agent_data["agent_name"],
        model=agent_data["model_name"],
        tools=all_tools,
        instruction=agent_data["instruction"],
    )

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        state={},
        app_name="mcp_app",
        user_id=user["user_id"],
    )

    content = types.Content(role="user", parts=[types.Part(text=query["prompt"]+query["history"])])

    runner = Runner(
        app_name="mcp_app",
        agent=agent,
        session_service=session_service,
    )

    response_stream = runner.run_async(
        session_id=session.id,
        user_id=session.user_id,
        new_message=content,
    )

    output = []
    async for message in response_stream:
        output.append(message.content.parts[0].text)

    return output

async def configure_agent(user, agent_data):
    all_tools = []
    try:
        for tool in agent_data["tools"]:
            if tool["connection_type"] == "stdio":
                sse_tool = MCPToolset(
                    connection_params=StdioServerParameters(
                    command=tool["command"],
                    args=tool["args"],
                    )
                )
                stdio_tool_data = await sse_tool.get_tools()
                all_tools.extend(stdio_tool_data)
            if tool["connection_type"] == "sse":
                sse_tool = MCPToolset(
                    connection_params=SseServerParams(
                    url=tool["url"],
                    headers=tool["headers"],
                    )
                )
                sse_tool_data = await sse_tool.get_tools()
                all_tools.extend(sse_tool_data)
            else:
                return f"Unknown connection type: {tool['connection_type']}"
    except Exception as e:
        print(e)

    agent = LlmAgent(
        name=agent_data["agent_name"],
        model=agent_data["model_name"],
        tools=all_tools,
        instruction=agent_data["instruction"],
    ) 