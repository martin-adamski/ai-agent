import os

from google.genai import types

def get_files_info(working_directory, directory="."):
	abs_target = os.path.abspath(os.path.join(working_directory, directory))
	abs_working = os.path.abspath(working_directory)

	if os.path.commonpath([abs_target, abs_working]) != abs_working:
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

	if not os.path.isdir(abs_target):
		return f'Error: "{directory}" is not a directory'

	try:
		lines = []
		for content in os.listdir(abs_target):
			string = f"- {content}: file_size={os.path.getsize(os.path.join(abs_target, content))} bytes, is_dir={os.path.isdir(os.path.join(abs_target, content))}"
			lines.append(string)
		return "\n".join(lines)
	except Exception as e:
		return f"Error: {e}"

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