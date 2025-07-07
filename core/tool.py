#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Base module for all CLI tools in the application.

	This module defines the `Tool` class, an abstract foundation for every CLI
	tool located in the `tools/` directory. It standardizes how tools handle
	command-line arguments and execute related behaviors.

	Each tool should inherit from `Tool`, define its own arguments and logic,
	and trigger execution by calling `_run()` in its constructor.

"""

from traceback import format_exc
from typing import Callable

from core.exceptions import ToolInitError
from core.icons import Icons

class Tool:

	""" Abstract base class for CLI tools.

		This class provides a standardized way for tools to define CLI arguments
		and map them to specific execution functions. It handles argument matching
		and dispatching of corresponding methods.

		Attributes:
			command (tuple[tuple[str, str], str]): CLI command pattern (argument string, alias, full command string).
			name (str): Tool name.
			path (str): Absolute file path to the tool.
			version (str): Version string of the tool.

			_args (list[tuple[tuple[str, str, str], str]]): List of accepted arguments and descriptions.
			_execs (list[Callable]): List of methods executed when a corresponding argument is found.

		Usage:
			Subclass must:
			- Populate `_args` with argument patterns
			- Populate `_execs` with corresponding execution functions
			- Call `_run(args)` in the constructor

	"""

	command	: tuple[tuple[str], str]	= (("", ""), "")
	name	: str						= ""
	path	: str						= ""
	version	: str						= ""

	def __init__(self):
		self._args	= self._args[:] + [
			(("-h", "--help", ""), "Show the helper commands menu"),
			(("-v", "--version", ""), "Show version of tool")
		]

		self._execs	= self._execs[:] + [
			lambda _:self._helper(),
			lambda _:self._version()
		]

		self.__validate()

	def __validate(self) -> None:
		try:
			if(
				not isinstance(self._args, list)
				or not isinstance(self._execs, list)
			):
				raise(ToolInitError(self.name, "Both `_args` and `_execs` must be lists."))

			if(len(self._args) != len(self._execs)):
				raise(ToolInitError(self.name, "`_args` and `_execs` must be of the same length."))

			for i, fn in enumerate(self._execs):
				if(not callable(fn)):
					raise(ToolInitError(self.name, f"Item at index {i} in `_execs` is not callable."))

			if(
				not self.name
				or not self.command
				or not self.path
				or not self.version
			):
				raise(ToolInitError(self.name, "Tool metadata (name, command, path, version) is incomplete."))

		except(ToolInitError):
			raise

		except Exception as e:
			raise(ToolInitError(self.name, f"Unexpected error during tool initialization: {e}"))

	def _run(self, args: list[str], default: Callable = None) -> bool:
		""" Main argument parser and dispatcher.

			Iterates through the tool's defined argument patterns (`_args`),
			and if a match is found in `args`, the corresponding function in `_execs`
			is executed.

			Args:
				args (list[str]): Command-line arguments passed to the tool.

			Returns:
				bool: True if command was launched, False otherwise.

		"""

		try:
			if(len(args) > 1):
				for i, arg in enumerate(self._args):
					if(args[1] in arg[0]):
						self._execs[i](args[2: len(args)])
						return(True)

			if(default):
				default()
				return(True)

			else:
				raise(ValueError(f'Uknown argument "{args[1]}"'))

		except(IndexError):
			print(' To see more of command, type "-h" or "--help" on arguments')

		except(ValueError) as e:
			print(f"{Icons.warn}{e}")

		except(Exception):
			print(f"{Icons.err}{format_exc()}")

		return(False)

	def _helper(self, jumps: list[int] = []) -> None:
		""" Displays formatted usage instructions and argument descriptions.

			This method builds a structured table displaying available CLI arguments
			and their purpose. It includes optional spacing between rows for clarity.

			Typically called in response to a `--help` or `-h` argument.

			Args:
				jumps (list[int], optional): List of indices after which to insert a line break
					for better visual grouping. Defaults to [].

		"""

		jumps = list[int]([ len(self._args)-3 ] + jumps[:])

		table = list[str]([
			"",
			f"Usage: {self.command[0][0]} <argument>\n",
			f"Arguments:{' '*(34-len('Arguments:'))}Descriptions:"
		])

		for i, a in enumerate(self._args):
			l = f"{a[0][0]}, {a[0][1]} {a[0][2]}"
			table.append("".join([
				"".join((f"{l}{' '*(34-len(l))}", f"\n{' '*35}* ".join(a[1]) if(isinstance(a[1], tuple)) else a[1])),
				'\n'*(1 if(i in jumps) else 0)
			]))

		print("\n".join([ f" {t}" for t in table ]))

	def _version(self) -> None:
		""" Displays the tool's name and version in the format: "<name> <version>".

			Typically called in response to a `--version` or `-v` argument.

		"""

		print(f" {self.name} {self.version}")

	def ask(self, msg: str = "Are you sure ?") -> bool:
		""" Ask a CLI question to confirm a choice.

			Args:
				msg (str, optional): The text to display on question.
					Defaults to "Are you sure ?".

			Returns:
				bool: True if it's "yes" or "y", False otherwise.

		"""

		return(bool(input(f"{msg} [y/N] ").lower() in ("y", "yes")))
