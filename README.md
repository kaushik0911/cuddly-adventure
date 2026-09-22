# SQL Analysis Agent

**Status: In progress**

This project is being developed as an agent that converts natural-language questions into PostgreSQL queries and eventually returns useful analysis from the database. The implementation is still under active development.

## Completed So Far

The current focus is building the database-schema context used by the SQL analysis agent.

- Added a `DatabaseUtil` helper that connects to PostgreSQL and inspects the `public` schema.
- The schema inspection collects table names, column names, data types, and up to five sample rows from each table.
- Added an `AgentSchema` Pydantic model to represent the agent state, including the user question, prompt context, generated SQL, safety result, execution result, and final answer.
- Added the `prompt_query_context` agent step, which:
  - Retrieves the current database schema details.
  - Builds a prompt containing the curated user question and schema information.
  - Instructs the LLM to generate executable PostgreSQL SQL.
  - Defaults generated results to a maximum of 10 rows unless the user requests a different number.
  - Stores the generated prompt and SQL in the agent state.
- Added an initial question-curation step that asks the configured LLM to make the user's question clearer and more structured.
- Added PostgreSQL table definitions and CSV-backed sample data for users, vehicles, rides, payments, and ratings.

## Current Structure

```text
agents/sql_analyst.py   Agent steps for question curation and SQL prompt generation
models/schema.py        Pydantic state model used by the agent
utils/database.py       PostgreSQL schema inspection and SQL execution helpers
utils/feed.py           Database configuration and table creation script
utils/llm_pick.py       Ollama LLM selection
data/                   CSV files containing sample domain data
main.py                 Application entry point (to be implemented)
```

## Database Schema

The current sample database models a ride-sharing service with these tables:

- `users`
- `vehicles`
- `rides`
- `payments`
- `ratings`

The schema includes primary keys, foreign-key relationships, indexes, and sample rows. The schema details are generated dynamically from PostgreSQL rather than being hard-coded into the SQL prompt.

## Prerequisites

- Python 3.13 or newer
- PostgreSQL
- [uv](https://docs.astral.sh/uv/)
- Ollama with the `llama3.2:latest` model available

Install the Python dependencies with:

```bash
uv sync
```

Set the PostgreSQL environment variables required by the project before running database-related code:

```bash
export PGHOST=localhost
export PGDATABASE=your_database
export PGUSER=your_user
export PGPASSWORD=your_password
```

## Development Status

The project does not yet provide a complete end-to-end workflow. The following pieces are still planned or in progress:

- Connect the agent steps into a complete LangGraph workflow.
- Add SQL safety validation before execution.
- Execute generated SQL and capture results in the agent state.
- Generate and return a final natural-language answer.
- Add tests and a user-facing command or API through `main.py`.

The repository should therefore be treated as an early development version, not a production-ready SQL analysis agent.
