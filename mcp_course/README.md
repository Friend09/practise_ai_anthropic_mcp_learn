# Model Context Protocol (MCP) Hands-on Course

Welcome to the Model Context Protocol (MCP) Hands-on Course! This course is designed to provide you with a practical, end-to-end understanding of MCP, focusing on its implementation in Python for real-world applications, including interaction with PostgreSQL databases and building a productivity application.

## Course Goal

This course aims to equip you with the knowledge and skills to:

- Understand the core concepts and architecture of MCP.
- Implement MCP servers and clients using Python.
- Integrate Large Language Models (LLMs) with external data sources, specifically PostgreSQL databases, using MCP.
- Develop a practical application leveraging MCP for task management (e.g., a "Things Productivity App").

## Course Structure

The course is divided into several modules, each building upon the previous one:

- **Module 1: Introduction to Model Context Protocol (MCP)**: Core concepts, architecture, and components of MCP.
- **Module 2: Setting Up Your Development Environment**: Python environment setup and necessary library installations.
- **Module 3: Building Your First MCP Server (End-to-End)**: Creating and interacting with a simple MCP server.
- **Module 4: Integrating with PostgreSQL using MCP**: Setting up PostgreSQL, implementing a PostgreSQL MCP server, and querying the database.
- **Module 5: Building a "Things Productivity App" with MCP**: Designing a data model and implementing an MCP server for managing projects, tasks, and subtasks.
- **Module 6: Advanced MCP Concepts and Best Practices**: Security, error handling, extensibility, performance, and deployment considerations.

Each module has a corresponding `moduleX_instructions.md` file that provides detailed explanations and steps.

## Getting Started

To begin this hands-on course, please follow these steps:

### 1. Clone or Download the Course Materials

If you received a `mcp_course.zip` file, extract its contents to your desired location. If you are accessing this from a repository, clone it:

```bash
git clone <repository_url>
cd mcp_course
```

### 2. Python Environment Setup

It's highly recommended to use a virtual environment to manage your Python dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### 3. Install Python Dependencies

Navigate to the `mcp_course` directory and install the required Python packages:

```bash
pip install fastmcp psycopg2-binary python-dotenv
```

### 4. PostgreSQL Database Setup (for Module 4 onwards)

Module 4 and beyond require a running PostgreSQL database. Please refer to `module4_instructions.md` for detailed instructions on how to set up PostgreSQL (using Homebrew or Docker) and create the sample `mcp_demo_db` database and `products` table.

**Important:** Create a `.env` file in the `mcp_course` directory with your PostgreSQL connection details. A template `.env` file is provided in this directory.

```
PG_HOST=localhost
PG_DATABASE=mcp_demo_db
PG_USER=postgres
PG_PASSWORD=mysecretpassword
PG_PORT=5432
```

Replace `mysecretpassword` with your actual PostgreSQL password.

### 5. Navigating the Course

Start with `module1_instructions.md` (which is covered in the `course_outline.md` and `mcp_research.md` files) and proceed sequentially through each `moduleX_instructions.md` file. Each module's instruction file will guide you through the concepts, code examples, and exercises.

### Running Examples

Each module's instructions will detail how to run the specific Python scripts (e.g., `system_info_server.py`, `pg_mcp_server.py`, `productivity_mcp_server.py`) and interact with them using `mcp_client.py`.

**General approach for running examples:**

1.  **Open two separate terminal windows.**
2.  **In Terminal 1 (for the MCP Server):**

    ```bash
    cd path/to/your/mcp_course
    python <server_script_name>.py
    ```

    The server will start and wait for input.

3.  **In Terminal 2 (for the MCP Client):**
    ```bash
    cd path/to/your/mcp_course
    python mcp_client.py
    ```
    The `mcp_client.py` is designed to run the respective server as a subprocess, send requests, and display responses for demonstration purposes. You will see the output of the interactions in Terminal 2.

**Note on Sandbox Environment Limitations:**

During the creation of this course, there were some technical limitations in the sandbox environment that prevented live demonstration of inter-process communication between the MCP server and client. However, the provided code and instructions are fully functional on your local machine (Mac, as specified) and will allow you to experience the end-to-end MCP flow.

## Support and Feedback

If you encounter any issues or have questions, please refer to the troubleshooting sections in the modules or reach out for assistance.

Enjoy learning about Model Context Protocols!

## Project Workflow Flowchart

To help you visualize the step-by-step process of working through this course, here is a flowchart outlining the typical workflow:

![Project Workflow Flowchart](workflow_flowchart.png)
