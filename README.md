# Graph Based ADK

This project serves as a memo for **ADK v2** and the implementation of a **graph-based workflow**.

## Structure

- `main.py`: Main entry point of the application.
- `MarketResearchWorkflow/`: Module containing the business logic, agents, and workflows. Check the [README in this directory](MarketResearchWorkflow/README.md) for detailed architecture explanations.
- `pyproject.toml`: Project dependencies and configuration.

## How to run the project

The project uses `pyproject.toml`. You can use **uv** for installation.

### Installation and execution with uv

```bash
# Sync the virtual environment and dependencies
uv sync

# Run the project
uv run main.py
```