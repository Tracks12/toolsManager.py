#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from json import dump, load
from os import listdir, mkdir, remove, system as shell
from os.path import abspath, dirname
from traceback import format_exc

import re

from core.colors import Colors
from core.config import Config
from core.icons import Icons
from core.tool import Tool

SCHEDULENAME_REGEX = str("(\\s)|([/:])")

class Shell(Tool):
	command	= (("shell", "sh"), "(sh)ell")
	name	= "Shell"
	path	= __file__
	version	= "1.0"

	def __init__(self, args: list[str]):
		super().__init__()

		self.__cfg	= Config()
		self.__path	= str(abspath(f"{dirname(abspath(__file__))}/../{self.name}"))
		self.__schedulesPath = abspath(f"{self.__path}/Schedules")
		self.__setup()

		self._args = [
			(("-c", "--command", "<command>"), "Run a bash command"),
			(("-d", "--delete-schedule", "<schedule>"), "Delete a schedule of commands"),
			(("-l", "--list-schedule", ""), "List all schedules save in workspace"),
			(("-n", "--new-schedule", "<schedule>"), "Create a schedule of commands"),
			(("-r", "--run-schedule", "<schedule>"), "Run a schedule of commands")
		] + self._args[:]

		self._execs = [
			lambda x:self._command(x),
			lambda x:self._deleteSchedule(x),
			lambda x:self._listSchedule(),
			lambda x:self._newSchedule(x),
			lambda x:self._runSchedule(x),
		] + self._execs[:]

		self._run(args)

	def __ask(self, msg: str = "Are you sure ?") -> bool:
		return(bool(input(f"{msg} [y/N] ").lower() in ("y", "yes")))

	def __checkExistSchedule(self, scheduleName: str) -> bool:
		__schedules = [ s.split(".")[0] for s in listdir(self.__schedulesPath) ]

		if(scheduleName in __schedules):
			return(True)

		print(f"{Icons.warn}Schedule doesn't exist on workspace")
		return(False)

	def __setup(self) -> None:
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

	def _run(self, args: list[str]) -> bool:
		try:
			for i, a in enumerate(self._args):
				if(args[1] in a[0]):
					self._execs[i](args[2: len(args)])
					return(True)

			self._command(args[1: len(args)])

		except(IndexError):
			print(' To see more of command type "-h" or "--help" on arguments')

		except(ValueError) as e:
			print(f"{Icons.warn}{e}")

		except(Exception):
			print(f"{Icons.err}{format_exc()}")

		return(False)

	def _command(self, args: list[str]) -> None:
		shell(" ".join(args))

	def _deleteSchedule(self, args: list[str]) -> None:
		__scheduleName = re.sub(SCHEDULENAME_REGEX, "-", args[0])

		if(self.__checkExistSchedule(__scheduleName)):
			print(f'{Icons.info}Delete "{__scheduleName}"')
			remove(abspath(f"{self.__schedulesPath}/{__scheduleName}.json"))

	def _listSchedule(self) -> None:
		__schedules = listdir(self.__schedulesPath)

		table = list[str]([ f" *  Name{' '*(18-len('Name'))}Path" ])
		for i, schedule in enumerate(__schedules, start=1):
			table.append("".join([
				f"{' '*(2-len(str(i)))}{Colors.green}{i}{Colors.end}.",
				f"{' '*1}{Colors.cyan}{schedule.replace('-', ':').split('.')[0]}{Colors.end}",
				f"{' '*(18-len(schedule.split('.')[0]))}{Colors.yellow}{abspath(f'{self.__schedulesPath}/{schedule}')}{Colors.end}"
			]))

		_ = "\n".join([ f' {t}' for t in table ])
		print(f"\n{_}")

	def _newSchedule(self, args: list[str]) -> None:
		__scheduleName = re.sub(SCHEDULENAME_REGEX, "-", args[0])
		__schedules = list[str]([])

		try:
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
