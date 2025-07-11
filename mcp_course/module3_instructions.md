
# Module 3: Building Your First MCP Server (End-to-End)

In this module, you will learn how to create a simple Model Context Protocol (MCP) server that provides basic system information. You will also learn how to run this server and interact with it using a client.

## 3.1 Creating the MCP Server

We have already created a Python script named `system_info_server.py` in your `mcp_course` directory. This script uses the `fastmcp` library to set up an MCP server that exposes a single tool: `get_system_info`.

```python
import platform
import sys
from mcp.server.fastmcp import FastMCP

class SystemInfoAnalyzer:
    def __init__(self):
        self.mcp = FastMCP("system_info_analyzer")
        print("MCP Server initialized", file=sys.stderr)
        self._register_tools()

    def _register_tools(self):
        @self.mcp.tool()
        async def get_system_info() -> dict:
            """Returns basic system information."""
            print("Fetching system information...", file=sys.stderr)
            info = {
                "system": platform.system(),
                "node_name": platform.node(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
            }
            print(f"System information fetched: {info}", file=sys.stderr)
            return info

    def run(self):
        try:
            print("Running MCP Server for System Info Analysis...", file=sys.stderr)
            self.mcp.run(transport="stdio")
        except Exception as e:
            print(f"Fatal Error in MCP Server: {str(e)}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    analyzer = SystemInfoAnalyzer()
    analyzer.run()
```

## 3.2 Running the MCP Server

To run this MCP server, you will need to install the `fastmcp` library. Open your terminal, navigate to the `mcp_course` directory, and run the following commands:

```bash
pip install fastmcp
python system_info_server.py
```

Once the server is running, you will see output indicating that the MCP server has been initialized and is running. The server will be listening for incoming MCP requests.

## 3.3 Interacting with the MCP Server

To interact with the MCP server, you would typically use an MCP client like Claude Desktop or Cursor. However, for demonstration purposes, you can simulate an MCP client interaction using `curl` or a simple Python script that sends a JSON-RPC request to the server.

### Using `curl` (Conceptual)

Since `fastmcp` uses `stdio` transport by default, direct `curl` interaction in a separate terminal is not straightforward without setting up a different transport (e.g., HTTP). However, conceptually, an MCP client would send a JSON-RPC request like this:

```json
{
    "jsonrpc": "2.0",
    "method": "get_system_info",
    "id": 1
}
```

And the server would respond with something like:

```json
{
    "jsonrpc": "2.0",
    "result": {
        "system": "Linux",
        "node_name": "sandbox",
        "release": "5.15.0-107-generic",
        "version": "#117-Ubuntu SMP PREEMPT Wed May 22 18:40:00 UTC 2024",
        "machine": "x86_64",
        "processor": "x86_64"
    },
    "id": 1
}
```

### Using a Simple Python Client

For a more practical hands-on approach, let's create a simple Python script that acts as an MCP client to interact with our `system_info_server.py`. Create a new file named `mcp_client.py` in your `mcp_course` directory:

```python
import subprocess
import json
import time

def run_mcp_server_and_client():
    # Start the MCP server in a subprocess
    print("Starting MCP server...")
    server_process = subprocess.Popen(
        ["python", "system_info_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(2) # Give the server a moment to start

    # Send a request to the MCP server
    request = {
        "jsonrpc": "2.0",
        "method": "get_system_info",
        "id": 1
    }
    print("Sending request to MCP server:", json.dumps(request, indent=2))
    server_process.stdin.write(json.dumps(request) + '\n')
    server_process.stdin.flush()

    # Read the response from the MCP server
    print("Waiting for response...")
    response_line = server_process.stdout.readline()
    print("Received response from MCP server:", response_line.strip())

    # Read any stderr output from the server (for debugging)
    stderr_output = server_process.stderr.read()
    if stderr_output:
        print("Server stderr:", stderr_output)

    # Terminate the server process
    server_process.terminate()
    server_process.wait()
    print("MCP server terminated.")

if __name__ == "__main__":
    run_mcp_server_and_client()
```

To run this client, navigate to the `mcp_course` directory in your terminal and execute:

```bash
python mcp_client.py
```

This script will start the `system_info_server.py` as a subprocess, send a request to it, read the response, and then terminate the server. This demonstrates an end-to-end interaction with a simple MCP server.

**Note**: In a real-world scenario with Claude Desktop or Cursor, the IDE itself handles the subprocess management and communication with the MCP server. This Python client is purely for understanding the underlying communication mechanism.


