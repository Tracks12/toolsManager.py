#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import listdir, mkdir
from os.path import abspath, basename, isdir
from shutil import rmtree
from sys import argv

from core.constants import EXTRACT_PATH, LIBS_PATH
from core.rarfile import RarFile

LIBS_REGISTRY = list[str]([
	"wslbuilder"
])

def ask(msg: str = "Are you sure ?") -> bool:
	return(bool((input(f"{msg} [y/N] ").lower() or "n") == "y"))

def clearLibs(paths: list[str]) -> None:
	for p in paths:
		try:
			rmtree(p)

		except(FileNotFoundError):
			pass

def install(registry: list[str]) -> bool:
	try:
		mkdir(EXTRACT_PATH)

	except(FileExistsError):
		pass

	__checkExists	= [ lib for lib in listdir(EXTRACT_PATH) if isdir(abspath(f"{EXTRACT_PATH}/{lib}")) if lib in registry ]
	__extractsPath	= [ abspath(f"{EXTRACT_PATH}/{m}") for m in registry ]
	__rarPaths		= [ abspath(f"{LIBS_PATH}/{m}.rar") for m in registry ]

	if(len(__checkExists)):
		for ce in __checkExists:
			print(f" (-) {ce}")

		if(not ask("Did you want to uninstall these packages ?")):
			print("[ CANCEL ]: Abort reinstallation !")
			return(False)

		print("[ INFO ]: Clearing installation ...")
		clearLibs(__extractsPath)
		print("[ INFO ]: Installation cleared !")

	for i, rp in enumerate(__rarPaths):
		try:
			with RarFile(rp) as __rf:
				print(f" ( ) Unpacking {rp} ... [{i}/{len(__rarPaths)}]", end="\r")
				__rf.extractall(EXTRACT_PATH)
				print(f" (*) {rp} Unpacked{' '*16}")

		except(FileNotFoundError):
			print(f"[ ERROR ]: {rp} not found{' '*(16+len(rp))}")
			pass

		except(Exception) as e:
			clearLibs(__extractsPath)
			print(f"\n[ ERROR ]: {e}{' '*(16+len(rp))}")
			return(False)

	print("[ OK ]: Installation finished !")
	return(True)

def uninstall(registry: list[str]) -> bool:
	__checkExists	= [ lib for lib in listdir(EXTRACT_PATH) if isdir(abspath(f"{EXTRACT_PATH}/{lib}")) if lib in registry ]
	__libsPath		= [ abspath(f"{EXTRACT_PATH}/{m}") for m in registry ]

	if(len(__checkExists)):
		for ce in __checkExists:
			print(f" (-) {ce}")

		if(not ask("Did you want to uninstall these packages ?")):
			print("[ CANCEL ]: Abort uninstallation !")
			return(False)

		print("[ INFO ]: Uninstallation finished !")
		clearLibs(__libsPath)

	return(True)

def arg() -> bool:
	__args = dict({
		"prefix": tuple[tuple[tuple[str], str]]((
			(("-i", "--install"), "<lib>"),
			(("-p", "--purge"), ""),
			(("-r", "--registry"), ""),
			(("-u", "--uninstall"), "<lib>"),
			(("-h", "--help"), "")
		)),
		"desc": tuple[str | tuple[str]]((
			"Install a dependency",
			"Purge all dependencies",
			"Show libs registry",
			"Uninstall a dependency",
			"Show the helper commands menu"
		))
	})

	try:
		if(argv[1] in __args["prefix"][0][0]): # -i, --install
			install([ argv[2] ])

		elif(argv[1] in __args["prefix"][1][0]): # -p, --purge
			uninstall(LIBS_REGISTRY)

		elif(argv[1] in __args["prefix"][2][0]): # -r, --registry
			print("[ INFO ]: Listing the package registry:")
			for i, lib in enumerate(LIBS_REGISTRY, 1):
				print(f" {' '*(3-len(str(i)))}{i}. {lib} -> {abspath(f'{LIBS_PATH}/{lib}.rar')}")
		
		elif(argv[1] in __args["prefix"][3][0]): # -u, --uninstall
			uninstall([ argv[2] ])

		elif(argv[1] in __args["prefix"][-1][0]): # -h, --help
			__table = list[str]([
				f"Usage: python {basename(__file__)} <argument>\n",
				f"Arguments:{' '*(34-len('Arguments:'))}Descriptions:"
			])

			for i, arg in enumerate(__args["prefix"]):
				__left = f"{arg[0][0]}, {arg[0][1]} {arg[1]}"
				__desc = f"\n{' '*35}* ".join(__args['desc'][i]) if(isinstance(__args['desc'][i], tuple)) else __args['desc'][i]
				__table.append("".join([
					f"{__left}{' '*(34-len(__left))}{__desc}",
					"\n"*(1 if(i in (len(__args['desc'])-2, len(__args['desc'])-1)) else 0)
				]))

			print("\n".join([ f" {t}" for t in __table ]))

	except(IndexError, KeyError):
		print(f"/!\\ - Insufficient arguments !")
		return(False)

	return(True)

def setup() -> bool:
	return(install(LIBS_REGISTRY))

if(__name__ == "__main__"):
	arg() if(len(argv) > 1) else setup()