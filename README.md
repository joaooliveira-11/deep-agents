# Langchain Deep Agents Project

[![Python](https://img.shields.io/badge/Python-≥3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-≥1.2.10-green?logo=langchain&logoColor=white)](https://python.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-≥1.0.10-green)](https://langchain-ai.github.io/langgraph/)
[![Pydantic](https://img.shields.io/badge/Pydantic-≥2.12.5-red?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)

> [!NOTE]
> This repository represents the work done in the [LangChain Academy Deep Agents Project](https://academy.langchain.com/courses/deep-agents-with-langgraph) course with up-to-date libraries versions.
> It is intended for educational purposes to demonstrate how to build a general-purpose AI agent using LangChain and LangGraph, following modern context engineering patterns.

## Overview

A general-purpose AI agent built with LangChain and LangGraph, inspired by the [LangChain Academy Deep Research](https://academy.langchain.com/courses/deep-research-with-langgraph) course. It implements key [context engineering patterns](https://docs.google.com/presentation/d/16aaXLu40GugY-kOpqDU4e-S0hD1FmHcNyF0rRRnb1OU/edit?slide=id.p#slide=id.p) used by modern agent systems like [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) and Claude Code:

- **Task Planning** — TODO lists to break down complex requests and track progress
- **File System Offloading** — Virtual file system to store research context without overloading the prompt
- **Sub-Agent Delegation** — Spawning isolated research agents to handle specific tasks without context pollution

![Deep Agents Overview](./assets/agent_header.png)

## Project Structure

```
src/
├── deep_agent.py                  # Main agent (manual wiring with create_agent)
├── deep_agent_with_abstraction.py # Main agent (using deepagents library)
├── prompts.py                     # All system prompts and tool descriptions
├── state.py                       # Agent state: DeepAgentState, Todo
├── utils.py                       # Message formatting (Rich) + file reducer
└── tools/
    ├── delegate_task.py           # Sub-agent delegation tool
    ├── file_sys.py                # Virtual file system (ls, read, write)
    ├── research.py                # Tavily search + web summarization
    └── todo.py                    # TODO management tools
```

There are **two entry points** — both produce the same agent behavior:

| File | Description |
|---|---|
| `deep_agent.py` | Manually wires tools, sub-agents, and prompts using `create_agent` |
| `deep_agent_with_abstraction.py` | Uses the [`deepagents`](https://pypi.org/project/deepagents/) library for a cleaner setup |

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
git clone git@github.com:joaooliveira-11/deep-agents.git
cd deep-agents
uv sync
```

### Environment Variables

Create a `.env` file in the project root by following needed values in `.env.sample`:

## Usage

### Run the main agent

```bash
uv run deep-agent "What is the Model Context Protocol?"
```

### Run the abstracted version

```bash
uv run deep-agent-abstracted "Compare React and Vue.js"
```

### Run without a question (uses default prompt)

```bash
uv run deep-agent
```

### Run as a Python module

```bash
uv run python -m src.deep_agent "Your question here"
```

## Agent Capabilities

| Capability | Tool | Description |
|---|---|---|
| 🔍 Web Search | `tavily_search` | Search the web and summarize results into files |
| 📝 Task Planning | `write_todos` / `read_todos` | Create and track TODO lists for complex tasks |
| 📁 File System | `ls` / `read_file` / `write_file` | Virtual file system to store and retrieve context |
| 🤔 Reflection | `think_tool` | Internal reasoning without external side effects |
| 🤖 Delegation | `delegate_task` | Spawn isolated sub-agents for parallel research |


