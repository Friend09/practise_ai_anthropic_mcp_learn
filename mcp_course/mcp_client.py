import subprocess
import json
import time
import os

def run_mcp_client_request(server_script, method, params):
    # Start the MCP server in a subprocess
    print(f"Starting MCP server ({server_script}) for method: {method} with params: {params}...")
    server_process = subprocess.Popen(
        ["python", server_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    time.sleep(3) # Give the server time to start

    # Send a request to the MCP server
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    print("Sending request to MCP server:", json.dumps(request, indent=2))
    try:
        server_process.stdin.write(json.dumps(request) + '\n')
        server_process.stdin.flush()
    except BrokenPipeError:
        print("Error: Server process stdin pipe is broken. Server might have exited prematurely.")
        stderr_output = server_process.stderr.read()
        if stderr_output:
            print("Server stderr (before client request):\n", stderr_output)
        server_process.terminate()
        server_process.wait()
        return

    # Read the response from the MCP server
    print("Waiting for response...")
    response_json = None
    try:
        while True:
            line = server_process.stdout.readline()
            if not line:
                if server_process.poll() is not None:
                    break
                time.sleep(0.1)
                continue
            print(f"Raw server stdout: {line.strip()}")
            try:
                response_json = json.loads(line)
                if "jsonrpc" in response_json and "id" in response_json:
                    break
            except json.JSONDecodeError:
                continue
    except Exception as e:
        print(f"Error reading from server stdout: {e}")

    if response_json:
        print("Received response from MCP server:", json.dumps(response_json, indent=2))
    else:
        print("No valid JSON-RPC response received.")

    stderr_output = server_process.stderr.read()
    if stderr_output:
        print("Server stderr (after client request):\n", stderr_output)

    server_process.terminate()
    server_process.wait()
    print("MCP server terminated.")

if __name__ == "__main__":
    # Example 1: Get system info (using system_info_server.py)
    print("\n--- Example 1: Get System Info ---")
    run_mcp_client_request("system_info_server.py", "get_system_info", [])

    # Example 2: Get table schema (using pg_mcp_server.py)
    print("\n--- Example 2: Get Table Schema ---")
    run_mcp_client_request("pg_mcp_server.py", "get_table_schema", {"table_name": "products"})

    # Example 3: Execute a query to get all products
    print("\n--- Example 3: Get All Products ---")
    run_mcp_client_request("pg_mcp_server.py", "execute_query", {"query": "SELECT * FROM products;"})

    # Example 4: Execute a query to get products in Electronics category
    print("\n--- Example 4: Get Electronics Products ---")
    run_mcp_client_request("pg_mcp_server.py", "execute_query", {"query": "SELECT product_name, price FROM products WHERE category = 'Electronics';"})

    # Example 5: Execute a query to get products with low stock
    print("\n--- Example 5: Get Low Stock Products ---")
    run_mcp_client_request("pg_mcp_server.py", "execute_query", {"query": "SELECT product_name, stock_quantity FROM products WHERE stock_quantity < 100;"})

    # Example 6: Create a new project
    print("\n--- Example 6: Create Project ---")
    run_mcp_client_request("productivity_mcp_server.py", "create_project", {"name": "Learn MCP", "description": "Mastering Model Context Protocols"})

    # Example 7: List all projects
    print("\n--- Example 7: List Projects ---")
    run_mcp_client_request("productivity_mcp_server.py", "list_projects", {})

    # Example 8: Create a task within a project (assuming P1 is created)
    print("\n--- Example 8: Create Task ---")
    run_mcp_client_request("productivity_mcp_server.py", "create_task", {"project_id": "P1", "name": "Understand MCP Architecture", "description": "Dive deep into MCP components"})

    # Example 9: List tasks for a specific project
    print("\n--- Example 9: List Tasks for Project P1 ---")
    run_mcp_client_request("productivity_mcp_server.py", "list_tasks", {"project_id": "P1"})

    # Example 10: Create a subtask within a task (assuming T1 is created)
    print("\n--- Example 10: Create Subtask ---")
    run_mcp_client_request("productivity_mcp_server.py", "create_subtask", {"task_id": "T1", "name": "Research MCP Hosts", "description": "Identify common MCP client applications"})

    # Example 11: List subtasks for a specific task
    print("\n--- Example 11: List Subtasks for Task T1 ---")
    run_mcp_client_request("productivity_mcp_server.py", "list_subtasks", {"task_id": "T1"})

    # Example 12: Get a specific project
    print("\n--- Example 12: Get Project P1 ---")
    run_mcp_client_request("productivity_mcp_server.py", "get_project", {"project_id": "P1"})

    # Example 13: Get a specific task
    print("\n--- Example 13: Get Task T1 ---")
    run_mcp_client_request("productivity_mcp_server.py", "get_task", {"task_id": "T1"})

    # Example 14: Get a specific subtask
    print("\n--- Example 14: Get Subtask S1 ---")
    run_mcp_client_request("productivity_mcp_server.py", "get_subtask", {"subtask_id": "S1"})


