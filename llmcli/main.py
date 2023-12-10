import io
import os
import sys
from typing import Annotated

import typer
from llama_cpp import Llama

app = typer.Typer()


def print_welcome():
    print("===================================")
    print("Beginn typing to start conversation")
    print("===================================")


@app.command("chat")
def chat(
    model_name: Annotated[str, typer.Option(help="Model name")] = "go-bruins-v2.Q5_K_M.gguf",
    temp: Annotated[float, typer.Option(help="The model temperature between 0-1. Larger values increase creativity but decrease factuality.")] = 0.2,
    top_k: Annotated[int, typer.Option(help="Top k")] = 40,
    top_p: Annotated[float, typer.Option(help="Randomly sample at each generation step from the top most likely tokens whose probabilities add up to top_p.")] = 0.95,
    repeat_penalty: Annotated[float, typer.Option(help="Penalize the model for repetition. Higher values result in less repetition.")] = 1.1,
    max_tokens: Annotated[int, typer.Option(help="The maximum number of tokens to generate.")] = 200,
):
    model_name = f"{os.path.expanduser('~/.cache/gpt4all/')}{model_name}"
    if not os.path.exists(model_name):
        print(f"No model found under {model_name}")

    print("Loading model...")
    llm = Llama(model_path=model_name, chat_format="chatml", verbose=False)
    print_welcome()

    messages = [
        {
            "role": "system",
            "content": "You are an assistant who gives answers.",
        },
    ]

    while True:
        prompt = input("User:<< ")
        messages.append({"role": "user", "content": prompt})
        response_stream = llm.create_chat_completion(messages, temperature=temp, top_k=top_k, top_p=top_p, repeat_penalty=repeat_penalty, stream=True)
        responses = []

        writer = io.StringIO()
        for r in response_stream:
            if "content" not in r["choices"][0]["delta"]:
                continue

            token = r["choices"][0]["delta"]["content"]
            print(token, end="", flush=True)
            writer.write(token)
            responses.append(token)

        print("")
        messages.append({"role": "assistant", "content": "".join(responses)})


@app.command("pipe")
def pipe(
    prompt: Annotated[str, typer.Argument(help="Command for gpt4all to execute on the piped input")],
    model_name: Annotated[str, typer.Option(help="Model name")] = "go-bruins-v2.Q5_K_M.gguf",
    temp: Annotated[float, typer.Option(help="The model temperature between 0-1. Larger values increase creativity but decrease factuality.")] = 0.2,
    top_k: Annotated[int, typer.Option(help="Top k")] = 40,
    top_p: Annotated[float, typer.Option(help="Randomly sample at each generation step from the top most likely tokens whose probabilities add up to top_p.")] = 0.95,
    repeat_penalty: Annotated[float, typer.Option(help="Penalize the model for repetition. Higher values result in less repetition.")] = 1.1,
    max_tokens: Annotated[int, typer.Option(help="The maximum number of tokens to generate.")] = 200,
):
    model_name = f"{os.path.expanduser('~/.cache/gpt4all/')}{model_name}"
    if not os.path.exists(model_name):
        print(f"No model found under {model_name}")

    input = "".join(list(sys.stdin))

    llm = Llama(model_path=model_name, chat_format="chatml", verbose=False)

    prompt = [
        {
            "role": "system",
            "content": f"You will be asked to do something on the following input.\nINPUT: {input}",
        },
        {
            "role": "user",
            "content": f"{prompt}",
        },
    ]
    response = llm(str(prompt), temperature=temp, top_k=top_k, top_p=top_p, max_tokens=max_tokens, repeat_penalty=repeat_penalty)
    token = response["choices"][0]["text"]

    writer = io.StringIO()
    print(token)
    writer.write(token)


def main():
    app()
