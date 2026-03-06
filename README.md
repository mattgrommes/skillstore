# Skillstore

A server and LLM skill for exposing discoverable, downloadable "skills" (markdown instructions) that teach LLMs how to interact with a site's APIs.

## What is Skillstore?

Skillstore enables websites to expose a `/skillstore` endpoint that LLM agents can query to discover and download skills relevant to the site. This allows LLMs to dynamically learn new capabilities without requiring manual skill installation.

## Example Flow

1. User asks their LLM: "Are there any open classes at MyGym?"
2. LLM (with skillstore skill) calls `https://mygym.com/skillstore`
3. LLM discovers a `class-schedule` skill and downloads it
4. LLM uses the new skill to fetch and display the class schedule

## Usage

### Running the Server

```bash
# Set required environment variables for production
export SKILLSTORE_SKILLS_DIR=/path/to/skills
export SKILLSTORE_SITE_URL=https://your-site.com

# Run the server
uv run uvicorn skillstore.main:app --reload
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SKILLSTORE_SKILLS_DIR` | Path to skills directory | `./skills` |
| `SKILLSTORE_SITE_URL` | Canonical site URL (recommended for production) | Uses request host |

### API Endpoints

- `GET /skillstore` - List available skills
- `GET /skillstore/skill/{skill_id}` - Download a specific skill

## Development

```bash
# Install dependencies
uv sync --dev

# Run tests
uv run pytest

# Lint
uv run ruff check .
```

## License

MIT
