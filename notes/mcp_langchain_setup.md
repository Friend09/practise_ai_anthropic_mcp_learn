# Setting up mcpdoc in Cursor

This guide will walk you through setting up mcpdoc on your M-series Mac to integrate llms.txt documentation into your Cursor tool.

## Prerequisites

1. Python 3 installed on your system
2. Cursor with Claude AI integration
3. Terminal access

## Installation Steps

### 1. Install mcpdoc and required dependencies

```bash
# Create a virtual environment (optional but recommended)
python -m venv mcpdoc-env
source mcpdoc-env/bin/activate

# Install mcpdoc and dependencies
pip install mcpdoc uvx
```

### 2. Configure Cursor to use mcpdoc

Open Cursor and navigate to Settings > MCP. This will open the `~/.cursor/mcp.json` file. Add the following configuration:

```json
{
  "mcpServers": {
    "langgraph-docs-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "mcpdoc",
        "mcpdoc",
        "--urls",
        "LangGraph:https://langchain-ai.github.io/langgraph/llms.txt LangChain:https://python.langchain.com/llms.txt",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

### 3. Configure Cursor Rules

Next, open Cursor Settings > Rules and update User Rules with:

```
for ANY question about LangGraph, use the langgraph-docs-mcp server to help answer --
+ call list_doc_sources tool to get the available llms.txt file
+ call fetch_docs tool to read it
+ reflect on the urls in llms.txt
+ reflect on the input question
+ call fetch_docs on any urls relevant to the question
```

### 4. Verify setup

1. Make sure the server is running in Cursor Settings > MCP tab
2. Try asking a question about LangGraph to test if your configuration is working

## Additional Configuration Options

### Custom Python Path

If you're using a specific Python environment, you can specify the path:

```json
{
  "mcpServers": {
    "langgraph-docs-mcp": {
      "command": "uvx",
      "args": [
        "--python",
        "/path/to/python",
        "--from",
        "mcpdoc",
        "mcpdoc",
        "--urls",
        "LangGraph:https://langchain-ai.github.io/langgraph/llms.txt",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

### Multiple Documentation Sources

You can add multiple documentation sources:

```bash
uvx --from mcpdoc mcpdoc \
  --urls "LangGraph:https://langchain-ai.github.io/langgraph/llms.txt" "LangChain:https://python.langchain.com/llms.txt" \
  --transport sse \
  --port 8082 \
  --host localhost
```

### Security Options

When using remote llms.txt files, mcpdoc automatically adds only that specific domain to the allowed domains list. For additional security options:

```bash
# Allow specific domains
mcpdoc --urls LangGraph:https://langchain-ai.github.io/langgraph/llms.txt --allowed-domains domain1.com domain2.com

# Allow all domains (use with caution)
mcpdoc --urls LangGraph:https://langchain-ai.github.io/langgraph/llms.txt --allowed-domains '*'
```

## Advanced Usage: YAML Configuration

Create a YAML configuration file (sample_config.yaml):

```yaml
# Sample configuration for mcp-mcpdoc server
- name: LangGraph Python
  llms_txt: https://langchain-ai.github.io/langgraph/llms.txt
```

Then run:

```bash
mcpdoc --yaml sample_config.yaml
```

## Troubleshooting

- Make sure your Python path is correctly configured
- Verify that the server is running in Cursor Settings > MCP tab
- Check that the llms.txt URLs are accessible from your network
- If you encounter issues, try increasing the timeout: `--timeout 15.0`
- Make sure to use the correct transport method (stdio for Cursor integration)
