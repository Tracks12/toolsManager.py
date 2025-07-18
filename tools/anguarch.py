#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/anguarch.py

from os import mkdir, system as shell
from os.path import abspath, dirname, relpath

from core.icons import Icons
from core.tool import Tool

class AnguArch(Tool):
	""" Say hello to the user
	"""

	command	= (("anguarch", "ang"), "(ang)uarch")
	name	= "AnguArch"
	path	= __file__
	version	= "0.1a"

	def __init__(self, args: list[str]):
		self.__path = str(abspath(f"{dirname(abspath(__file__))}/../{self.name}"))
		self.__setup()

		self._args	= [
			(("-n", "--new", "<name> <pattern>"), "Generate an angular project with specific design pattern")
		]

		self._execs = [
			lambda x:self._new(x)
		]

		super().__init__()
		self._run(args, lambda:self._helper())

	def __setup(self) -> None:
		""" Ensure the workspace directory exists for Angular projects.

			Creates the workspace path if it does not exist.
			Prints informative messages depending on the outcome.

		"""

		try:
			mkdir(self.__path)
			print(f"{Icons.info}Create path workspace for {self.name} tool at {self.__path}")

		except(FileExistsError):
			print(f"{Icons.info}Using {self.__path} for {self.name} workspace")

		except(PermissionError):
			print(f'{Icons.warn}Permission denied: Unable to create "{self.__path}".')

		except(Exception) as e:
			print(f"{Icons.err}An error occurred: {e}")

	def _new(self, args: list[str]) -> None:
		shell(f"ng v")
		shell(f"ng n {args[0]} --directory {relpath(f"{self.__path}/{args[0]}")} --routing --style=scss --skip-install --skip-git")
