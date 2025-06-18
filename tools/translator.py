#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/translator.py

from core.tool import Tool

class Translator(Tool):
	""" Say hello to the user
	"""

	command	= (("translator", "tr"), "(tr)anslator")
	name	= "Translator"
	path	= __file__
	version	= "0.1a"

	def __init__(self, args: list[str]):
		super().__init__()

		self._args	= [
			(("-s", "--say-hello", ""), "Say a hello world")
		] + self._args[:]

		self._execs = [
			lambda x:self._sayHello(x)
		] + self._execs[:]

		self._run(args)

	def _sayHello(self, args: list[str]) -> bool:
		print(f"Hello world :D")
		return(True)
