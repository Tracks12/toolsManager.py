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

REGEX_ARGS = str("\\s(?=(?:[^\"'`]*[\"'`][^\"'`]*[\"'`])*[^\"'`]*$)")

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
	print(f"{' '*1}*  Name{' '*(12-len('Name'))}Path")
	for i, tool in enumerate(tools, start=1):
		print(f"{' '*(2-len(str(i)))}{i}. {tool.name}{' '*(12-len(tool.name))}{tool.path}", end="\n"*(2 if(i == len(tools)) else 1))

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
