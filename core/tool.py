#!/bin/python3
# -*- coding: utf-8 -*-

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
			print(f"{Icons.warn}{format_exc()}")

		return(False)

	def _helper(self, jumps: list[int] = []) -> None:
		jumps = [ len(self._args)-3 ] + jumps[:]

		print(f" Launching: {self.command[0][0]} <arg>", end="\n"*2)
		print(f" Arguments:")

		for i, a in enumerate(self._args):
			l = f"{a[0][0]}, {a[0][1]} {a[0][2]}"
			print(f" {l}{' '*(30-len(l))}{a[1]}", end="\n"*2 if(i in jumps) else "\n")

	def _version(self) -> None:
		print(f" {self.name} {self.version}")