
# Module 5: Building a "Things Productivity App" with MCP

In this module, you will build a prototype Model Context Protocol (MCP) server for a "Things Productivity App" that can manage projects, tasks, and subtasks. This will demonstrate how MCP can be used to create intelligent agents that interact with custom application logic and data.

## 5.1 Designing the Data Model

For this prototype, we will use a simple in-memory data store to represent our productivity data. In a real-world application, this would typically be a database (like PostgreSQL, as covered in Module 4) or a more robust persistence layer. Our data model will consist of:

*   **Projects**: Top-level containers for tasks.
    *   `id`: Unique identifier (e.g., "P1", "P2")
    *   `name`: Name of the project
    *   `description`: Optional description
    *   `tasks`: List of task IDs belonging to this project
*   **Tasks**: Individual tasks within a project.
    *   `id`: Unique identifier (e.g., "T1", "T2")
    *   `project_id`: ID of the parent project
    *   `name`: Name of the task
    *   `description`: Optional description
    *   `subtasks`: List of subtask IDs belonging to this task
*   **Subtasks**: Smaller, granular steps within a task.
    *   `id`: Unique identifier (e.g., "S1", "S2")
    *   `task_id`: ID of the parent task
    *   `name`: Name of the subtask
    *   `description`: Optional description

## 5.2 Implementing the Productivity MCP Server

We have created a Python script named `productivity_mcp_server.py` in your `mcp_course` directory. This script uses `fastmcp` to expose tools for managing projects, tasks, and subtasks based on the data model described above.

Here are the key tools implemented in `productivity_mcp_server.py`:

### Project Management Tools:
*   `create_project(name: str, description: str = "") -> dict`: Creates a new project.
*   `get_project(project_id: str) -> dict`: Retrieves a project by its ID.
*   `list_projects() -> dict`: Lists all projects.

### Task Management Tools:
*   `create_task(project_id: str, name: str, description: str = "") -> dict`: Creates a new task within a project.
*   `get_task(task_id: str) -> dict`: Retrieves a task by its ID.
*   `list_tasks(project_id: str = None) -> dict`: Lists all tasks, optionally filtered by project ID.

### Subtask Management Tools:
*   `create_subtask(task_id: str, name: str, description: str = "") -> dict`: Creates a new subtask within a task.
*   `get_subtask(subtask_id: str) -> dict`: Retrieves a subtask by its ID.
*   `list_subtasks(task_id: str = None) -> dict`: Lists all subtasks, optionally filtered by task ID.

## 5.3 Running the Productivity MCP Server

To run this MCP server, navigate to the `mcp_course` directory in your terminal and execute:

```bash
python productivity_mcp_server.py
```

This server will run and listen for MCP requests via stdio.

## 5.4 Interacting with the Productivity MCP Server

We will modify our `mcp_client.py` to send requests to the `productivity_mcp_server.py`. Update the `mcp_client.py` file in your `mcp_course` directory with the following content:

```python
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
    # Example 1: Create a new project
    print("\n--- Example 1: Create Project ---")
    run_mcp_client_request("productivity_mcp_server.py", "create_project", {"name": "Learn MCP", "description": "Mastering Model Context Protocols"})

    # Example 2: List all projects
    print("\n--- Example 2: List Projects ---")
    run_mcp_client_request("productivity_mcp_server.py", "list_projects", {})

    # Example 3: Create a task within a project (assuming P1 is created)
    print("\n--- Example 3: Create Task ---")
    run_mcp_client_request("productivity_mcp_server.py", "create_task", {"project_id": "P1", "name": "Understand MCP Architecture", "description": "Dive deep into MCP components"})

    # Example 4: List tasks for a specific project
    print("\n--- Example 4: List Tasks for Project P1 ---")
    run_mcp_client_request("productivity_mcp_server.py", "list_tasks", {"project_id": "P1"})

    # Example 5: Create a subtask within a task (assuming T1 is created)
    print("\n--- Example 5: Create Subtask ---")
    run_mcp_client_request("productivity_mcp_server.py", "create_subtask", {"task_id": "T1", "name": "Research MCP Hosts", "description": "Identify common MCP client applications"})

    # Example 6: List subtasks for a specific task
    print("\n--- Example 6: List Subtasks for Task T1 ---")
    run_mcp_client_request("productivity_mcp_server.py", "list_subtasks", {"task_id": "T1"})

    # Example 7: Get a specific project
    print("\n--- Example 7: Get Project P1 ---")
    run_mcp_client_request("productivity_mcp_server.py", "get_project", {"project_id": "P1"})

    # Example 8: Get a specific task
    print("\n--- Example 8: Get Task T1 ---")
    run_mcp_client_request("productivity_mcp_server.py", "get_task", {"task_id": "T1"})

    # Example 9: Get a specific subtask
    print("\n--- Example 9: Get Subtask S1 ---")
    run_mcp_client_request("productivity_mcp_server.py", "get_subtask", {"subtask_id": "S1"})

```

**How to run this example (on your local Mac):**

1.  **Ensure you have `fastmcp` installed:**
    ```bash
    cd path/to/your/mcp_course
    pip install fastmcp
    ```
2.  **Run the client script:**
    ```bash
    python mcp_client.py
    ```

This script will sequentially start the `productivity_mcp_server.py` as a subprocess for each example, send the respective MCP request, read the response, and then terminate the server. You will see the output of each interaction directly in your terminal.

This hands-on exercise demonstrates how an MCP client can leverage an MCP server to interact with a custom application, enabling your LLM applications to manage and interact with your productivity data.


