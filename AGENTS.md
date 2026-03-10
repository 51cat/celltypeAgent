# AGENTS.md

Coding agent instructions for the celltypeAgent repository.

## Project Overview

This is a multi-agent system for cell type annotation in single-cell RNA sequencing analysis. It implements LLM-based agents without external frameworks (like langchain) for educational purposes. The system uses OpenAI-compatible APIs to interact with various LLM models for biological data analysis.

## Build/Lint/Test Commands

### Installation

```bash
pip install -e .
```

### Running Tests

No test framework is currently configured. To run a single test manually:

```bash
python -m pytest tests/test_file.py::test_function_name -v
```

Or run module directly:

```bash
python celltypeAgent/nodes/anno_cluster_node.py
python celltypeAgent/llm/n1n.py
```

### Linting and Formatting

No linting tools are currently configured. Recommended commands:

```bash
ruff check .
ruff format .
```

Or with flake8/black:

```bash
flake8 celltypeAgent/
black celltypeAgent/
```

### Type Checking

```bash
mypy celltypeAgent/
```

## Project Structure

```
celltypeAgent/
├── agent.py              # Main entry point for running agents
├── llm/                  # LLM abstraction layer
│   ├── base.py           # Abstract base class for LLM implementations
│   ├── n1n.py            # N1N API implementation (OpenAI-compatible)
│   ├── message.py        # Message handling class
│   └── tool.py           # Tool documentation extraction
├── nodes/                # Agent node implementations
│   ├── paramcollector_node.py   # Parameter collection agent
│   └── anno_cluster_node.py     # Cell type annotation agent
├── tools/                # Utility functions and tools
│   ├── agent_tools.py    # Tool functions for agents
│   └── utils.py          # Helper utilities (JSON parsing, etc.)
└── prompt/               # Prompt templates
    └── prompt.py         # System prompts for different agents
```

## Code Style Guidelines

### Imports

Use absolute imports from the package root:

```python
from celltypeAgent.llm.n1n import N1N_LLM
from celltypeAgent.nodes.paramcollector_node import ParamCollectorNode
from celltypeAgent.tools.utils import extract_and_validate_json
```

Group imports logically:
1. Standard library imports
2. Third-party imports
3. Local package imports

Separate groups with blank lines.

### Naming Conventions

- **Classes**: PascalCase (e.g., `CelltypeAnnoNode`, `ParamCollectorNode`, `BaseLLM`)
- **Functions/Methods**: snake_case (e.g., `extract_and_validate_json`, `get_table_context`)
- **Variables**: snake_case (e.g., `final_dict`, `message_input`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `BASE_URL`, `PARAM_COLLECTOR_PROMPT`)
- **Private attributes**: Prefix with underscore (e.g., `_message`)

### Type Hints

Use type hints for function parameters and return values:

```python
def invoke(self, message_input: Message, **kwargs) -> str:
def extract_and_validate_json(text, required_keys=None):
```

Use modern union syntax for optional types:

```python
def __init__(self, api_key: str, model_name: str | None = None, base_url: str | None = None):
```

### Docstrings

Use Chinese docstrings for function documentation:

```python
def execute_task(func, params_dict):
    """
    执行传入的函数并返回执行状态。
    
    Args:
        func: 要执行的目标函数
        params_dict: 字典格式的参数
        
    Returns:
        tuple: (bool, any) 
               第一个元素是是否成功 (True/False)，
               第二个元素是函数的返回值或捕获到的异常对象。
    """
```

### Classes

- Define `__init__` as the first method
- Use `@property` decorators for getters
- Follow the pattern of `prep()` for setup and `run()` for execution

```python
class SomeNode:
    def __init__(self, llm, param) -> None:
        self.llm = llm
        self.param = param
    
    def prep(self):
        self.system_prompt = "..."
    
    def run(self):
        return self.llm.invoke(...)
```

### Error Handling

Use try-except blocks with specific exception types:

```python
try:
    data = json.loads(match.group())
except (json.JSONDecodeError, TypeError):
    return None
```

Return tuples with status for error handling in utilities:

```python
try:
    result = func(**params_dict)
    return True, result
except Exception as e:
    return False, e
```

### Testing Pattern

Each module can include a `main()` function for manual testing:

```python
def main():
    llm = N1N_LLM(api_key='...', model_name='...', base_url="...")
    node = SomeNode(llm, params)
    node.prep()
    result = node.run()
    print(result)

if __name__ == '__main__':
    main()
```

### Formatting

- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Blank lines between class methods
- No trailing whitespace

### Module Organization

- `__init__.py` files can re-export from submodules
- Keep prompts in separate files under `prompt/`
- Keep tools separate from agent logic

## Key Patterns

### LLM Base Class

All LLM implementations must inherit from `BaseLLM` and implement:

```python
def invoke(self, system_prompt: str, user_prompt: str, **kwargs) -> str
def get_default_model(self) -> str
```

### Message Handling

Use the `Message` class for conversation management:

```python
message = Message(system_prompt)
message.add_user_message("user input")
message.add_ai_message("ai response")
response = llm.invoke_stream(message)
```

### Agent Node Pattern

Nodes follow a consistent pattern:
1. `__init__`: Initialize with LLM and parameters
2. `prep()`: Prepare prompts and state
3. `run()`: Execute the main logic and return results

## Dependencies

- `openai` - OpenAI API client for LLM interactions
- `pandas` - Data manipulation for gene expression data

## Notes

- API keys should not be committed (currently hardcoded for development - use environment variables in production)
- The system is designed for Chinese language interaction by default
- Prompts are bilingual (Chinese with English technical terms)
