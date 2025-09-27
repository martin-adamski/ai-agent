import os

from google.genai import types


def write_file(working_directory, file_path, content):

	abs_target = os.path.abspath(os.path.join(working_directory, file_path))
	abs_working = os.path.abspath(working_directory)

	if os.path.commonpath([abs_target, abs_working]) != abs_working:
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

	try:
		if not os.path.exists(abs_target):
			os.makedirs(os.path.dirname(abs_target), exist_ok=True)
	except Exception as e:
		return f"Error: creating directory: {e}"

	try:
		with open(abs_target, "w") as f:
			f.write(content)
			return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
		return f"Error: writing to the file: {e}"

schema_write_file= types.FunctionDeclaration(
    name="write_file",
    description="Write (or overwrite) contents to the file in the provided file path, constrained to the working directory. If the file path is not file, necessary directories are created first.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path of the python file to be written to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to be written into the file",
            ),
        },
        required=['file_path','content']
    ),
)