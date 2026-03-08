# Tipster

AI-powered CLI tip generator for topics you care about.

## Features

- **AI-Generated Tips**: Get practical tips powered by AI about any topic
- **Multiple Providers**: Support for OpenAI, Anthropic, Gemini, DeepSeek, GLM, and Ollama (local)
- **Tip of the Day**: Cached daily tip feature
- **Favorites**: Mark tips as favorites for quick access
- **Search**: Find tips by content or labels
- **Export/Import**: Backup and restore your tips (JSON or CSV)

## Installation

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Quick Install

```bash
# Clone the repository
git clone https://github.com/tiakas/tipster.git
cd tipster/tipster_python

# Install dependencies
uv sync

# Run directly with uv
uv run tipster --help
```

### Install as CLI (Recommended)

```bash
# Install in editable mode
uv pip install -e .

# Or build and install
uv build
uv pip install dist/tipster_python-*.whl
```

## Development Setup

### 1. Clone and Setup

```bash
git clone https://github.com/tiakas/tipster.git
cd tipster/tipster_python
```

### 2. Install Dependencies

```bash
# Create virtual environment and install dependencies
uv sync

# Install dev dependencies (if any)
uv sync --dev
```

### 3. Run in Development

```bash
# Run directly (uses .venv)
uv run tipster --help

# Or activate venv and run
source .venv/bin/activate
tipster --help
```

### 4. Running Tests

```bash
# Run tests with pytest
uv run pytest

# Or with coverage
uv run pytest --cov=tipster --cov-report=term-missing
```

## Quick Start

### 1. Configure Tipster

```bash
# Set your AI provider
tipster config -p openai

# Set your API key
tipster config -k "your-api-key"

# Or use environment variables
export OPENAI_API_KEY="your-api-key"
export ANTHROPIC_API_KEY="your-api-key"
```

Supported providers: `openai`, `anthropic`, `gemini`, `deepseek`, `glm`, `ollama`

### 2. Add Topics

```bash
# Add a topic - tipster will generate a tip using AI
tipster topics new python
tipster topics new basketball
tipster topics new go
```

### 3. Get Tips

```bash
# Get a new tip about a specific topic
tipster tips new python

# Get a random tip
tipster tips new
```

## Commands

### Tips Management

| Command | Description |
|---------|-------------|
| `tips new [topic]` | Generate a new tip (random topic if not specified) |
| `tips show <id>` | Display a specific tip by ID |
| `tips delete <id>` | Delete a tip by ID |
| `tips list` | List all tips |
| `tips list <topic>` | List tips for a specific topic |

### Favorites

| Command | Description |
|---------|-------------|
| `fav add <id>` | Add a tip to favorites |
| `fav list` | Show all favorite tips |
| `fav remove <id>` | Remove a tip from favorites |

### Topics Management

| Command | Description |
|---------|-------------|
| `topics new <topic>` | Add a topic and generate a tip |
| `topics list` | List all topics |
| `topics delete <topic>` | Remove a topic and all its tips |

### Search

| Command | Description |
|---------|-------------|
| `search <query>` | Search tips by content or labels |

### Configuration

| Command | Description |
|---------|-------------|
| `config` | Show current configuration |
| `config -p <provider>` | Set AI provider |
| `config -m <model>` | Set AI model |
| `config -k <key>` | Set API key |

### Export/Import

| Command | Description |
|---------|-------------|
| `export` | Export tips to JSON (stdoutexport -) |
| `f json -o file.json` | Export tips to JSON file |
| `export -f csv -o file.csv` | Export tips to CSV file |
| `import <file>` | Import tips from JSON file |

### Other

| Command | Description |
|---------|-------------|
| `version` | Show version info |

## Configuration Options

### Set Provider

```bash
tipster config -p openai      # OpenAI (default model: gpt-4)
tipster config -p anthropic  # Anthropic (default model: claude-3-5-sonnet-20241022)
tipster config -p gemini     # Gemini (default model: gemini-1.5-pro)
tipster config -p deepseek   # DeepSeek (default model: deepseek-chat)
tipster config -p glm       # GLM (default model: glm-4)
tipster config -p ollama    # Ollama (local, default model: llama2)
```

### Set Model

```bash
tipster config -m gpt-4
tipster config -m gpt-4o
```

### Set API Key

```bash
# Via command
tipster config -k "your-api-key"

# Or via environment variables
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"
export GLM_API_KEY="your-key"
```

### Show Configuration

```bash
tipster config
```

## Data Storage

Config and tips are stored in `~/.tipster/`:

```
~/.tipster/
├── config.json   # Provider, model, API key, topics
└── tips.json     # All tips with favorites
```

## Development

### Project Structure

```
tipster/
├── .github/
│   └── workflows/       # GitHub Actions
├── tipster/
│   ├── __main__.py      # CLI entry point
│   ├── cmd/             # CLI commands
│   │   ├── __init__.py
│   │   ├── tips.py
│   │   ├── fav.py
│   │   ├── topics.py
│   │   ├── config_cmd.py
│   │   ├── export.py
│   │   ├── import_cmd.py
│   │   ├── search.py
│   │   └── version.py
│   ├── ai/              # AI providers
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   ├── gemini.py
│   │   ├── deepseek.py
│   │   ├── glm.py
│   │   └── ollama.py
│   ├── config.py        # Configuration
│   └── storage.py       # Data storage
├── tests/               # Test suite
├── pyproject.toml
└── README.md
```

### Adding a New AI Provider

1. Create a new file in `tipster/ai/` (e.g., `newprovider.py`)
2. Implement the `Client` interface:

```python
from tipster.ai import Client, TipResponse, register_provider

class NewProviderClient(Client):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model or "default-model"

    def generate_tip(self, topic: str) -> TipResponse:
        # Implementation here
        pass

register_provider("newprovider", NewProviderClient)
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_storage.py

# Run with coverage
uv run pytest --cov=tipster
```

## Publishing to PyPI

This project uses [trusted publishing](https://docs.pypi.org/trusted-publishers/) - no credentials need to be configured.

### Prerequisites

1. **PyPI Account**: Create an account at [PyPI](https://pypi.org)
2. **Trusted Publisher**: Configure in PyPI project settings (see below)

### Setup Trusted Publishing

1. Create an environment named `pypi` in your GitHub repository under "Settings" -> "Environments"

2. Add a [trusted publisher](https://docs.pypi.org/trusted-publishers/adding-a-publisher/) to your PyPI project:
   - Go to your project on PyPI -> "Publishing" settings
   - Add a new trusted publisher
   - Select your GitHub repository
   - Environment name: `pypi`
   - Workflow name: `publish.yml`
   - Branch: `main`

### Build and Publish

```bash
# Build the package
uv build

# Publish to PyPI (when triggering from CI)
uv publish
```

### Using GitHub Actions

The `.github/workflows/publish.yml` workflow publishes automatically when you push a tag:

```bash
# Create and push a version tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push --tags
```

This will:
1. Build the package
2. Publish to PyPI using trusted publishing

### Version Bumping

Update version in `pyproject.toml` before each release:

```toml
version = "0.1.0"  # bump to 0.2.0, etc.
```

Then create a new tag and push:

```bash
git tag -a v0.2.0 -m "Release v0.2.0"
git push --tags
```

### Checklist Before Publishing

- [ ] Update version in `pyproject.toml`
- [ ] Update README with any new features
- [ ] Verify tests pass
- [ ] Check package metadata on PyPI page

## License

MIT License - see LICENSE for details.
