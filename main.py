#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
	# --- Importation des dépendances internes ---
	from os import system as shell
	from platform import system
	from re import split
	from sys import argv, version_info

	if(version_info.major < 3):
		raise(RuntimeError)

	if(system() == "Linux"): # Dépendances pour Linux
		import readline

	# --- Importation des dépendances internes ---
	from core import INFO, REGEX_ARGS
	from core import helper, launch, sortTools, splash, version
	from core.colors import Colors
	from core.icons import Icons
	from core.config import Config, getConfig, setConfig

	from tools import TOOLS

except(RuntimeError) as e:
	print("/!\\ - Program must be run with Python 3")
	exit()

except(ModuleNotFoundError) as e:
	print("[ ERROR ]: " + e.msg)
	exit()

def arg(cfg: Config) -> bool:
	__args = dict({
		"prefix": tuple[tuple[tuple[str], str]]((
			(("-l", "--list"), ""),
			(("-s", "--set"), "<prop> <value>"),
			(("-t", "--tool"), "<tool>"),
			(("-h", "--help"), ""),
			(("-D", "--debug"), ""),
			(("-v", "--version"), "")
		)),
		"desc": tuple[str | tuple[str]]((
			"List all registered python tools",
			("Apply new configuration value on property", "prop: colors|encode|splash"),
			"Start a selected tools by name",
			"Show the helper commands menu",
			"Launch the script in debug mod",
			"Show version of script"
		))
	})

	try:
		if(argv[1] in __args["prefix"][0][0]): # -l, --list
			sortTools(TOOLS)

		elif(argv[1] in __args["prefix"][1][0]): # -s, --set
			setConfig(cfg, argv[2], argv[3])

		elif(argv[1] in __args["prefix"][2][0]): # -t, --tool
			for tool in TOOLS:
				if(argv[2] in tool.command[0]):
					launch(tool, argv[2:len(argv)])

		elif(argv[1] in __args["prefix"][-3][0]): # -h, --help
			__table = list[str]([
				f"{INFO['name']} by {INFO['author']}",
				f"Github: {INFO['github']}\n",
				"Usage: python main.py <argument>\n",
				f"Arguments:{' '*(34-len('Arguments:'))}Descriptions:"
			])

			for i, arg in enumerate(__args["prefix"]):
				__left = f"{arg[0][0]}, {arg[0][1]} {arg[1]}"
				__desc = f"\n{' '*35}* ".join(__args['desc'][i]) if(isinstance(__args['desc'][i], tuple)) else __args['desc'][i]
				__table.append(f"{__left}{' '*(34-len(__left))}{__desc}{"\n"*(1 if(i in (2, len(__args['desc'])-1)) else 0)}")

			print("\n".join([ f" {t}" for t in __table ]))

		elif(argv[1] in __args["prefix"][-2][0]): # -D, --debug
			__isLinux = bool(system() == "Linux")

			while(True):
				shell("clear" if(__isLinux) else "cls")
				print(f"{Icons.info}Lanched in debug mod")
				shell(f"python{'3' if(__isLinux) else ''} main.py")
				input(f"{Icons.info}Press any keys to continue...")

		elif(argv[1] in __args["prefix"][-1][0]): # -v, --version
			version()

	except(IndexError, KeyError):
		print(f"{Icons.warn}Insufficient arguments !")
		return(False)

	return(True)

def config(cfg: Config) -> bool:
	__cmds = list[tuple]([
		(("set", "s"), "(s)et"),
		(("get", "g"), "(g)et"),
		(("help", "h"), "(h)elp"),
		(("back", "b"), "(b)ack")
	])

	helper(__cmds)

	while(True):
		prompt = str(input(f"({Colors.green}{INFO['name']}{Colors.end})[{Colors.purple}settings{Colors.end}]> {Colors.cyan}"))
		print(end=Colors.end)

		__args = list[str](split(REGEX_ARGS, prompt))

		if(__args[0] in __cmds[0][0]):
			try:
				setConfig(cfg, __args[1], __args[2])

			except(IndexError):
				print(f"{Icons.warn}No value was entered !")

			except(Exception) as e:
				print(f"{Icons.err}{e}")

		elif(__args[0] in __cmds[1][0]):
			try:
				getConfig(cfg, __args[1])

			except(IndexError):
				print(f"{Icons.warn}No value was entered !")

		elif(__args[0] in __cmds[-2][0]):
			helper(__cmds)

		elif(__args[0] in __cmds[-1][0]):
			break

		elif(not __args[0]):
			pass

		else:
			print(f"{Icons.warn}Uknown command !")

	return(True)

def main(cfg: Config) -> bool:
	__cmds = list[tuple]([ tool.command for tool in TOOLS ] + [
		(("settings", "s"), "(s)ettings"),
		(("version", "v"), "(v)ersion"),
		(("help", "h"), "(h)elp"),
		(("quit", "q"), "(q)uit")
	])

	if(cfg.getSplash()):
		splash()

	helper(__cmds)

	while(True):
		prompt = str(input(f"({Colors.green}{INFO['name']}{Colors.end})> {Colors.cyan}"))
		print(end=Colors.end)

		__args = list[str](split(REGEX_ARGS, prompt))
		__f = bool(False)

		for i, command in enumerate(__cmds[0:len(__cmds)-4]):
			if(__args[0] in command[0]):
				try:
					__f = bool(True)
					launch(TOOLS[i], __args)
					break

				except:
					print(f'{Icons.err}"{command[0][0]}" not implemented !')

		if(not __f):
			if(__args[0] in __cmds[-4][0]):
				config(cfg)

			elif(__args[0] in __cmds[-3][0]):
				version()

			elif(__args[0] in __cmds[-2][0]):
				helper(__cmds)

			elif(__args[0] in __cmds[-1][0]):
				break

			elif((not __args[0]) or __f):
				pass

			else:
				print(f"{Icons.warn}Uknown command !")

	return(True)

if(__name__ == "__main__"):
	__cfg = Config()
	arg(__cfg) if(len(argv) > 1) else main(__cfg)
