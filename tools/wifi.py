#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/wifi.py

from core.tool import Tool

class Wifi(Tool):
	""" Say hello to the user
	"""

	command	= (("wifi", "wi"), "(wi)fi")
	name	= "Wifi"
	path	= __file__
	version	= "0.1a"

	def __init__(self, args: list[str]):
		self._args	= [
			(("-s", "--say-hello", ""), "Say a hello world")
		]

		self._execs = [
			lambda x:self._sayHello(x)
		]

		super().__init__()
		self._run(args)

	def _sayHello(self, args: list[str]) -> bool:
		print(f"Hello world :D")
		return(True)
