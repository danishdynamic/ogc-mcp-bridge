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

- Connect & Discover: * Open the URL provided (typically http://localhost:6274).

- Click Connect to trigger the initialize handshake.

- Navigate to the Tools tab to see the ogc_hello_world process dynamically mapped as an MCP tool.


4. **Test the Tool:** You can also test the tool directly from the MCP Inspector by providing the required input parameters and executing it to see the response from the OGC API like i input "name": "Alice" and check the output.



### ✅ Full Lifecycle Validation (Proof of Concept)

The following steps confirm the entire system is operational, from discovery to execution:

- Discovery: The bridge automatically fetches metadata from /processes and generates a JSON Schema.

- Execution: By selecting the ogc_hello_world tool in the Inspector and providing a name argument, the bridge successfully proxies the request to the OGC backend.

- Result: The OGC output is retrieved, parsed, and returned to the MCP client as a success message.

### 🔒 Security & Production Scaling
While this is a local proof-of-concept, the architecture is designed for production environments:

- Validation: Uses Pydantic-based input sanitization to prevent injection.

- Security: Designed to integrate with API Gateways (e.g., Nginx/Kong) using OAuth2/OpenID Connect for sensitive /jobs endpoints.

- Scaling: The containerized nature allows for horizontal scaling via Kubernetes (K8s) to handle high-concurrency geospatial processing.

### 🛡️ Resilience & Anti-Flooding Measures

To ensure the API remains responsive and protected against volumetric attacks (flooding):
- **Rate Limiting:** Implementation of request-per-IP thresholds to prevent abuse and ensure fair resource distribution.
- **Timeout Management:** Strict execution limits on all OGC process calls to prevent resource exhaustion from hanging or "slow" malicious requests.
- **Edge Protection:** Designed to sit behind a Reverse Proxy (Nginx) or WAF to filter malformed packets and DDoS traffic at the network perimeter.