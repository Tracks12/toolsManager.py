#!/bin/python3
# -*- coding: utf-8 -*-

from os import listdir, mkdir, remove, rmdir, rename, system as shell
from os.path import abspath, dirname

from core.icons import Icons
from core.tool import Tool

class WslBuilder(Tool):
	command	= (("wslbuilder", "wb"), "(wb)wslbuilder")
	name	= "WSLBuilder"
	path = __file__
	version	= "0.1a"

	_args	= [
		(("-c", "--create", "<name>"), "Create a wsl distribution"),
		(("-d", "--delete", "<name>"), "Remove a wsl distribution image and disk"),
		(("-D", "--full-delete", "<name>"), "Remove a wsl distribution image and disk with docker traces"),
		(("-e", "--export", "<name>"), "Remove a wsl distribution into a tar image"),
		(("-I", "--init", ""), "Init a wsl builder instance with docker"),
		(("-l", "--list", ""), "List all wsl distributions"),
		(("-s", "--start", "<name>"), "Launch a wsl instance"),
	] + Tool._args[:]

	__path = str(abspath(f"{dirname(abspath(__file__))}/../{name}"))

	def __init__(self, args: list[str]):
		Tool.__init__(self)

		try:
			mkdir(self.__path)
			print(f"{Icons.info}Create path workspace for {self.name} tool at {self.__path}")

		except FileExistsError:
			print(f"{Icons.info}Using {self.__path} for {self.name} workspace already exist")

		except PermissionError:
			print(f"{Icons.warn}Permission denied: Unable to create '{self.__path}'.")

		except Exception as e:
			print(f"{Icons.warn}An error occurred: {e}")

		self._execs = [
			lambda x:self._create(x),
			lambda x:self._delete(x),
			lambda x:self._fullDelete(x),
			lambda x:self._export(x),
			lambda x:self._init(),
			lambda x:self._list(),
			lambda x:self._start(x),
		] + self._execs[:]

		self._run(args)

	def _create(self, args: list[str]) -> None:
		try:
			mkdir(f"{self.__path}/{args[0]}")
			shell(f"wsl docker pull {args[0]}")
			shell(f"wsl docker run -d --name {args[0]} {args[0]}:latest")
			shell(f"wsl docker export {args[0]} > {args[0]}.tar")
			rename(f"{args[0]}.tar", f"{self.__path}/{args[0]}/{args[0]}.tar")
			shell(f"wsl --import {args[0]} {self.__path}/{args[0]} {self.__path}/{args[0]}/{args[0]}.tar")

			self._start(args)

		except FileExistsError:
			print(f"{Icons.warn}Wsl distribution already exist on workspace")

	def _delete(self, args: list[str]) -> None:
		distros = listdir(self.__path)

		try:
			if(args[0] in distros):
				shell(f"wsl --unregister {args[0]}")
				remove(f"{self.__path}/{args[0]}/{args[0]}.tar")
				rmdir(f"{self.__path}/{args[0]}")

			else:
				raise FileNotFoundError

		except FileNotFoundError:
			print(f"{Icons.warn}Wsl distribution doesn't exist on workspace")

	def _fullDelete(self, args: list[str]) -> None:
		shell(f"wsl docker rm {args[0]}")
		shell(f"wsl docker rmi {args[0]}:latest")

		self._delete(args)

	def _export(self, args: list[str]) -> None:
		distros = listdir(self.__path)

		if(args[0] in distros):
			shell(f"wsl --export {args[0]} {self.__path}/{args[0]}/{args[0]}.tar")

		else:
			print(f"{Icons.warn}Wsl distribution doesn't exist on workspace")

	def _init(self) -> None:
		__libspath = abspath(f"{self.__path}/../libs/wslbuilder")

		shell(f"wsl --import wslbuilder {__libspath} {__libspath}/image.tar")
		shell("wsl -s wslbuilder")
		shell("wsl apk update")
		shell("wsl apk add docker openrc")
		shell("wsl service docker start")
		shell('wsl touch "/../run/openrc/softlevel"')
		shell("wsl service docker start")
		shell("wsl docker ps")

	def _list(self) -> None:
		distros = listdir(self.__path)

		print(f"\n {' '*1}*  Name{' '*(12-len('Name'))}Path")
		for i, distro in enumerate(distros, start=1):
			print(f" {' '*(2-len(str(i)))}{i}. {distro}{' '*(12-len(distro))}{abspath(f'{self.__path}/{distro}')}")

	def _start(self, args: list[str]) -> None:
		distros = listdir(self.__path)

		if(args[0] in distros):
			shell(f"wsl -d {args[0]}")

		else:
			print(f"{Icons.warn}Wsl distribution doesn't exist on workspace")
