#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/wifi.py

from subprocess import CalledProcessError, check_output as prompt

from core.colors import Colors
from core.icons import Icons
from core.tool import Tool

class Wifi(Tool):
	""" Wifi tool to retrieve saved wifi passwords
	"""

	command	= (("wifi", "wi"), "(wi)fi")
	name	= "Wifi"
	path	= __file__
	version	= "1.0"

	def __init__(self, args: list[str]):
		self._args	= [
			(("-p", "--password", "*"), ("Get the password of the registered wifi network", "opt: -e to specify the encoding")),
		]

		self._execs = [
			lambda x:self._getWifiPasswords(x)
		]

		super().__init__()
		self._run(args, lambda:self._helper())

	def _getWifiPasswords(self, args: list[str]) -> None:
		try:
			encode	= str("ansi")
			if("-e" in args):
				encode = args[args.index("-e")+1] if(len(args) > args.index("-e")+1) else encode

			__cmd	= prompt(["netsh", "wlan", "show", "profiles"]).decode(encode).split("\n")
			__wifis	= list[str]([ line.split(":")[1][1:-1] for line in __cmd if("Profil Tous les utilisateurs" in line) ])
			__cmd	= prompt(["netsh", "wlan", "show", "interfaces"]).decode(encode).split("\n")
			__crnt	= list[str]([ line.split(":")[1][1:-2] for line in __cmd if("Profil" in line) ])

			_m		= int(len(str(len(__wifis))) + 1)
			_s		= int(20)
			table	= list[str]([ f"\n{' '*(_m-1)}*  {'SSID':<{_s}}Password" ])

			for i, wifi in enumerate(__wifis, 1):
				__cmd = prompt(["netsh", "wlan", "show", "profiles", wifi, "key=clear"]).decode(encode).split("\n")
				__password = list[str]([ line.split(":")[1][1:-1] for line in __cmd if("Contenu de la cl" in line) ])

				table.append("".join([
					f"{' '*(_m-len(str(i)))}{Colors.cyan}{i}{Colors.end}. ",
					f"{Colors.purple}{wifi:<{_s}}{Colors.end}",
					f"{Colors.yellow}{(__password[0] if(len(__password)) else '-'):<{_s*2}}{Colors.end}",
					f"[ {Colors.green}CURRENT{Colors.end} ]" if wifi in __crnt else ""
				]))

			print("\n".join(table))

		except(CalledProcessError) as e:
			print(f"{Icons.err}{e}")
