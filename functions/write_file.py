import os


def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
        valid_file_path = os.path.commonpath([abs_working_directory, target_file_path]) == abs_working_directory

        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_directory = os.path.dirname(target_file_path)
        os.makedirs(parent_directory, exist_ok=True)

        with open(target_file_path, 'w') as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'