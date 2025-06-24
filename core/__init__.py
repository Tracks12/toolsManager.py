#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Package initialization for `core`.

	This module initializes the `core` package by defining essential functions and variables,
	such as `get_config()` for loading configurations and `initialize_logger()` for setting up logging.
	It ensures that the core components are ready for use when the package is imported.

	Constants:
	- INFO: Contains application information such as version, git commit hash, and other metadata.
	- REGEX_ARGS: A regular expression pattern used to parse and split argument strings into lists.
	- UNITS: Units of measurement for bytes, including b, Kb, Mb, Gb, Tb, etc., to facilitate size conversions.

"""

from time import sleep
from traceback import format_exc

from core.colors import Colors
from core.config import ACCEPT_ENCODING, Config, getConfig, setConfig
from core.generate import Generate
from core.icons import Icons
from core.tool import Tool

INFO = dict[str, str]({
	"author": "Florian Cardinal",
	"github": "https://github.com/Tracks12/toolsManager.py",
	"name": "toolsManager.py",
	"version": "0.1",
})
""" Contains application information such as version, git commit hash, and other metadata
"""

REGEX_ARGS = str("\\s(?=(?:[^\"'`]*[\"'`][^\"'`]*[\"'`])*[^\"'`]*$)")
""" A regular expression pattern used to parse and split argument strings into lists
"""

UNITS = tuple[str](("b", "Kb", "Mb", "Gb", "Tb"))
""" Units of measurement for bytes, including b, Kb, Mb, Gb, Tb, etc., to facilitate size conversions
"""

def helper(commands: tuple) -> None:
	colors	= tuple[str]((Colors.cyan, Colors.yellow, Colors.red))
	screen	= list[str]([ "List of commands:\n" ])

	for i, command in enumerate(commands):
		c	= int(1 if(i in range((len(commands)-4), (len(commands)-1))) else 0)
		c	= int(2 if(i in range((len(commands)-1), (len(commands)))) else c)
		sep	= str('\n' if(i in (len(commands)-5, len(commands)-2)) else '')

		screen.append(f"{colors[c]}{command[1]}{Colors.end}{sep}")

	print(("\n").join([ f" {s}" for s in screen ]), end="\n\n")

def launch(tool: Tool, args: list[str]) -> bool:
	try:
		print(f'{Icons.play}Starting "{tool.name}" ...')
		tool(args)

	except(Exception):
		print(f"{Icons.err}{format_exc()}")

	finally:
		print()
		return(True)

def sortTools(tools: list[Tool]) -> list[Tool]:
	table = list[str]([ f" *  Name{' '*(14-len('Name'))}Version{' '*(9-len('Version'))}Command{' '*(16-len('Command'))}Path" ])
	for i, tool in enumerate(tools, start=1):
		table.append("".join([
			f"{' '*(2-len(str(i)))}{Colors.green}{i}{Colors.end}.",
			f"{' '*1}{tool.name}",
			f"{' '*(14-len(tool.name))}{Colors.purple}{tool.version}{Colors.end}"
			f"{' '*(9-len(tool.version))}{Colors.cyan}{tool.command[1]}{Colors.end}"
			f"{' '*(16-len(tool.command[1]))}{Colors.yellow}{tool.path}{Colors.end}"
		]))

	_ = "\n".join([ f" {t}" for t in table ])
	print(f"\n{_}", end="\n"*2)
	return(tools)

def splash(spacing: int = 2) -> None:
	for i, row in enumerate((
		" {}_              _    __  __{}".format(Colors.yellow+Colors.bold, Colors.end),
		"{}| |            | |  |  \\/  |{}".format(Colors.yellow+Colors.bold, Colors.end),
		"{}| |_ ___   ___ | | _|_\\  / | __ _ _ __   __ _  __ _  ___ _ __{}".format(Colors.yellow+Colors.bold, Colors.end),
		"{}| __/ _ \\ / _ \\| |/ _/|\\/| |/ _` | '_ \\ / _` |/ _` |/ _ \\ '__|{}".format(Colors.yellow+Colors.bold, Colors.end),
		"{}| || (_) | (_) | _\\ \\ |  | | (_| | | | | (_| | (_| |  __/ |{}".format(Colors.yellow+Colors.bold, Colors.end),
		" {}\\__\\___/ \\___/|/___/_|  |_|\\__,_|_| |_|\\__,_|\\__, |\\___|_|{}".format(Colors.yellow+Colors.bold, Colors.end),
		"   {}version: {}{}                               {}|___/{}".format(Colors.purple, INFO["version"], Colors.end, Colors.yellow+Colors.bold, Colors.end),
	)):
		print(f"{' '*spacing}{row}", end="\n"*(2 if(i == 6) else 1))
		sleep(.025)

def stringSize(size: int) -> str:
	size = [size, UNITS[0]]

	for i in range(1, len(UNITS)):
		size[0] /= 1000
		size[1] = UNITS[i]
		if(size[0] < 1024):
			break

	return(f"{round(size[0], 2)} {size[1]}")

def version() -> dict[str, str]:
	print(f" {INFO['name']} {INFO['version']}", end="\n"*2)
	return(INFO)
