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


