# Large Languge Models for the terminal

Interact with LLMs from your terminal. All models are executed locally on your machine.

Don't remember a specific command? `llm-cli` can generate and execute terminal scripts for you. E.g `llm-cli cli "Move all files in that are bigger than 1GB from /project to /tmp. Put the suffix 'to-big-' in front of each file."`

You can chat with a LLM from within your terminal with `llm-cli chat`.

On first use, `llm-cli` downloads default models for chat and code generation. To specify a different model look at `llm-cli --help`.

Features:

- Intelligent terminal. Type in what you want, and execute the generated bash script.
- Chat. Chat with the LLM.
- Pipe content to the LLM and analyze it with a prompt.

## Example usage

```
llm-cli cli "List all files in ~/Downloads, sort by file size and output the file size in megabytes with the filename"

llm-cli cli "Rename all files in /project that start with 'test'. Replace 'test' with 'stage'"

cat pyproject.toml | llm-cli pipe --max-tokens 1000 "Explain line by line"

llm-cli chat

llm-cli --help
```

## Installation

```
python -m venv .venv
. .venv/bin/activate
pip install git+https://github.com/krenzaslv/llm-cli.git
```
