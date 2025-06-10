#!/bin/python3
# -*- coding: utf-8 -*-

from time import sleep
from traceback import format_exc

from core.colors import Colors
from core.config import Config
from core.icons import Icons
from core.tool import Tool

INFO = dict[str, str]({
	"name": "toolsManager.py",
	"version": "0.1"
})

REGEX_ARGS	= str("\\s(?=(?:[^\"'`]*[\"'`][^\"'`]*[\"'`])*[^\"'`]*$)")
UNITS		= tuple[str](("o", "ko", "Mo", "Go", "To"))

def helper(commands: tuple) -> None:
	colors	= tuple[str]((Colors.cyan, Colors.yellow, Colors.red))
	screen	= list[str]([ " List of commands:\n" ])

	for i, command in enumerate(commands):
		c	= int(1 if(i in range((len(commands)-4), (len(commands)-1))) else 0)
		c	= int(2 if(i in range((len(commands)-1), (len(commands)))) else c)
		sep	= str('\n' if(i in (len(commands)-5, len(commands)-2)) else '')

		command = str(f" {colors[c]}{command[1]}{Colors.end}{sep}")

		screen.append(command)

	print(("\n").join(screen), end="\n\n")

def launch(tool: Tool, args: list[str]) -> bool:
	try:
		print(f'{Icons.play}Starting "{tool.name}" ...')
		tool(args)
	
	except Exception:
		print(f"{Icons.warn}{format_exc()}")

	finally:
		print()
		return(True)

def sortTools(tools: list[Tool]) -> list[Tool]:
	print(f"\n {' '*1}*  Name{' '*(12-len('Name'))}Command{' '*(16-len('Command'))}Path")
	for i, tool in enumerate(tools, start=1):
		print(f" {' '*(2-len(str(i)))}{i}. {tool.name}{' '*(12-len(tool.name))}{tool.command[1]}{' '*(16-len(tool.command[1]))}{tool.path}", end="\n"*(2 if(i == len(tools)) else 1))

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

def version() -> dict[str, str]:
	print(f" {INFO['name']} {INFO['version']}", end="\n"*2)
	return(INFO)
