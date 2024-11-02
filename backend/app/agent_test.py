from agents import OpenAIAgent, GeminiAgent
from agent_tools import web_search


def main(): 
    # Define the tools with proper function descriptions
    tools_list = [{
        "name": "web_search",
        "description": "Search the web for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    }]
    tools_map = {"web_search": web_search}

    # Pass the tools list to the agent, not the values of tools_map
    agent = GeminiAgent(
        instructions="You are a helpful assistant",
        tools_map=tools_map
    )

    print(agent.submit("Tell me the last price of Apple stock."))

if __name__ == "__main__":
    main()