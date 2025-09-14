# Agentic Research Workflow

An automated research workflow powered by LangChain, Ollama, and LangGraph.  
This project takes a research topic, generates research points, summarizes them, writes a full article, and finally critiques the result using a multi-node workflow.

---

## Features

- **Planner Node**: Estimates research complexity and token usage.
- **Research Node**: Generates research points based on topic and complexity.
- **Summarizer Node**: Summarizes research results for writing.
- **Writer Node**: Produces a comprehensive article from the summary.
- **Critic Node**: Evaluates the article and determines next steps.

---

## Tech Stack

- **Python 3.11**
- **FastAPI** for API endpoints
- **LangChain + LangChain-Ollama** for LLM interactions
- **LangGraph** for workflow orchestration
- **Pydantic** for state management
- **Uvicorn** as the ASGI server

---

## Project Workflow
```mermaid
flowchart TD
    Start --> Planner["Planner Node"]
    Planner --> Researcher["Research Node"]
    Researcher --> Summarizer["Summarizer Node"]
    Summarizer --> Writer["Writer Node"]
    Writer --> Critic["Critic Node"]
    Critic -->|Pass| End["End"]
    Critic -->|Fail: research| Researcher
    Critic -->|Fail: summarize| Summarizer
    Critic -->|Fail: write| Writer


## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd agentic-research-workflow

2. Install the dependencies
poetry install

3. Run the FastAPI server:
poetry run uvicorn app.main:app --reload

or Use launch.json



