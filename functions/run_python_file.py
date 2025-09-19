import subprocess
import os
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not os.path.commonpath([working_directory, full_path]) == working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        
        if not full_path.lower().endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        
        result = subprocess.run([sys.executable, full_path, *args], capture_output = True, text = True, timeout = 30, cwd = working_directory)

        stdout_line = result.stdout or ""
        stderr_line = result.stderr or ""
        return_string = f"STDOUT: {stdout_line}\nSTDERR: {stderr_line}" 
        
        if not stdout_line and not stderr_line:
            return "No output produced."
        
        if result.returncode != 0:
            return_string += f"\nProcess exited with code {result.returncode}"

        return return_string
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to execute.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The extra arguments to add to the execution command.",
            ),
        },
    ),
)