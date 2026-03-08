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
tipster_python/
├── tipster/
│   ├── __main__.py      # CLI entry point
│   ├── cmd/             # CLI commands
│   │   └── __init__.py
│   ├── ai/              # AI providers
│   │   ├── __init__.py
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   ├── gemini.py
│   │   ├── deepseek.py
│   │   ├── glm.py
│   │   └── ollama.py
│   ├── config/          # Configuration
│   │   └── __init__.py
│   └── storage/         # Data storage
│       └── __init__.py
└── pyproject.toml
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

### Prerequisites

1. **PyPI Account**: Create an account at [PyPI](https://pypi.org)
2. **Test PyPI Account**: Create an account at [Test PyPI](https://test.pypi.org) (recommended for testing)
3. **API Token**: Generate API tokens at:
   - [PyPI API Tokens](https://pypi.org/manage/account/token/)
   - [Test PyPI API Tokens](https://test.pypi.org/manage/account/token/)

### Setup PyPI Credentials

Create `~/.pypirc` file:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <your-pypi-token>

[testpypi]
username = __token__
password = <your-test-pypi-token>
```

### Build the Package

```bash
# Clean previous builds
rm -rf dist/

# Build the package
uv build

# This creates:
# dist/tipster_python-0.1.0-py3-none-any.whl
# dist/tipster_python-0.1.0.tar.gz
```

### Test on Test PyPI (Recommended)

```bash
# Upload to Test PyPI
uv publish -r testpypi

# Or using twine
twine upload -r testpypi dist/*
```

### Install from Test PyPI to Verify

```bash
# Create a virtual environment
python -m venv test_env
source test_env/bin/activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ tipster-python

# Test the package
tipster --help

# Cleanup
deactivate
rm -rf test_env
```

### Publish to PyPI

```bash
# Upload to PyPI
uv publish -r pypi

# Or using twine
twine upload dist/*
```

### Version Bumping

Update version in `pyproject.toml` before each release:

```toml
version = "0.1.0"  # bump to 0.2.0, etc.
```

Then rebuild and publish:

```bash
uv build
twine upload dist/*
```

### Using GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Build package
        run: uv build

      - name: Publish to PyPI
        run: uv publish -r pypi
        env:
          UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

### Checklist Before Publishing

- [ ] Update version in `pyproject.toml`
- [ ] Update README with any new features
- [ ] Test on Test PyPI first
- [ ] Verify package installs correctly
- [ ] Check package metadata on PyPI page

## License

MIT License - see LICENSE for details.
