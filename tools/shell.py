#!/bin/python3
# -*- coding: utf-8 -*-

from os import system as shell
from traceback import format_exc

from core.icons import Icons
from core.tool import Tool

class Shell(Tool):
	command	= (("shell", "sh"), "(sh)ell")
	name	= "Shell"
	path	= __file__
	version	= "0.1a"

	def __init__(self, args: list[str]):
		super().__init__()

		self._args = [
			(("-c", "--command", ""), "Run a bash command")
		] + self._args[:]

		self._execs = [
			lambda x:self._exec(x)
		] + self._execs[:]

		self._run(args)

	def _run(self, args: list[str]) -> bool:
		try:
			for i, a in enumerate(self._args):
				if(args[1] in a[0]):
					self._execs[i](args[2: len(args)])
					return(True)

			self._exec(args[1: len(args)])

		except(IndexError):
			print(' To see more of command type "-h" or "--help" on arguments')

		except(ValueError) as e:
			print(f"{Icons.warn}{e}")

		except(Exception):
			print(f"{Icons.err}{format_exc()}")

		return(False)

	def _exec(self, args: list[str]) -> None:
		shell(" ".join(args))
