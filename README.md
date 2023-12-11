# Large Language Models for the terminal

Interact with LLMs from your terminal. All models are executed locally on your machine.

Don't remember a specific command? `llm-terminal` can generate and execute terminal scripts for you. E.g `llm-terminal cli "Move all files that are bigger than 1GB from /project to /tmp. Put the suffix 'to-big-' in front of each file."`

> [!WARNING]  
> By default `llm-terminal cli` will print the generated code and ask for permission to execute. Review the generated code carefully before execution. You can disable code review with the `--execute` flag.

You can chat with a LLM from within your terminal with `llm-terminal chat`.

On first use, `llm-terminal` downloads default models for chat and code generation. To specify a different model look at `llm-terminal--help`.

Features:

- Intelligent terminal. Type in what you want, and execute the generated bash script.
- Chat. Chat with the LLM.
- Pipe content to the LLM and analyze it with a prompt.

## Example usage

```
llm-terminal cli "List all files in ~/Downloads, sort by file size and output the file size in megabytes with the filename"

llm-terminal cli "Rename all files in /project that start with 'test'. Replace 'test' with 'stage'"

cat pyproject.toml | head | llm-terminal pipe --max-tokens 1000 "Explain line by line"

llm-terminal chat

llm-terminal--help
```

## Installation

```
python -m venv .venv
. .venv/bin/activate
pip install git+https://github.com/krenzaslv/llm-terminal.git
```
