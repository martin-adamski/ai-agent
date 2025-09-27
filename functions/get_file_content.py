import os
from config import MAX_CHARS

from google.genai import types


def get_file_content(working_directory, file_path):

	abs_target = os.path.abspath(os.path.join(working_directory, file_path))
	abs_working = os.path.abspath(working_directory)

	if os.path.commonpath([abs_target, abs_working]) != abs_working:
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

	if not os.path.isfile(abs_target):
		f'Error: File not found or is not a regular file: "{file_path}"'

	try:
		with open(abs_target, "r") as f:
			chunk = f.read(MAX_CHARS + 1)

			if len(chunk) <= MAX_CHARS:
				return chunk
			else:
				return chunk[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
	except Exception as e:
		return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the contents of a file, returned as string, constrained to the working directory. The file content string is capped at 10 000 length.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path of the file whose contents to get",
            ),
        },
        required=["file_path"]
    ),
)