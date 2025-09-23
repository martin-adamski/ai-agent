import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("Prompts not provided")
        sys.exit(1)

    user_prompt = " ".join(args)

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose, user_prompt)


def generate_content(client, messages, verbose, user_prompt):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
            )
        )

    if response.function_calls:
        for fc in response.function_calls:
            print(f"Calling function: {fc.name}({fc.args})")
    else:
        print("Response:")
        print(response.text)

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
