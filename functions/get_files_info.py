import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        working_directory = os.path.abspath(working_directory)
        if directory == ".":
            full_path = os.path.join(working_directory, "")
        else: 
            full_path = os.path.join(working_directory, directory)

        full_path = os.path.abspath(full_path)
        
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        if not os.path.commonpath([working_directory, full_path]) == working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        dir_contents_list = os.listdir(full_path)
        dir_contents= ''
        for file in dir_contents_list:
            file_path = os.path.join(full_path, file)
            dir_contents += f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)} \n"

        return dir_contents
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)