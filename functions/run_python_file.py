import os, subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=f"Run a Python file and return its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a file relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of strings representing arguments",
                items=types.Schema(type=types.Type.STRING),
            )
        },
        required=["file_path",],
    ),
)
def run_python_file(woking_directory, file_path, args=None):
    try:
        abs_woking_directory = os.path.abspath(woking_directory)
        target_file_path = os.path.normpath(os.path.join(abs_woking_directory, file_path))
        valid_file_path = os.path.commonpath([abs_woking_directory, target_file_path]) == abs_woking_directory
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]
        if args:
            command.extend(args)

        result = subprocess.run(command,
                       cwd=abs_woking_directory,
                       text=True,
                       capture_output=True,
                       timeout=30)
        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output += "No output produced"
        if result.stdout:
            output += f'STDOUT: {result.stdout}'
        if result.stderr:
            output += f'STDERR: {result.stderr}'
        return output
    except Exception as e:
        return f'Error: executing Python file {e}'
