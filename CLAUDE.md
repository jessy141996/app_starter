# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An MCP (Model Context Protocol) server that exposes document-processing tools to AI assistants. Built with FastMCP and Python.

## Commands

```bash
# Setup
uv venv
source .venv/bin/activate
uv pip install -e .

# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_document.py

# Run a single test method
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

The server entry point is `main.py`, which creates a `FastMCP` instance and registers tool functions. Tools are plain Python functions defined in `tools/` and registered via `mcp.tool()()`. Tests use pytest with class-based organization and binary fixture files in `tests/fixtures/`.

**Tool registration flow:** define function in `tools/` → import in `main.py` → register with `mcp.tool()(function_name)`.

## Defining MCP Tools

Tools are Python functions registered with the MCP server via `mcp.tool()`. Follow these conventions:

**Parameter descriptions** — use `Field` from pydantic:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
```

**Docstrings** must include:
1. A one-line summary
2. Detailed explanation of functionality
3. When to use (and when not to use) the tool
4. Usage examples with expected input/output

See `tools/math.py` for a complete example of this pattern.

## Code Style

- Always apply appropriate type annotations to function arguments.

## Dependencies

- `mcp[cli]==1.8.0` — MCP server framework (FastMCP)
- `markitdown[docx,pdf]` — binary document to markdown conversion
- `pydantic` — parameter validation and Field descriptions
- `pytest` — testing
