#!/bin/python3
# -*- coding: utf-8 -*-

from os import system as shell

from core.tool import Tool

class Shell(Tool):
	command	= (("shell", "sh"), "(sh)ell")
	name	= "Shell"
	path = __file__
	version	= "0.1a"

	_args	= [
		(("-c", "--command", ""), "Run a bash command")
	] + Tool._args[:]

	def __init__(self, args: list[str]):
		Tool.__init__(self)

		self._execs = [
			lambda x:self._exec(x)
		] + self._execs[:]

		self._run(args)

	def _exec(self, args: list[str]) -> None:
		shell(" ".join(args))
