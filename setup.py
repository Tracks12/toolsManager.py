#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import listdir
from os.path import abspath, isdir
from shutil import rmtree

from core.rarfile import RarFile

LIBS_REGISTRY = list[str]([
	"wslbuilder"
])

def clearLibs(paths: list[str]) -> None:
	for p in paths:
		try:
			rmtree(p)

		except(FileNotFoundError):
			pass

def setup() -> bool:
	__extractPath	= abspath("libs/")
	__rarPaths		= [ abspath(f"{__extractPath}/{m}.rar") for m in LIBS_REGISTRY ]
	__libsPath		= [ abspath(f"{__extractPath}/{m}") for m in LIBS_REGISTRY ]

	if(len([ d for d in listdir(__extractPath) if isdir(abspath(f"{__extractPath}/{d}")) ])):
		print("[ INFO ]: Clearing installation ...")
		clearLibs(__libsPath)

	for i, rp in enumerate(__rarPaths):
		try:
			with RarFile(rp) as __rf:
				print(f" ( ) Unpacking {rp} ... [{i}/{len(__rarPaths)}]", end="\r")
				__rf.extractall(__extractPath)
				print(f" (*) {rp} Unpacked{' '*16}")

		except(Exception) as e:
			clearLibs(__libsPath)
			print(f"\n[ ERROR ]: {e}{' '*(16+len(rp))}")
			return(False)

	print("[ OK ]: Installation finished !")
	return(True)

if(__name__ == "__main__"):
	setup()