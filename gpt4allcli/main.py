import io
import os
import sys
from typing import Annotated

import typer
from gpt4all import GPT4All
from gpt4all.gpt4all import Path

app = typer.Typer()


def print_welcome():
    print("===================================")
    print("Beginn typing to start conversation")
    print("===================================")


@app.command("chat")
def chat(
    model_name: Annotated[str, typer.Option(help="Model name")] = "wizardlm-13b-v1.2.Q4_0.gguf",
    max_tokens: Annotated[int, typer.Option(help="The maximum number of tokens to generate.")] = 200,
    temp: Annotated[float, typer.Option(help="The model temperature between 0-1. Larger values increase creativity but decrease factuality.")] = 0.9,
    top_k: Annotated[int, typer.Option(help="The maximum number of tokens to generate.")] = 40,
    top_p: Annotated[float, typer.Option(help="Randomly sample at each generation step from the top most likely tokens whose probabilities add up to top_p.")] = 0.9,
    repeat_penalty: Annotated[float, typer.Option(help="Penalize the model for repetition. Higher values result in less repetition.")] = 1.1,
    repeat_last_n: Annotated[int, typer.Option(help="Penalize the model for repetition. Higher values result in less repetition.")] = 64,
):
    if not os.path.exists(os.path.join(str(Path.home()), ".cache", "gpt4all", model_name).replace("\\", "\\\\")):
        print(f"Downloading model {model_name}...")

    print("Loading model...")

    model = GPT4All(model_name)
    model.model.set_thread_count(8)

    print_welcome()
    with model.chat_session():
        while True:
            message = input("-> ")

            response_generator = model.generate(
                message,
                max_tokens=max_tokens,
                temp=temp,
                top_k=top_k,
                top_p=top_p,
                repeat_penalty=repeat_penalty,
                repeat_last_n=repeat_last_n,
                streaming=True,
            )

            response = io.StringIO()
            for token in response_generator:
                print(token, end="", flush=True)
                response.write(token)

            response_message = {"role": "assistant", "content": response.getvalue()}
            response.close()
            model.current_chat_session.append(response_message)

            print()


@app.command("pipe")
def pipe(
    command: Annotated[str, typer.Argument(help="Command for gpt4all to execute on the piped input")],
    model_name: Annotated[str, typer.Option(help="Model name")] = "wizardlm-13b-v1.2.Q4_0.gguf",
    max_tokens: Annotated[int, typer.Option(help="The maximum number of tokens to generate.")] = 400,
    temp: Annotated[float, typer.Option(help="The model temperature between 0-1. Larger values increase creativity but decrease factuality.")] = 0.1,
    top_k: Annotated[int, typer.Option(help="The maximum number of tokens to generate.")] = 1,
    top_p: Annotated[float, typer.Option(help="Randomly sample at each generation step from the top most likely tokens whose probabilities add up to top_p.")] = 0.9,
    repeat_penalty: Annotated[float, typer.Option(help="Penalize the model for repetition. Higher values result in less repetition.")] = 1.1,
    repeat_last_n: Annotated[int, typer.Option(help="Penalize the model for repetition. Higher values result in less repetition.")] = 64,
):
    if not os.path.exists(os.path.join(str(Path.home()), ".cache", "gpt4all", model_name).replace("\\", "\\\\")):
        print(f"Downloading model {model_name}...")

    model = GPT4All(model_name)
    model.model.set_thread_count(8)

    prompt = "".join(list(sys.stdin))
    prompt = f"{command}:\n{prompt}"

    response = model.generate(
        prompt,
        max_tokens=max_tokens,
        temp=temp,
        top_k=top_k,
        top_p=top_p,
        repeat_penalty=repeat_penalty,
        repeat_last_n=repeat_last_n,
    )

    print(response)


def main():
    app()
