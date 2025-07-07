#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/wifi.py

from subprocess import check_output as prompt

from core.tool import Tool

class Wifi(Tool):
	""" Wifi tool to retrieve saved wifi passwords
	"""

	command	= (("wifi", "wi"), "(wi)fi")
	name	= "Wifi"
	path	= __file__
	version	= "0.1a"

	def __init__(self, args: list[str]):
		self._args	= [
			(("-p", "--password", ""), "Get the password of the registered wifi network"),
		]

		self._execs = [
			lambda x:self._getWifiPasswords()
		]

		super().__init__()
		self._run(args)

	def _getWifiPasswords(self) -> None:
		__cmd	= prompt(["netsh", "wlan", "show", "profiles"]).decode("ansi").split("\n")
		__wifis	= [ line.split(":")[1][1:-1] for line in __cmd if("Profil Tous les utilisateurs" in line) ]

		_m		= 1
		_s		= 20
		__table	= [ f"{' '*_m}*  {'Name':<{_s}}Password", "" ]

		for i, wifi in enumerate(__wifis, 1):
			__cmd = prompt(["netsh", "wlan", "show", "profiles", wifi, "key=clear"]).decode("ansi").split("\n")
			__password = [ line.split(":")[1][1:-1] for line in __cmd if("Contenu de la cl" in line) ]

			try:
				__table.append(f"{' '*_m}{i}. {wifi:<{_s}}{__password[0]}")

			except(Exception):
				__table.append(f"{' '*_m}{i}. {wifi:<{_s}}-")

		print("\n".join(__table))
