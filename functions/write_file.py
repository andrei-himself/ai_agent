import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.join(working_directory, file_path)
        directory = os.path.dirname(full_path)

        if directory and not os.path.exists(full_path):
            os.makedirs(directory, exist_ok=True)

        if not os.path.commonpath([working_directory, full_path]) == working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content or "")

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content to the given file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)