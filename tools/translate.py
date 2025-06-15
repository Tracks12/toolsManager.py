#!/bin/python3
# -*- coding: utf-8 -*-

from os.path import abspath, dirname

from core.icons import Icons
from core.tool import Tool

class Translate(Tool):
	command	= (("translate", "tr"), "(tr)anslate")
	name	= "Translate"
	path	= __file__
	version	= "0.1a"

	__path = str(abspath(f"{dirname(abspath(__file__))}/../{name}"))

	def __init__(self, args: list[str]):
		super().__init__()

		self.__setup()

		self._args = [] + self._args[:]
		self._execs = [] + self._execs[:]

		self._run(args)

	def __setup(self) -> None:
		pass