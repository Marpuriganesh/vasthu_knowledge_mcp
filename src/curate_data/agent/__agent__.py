from langchain_mcp_adapters.client import MultiServerMCPClient

# from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from src.curate_data.read_config import config
from langchain_mcp_adapters.sessions import StreamableHttpConnection

client = MultiServerMCPClient(
    {
        "vasthu_knowledge_mcp": StreamableHttpConnection(
            transport="streamable_http",  # Now cleanly typed as an MCP Connection object
            url=str(config.get("vasthu_mcp_tools_url", "")),
        )
    }
)


llm_config = config.get("local_ai", {"openai_chat": {}}).get("openai_chat", {})

llm = ChatOpenAI(
    base_url=llm_config.get("base_url", ""),
    api_key=llm_config.get("api_key", ""),
    model=llm_config.get("model", ""),  # Use the name shown in LM Studio
    # Trigger reasoning effort based on your version of langchain-openai
    reasoning_effort=llm_config.get("reasoning_effort", ""),
)


async def local_create_agent():
    tools = await client.get_tools()
    total_tools = []

    # Ensure MCP tools explicitly show plain-text descriptions to the local LLM
    for tool in tools:
        # Force the local model to see it as a standard function
        tool.description = f"{tool.description} (Arguments must be provided as clean text/JSON variables)"
        total_tools.append(tool)


    agent = create_agent(
        model=llm,
        tools=total_tools,
    )
    return agent


async def test_agent():
    agent = await local_create_agent()
    config = {"configurable": {"user_id": "local-user-123"}}

    input = {
        "messages": [
            {
                "role": "user",
                "content": """check what is present in the index,rules,directions,rooms and consequences and let me know""",
            }
        ]
    }

    async for chunk in agent.astream(input, config=config, stream_mode="updates"):
        for node_name, node_output in chunk.items():
            print(f"📦 Node Executed: [{node_name}]")
        print("-" * 40)

        # Format and display messages inside the node output nicely
        if "messages" in node_output:
            for msg in node_output["messages"]:
                # Check for tool execution calls made by the model
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    print("🛠️ Model requested Tool Call:")
                    for call in msg.tool_calls:
                        print(f"   -> Tool Name: {call['name']}")
                        print(f"   -> Arguments: {call['args']}")

                # Check for tool results being sent back to the graph
                elif msg.type == "tool":
                    print("📥 Tool Returned Data:")
                    print(f"   {msg.content}")

                # Check for standard model output text
                elif msg.content:
                    print("🤖 Model Response Content:")
                    print(f"   {msg.content}")

        print("-" * 40 + "\n")

    print("--- GRAPH EXECUTION FINISHED ---")


async def test_model():
    tools = await client.get_tools()

    total_tools = []

    # Ensure MCP tools explicitly show plain-text descriptions to the local LLM
    for tool in tools:
        # Force the local model to see it as a standard function
        tool.description = f"{tool.description} (Arguments must be provided as clean text/JSON variables)"
        total_tools.append(tool)

    binded_llm = llm.bind_tools(total_tools)

    # A prompt that forces the model to use its reasoning logic
    prompt = "tell me about the tools that are available to you?"

    print(
        f"Streaming Output from LM Studio (includes thinking tags):\n\nprompt:{prompt}\n"
    )

    # Use standard .stream() to catch everything from the server in real-time
    for chunk in binded_llm.stream(prompt):
        additional_kwargs = chunk.additional_kwargs

        # 1. Look for the reasoning/thinking token
        if "reasoning_content" in additional_kwargs:
            print(additional_kwargs["reasoning_content"], end="", flush=True)

        if chunk.content:
            print(chunk.content, end="", flush=True)

    print("\n\nStream Finished.")
