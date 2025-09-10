# Agentic AI using OPEN AI
This repo contains Agentic AI learning

## What is Agentic AI?

Agentic AI refers to AI systems that can autonomously decide which steps to take, which tools to use, and how to adapt their strategy to achieve a goal. Unlike fixed pipelines, agents observe, reason, act, and iterate—often coordinating multiple specialized sub-agents to complete complex tasks.

## Agent v/s Workflows?

Workflows are designed for predefined, step-by-step processes, while agents are more autonomous, dynamically choosing steps and tools to achieve a goal.

While, Agents are AI systems that can dynamically choose actions, tools, and steps to achieve a goal

## Customer Care Agent (folder: `customer-care-agent`)

An OpenAI-powered customer support prototype focused on watch products.

- **Goal**: Simulate a friendly brand rep that can chat with users and answer questions about a watch catalog.
- **Data generation**: Builds a small synthetic catalog at runtime (brand, movement, gender, availability, style, material, season, launch year, price, description) and saves it to `products-01.csv`.
- **Multi-agent workflow**:
  - **Refiner Agent**: Cleans up a user's natural-language request.
  - **Query Generator Agent**: Produces a valid pandas expression over the in-memory DataFrame.
  - **Query Execution Agent**: Runs the expression and returns formatted results.
- **Models/stack**: Uses `gpt-4o-mini` via the OpenAI SDK, `pandas` for data, and a simple streamed console runner with handoffs and tracing.
- **Artifacts**:
  - `customer-care-agent/agent.py`: Console chat entry point and agent wiring.
  - `customer-care-agent/README.md`: Brief feature overview.
  - `customer-care-agent/watch_agent.ipynb`, `customer-care-agent/ticket_agent.ipynb`: Notebooks exploring the agent flow.

Quickstart:

1) Set `OPENAI_API_KEY` in your environment
2) Run: `python customer-care-agent/agent.py`
3) Ask for watches (e.g., “Show men’s chronographs under $3000”) and the agent will refine → generate → execute a pandas query and display matching items.

## Project Structure

- `1-foundations/`: Labs and notebooks exploring core agentic patterns (`agents.ipynb`, `structured-output.ipynb`, etc.).
- `customer-care-agent/`: Watch-focused customer support agent (multi-agent orchestration, data generation, CLI runner).
- `pyproject.toml`: Project dependencies and tool config.
- `uv.lock`: Lockfile for reproducible Python environments.
