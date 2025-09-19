import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
prompt = sys.argv[1]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

def call_function(function_call_part, verbose=False):
    func_name = function_call_part.name
    args = dict(function_call_part.args or {})
    args["working_directory"] = "./calculator"
    registry = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    if func_name not in registry:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"}
                )
            ]
        )

    if verbose:
        print(f"Calling function: {func_name}({args})")
    else: print(f"- Calling function: {func_name}")

    func = registry[func_name]
    function_result = func(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": function_result}
            )
        ]
    )

for _ in range(20):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=config
    )

    for candidate in response.candidates:
        messages.append(candidate.content)
        
    if response.function_calls:
        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose=verbose)
            messages.append(function_call_result)
    else:
        if response.text: 
            if verbose:
                print(f"User prompt: {prompt}")
            print(response.text)
            break
            

