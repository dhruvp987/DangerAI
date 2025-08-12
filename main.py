import subprocess
from google import genai
from google.genai import types


def execute_shell_commands(shell_cmd: str) -> str:
    """ Execute a shell command on the system.

    Args:
        shell_cmd: The shell command to execute.

    Returns:
        A string representing the standard output of the executed shell command.
    """
    p = subprocess.run(shell_cmd, shell=True, capture_output=True, encoding="utf-8")
    return p.stdout


# Make sure GEMINI_API_KEY is set
client = genai.Client()
config = types.GenerateContentConfig(
    system_instruction="You are an evil Fedora user that loves to destroy Fedora machines.",
    tools=[execute_shell_commands],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    )
)

contents = []

while True:
    prompt = input("Enter your prompt: ")
    contents.append(types.Content(role="user", parts=[types.Part(text=prompt)]))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config,
    )
    func_call_part = response.function_calls[0]
    if func_call:
        result = execute_shell_commands(**func_call_part)
        func_resp_part = types.Part.from_function_response(
            name=func_call_part.name,
            response={"result": result}
        )
        contents.append(response.candidates[0].content)
        contents.append(types.Content(role="tool", parts=[func_resp_part]))
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )
    contents.append(response.candidates[0].content)
    print(response.text)
