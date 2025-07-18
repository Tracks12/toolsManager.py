#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/anguarch.py

from os import chdir, mkdir, system as shell
from os.path import abspath, dirname, relpath

from core.icons import Icons
from core.tool import Tool

class AnguArch(Tool):
	""" AnguArch tool for generating Angular projects with specific design patterns.

		This tool provides functionality to create new Angular projects with a specified design pattern.
		It ensures the workspace directory exists and provides methods to generate projects.

		Attributes:
			command (tuple): The command aliases for the tool.
			name (str): The name of the tool.
			path (str): The path to the tool's directory.
			version (str): The version of the tool.

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
		""" Generate a new Angular project with a specific design pattern.

			Args:
				args (list[str]): The command line arguments for the tool.

			Raises:
				RuntimeError: If the Angular CLI is not installed or the command fails.

		"""

		chdir(self.__path)
		shell(f"ng v")
		shell(f"ng n {args[0]} --routing --style=scss --skip-install --skip-git --skip-tests --defaults")

		chdir(f"{self.__path}/{args[0]}")
		cmds = [
			"ng g c _common/components/button --skip-tests",
			"ng g e _common/enums/http-code.enum",
			"ng g e _common/enums/user-role.enum",
			"ng g g _common/guards/is-admin --skip-tests",
			"ng g g _common/guards/is-authenticated --skip-tests",
			"ng g g _common/guards/is-logged-in --skip-tests",
			"ng g i _common/models/user.model",
			"ng g s _common/services/api/api --skip-tests",
			"ng g s _common/services/api/api-sign --skip-tests",
			"ng g s _common/services/auth --skip-tests",
			"ng g c admin --skip-tests",
			"ng g c admin/menu --skip-tests",
			"ng g c error --skip-tests",
			"ng g c main --skip-tests",
			"ng g c main/about --skip-tests",
			"ng g c main/header --skip-tests",
			"ng g c main/home --skip-tests",
			"ng g c main/menu --skip-tests",
			"ng g c main/footer --skip-tests",
			"ng g c maintenance --skip-tests",
			"ng g c sign --skip-tests",
			"ng g c sign/forget-password --skip-tests",
			"ng g c sign/sign-in --skip-tests",
			"ng g c sign/sign-up --skip-tests",
		]

		shell(" | ".join(cmds))