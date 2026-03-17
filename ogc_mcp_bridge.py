import asyncio
import httpx
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# 1. Initialize the MCP Server
server = Server("ogc-mcp-bridge")

# 2. Define the "Hello World" tool for the AI
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return await discover_ogc_tools()


# 3. Handle the logic when the AI calls the tool
@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None) -> list[types.TextContent]:

    if arguments is None:
        arguments = {}

    if name == "ogc_hello_world":
        user_input = arguments.get("name", "Developer")
        
        # Call your Docker container
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "http://localhost:5000/processes/hello-world/execution",
                    json={"inputs": {"name": user_input}},
                    timeout=10.0
                )
                data = response.json()
            except httpx.HTTPError as e:
                print(f"Error calling OGC API: {e}")
                raise ValueError(f"Error calling OGC API: {e}")
            # Assuming the OGC API returns the greeting in the response
            return [types.TextContent(type="text", text=str(data))]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ogc-mcp-bridge",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

async def discover_ogc_tools() -> list[types.Tool]:
    """Dynamically fetches all available OGC processes and converts them to MCP Tools."""
    async with httpx.AsyncClient() as client:
        try:
            # 1. Get the list of all processes
            response = await client.get("http://localhost:5000/processes?f=json")
            response.raise_for_status()
            processes = response.json().get("processes", [])
            
            mcp_tools = []
            for proc in processes:
                # 2. Map OGC Metadata to MCP Tool structure
                mcp_tools.append(
                    types.Tool(
                        name=f"ogc_{proc['id'].replace('-', '_')}",
                        description=proc.get('description', 'OGC Process'),
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "Input for the process"}
                            },
                            "required": ["name"]
                        }
                    )
                )
            return mcp_tools
        except Exception as e:
            # Fallback to a basic list if the API is down
            return [types.Tool(name="error_tool", description=f"Discovery failed: {e}", inputSchema={"type": "object", "properties": {}})]
        

if __name__ == "__main__":
    asyncio.run(main())