import os

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