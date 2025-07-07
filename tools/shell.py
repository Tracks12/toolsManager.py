#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Shell Tool - Shell Command Scheduler and Executor

	This tool provides an interface to execute shell commands and manage
	schedules of shell commands that can be saved, listed, deleted, and run.

	Features:
	- Execute arbitrary shell commands directly from Python.
	- Create schedules of multiple shell commands stored as JSON files.
	- List all saved schedules in a workspace directory.
	- Delete schedules with confirmation or forced option.
	- Run saved schedules sequentially with optional pauses between commands.

	Schedules are saved in a dedicated workspace directory:
		<workspace_root>/Shell/Schedules/

	Example:
		$ shell --new-schedule mytasks
		$ shell --list-schedule
		$ shell --run-schedule mytasks -p

"""

# tools/shell.py

from json import dump, load
from os import listdir, mkdir, remove, system as shell
from os.path import abspath, dirname

import re

from core.colors import Colors
from core.config import Config
from core.icons import Icons
from core.tool import Tool

SCHEDULENAME_REGEX = str("(\\s)|([/:])")

class Shell(Tool):
	""" Tool to manage shell command schedules and execute shell commands from Python.

		Shell allows you to:
		- Execute arbitrary shell commands.
		- Create, list, delete, and run schedules of commands stored as JSON files.
		- Manage schedules in a dedicated workspace folder.
		- Optionally pause between commands when running a schedule.

		Commands:
		- `-c, --command`: Run a single shell command.
		- `-n, --new-schedule`: Create a new schedule of shell commands.
		- `-l, --list-schedule`: List all saved schedules.
		- `-d, --delete-schedule`: Delete an existing schedule.
		- `-r, --run-schedule`: Run a saved schedule, optionally pausing between commands.

		Example:
			`~$ shell --new-schedule mytasks`
			`~$ shell --list-schedule`
			`~$ shell --run-schedule mytasks -p`

	"""

	command	= (("shell", "sh"), "(sh)ell")
	name	= "Shell"
	path	= __file__
	version	= "1.0"

	def __init__(self, args: list[str]):
		self.__cfg	= Config()
		self.__path	= str(abspath(f"{dirname(abspath(__file__))}/../{self.name}"))
		self.__schedulesPath = abspath(f"{self.__path}/Schedules")
		self.__setup()

		self._args = [
			(("-c", "--command", "<cmd>"), "Run a bash command"),
			(("-d", "--delete-schedule", "<sch> *"), ("Delete a schedule of commands", "opt: -f to delete without asking")),
			(("-l", "--list-schedule", ""), "List all schedules save in workspace"),
			(("-n", "--new-schedule", "<sch>"), "Create a schedule of commands"),
			(("-r", "--run-schedule", "<sch> *"), ("Run a schedule of commands", "opt: -p to pause between all commands"))
		]

		self._execs = [
			lambda x:self._command(x),
			lambda x:self._deleteSchedule(x),
			lambda x:self._listSchedule(),
			lambda x:self._newSchedule(x),
			lambda x:self._runSchedule(x),
		]

		super().__init__()
		self._run(args, lambda:self._command(args[1: len(args)]))

	def __checkExistSchedule(self, scheduleName: str) -> bool:
		""" Checks if a schedule with the given name exists in the workspace's schedules directory.
			The schedule name is normalized by removing spaces and replacing special characters with hyphens.

			Args:
				scheduleName (str): Name of the schedule to check.

			Returns:
				bool: True if the schedule exists, False otherwise.

		"""

		__schedules = [ s.split(".")[0] for s in listdir(self.__schedulesPath) ]

		if(scheduleName in __schedules):
			return(True)

		print(f"{Icons.warn}Schedule doesn't exist on workspace")
		return(False)

	def __setup(self) -> None:
		""" Setup the workspace directories for Shell tool.

			Creates the main workspace folder and the Schedules subfolder.
			Handles exceptions and prints status messages.

		"""

		try:
			mkdir(self.__path)
			mkdir(self.__schedulesPath)
			print(f"{Icons.info}Create path workspace for {self.name} tool at {self.__path}")

		except(FileExistsError):
			print(f"{Icons.info}Using {self.__path} for {self.name} workspace")

		except(PermissionError):
			print(f"{Icons.warn}Permission denied: Unable to create '{self.__path}'.")

		except(Exception) as e:
			print(f"{Icons.err}An error occurred: {e}")

	def _command(self, args: list[str]) -> None:
		shell(" ".join(args))

	def _deleteSchedule(self, args: list[str]) -> None:
		""" Delete a saved schedule from the workspace.

			Args:
				args (list[str]): Arguments containing the schedule name and optional flags.

			Raises:
				FileNotFoundError: If the schedule does not exist.

		"""

		try:
			__scheduleName = re.sub(SCHEDULENAME_REGEX, "-", args[0])

			if(not self.__checkExistSchedule(__scheduleName)):
				raise(FileNotFoundError("Schedule doesn't exist on workspace"))

			if(("-f" in args) or self.ask(f"Confirm the deletion of {args[0]} ?")):
				remove(abspath(f"{self.__schedulesPath}/{__scheduleName}.json"))
				print(f'{Icons.info}"{__scheduleName}" was deleted from {self.__path}')

		except(FileNotFoundError) as e:
			print(f"{Icons.warn}{e}")

	def _listSchedule(self) -> None:
		""" List all saved schedules in the workspace.

			Prints a formatted table of schedule names and their paths.

		"""

		__schedules = listdir(self.__schedulesPath)

		table = list[str]([ f" *  {'Name':<{18}}Path" ])
		for i, schedule in enumerate(__schedules, start=1):
			table.append("".join([
				f"{' '*(2-len(str(i)))}{Colors.green}{i}{Colors.end}. ",
				f"{Colors.cyan}{schedule.replace('-', ':').split('.')[0]:<{18}}{Colors.end}",
				f"{Colors.yellow}{abspath(f'{self.__schedulesPath}/{schedule}')}{Colors.end}"
			]))

		_ = "\n".join([ f' {t}' for t in table ])
		print(f"\n{_}")

	def _newSchedule(self, args: list[str]) -> None:
		""" Create a new schedule by interactively entering commands.

			Args:
				args (list[str]): Arguments containing the schedule name.

			Raises:
				FileExistsError: If the schedule already exists.
				IndexError: If no schedule name was provided.

		"""

		try:
			__scheduleName = re.sub(SCHEDULENAME_REGEX, "-", args[0])
			__schedules = list[str]([])

			if(self.__checkExistSchedule(__scheduleName)):
				raise(FileExistsError(f'Schedule "{args[0]}" already exist in {self.__schedulesPath}'))

			print(f'Enter the following commands on the new "{args[0]}" schedule')
			while(True):
				__schedule = input(f"{args[0]}[{len(__schedules)}]: ")

				if(not __schedule):
					break

				__schedules.append(__schedule)

			if(len(__schedules)):
				print(f'Saving schedules in "{args[0]}"')
				with open(abspath(f"{self.__schedulesPath}/{__scheduleName}.json"), "w", encoding=self.__cfg.getEncoding()) as json:
					_ = dict({ "schedules" : __schedules })
					dump(dict(_), json, sort_keys=True, indent=2)

			print(f'"{args[0]}" schedule was created in {self.__schedulesPath}')

		except(IndexError):
			print(f"{Icons.warn}No schedule name was specified !")

		except(FileExistsError) as e:
			print(f"{Icons.warn}{e}")

	def _runSchedule(self, args: list[str]) -> None:
		""" Run a saved schedule of commands sequentially.

			Args:
				args (list[str]): Arguments containing the schedule name and optional flags.

			Behavior:
			- Loads the schedule commands from JSON file.
			- Runs each command in order.
			- If `-p` flag is given, pauses between commands waiting for user input.

		"""

		__scheduleName = re.sub(SCHEDULENAME_REGEX, "-", args[0])

		if(self.__checkExistSchedule(__scheduleName)):
			print(f"{Icons.play}Running {args[0]} ...")

			with open(abspath(f"{self.__schedulesPath}/{__scheduleName}.json"), "r", encoding=self.__cfg.getEncoding()) as json:
				_ = dict[str, list[str]](load(json))
				__schedules	= _["schedules"]

			if(len(__schedules)):
				for i, schedule in enumerate(__schedules):
					print(f" [{i}]: {schedule}")
					self._command([ schedule ])

					if(("-p" in args) and (i+1 < len(__schedules))):
						input(f'Next command: "$ {__schedules[i+1]}"')
