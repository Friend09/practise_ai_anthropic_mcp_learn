import sys
import json
from mcp.server.fastmcp import FastMCP

# In-memory data store for demonstration
# In a real application, this would be a database
productivity_data = {
    "projects": {},
    "tasks": {},
    "subtasks": {}
}

next_project_id = 1
next_task_id = 1
next_subtask_id = 1

class ProductivityAnalyzer:
    def __init__(self):
        self.mcp = FastMCP("productivity_analyzer")
        print("Productivity MCP Server initialized", file=sys.stderr)
        self._register_tools()

    def _register_tools(self):
        # Project Management Tools
        @self.mcp.tool()
        async def create_project(name: str, description: str = "") -> dict:
            """Creates a new project."""
            global next_project_id
            project_id = f"P{next_project_id}"
            productivity_data["projects"][project_id] = {
                "id": project_id,
                "name": name,
                "description": description,
                "tasks": []
            }
            next_project_id += 1
            print(f"Project created: {project_id} - {name}", file=sys.stderr)
            return {"success": True, "project": productivity_data["projects"][project_id]}

        @self.mcp.tool()
        async def get_project(project_id: str) -> dict:
            """Retrieves a project by its ID."""
            project = productivity_data["projects"].get(project_id)
            if project:
                print(f"Project retrieved: {project_id}", file=sys.stderr)
                return {"success": True, "project": project}
            else:
                print(f"Project not found: {project_id}", file=sys.stderr)
                return {"success": False, "error": "Project not found"}

        @self.mcp.tool()
        async def list_projects() -> dict:
            """Lists all projects."""
            projects = list(productivity_data["projects"].values())
            print(f"Listing {len(projects)} projects.", file=sys.stderr)
            return {"success": True, "projects": projects}

        # Task Management Tools
        @self.mcp.tool()
        async def create_task(project_id: str, name: str, description: str = "") -> dict:
            """Creates a new task within a project."""
            global next_task_id
            if project_id not in productivity_data["projects"]:
                print(f"Project not found: {project_id}", file=sys.stderr)
                return {"success": False, "error": "Project not found"}

            task_id = f"T{next_task_id}"
            task = {
                "id": task_id,
                "project_id": project_id,
                "name": name,
                "description": description,
                "subtasks": []
            }
            productivity_data["tasks"][task_id] = task
            productivity_data["projects"][project_id]["tasks"].append(task_id)
            next_task_id += 1
            print(f"Task created: {task_id} - {name} for project {project_id}", file=sys.stderr)
            return {"success": True, "task": task}

        @self.mcp.tool()
        async def get_task(task_id: str) -> dict:
            """Retrieves a task by its ID."""
            task = productivity_data["tasks"].get(task_id)
            if task:
                print(f"Task retrieved: {task_id}", file=sys.stderr)
                return {"success": True, "task": task}
            else:
                print(f"Task not found: {task_id}", file=sys.stderr)
                return {"success": False, "error": "Task not found"}

        @self.mcp.tool()
        async def list_tasks(project_id: str = None) -> dict:
            """Lists all tasks, optionally filtered by project_id."""
            tasks = []
            if project_id:
                if project_id not in productivity_data["projects"]:
                    print(f"Project not found: {project_id}", file=sys.stderr)
                    return {"success": False, "error": "Project not found"}
                task_ids = productivity_data["projects"][project_id]["tasks"]
                tasks = [productivity_data["tasks"][tid] for tid in task_ids]
            else:
                tasks = list(productivity_data["tasks"].values())
            print(f"Listing {len(tasks)} tasks.", file=sys.stderr)
            return {"success": True, "tasks": tasks}

        # Subtask Management Tools
        @self.mcp.tool()
        async def create_subtask(task_id: str, name: str, description: str = "") -> dict:
            """Creates a new subtask within a task."""
            global next_subtask_id
            if task_id not in productivity_data["tasks"]:
                print(f"Task not found: {task_id}", file=sys.stderr)
                return {"success": False, "error": "Task not found"}

            subtask_id = f"S{next_subtask_id}"
            subtask = {
                "id": subtask_id,
                "task_id": task_id,
                "name": name,
                "description": description
            }
            productivity_data["subtasks"][subtask_id] = subtask
            productivity_data["tasks"][task_id]["subtasks"].append(subtask_id)
            next_subtask_id += 1
            print(f"Subtask created: {subtask_id} - {name} for task {task_id}", file=sys.stderr)
            return {"success": True, "subtask": subtask}

        @self.mcp.tool()
        async def get_subtask(subtask_id: str) -> dict:
            """Retrieves a subtask by its ID."""
            subtask = productivity_data["subtasks"].get(subtask_id)
            if subtask:
                print(f"Subtask retrieved: {subtask_id}", file=sys.stderr)
                return {"success": True, "subtask": subtask}
            else:
                print(f"Subtask not found: {subtask_id}", file=sys.stderr)
                return {"success": False, "error": "Subtask not found"}

        @self.mcp.tool()
        async def list_subtasks(task_id: str = None) -> dict:
            """Lists all subtasks, optionally filtered by task_id."""
            subtasks = []
            if task_id:
                if task_id not in productivity_data["tasks"]:
                    print(f"Task not found: {task_id}", file=sys.stderr)
                    return {"success": False, "error": "Task not found"}
                subtask_ids = productivity_data["tasks"][task_id]["subtasks"]
                subtasks = [productivity_data["subtasks"][sid] for sid in subtask_ids]
            else:
                subtasks = list(productivity_data["subtasks"].values())
            print(f"Listing {len(subtasks)} subtasks.", file=sys.stderr)
            return {"success": True, "subtasks": subtasks}

    def run(self):
        try:
            print("Running MCP Server for Productivity Analysis...", file=sys.stderr)
            self.mcp.run(transport="stdio")
        except Exception as e:
            print(f"Fatal Error in MCP Server: {str(e)}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    analyzer = ProductivityAnalyzer()
    analyzer.run()


