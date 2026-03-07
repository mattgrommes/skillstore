# Skillstore Protocol

An LLM skill for bringing in discoverable, downloadable "skills" (markdown instructions) that teach LLMs how to interact with a site's APIs. Also a sample server that show the endpoints a site would use to provide its end of the protocol.

NOTE: This idea is in active development and needs a lot more thinking. Simple use cases work though and I believe the idea is sound.

## Details

Skillstore enables websites to expose a `/skillstore` endpoint that LLM agents can query to discover and download skills relevant to the site. This allows LLMs to dynamically learn new capabilities without requiring manual skill installation.

Right now the examples I've tested are only downloading a SKILL.md file. The next step is going to be working on providing a Skill package that includes code such as a simple API client with auth.

## Example Flow

1. User asks their LLM: "Are there any open classes at MyGym?"
2. The first time, the user also needs to provide the website URL of MyGym. "Their website is https://example.com"
3. LLM (with skillstore skill) calls `https://example.com/skillstore`
4. LLM discovers a `class-schedule` skill and downloads it
5. LLM uses the new skill to fetch and display the class schedule

## Usage

On the user side, just download and install the skillstore-skill.

On the server side, you just have to provide a /skillstore endpoint which returns json with a list of skills availble. You also need to have endpoints for each skill. Until more documentation is available, see below and the sample server.

### Running the test/sample Server

# Run the server

```bash
uv run uvicorn skillstore.main:app --reload
```

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
