
# Module 4: Integrating with PostgreSQL using MCP

In this module, you will learn how to integrate Model Context Protocols (MCP) with a PostgreSQL database. This will enable your LLM applications to interact with your database, perform queries, and retrieve information in a structured manner.

## 4.1 Setting Up a Sample PostgreSQL Database

To follow along with this module, you will need a running PostgreSQL database instance on your Mac. If you don't have one, here are a few ways to set it up:

### Option 1: Using Homebrew (Recommended for Mac)

1.  **Install Homebrew** (if you haven't already):
    Open your terminal and run:
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
2.  **Install PostgreSQL:**
    ```bash
    brew install postgresql
    ```
3.  **Start PostgreSQL Service:**
    ```bash
    brew services start postgresql
    ```
    You can check its status with `brew services list`.

### Option 2: Using Docker

If you prefer using Docker, you can run a PostgreSQL container:

1.  **Install Docker Desktop** for Mac (if you haven't already).
2.  **Pull and run the PostgreSQL image:**
    ```bash
    docker pull postgres
    docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
    ```
    This will start a PostgreSQL container with a database named `postgres`, user `postgres`, and password `mysecretpassword` on port `5432`.

### 4.1.1 Creating a Sample Database and Table

Once PostgreSQL is running, you can connect to it using a client like `psql` (installed with Homebrew PostgreSQL) or DataGrip (which you mentioned you use). Let's create a sample database and a table for our exercises.

Connect to your PostgreSQL server (e.g., using `psql`):

```bash
psql postgres
```

Then, execute the following SQL commands to create a database and a sample `products` table:

```sql
CREATE DATABASE mcp_demo_db;
\c mcp_demo_db;

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL
);

INSERT INTO products (product_name, category, price, stock_quantity) VALUES
('Laptop', 'Electronics', 1200.00, 50),
('Mouse', 'Electronics', 25.00, 200),
('Keyboard', 'Electronics', 75.00, 100),
('Desk Chair', 'Furniture', 150.00, 30),
('Monitor', 'Electronics', 300.00, 75),
('Coffee Table', 'Furniture', 80.00, 40),
('Headphones', 'Electronics', 100.00, 150),
('Bookshelf', 'Furniture', 60.00, 60);

```

## 4.2 Understanding the PostgreSQL MCP Server

We have created a Python script named `pg_mcp_server.py` in your `mcp_course` directory. This script uses `fastmcp` to expose tools for interacting with a PostgreSQL database. It includes two main tools:

*   `execute_query(query: str)`: Executes a read-only SQL query and returns the results.
*   `get_table_schema(table_name: str)`: Returns the schema (column names and types) for a given table.

**Important:** This server uses environment variables for database connection details for security. You will need to create a `.env` file in the `mcp_course` directory with your PostgreSQL credentials:

```
PG_HOST=localhost
PG_DATABASE=mcp_demo_db
PG_USER=postgres
PG_PASSWORD=mysecretpassword
PG_PORT=5432
```

Make sure to replace `mysecretpassword` with your actual PostgreSQL password if you changed it during setup.

## 4.3 Running the PostgreSQL MCP Server

To run this MCP server, you will need to install the necessary Python packages. Open your terminal, navigate to the `mcp_course` directory, and run:

```bash
pip install fastmcp psycopg2-binary python-dotenv
python pg_mcp_server.py
```

Similar to the previous module, this server will run and listen for MCP requests via stdio. You won't see immediate output until a client sends a request.

## 4.4 Interacting with the PostgreSQL MCP Server

We will modify our `mcp_client.py` to send requests to the PostgreSQL MCP server. Update the `mcp_client.py` file in your `mcp_course` directory with the following content:

```python
import subprocess
import json
import time
import os

def run_mcp_client_request(method, params):
    # Start the MCP server in a subprocess
    print(f"Starting MCP server for method: {method} with params: {params}...")
    server_process = subprocess.Popen(
        ["python", "pg_mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    time.sleep(3) # Give the server time to start and load .env

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
    # Example 1: Get table schema
    print("\n--- Example 1: Get Table Schema ---")
    run_mcp_client_request("get_table_schema", {"table_name": "products"})

    # Example 2: Execute a query to get all products
    print("\n--- Example 2: Get All Products ---")
    run_mcp_client_request("execute_query", {"query": "SELECT * FROM products;"})

    # Example 3: Execute a query to get products in Electronics category
    print("\n--- Example 3: Get Electronics Products ---")
    run_mcp_client_request("execute_query", {"query": "SELECT product_name, price FROM products WHERE category = 'Electronics';"})

    # Example 4: Execute a query to get products with low stock
    print("\n--- Example 4: Get Low Stock Products ---")
    run_mcp_client_request("execute_query", {"query": "SELECT product_name, stock_quantity FROM products WHERE stock_quantity < 100;"})

```

**How to run this example (on your local Mac):**

1.  **Ensure PostgreSQL is running** and you have created the `mcp_demo_db` database and `products` table as described in Section 4.1.1.
2.  **Create a `.env` file** in your `mcp_course` directory with your PostgreSQL connection details.
3.  **Install Python dependencies:**
    ```bash
    cd path/to/your/mcp_course
    pip install fastmcp psycopg2-binary python-dotenv
    ```
4.  **Run the client script:**
    ```bash
    python mcp_client.py
    ```

This script will sequentially start the `pg_mcp_server.py` as a subprocess for each example, send the respective MCP request, read the response, and then terminate the server. You will see the output of each interaction directly in your terminal.

This hands-on exercise demonstrates how an MCP client can leverage an MCP server to interact with a PostgreSQL database using natural language-like commands (via the `execute_query` and `get_table_schema` tools), making your LLM applications data-aware.


