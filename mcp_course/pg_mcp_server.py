import sys
import os
import json
import psycopg2
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

class PostgreSQLAnalyzer:
    def __init__(self):
        load_dotenv() # Load environment variables from .env file
        self.mcp = FastMCP("postgresql_analyzer")
        print("PostgreSQL MCP Server initialized", file=sys.stderr)
        self._register_tools()

    def _get_db_connection(self):
        try:
            conn = psycopg2.connect(
                host=os.getenv("PG_HOST", "localhost"),
                database=os.getenv("PG_DATABASE", "testdb"),
                user=os.getenv("PG_USER", "user"),
                password=os.getenv("PG_PASSWORD", "password"),
                port=os.getenv("PG_PORT", "5432")
            )
            return conn
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}", file=sys.stderr)
            return None

    def _register_tools(self):
        @self.mcp.tool()
        async def execute_query(query: str) -> dict:
            """Executes a read-only SQL query against the PostgreSQL database and returns the results."""
            print(f"Executing query: {query}", file=sys.stderr)
            conn = None
            try:
                conn = self._get_db_connection()
                if conn is None:
                    return {"error": "Failed to connect to database."}

                cur = conn.cursor()
                cur.execute(query)
                
                # Fetch column names
                column_names = [desc[0] for desc in cur.description]
                
                # Fetch all rows and convert to list of dictionaries
                rows = cur.fetchall()
                results = []
                for row in rows:
                    results.append(dict(zip(column_names, row)))

                cur.close()
                conn.close()
                print(f"Query executed successfully. Rows returned: {len(results)}", file=sys.stderr)
                return {"success": True, "data": results}
            except psycopg2.Error as e:
                print(f"Database error: {e}", file=sys.stderr)
                return {"error": f"Database error: {e}"}
            except Exception as e:
                print(f"An unexpected error occurred: {e}", file=sys.stderr)
                return {"error": f"An unexpected error occurred: {e}"}
            finally:
                if conn:
                    conn.close()

        @self.mcp.tool()
        async def get_table_schema(table_name: str) -> dict:
            """Returns the schema (column names and types) for a given table."""
            print(f"Fetching schema for table: {table_name}", file=sys.stderr)
            conn = None
            try:
                conn = self._get_db_connection()
                if conn is None:
                    return {"error": "Failed to connect to database."}

                cur = conn.cursor()
                cur.execute(f"""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                """, (table_name,))
                
                schema = []
                for row in cur.fetchall():
                    schema.append({"column_name": row[0], "data_type": row[1]})

                cur.close()
                conn.close()
                print(f"Schema for {table_name} fetched successfully.", file=sys.stderr)
                return {"success": True, "schema": schema}
            except psycopg2.Error as e:
                print(f"Database error: {e}", file=sys.stderr)
                return {"error": f"Database error: {e}"}
            except Exception as e:
                print(f"An unexpected error occurred: {e}", file=sys.stderr)
                return {"error": f"An unexpected error occurred: {e}"}
            finally:
                if conn:
                    conn.close()

    def run(self):
        try:
            print("Running MCP Server for PostgreSQL Analysis...", file=sys.stderr)
            self.mcp.run(transport="stdio")
        except Exception as e:
            print(f"Fatal Error in MCP Server: {str(e)}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    analyzer = PostgreSQLAnalyzer()
    analyzer.run()


