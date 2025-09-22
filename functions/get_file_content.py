import os
from config import MAX_CHARS

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