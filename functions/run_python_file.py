import os
import subprocess
import sys

from google.genai import types


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


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the python file in the specified directory with along with the arguments, if provided, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative file path of the python file to be run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments in array form to be passed into the python code to be run",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=['file_path']
    ),
)