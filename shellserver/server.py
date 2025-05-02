from mcp.server.fastmcp import FastMCP
import subprocess
import re
import os
from typing import Optional, List

# Create an MCP server
mcp = FastMCP("Terminal Server")

@mcp.resource("documentation://mcp-python-sdk/readme")
def get_mcp_python_sdk_readme() -> str:
    """Get the MCP Python SDK README documentation"""
    readme_path = "/Users/vamsi_mbmax/Library/CloudStorage/OneDrive-Personal/01_vam_PROJECTS/LEARNING/proj_AI/dev_proj_AI/practise_ai_anthropic_mcp_learn/notes/mcp_python_sdk_readme.md"

    try:
        with open(readme_path, "r") as file:
            return file.read()
    except Exception as e:
        return f"Error reading README file: {str(e)}"

@mcp.tool()
def run_terminal_command(command: str, shell: bool = True) -> dict:
    """Run a terminal command and return its output

    Args:
        command: The command to execute in the terminal
        shell: Whether to run command in a shell

    Returns:
        A dictionary with stdout, stderr, and return code
    """
    # Check for file deletion patterns
    deletion_patterns = [
        r"\brm\s+",           # rm command
        r"\bunlink\s+",       # unlink command
        r"\brmdir\s+",        # rmdir command
        r"del\s+",            # Windows del command
        r"remove-item",       # PowerShell remove-item
        r"rd\s+",             # Windows rd command
        r"fs\.unlink",        # Node.js fs.unlink
        r"os\.remove",        # Python os.remove
        r"shutil\.rmtree",    # Python shutil.rmtree
    ]

    # Check if command contains any deletion patterns
    for pattern in deletion_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return {
                "stdout": "",
                "stderr": "File deletion commands are not allowed for security reasons.",
                "return_code": 1
            }

    try:
        # Execute the command
        process = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True
        )

        # Return the results
        return {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "return_code": process.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "return_code": 1
        }

if __name__ == "__main__":
    mcp.run("stdio")
