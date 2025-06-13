#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Base class for tool objects.

	Defines the `Tool` class which serves as the foundational object for
	creating individual tools compatible with the tools registry.
	Provides core functionalities and interface methods to ensure
	integration with the overall tool management system.

"""

from traceback import format_exc

from core.icons import Icons

class Tool:
	command	: tuple[tuple[str, str], str]	= (("", ""), "")
	name	: str							= ""
	path	: str							= ""
	version	: str							= ""

	_args	: list[tuple[tuple[str, str, str], str]]	= [
		(("-h", "--help", ""), "Show the helper commands menu"),
		(("-v", "--version", ""), "Show version of tool")
	]

	def __init__(self):
		self._execs = [
			lambda x:self._helper(),
			lambda x:self._version()
		]

	def _run(self, args: list[str]) -> bool:
		try:
			for i, a in enumerate(self._args):
				if(args[1] in a[0]):
					self._execs[i](args[2: len(args)])
					return(True)

			raise ValueError(f'Uknown argument "{args[1]}"')

		except IndexError:
			print(' To see more of command type "-h" or "--help" on arguments')

		except ValueError as e:
			print(f"{Icons.warn}{e}")

		except Exception:
			print(f"{Icons.err}{format_exc()}")

		return(False)

	def _helper(self, jumps: list[int] = []) -> None:
		jumps = list[int]([ len(self._args)-3 ] + jumps[:])

		table = list[str]([
			"",
			f"Usage: {self.command[0][0]} <argument>\n",
			f"Arguments:{' '*(34-len('Arguments:'))}Descriptions:"
		])

		for i, a in enumerate(self._args):
			l = f"{a[0][0]}, {a[0][1]} {a[0][2]}"
			table.append(f"{l}{' '*(34-len(l))}{a[1]}{"\n"*(1 if(i in jumps) else 0)}")

		print("\n".join([ f" {t}" for t in table ]))

	def _version(self) -> None:
		print(f" {self.name} {self.version}")