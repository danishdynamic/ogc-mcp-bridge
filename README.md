# GSoC 2026: MCP for OGC APIs - Code Challenge
**Applicant:** sk ali dara
**Status:** Successfully Established & Verified

## 🏗️ Architecture Overview
This proof-of-concept demonstrates a modular "Bridge" architecture:
1. **Backend:** A containerized `pygeoapi` instance providing OGC API - Processes.
2. **Protocol Layer:** A Python-based MCP Server using the `mcp` SDK.
3. **Bridge Logic:** Maps the OGC `hello-world` process to an MCP `Tool` definition.

## 🚀 How to Run
1. **Start the OGC Engine:**
   ```powershell
   docker run --rm --name ogc-debug -p 5000:80 -v ${PWD}/my_config.yml:/pygeoapi/local.config.yml geopython/pygeoapi


## 🚀 Quick Steps to Verify the Bridge (MCP Inspector)

To interact with the OGC tools via a graphical interface and verify the protocol handshake, follow these steps:

1. **Start the OGC Engine:** Ensure your Docker container is running on port `5000`.
2. **Launch the MCP Inspector:** Run the following command in your terminal from the project root:
   ```bash
   npx @modelcontextprotocol/inspector py ogc_mcp_bridge.py

3. **Inspect the Tools:** In the MCP Inspector interface, you should see the `hello-world` tool listed. Click on it to view its details and verify that it is correctly mapped from the OGC process.


4. **Test the Tool:** You can also test the tool directly from the MCP Inspector by providing the required input parameters and executing it to see the response from the OGC API like i input "name": "Alice" and check the output.