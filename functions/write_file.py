import os

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