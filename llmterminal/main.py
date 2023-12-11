import subprocess
import sys
from typing import Annotated

import typer
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

app = typer.Typer()


@app.command("chat")
def chat(
    model_name: Annotated[str, typer.Option(help="Model name")] = "go-bruins-v2.Q5_K_M.gguf",
    repo_id: Annotated[str, typer.Option(help="Name of the huggingface repo")] = "TheBloke/go-bruins-v2-GGUF",
    temp: Annotated[float, typer.Option(help="The model temperature between 0-1. Larger values increase creativity but decrease factuality.")] = 0.2,
    top_k: Annotated[int, typer.Option(help="Top k")] = 40,
    top_p: Annotated[float, typer.Option(help="Randomly sample at each generation step from the top most likely tokens whose probabilities add up to top_p.")] = 0.95,
    repeat_penalty: Annotated[float, typer.Option(help="Penalize the model for repetition. Higher values result in less repetition.")] = 1.1,
    max_tokens: Annotated[int, typer.Option(help="The maximum number of tokens to generate.")] = 200,
):
    llm = get_model(repo_id, model_name)

    messages = [
        {
            "role": "system",
            "content": "You are an assistant who gives answers to everything a user asks.",
        },
    ]

    while True:
        prompt = input("User:>> ")
        messages.append({"role": "user", "content": prompt})
        response_stream = llm.create_chat_completion(messages, temperature=temp, max_tokens=max_tokens, top_k=top_k, top_p=top_p, repeat_penalty=repeat_penalty, stream=True)
        responses = []

        for r in response_stream:
            if "content" not in r["choices"][0]["delta"]:
                continue

            token = r["choices"][0]["delta"]["content"].replace("<0x0A>", "\n")
            token = token.replace("<br>", "\n")
            print(token, end="", flush=True)
            responses.append(token)

        print("")
        messages.append({"role": "assistant", "content": "".join(responses)})


@app.command("cli")
def cli(
    prompt: Annotated[str, typer.Argument(help="Prompt what bash script to generate")],
    model_name: Annotated[str, typer.Option(help="Model name")] = "codellama-7b-instruct.Q5_K_M.gguf",
    execute: Annotated[bool, typer.Option(help="Execute code without review.")] = False,
    repo_id: Annotated[str, typer.Option(help="Name of the huggingface repo")] = "TheBloke/CodeLlama-7B-Instruct-GGUF",
    temp: Annotated[float, typer.Option(help="The model temperature between 0-1. Larger values increase creativity but decrease factuality.")] = 0.2,
    top_k: Annotated[int, typer.Option(help="Top k")] = 40,
    top_p: Annotated[float, typer.Option(help="Randomly sample at each generation step from the top most likely tokens whose probabilities add up to top_p.")] = 0.95,
    repeat_penalty: Annotated[float, typer.Option(help="Penalize the model for repetition. Higher values result in less repetition.")] = 1.1,
    max_tokens: Annotated[int, typer.Option(help="The maximum number of tokens to generate.")] = 200,
):
    llm = get_model(repo_id, model_name)
    messages = [
        {
            "role": "system",
            "content": "You are a terminal assistant that generates bash scripts from a given input. Print results to stdout except if asked otherwise.",
        },
        {
            "role": "user",
            "content": f"{prompt}",
        },
    ]

    response_stream = llm.create_chat_completion(messages, temperature=temp, top_k=top_k, max_tokens=max_tokens, top_p=top_p, repeat_penalty=repeat_penalty, stream=True)
    responses = []

    for r in response_stream:
        if "content" not in r["choices"][0]["delta"]:
            continue

        token = r["choices"][0]["delta"]["content"].replace("<0x0A>", "\n")
        token = token.replace("<br>", "\n")
        print(token, end="", flush=True)
        responses.append(token)

    print("")
    if not execute:
        execute = typer.confirm("Do you want to execute the command?")
        if execute:
            subprocess.run(["sh", "-c", f'{"".join(responses)}'])
    else:
        subprocess.run(["sh", "-c", f'{"".join(responses)}'])



@app.command("pipe")
def pipe(
    prompt: Annotated[str, typer.Argument(help="Command for gpt4all to execute on the piped input")],
    model_name: Annotated[str, typer.Option(help="Model name")] = "go-bruins-v2.Q5_K_M.gguf",
    repo_id: Annotated[str, typer.Option(help="Name of the huggingface repo")] = "TheBloke/go-bruins-v2-GGUF",
    temp: Annotated[float, typer.Option(help="The model temperature between 0-1. Larger values increase creativity but decrease factuality.")] = 0.2,
    top_k: Annotated[int, typer.Option(help="Top k")] = 40,
    top_p: Annotated[float, typer.Option(help="Randomly sample at each generation step from the top most likely tokens whose probabilities add up to top_p.")] = 0.95,
    repeat_penalty: Annotated[float, typer.Option(help="Penalize the model for repetition. Higher values result in less repetition.")] = 1.1,
    max_tokens: Annotated[int, typer.Option(help="The maximum number of tokens to generate.")] = 200,
):
    llm = get_model(repo_id, model_name)

    input = "".join(list(sys.stdin))
    prompt = [
        {
            "role": "system",
            "content": f"You will be asked to do something on the following input: \n{input}",
        },
        {
            "role": "user",
            "content": f"{prompt}",
        },
    ]
    response_stream = llm.create_chat_completion(prompt, temperature=temp, top_k=top_k, max_tokens=max_tokens, top_p=top_p, repeat_penalty=repeat_penalty, stream=True)

    for r in response_stream:
        if "content" not in r["choices"][0]["delta"]:
            continue

        token = r["choices"][0]["delta"]["content"].replace("<0x0A>", "\n")
        token = token.replace("<br>", "\n")
        print(token, end="", flush=True)


def get_model(repo_id: str, model_name: str):
    model_path = hf_hub_download(repo_id=repo_id, filename=model_name)
    print("Loading model...")
    llm = Llama(model_path=model_path, chat_format="chatml", verbose=False)
    return llm


def main():
    app()
