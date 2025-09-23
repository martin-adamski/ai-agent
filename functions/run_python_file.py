import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):

	abs_target = os.path.abspath(os.path.join(working_directory, file_path))
	abs_working = os.path.abspath(working_directory)

	if os.path.commonpath([abs_target, abs_working]) != abs_working:
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

	if not os.path.exists(abs_target):
		return f'Error: File "{file_path}" not found.'

	if not abs_target.endswith(".py"):
		return f'Error: "{file_path}" is not a Python file.'

	try:
		run = subprocess.run(
			[sys.executable, abs_target, *args]
			, cwd = abs_working
			, timeout = 30
			, capture_output = True
			, text = True
		)

		return_str = f"STDOUT: {run.stdout}\nSTDERR: {run.stderr}\n"
		
		if run.returncode != 0:
			return return_str + f"Process exited with code {run.returncode}"

		if not run.stdout and not run.stderr:
			return "No output produced."

		return return_str

	except Exception as e:
		return f"Error: executing Python file: {e}"