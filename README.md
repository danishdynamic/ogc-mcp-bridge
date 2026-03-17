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