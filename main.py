#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.codes import CODE_ERR, CODE_EXIT, CODE_OK

try:
	# --- Importing external dependencies ---
	from os import environ, system as shell
	from os.path import basename
	from platform import system
	from re import split
	from sys import argv, version_info

	if(version_info.major < 3):
		raise(RuntimeError)

	if(system() == "Linux"): # Dependencies for Linux
		import readline

	# --- Importing internal dependencies ---
	from core import helper, launch, sortTools, splash, version
	from core.colors import Colors
	from core.constants import CMD_CLEAR, CMD_PYTHON, INFO, REGEX_ARGS
	from core.config import Config, getConfig, setConfig
	from core.generate import Generate
	from core.icons import Icons

	# --- Importing the tool registry ---
	from tools import TOOLS

except(RuntimeError):
	print("/!\\ - Program must be run with Python 3")
	exit(CODE_ERR)

except(ModuleNotFoundError) as e:
	print("[ ERROR ]: " + e.msg)
	print(f' (?) - Try to run "pip install -r requirements.txt" or "pip install {e.name}" to install missing dependencies')
	exit(CODE_ERR)

def arg(cfg: Config) -> int:
	""" Launch method in argument mode

		Args:
			cfg (Config): the user config instance

		Returns:
			int: the code of the execution
			- CODE_OK: when the execution is successful
			- CODE_ERR: when an error occurs

	"""

	__args = dict({
		"prefix": tuple[tuple[tuple[str], str]]((
			(("-g", "--generate"), ""),
			(("-l", "--list"), ""),
			(("-s", "--set"), "<prop> <value>"),
			(("-t", "--tool"), "<tool>"),
			(("-h", "--help"), ""),
			(("-D", "--debug"), ""),
			(("-v", "--version"), "")
		)),
		"desc": tuple[str | tuple[str]]((
			"Generate a tool with interactive inputs",
			"List all registered python tools",
			("Apply new configuration value on property", "prop: colors|encode|splash"),
			"Start a selected tools by name",
			"Show the helper commands menu",
			"Launch the script in debug mod",
			"Show version of script"
		))
	})

	try:
		if(argv[1] in __args["prefix"][0][0]): # -g, --generate
			Generate()

		elif(argv[1] in __args["prefix"][1][0]): # -l, --list
			sortTools(TOOLS)

		elif(argv[1] in __args["prefix"][2][0]): # -s, --set
			setConfig(cfg, argv[2], argv[3])

		elif(argv[1] in __args["prefix"][3][0]): # -t, --tool
			for tool in TOOLS:
				if(argv[2] in tool.command[0]):
					launch(tool, argv[2:len(argv)])

		elif(argv[1] in __args["prefix"][-3][0]): # -h, --help
			__table = list[str]([
				f"{INFO['name']} by {INFO['author']}",
				f"Github: {INFO['github']}\n",
				f"Usage: python {basename(__file__)} <argument>\n",
				f"{'Arguments':<{34}}Descriptions:"
			])

			for i, arg in enumerate(__args["prefix"]):
				__left = f"{arg[0][0]}, {arg[0][1]} {arg[1]}"
				__desc = f"\n{' '*35}* ".join(__args['desc'][i]) if(isinstance(__args['desc'][i], tuple)) else __args['desc'][i]
				__table.append("".join([
					f"{__left:<{34}}{__desc}",
					"\n"*(1 if(i in (len(__args['desc'])-4, len(__args['desc'])-1)) else 0)
				]))

			print("\n".join([ f" {t}" for t in __table ]))

		elif(argv[1] in __args["prefix"][-2][0]): # -D, --debug
			environ["TM_DEBUG"] = "1"
			__cmd = str(f"{CMD_PYTHON} -B {__file__}")

			while(True):
				shell(CMD_CLEAR)
				print(f"{Icons.info}Debug mode enabled, running command: {__cmd}")
				shell(__cmd)
				input(f"{Icons.info}Press any keys to continue...")

		elif(argv[1] in __args["prefix"][-1][0]): # -v, --version
			version()

	except(IndexError, KeyError):
		print(f"{Icons.warn}Insufficient arguments !")
		return(CODE_ERR)

	return(CODE_OK)

def config(cfg: Config) -> bool:
	""" Config function to apply user settings

		Args:
			cfg (Config): the user config instance

		Returns:
			bool: True value when exiting

	"""

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

		try:
			if(__args[0] in __cmds[0][0]): # set, s
				setConfig(cfg, __args[1], __args[2])

			elif(__args[0] in __cmds[1][0]): # get, g
				getConfig(cfg, __args[1])

			elif(__args[0] in __cmds[-2][0]): # help, h
				helper(__cmds)

			elif(__args[0] in __cmds[-1][0]): # back, b
				break

			elif(not __args[0]):
				pass

			else:
				print(f"{Icons.warn}Uknown command !")

		except(IndexError):
			print(f"{Icons.warn}No value was entered !")

		except(Exception) as e:
			print(f"{Icons.err}{e}")

	return(True)

def main(cfg: Config) -> int:
	""" Main launch method

		Args:
			cfg (Config): the user config instance

		Returns:
			int: the code of the execution
			- CODE_OK: when the execution is successful

	"""

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
				__f = bool(True)
				launch(TOOLS[i], __args)
				break

		if(not __f):
			if(__args[0] in __cmds[-4][0]): # settings, s
				config(cfg)

			elif(__args[0] in __cmds[-3][0]): # version, v
				version()

			elif(__args[0] in __cmds[-2][0]): # help, h
				helper(__cmds)

			elif(__args[0] in __cmds[-1][0]): # quit, q
				break

			elif((not __args[0]) or __f):
				pass

			else:
				print(f"{Icons.warn}Uknown command !")

	return(CODE_OK)

if(__name__ == "__main__"):
	try:
		__cfg = Config()
		exit(arg(__cfg) if(len(argv) > 1) else main(__cfg))

	except(KeyboardInterrupt):
		print(f"{Icons.info}Exiting...")
		exit(CODE_EXIT)
