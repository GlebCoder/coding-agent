import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
def get_files_info(working_directory, directory="."):
    try:
        abs_path_working_dir = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abs_path_working_dir, directory))
        valid_target_dir = os.path.commonpath([target_directory, abs_path_working_dir]) == abs_path_working_dir

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        content_dir = os.listdir(target_directory)
        list_files = []
        for file in content_dir:
            file_path = os.path.join(target_directory, file)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            ele = f"- {file}: file_size={file_size} bytes, is_dir={is_dir}"
            list_files.append(ele)
        return "\n".join(list_files)
    except Exception as ex:
        print(f"Error: {ex}")

