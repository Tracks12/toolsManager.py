#!/bin/python3
# -*- coding: utf-8 -*-

from os import system as shell
from platform import system
from sys import argv, version_info

import re

if(system() == "Linux"):
	import readline

if(version_info.major < 3):
	print("/!\\ - Program must be run with Python 3")
	exit()

# Importation des dépendances internes
from core import INFO, REGEX_ARGS, Colors, Config, Icons, launch, sortTools, splash, version
from tools import TOOLS

def arg() -> bool:
	args = dict({
		"prefix": tuple[tuple[tuple[str], str]]((
			(("-l", "--list"), ""),
			(("-t", "--tool"), "<toolName>"),
			(("-h", "--help"), ""),
			(("-D", "--debug"), ""),
			(("-v", "--version"), "")
		)),
		"desc": tuple[str]((
			"List all registered python tools",
			"Start a selected tools by name",
			"Show the helper commands menu",
			"Launch the script in debug mod",
			"Show version of script"
		))
	})

	if(argv[1] in args["prefix"][0][0]): # -l, --list
		sortTools(TOOLS)

	elif(argv[1] in args["prefix"][1][0]): # -t, --tool
		for tool in TOOLS:
			if(argv[2] in tool.command[0]):
				launch(tool, argv[2:len(argv)])

	elif(argv[1] in args["prefix"][-3][0]): # -h, --help
		print(f" {INFO['name']}")
		print(f" Launching: python main.py <arg>", end="\n"*2)
		print(f" Arguments:")

		for i, arg in enumerate(args["prefix"]):
			left = f"{arg[0][0]}, {arg[0][1]} {arg[1]}"
			print(f" {left}{' '*(30-len(left))}{args['desc'][i]}", end="\n"*(2 if(i in (1, len(args['desc'])-1)) else 1))

	elif(argv[1] in args["prefix"][-2][0]): # -D, --debug
		isLinux = bool(system() == "Linux")

		while(True):
			shell("clear" if(isLinux) else "cls")
			print(f"{Icons.info}Lanched in debug mod")
			shell(f"python{'3' if(isLinux) else ''} main.py")
			input(f"{Icons.info}Press any keys to continue...")

	elif(argv[1] in args["prefix"][-1][0]): # -v, --version
		version()

	return(True)

def config(cfg: Config) -> bool:
	while(True):
		prompt = str(input(f"({Colors.green}{INFO['name']}{Colors.end})[{Colors.purple}settings{Colors.end}]> {Colors.cyan}"))
		print(end=Colors.end)

		args = list[str](re.split(REGEX_ARGS, prompt))

		if(args[0] in ("set", "s")):
			try:
				isApplied = bool(False)

				match(args[1]):
					case "encode":
						isApplied = cfg.setEncoding(args[2])

					case "splash":
						isApplied = cfg.setSplash(args[2].lower() == "true")

				print(f'{Icons.info if(isApplied) else Icons.warn}{args[2]} {"is" if(isApplied) else "is not"} applied')

			except IndexError:
					print(f"{Icons.warn}No value was entered !")

			except Exception as e:
				print(f"{Icons.warn}{e}")

		elif(args[0] in ("get", "g")):
			match(args[1]):
				case "encode":
					print(cfg.getEncoding())

				case "splash":
					print(cfg.getSplash())

		elif(args[0] in ("quit", "q")):
			break

		elif(args[0] == ""):
			pass

		else:
			print(f"{Icons.warn}Uknown command !")

	return(True)

def main(cfg: Config) -> bool:
	def helper(commands: tuple) -> None:
		colors = tuple[str]((Colors.cyan, Colors.yellow, Colors.red))
		screen = list[str]([ " List of commands:\n" ])

		for i, command in enumerate(commands):
			c = int(1 if(i in range((len(commands)-4), (len(commands)-1))) else 0)
			c = int(2 if(i in range((len(commands)-1), (len(commands)))) else c)
			sep = str('\n' if(i in (len(commands)-5, len(commands)-2)) else '')

			command = str(f" {colors[c]}{command[1]}{Colors.end}{sep}")

			screen.append(command)

		print(("\n").join(screen), end="\n\n")

	commands = list[tuple]([
		(("settings", "set"), "(set)tings"),
		(("version", "ver"), "(ver)sion"),
		(("help", "h"), "(h)elp"),
		(("quit", "q"), "(q)uit")
	])

	TOOLS.reverse()
	for tool in TOOLS:
		commands = [tool.command] + commands[:]

	TOOLS.reverse()

	if(cfg.getSplash()):
		splash()

	helper(commands)

	while(True):
		prompt = str(input(f"({Colors.green}{INFO['name']}{Colors.end})> {Colors.cyan}"))
		print(end=Colors.end)

		args = list[str](re.split(REGEX_ARGS, prompt))
		f = bool(False)

		for i, command in enumerate(commands[0:len(commands)-4]):
			if(args[0] in command[0]):
				try:
					f = bool(True)
					launch(TOOLS[i], args)
					break

				except:
					print(f'{Icons.warn}"{command[0][0]}" not implemented !')

		if(args[0] in commands[-4][0]):
			config(cfg)

		elif(args[0] in commands[-3][0]):
			version()

		elif(args[0] in commands[-2][0]):
			helper(commands)

		elif(args[0] in commands[-1][0]):
			break

		elif(args[0] == "" or f):
			pass

		else:
			print(f"{Icons.warn}Uknown command !")

	return(True)

if(__name__ == "__main__"):
	cfg = Config()

	arg() if(len(argv) > 1) else main(cfg)
