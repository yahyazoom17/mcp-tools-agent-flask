# MCP Tools Agent Flask

A Flask-based web service that provides an AI agent interface using Google's AI Development Kit (ADK) with Model Context Protocol (MCP) tool integration. This service allows you to create and interact with AI agents that can use various tools through MCP connections.

## 🚀 Features

- **AI Agent Creation**: Configure AI agents with custom instructions and tools
- **MCP Tool Integration**: Support for both SSE (Server-Sent Events) and STDIO MCP tool connections
- **RESTful API**: Simple HTTP endpoints for agent interaction
- **Session Management**: Built-in session handling for conversational AI
- **Google Gemini Integration**: Powered by Google's Gemini models

## 📋 Prerequisites

- Python 3.8+
- Google API Key with access to Gemini models
- MCP-compatible tools (optional, for enhanced functionality)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mcp-tools-agent-flask
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 🚀 Quick Start

1. **Start the Flask server**
   ```bash
   python app.py
   ```
   The server will start on `http://localhost:3000`

2. **Test the connection**
   ```bash
   curl http://localhost:3000
   ```
   You should see: `Hello, World!`

## 📡 API Endpoints

### GET /
Simple health check endpoint.

**Response:**
```
Hello, World!
```

### POST /ask_agent
Main endpoint for interacting with AI agents.

**Request Body:**
```json
{
  "user": {
    "user_id": "unique_user_identifier"
  },
  "agent_data": {
    "agent_name": "My Assistant",
    "model_name": "gemini-1.5-flash",
    "instruction": "You are a helpful assistant that...",
    "tools": [
      {
        "connection_type": "sse",
        "url": "https://example.com/mcp-server",
        "headers": {
          "Authorization": "Bearer token"
        }
      },
      {
        "connection_type": "stdio",
        "command": "node",
        "args": ["./mcp-server.js"]
      }
    ]
  },
  "query": {
    "prompt": "What's the weather like today?",
    "history": "Previous conversation context..."
  }
}
```

**Response:**
```json
{
  "response": ["Agent response parts..."]
}
```

**Error Response:**
```json
{
  "error": "Error message description"
}
```

### POST /create_agent
Endpoint for agent creation (currently under development).

## 🔧 Configuration

### Agent Configuration

Agents are configured with the following parameters:

- **agent_name**: Display name for the agent
- **model_name**: Google Gemini model to use (e.g., "gemini-1.5-flash", "gemini-1.5-pro")
- **instruction**: System prompt that defines the agent's behavior
- **tools**: Array of MCP tools the agent can use

### Tool Configuration

#### SSE (Server-Sent Events) Tools
```json
{
  "connection_type": "sse",
  "url": "https://your-mcp-server.com/sse",
  "headers": {
    "Authorization": "Bearer your-token",
    "Content-Type": "application/json"
  }
}
```

#### STDIO Tools
```json
{
  "connection_type": "stdio",
  "command": "python",
  "args": ["-m", "your_mcp_server"]
}
```

## 🧪 Example Usage

### Basic Chat Example

```python
import requests

# Configure your agent
agent_config = {
    "user": {"user_id": "user123"},
    "agent_data": {
        "agent_name": "Code Assistant",
        "model_name": "gemini-1.5-flash",
        "instruction": "You are a helpful coding assistant. Help users with programming questions and code review.",
        "tools": []
    },
    "query": {
        "prompt": "How do I create a Python dictionary?",
        "history": ""
    }
}

# Send request
response = requests.post(
    "http://localhost:3000/ask_agent",
    json=agent_config
)

print(response.json())
```

### With MCP Tools Example

```python
import requests

# Agent with file system tools
agent_config = {
    "user": {"user_id": "user123"},
    "agent_data": {
        "agent_name": "File Assistant",
        "model_name": "gemini-1.5-pro",
        "instruction": "You can help users manage files and directories.",
        "tools": [
            {
                "connection_type": "stdio",
                "command": "npx",
                "args": ["@modelcontextprotocol/server-filesystem", "/path/to/directory"]
            }
        ]
    },
    "query": {
        "prompt": "List the files in the current directory",
        "history": ""
    }
}

response = requests.post("http://localhost:3000/ask_agent", json=agent_config)
print(response.json())
```

## 🏗️ Project Structure

```
mcp-tools-agent-flask/
├── agent_config/
│   └── my_agent/
│       ├── __init__.py
│       └── agent.py          # Core agent logic
├── app.py                    # Flask application
├── common.py                 # Common utilities
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🔍 Key Components

### Agent Module (`agent_config/my_agent/agent.py`)
- **process_query()**: Main function for processing user queries
- **configure_agent()**: Sets up agent with tools and configuration
- MCP tool integration for both SSE and STDIO connections

### Flask App (`app.py`)
- RESTful API endpoints
- Request/response handling
- Error management

## 🚨 Error Handling

The application includes comprehensive error handling:

- **Missing Query**: Returns 400 error if query is not provided
- **Tool Connection Errors**: Gracefully handles MCP tool connection failures
- **Agent Configuration Errors**: Validates required agent parameters
- **Runtime Errors**: Catches and returns descriptive error messages

## 🔒 Security Considerations

- Store API keys in environment variables, never in code
- Validate all input data before processing
- Consider implementing rate limiting for production use
- Use HTTPS in production environments
- Sanitize file paths if using filesystem tools

## 🐛 Debugging

To enable debug logging, modify the logging configuration in `agent.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key for Gemini models | Yes |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the console logs for detailed error messages
2. Verify your Google API key is valid and has appropriate permissions
3. Ensure MCP tools are properly configured and accessible
4. Review the request format matches the expected schema

## 🔗 Related Links

- [Google AI Development Kit Documentation](https://github.com/google/genai-adk)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Note**: This project is in active development. Some features may be incomplete or subject to change.
