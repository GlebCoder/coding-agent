import os

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

