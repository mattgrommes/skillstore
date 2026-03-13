# Skillstore Protocol

The Skillstore protocol is an idea for a simple standardized way of providing and discovering downloadable "skills" (markdown instructions) that teach LLMs how to interact with a site. This repo provides an example Skill and a sample server that shows the endpoints needed.

The skills can also provide other options as well such as providing contact info and possibly directing the LLM how to navigate a website that doesn't have an API. There's lot to discover about this idea.

NOTE: This idea is in active development and needs a lot more thinking. Simple use cases work though and I believe the idea is sound.

## Details

Skillstore enables websites to expose a `/skillstore` endpoint that LLM agents can query to discover and download skills relevant to the site. This allows LLMs to dynamically learn new capabilities without requiring manual skill installation.

Right now the examples I've tested are only downloading a SKILL.md file. The next step is going to be working on providing a Skill package that includes code such as a simple API client with auth. Coming soon!

## Example Flow

1. User tells their agent "Book me a yoga class at my gym this Monday. Their website is https://example.com. Permanently download the skill for next time."
    They can also specify not to download the skill and it should still work for this prompt.
2. Agent (with skillstore skill) calls `https://example.com/skillstore`and retrieves a list of available skills.
3. Agent discovers the 'book-appointment' skill. This skill tells the agent to download the `class-schedule` skill if needed.
4. Agent discovers a `class-schedule` skill and uses it to find the schedule.
5. Agent uses the new skill to submit the class booking.
6. Success!

## Usage

On the user side, just download and install the skillstore-skill.

On the server side, you just have to provide a /skillstore endpoint which returns json with a list of skills availble. You also need to have endpoints for each skill. Until more documentation is available, see below and the sample server.

## Running the test/sample Server

### Run the server

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

##

This was developed by Matt Grommes. See more of my fine web products at https://grommesmade.com and https://mattorama.net.

Thanks for checking out this idea and I hope it's useful!
