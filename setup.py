#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import abspath
from shutil import rmtree

from core.rarfile import RarFile

def clearLibs(paths: list[str]) -> None:
	if(len(paths)):
		for p in paths:
			try:
				rmtree(p)

			except(FileNotFoundError):
				pass

def setup() -> bool:
	__libs			= list[str]([
		"wslbuilder"
	])

	__extractPath	= abspath("libs/")
	__rarPaths		= [ abspath(f"{__extractPath}/{m}.rar") for m in __libs ]
	__libsPath		= [ abspath(f"{__extractPath}/{m}") for m in __libs ]

	print("[ INFO ]: Clearing installation ...")
	clearLibs(__libsPath)

	for i, rp in enumerate(__rarPaths):
		with RarFile(rp) as __rf:
			try:
				print(f" ( ) Unpacking {rp} ... [{i}/{len(__rarPaths)}]", end="\r")
				__rf.extractall(__extractPath)
				print(f" (*) {rp} Unpacked{' '*16}")

			except(Exception) as e:
				clearLibs(__libsPath)
				print(f"[ ERROR ]: {e}{' '*(16+len(rp))}")
				return(False)

	print("[ OK ]: Installation finished !")
	return(True)

if(__name__ == "__main__"):
	setup()