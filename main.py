#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
	# --- Importation des dépendances internes ---
	from os import system as shell
	from platform import system
	from sys import argv, version_info

	if(version_info.major < 3):
		raise(SystemError)

	import re

	if(system() == "Linux"): # Dépendances pour Linux
		import readline

	# --- Importation des dépendances internes ---
	from core import INFO, REGEX_ARGS
	from core import Colors, Config, Icons
	from core import helper, launch, sortTools, splash, version

	from tools import TOOLS

except(SystemError):
	print("/!\\ - Program must be run with Python 3")
	exit()

except(ModuleNotFoundError) as e:
	print(e)
	exit()

def arg() -> bool:
	args = dict({
		"prefix": tuple[tuple[tuple[str], str]]((
			(("-l", "--list"), ""),
			(("-t", "--tool"), "<tool>"),
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
		table = list[str]([
			f"{INFO['name']} by {INFO['author']}",
			f"Github: {INFO['github']}\n",
			"Usage: python main.py <argument>\n",
			f"Arguments:{' '*(34-len('Arguments:'))}Descriptions:"
		])

		for i, arg in enumerate(args["prefix"]):
			left = f"{arg[0][0]}, {arg[0][1]} {arg[1]}"
			table.append(f"{left}{' '*(34-len(left))}{args['desc'][i]}{"\n"*(1 if(i in (1, len(args['desc'])-1)) else 0)}")

		print("\n".join([ f" {t}" for t in table ]))

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
	commands = list[tuple]([
		(("set", "s"), "(s)et"),
		(("get", "g"), "(g)et"),
		(("help", "h"), "(h)elp"),
		(("back", "b"), "(b)ack")
	])

	helper(commands)

	while(True):
		prompt = str(input(f"({Colors.green}{INFO['name']}{Colors.end})[{Colors.purple}settings{Colors.end}]> {Colors.cyan}"))
		print(end=Colors.end)

		args = list[str](re.split(REGEX_ARGS, prompt))

		if(args[0] in commands[0][0]):
			try:
				isApplied = bool(False)

				match(args[1]):
					case("colors"):
						isApplied = cfg.setColors(args[2])

					case("encode"):
						isApplied = cfg.setEncoding(args[2])

					case("splash"):
						isApplied = cfg.setSplash(args[2].lower() == "true")
					
					case(_):
						raise(Exception("Uknown property !"))

				print(f'{Icons.info if(isApplied) else Icons.err}{args[2]} {"is" if(isApplied) else "is not"} applied')

			except(IndexError):
				print(f"{Icons.warn}No value was entered !")

			except(Exception) as e:
				print(f"{Icons.err}{e}")

		elif(args[0] in commands[1][0]):
			try:
				output = list[str]([])

				match(args[1]):
					case "colors":
						output.append(cfg.getColors())

					case "encode":
						output.append(cfg.getEncoding())

					case "splash":
						output.append(cfg.getSplash())

					case "all":
						output.append(f"colors: {cfg.getColors()}")
						output.append(f"encode: {cfg.getEncoding()}")
						output.append(f"splash: {cfg.getSplash()}")

					case _:
						output.append(f"{Icons.warn}Uknown value was entered !"[1:-1])

				print("\n".join([ f" {o}" for o in output ]), end="\n"*2)

			except(IndexError):
				print(f"{Icons.warn}No value was entered !")

		elif(args[0] in commands[-2][0]):
			helper(commands)

		elif(args[0] in commands[-1][0]):
			break

		elif(not args[0]):
			pass

		else:
			print(f"{Icons.warn}Uknown command !")

	return(True)

def main(cfg: Config) -> bool:
	commands = list[tuple]([ tool.command for tool in TOOLS ] + [
		(("settings", "s"), "(s)ettings"),
		(("version", "v"), "(v)ersion"),
		(("help", "h"), "(h)elp"),
		(("quit", "q"), "(q)uit")
	])

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
					print(f'{Icons.err}"{command[0][0]}" not implemented !')

		if(not f):
			if(args[0] in commands[-4][0]):
				config(cfg)

			elif(args[0] in commands[-3][0]):
				version()

			elif(args[0] in commands[-2][0]):
				helper(commands)

			elif(args[0] in commands[-1][0]):
				break

			elif((not args[0]) or f):
				pass

			else:
				print(f"{Icons.warn}Uknown command !")

	return(True)

if(__name__ == "__main__"):
	cfg = Config()

	arg() if(len(argv) > 1) else main(cfg)
