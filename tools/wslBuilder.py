#!/bin/python3
# -*- coding: utf-8 -*-

from os import listdir, mkdir, remove, rmdir, system as shell
from os.path import abspath, dirname, getsize

from core import UNITS
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

	def __checkDockerStatus(self) -> bool:
		return bool(shell(f"wsl service docker status"))

	def _create(self, args: list[str]) -> None:
		__distroName = args[0].replace(':', '-')
		__distroPath = abspath(f"{self.__path}/{__distroName}")

		try:
			mkdir(__distroPath)

			if(self.__checkDockerStatus()):
				raise(Exception("Docker wasn't started on wsl"))

			if(shell(f"wsl docker pull {args[0]}")):
				raise(Exception(f"Docker hasn't found {args[0]} image"))

			shell(f"wsl docker run -d --name {__distroName} {args[0]}")
			shell(f"wsl docker export {__distroName} > {__distroPath}/{__distroName}.tar")
			shell(f"wsl --import {__distroName} {__distroPath} {__distroPath}/{__distroName}.tar")

			self._start(args)

		except(FileExistsError):
			print(f"{Icons.warn}Wsl distribution already exist on workspace")

		except(Exception) as e:
			print(f"{Icons.warn}{e}")
			rmdir(__distroPath)

	def _delete(self, args: list[str]) -> None:
		__distros = listdir(self.__path)
		__distroName = args[0].replace(':', '-')
		__distroPath = abspath(f"{self.__path}/{__distroName}")

		try:
			if(__distroName in __distros):
				shell(f"wsl --unregister {__distroName}")
				remove(f"{__distroPath}/{__distroName}.tar")
				rmdir(f"{__distroPath}")

			else:
				raise FileNotFoundError

		except FileNotFoundError:
			print(f"{Icons.warn}Wsl distribution doesn't exist on workspace")

	def _fullDelete(self, args: list[str]) -> None:
		__distroName = args[0].replace(':', '-')

		shell(f"wsl docker rm {__distroName}")
		shell(f"wsl docker rmi {args[0]}")

		self._delete(args)

	def _export(self, args: list[str]) -> None:
		__distros = listdir(self.__path)
		__distroName = args[0].replace(':', '-')
		__distroPath = abspath(f"{self.__path}/{__distroName}")

		if(__distroName in __distros):
			shell(f"wsl --export {__distroName} {__distroPath}/{__distroName}.tar")

		else:
			print(f"{Icons.warn}Wsl distribution doesn't exist on workspace")

	def _init(self) -> None:
		__libspath = abspath(f"{self.__path}/../libs/wslbuilder")

		shell(f"wsl --import wslbuilder {__libspath} {__libspath}/wslbuilder.tar")
		shell("wsl -s wslbuilder")
		shell("wsl apk update")
		shell("wsl apk add docker openrc")

		if(self.__checkDockerStatus):
			if(shell("wsl service docker start")):
				shell('wsl touch "/../run/openrc/softlevel"')
				shell("wsl service docker start")

	def _list(self) -> None:
		__distros = listdir(self.__path)

		print(f"\n {' '*1}*  Name{' '*(18-len('Name'))}Size{' '*(12-len('Size'))}Path")
		for i, distro in enumerate(__distros, start=1):
			size = [getsize(abspath(f"{self.__path}/{distro}/ext4.vhdx")), UNITS[0]]

			for j in range(1, len(UNITS)):
				size[0] /= 1000
				size[1] = UNITS[j]
				if(size[0] < 1024):
					break

			size = f"{round(size[0], 2)} {size[1]}"

			print(f" {' '*(2-len(str(i)))}{i}. {distro.replace('-', ':')}{' '*(18-len(distro))}{size}{' '*(12-len(size))}{abspath(f'{self.__path}/{distro}')}")

	def _start(self, args: list[str]) -> None:
		__distros = listdir(self.__path)
		__distroName = args[0].replace(':', '-')

		if(__distroName in __distros):
			shell(f"wsl -d {__distroName}")

		else:
			print(f"{Icons.warn}Wsl distribution doesn't exist on workspace")
