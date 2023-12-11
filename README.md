# CLI for Large Languge Models

Local cli for LLMs.
Features:

- Intelligent terminal. Type in what you want, and execute the generated bash script.
- Chat. Chat with the LLM.
- Pipe content to the LLM and analyze it with a prompt.

## Example usage

```
llm-cli cli "List all files in ~/Downloads, sort by file size and output the file size in megabytes with the filename"

llm-cli cli "Rename all files in /tmp that start with 'test'. Replace 'test' with 'stage'"


cat pyproject.toml | llm-cli pipe --max-tokens 1000 "Explain line by line"

llm-cli chat
```

## Installation

```
python -m venv .venv
. .venv/bin/activate
pip install git+https://github.com/krenzaslv/llm-cli.git
```
