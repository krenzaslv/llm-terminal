# CLI for Large Languge Models

Local cli for llms.

## Example usage

```
cat pyproject.toml | llm-cli pipe --max-tokens 1000 "Give an explenation of the following file"
llm-cli chat
```

## Installation

```
python -m venv .venv
. .venv/bin/activate
pip install git+https://github.com/krenzaslv/llm-cli.git
```
