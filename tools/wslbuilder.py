#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Docker image management for WSL.

	This module allows for the creation and management of Docker images compatible with Windows
	Subsystem for Linux (WSL). It facilitates the customization and integration of Docker images
	into a WSL environment, simplifying application deployment within this environment.

	Note:
		Don't forget to run `$ python setup.py` to install wslbuilder dependencies, you can ignore the installation if you have a default wsl instance with a running docker daemon

"""

from os import listdir, mkdir, remove, rmdir, system as shell
from os.path import abspath, dirname, getsize, isdir

import re

from core import stringSize
from core.colors import Colors
from core.icons import Icons
from core.tool import Tool

DISTRONAME_REGEX = str("(\\s)|([/:])")

class WslBuilder(Tool):
	command	= (("wslbuilder", "wb"), "(wb)wslbuilder")
	name	= "WSLBuilder"
	path	= __file__
	version	= "1.1"

	def __init__(self, args: list[str]):
		super().__init__()

		self.__path = str(abspath(f"{dirname(abspath(__file__))}/../{self.name}"))
		self.__setup()

		self._args = [
			(("-c", "--create", "<distro>"), "Create a wsl distribution"),
			(("-d", "--delete", "<distro>"), "Remove a wsl distribution image and disk"),
			(("-D", "--full-delete", "<distro>"), "Remove a wsl distribution image and disk with docker traces"),
			(("-e", "--export", "<distro>"), "Export a wsl distribution into a tar image"),
			(("-i", "--install", "<distro>"), "Install a wsl distribution to workspace"),
			(("-I", "--init", ""), "Init a wsl builder instance with docker"),
			(("-l", "--list", ""), "List all wsl distributions"),
			(("-S", "--stat", "<distro>"), "Show statistics about a wsl distributions"),
			(("-s", "--start", "<distro>"), "Launch a wsl instance")
		] + self._args[:]

		self._execs= [
			lambda x:self._create(x),
			lambda x:self._delete(x),
			lambda x:self._fullDelete(x),
			lambda x:self._export(x),
			lambda x:self._install(x),
			lambda x:self._init(),
			lambda x:self._list(),
			lambda x:self._stat(x),
			lambda x:self._start(x)
		] + self._execs[:]

		self._run(args)

	def __ask(self, msg: str = "Are you sure ?") -> bool:
		return(bool(input(f"{msg} [y/N] ").lower() in ("y", "yes")))

	def __checkActiveDistro(self, distroname: str) -> bool:
		__distroPath = abspath(f"{self.__path}/{distroname}")
		__distroRepo = listdir(__distroPath)

		if("ext4.vhdx" in __distroRepo):
			return(True)

		print(f"{Icons.warn}Wsl distribution is inactive")
		return(False)

	def __checkDockerStatus(self) -> bool:
		return(bool(shell(f"wsl service docker status")))

	def __checkExistDistro(self, distroName: str) -> bool:
		__distros = listdir(self.__path)

		if(distroName in __distros):
			return(True)

		print(f"{Icons.warn}Wsl distribution doesn't exist on workspace")
		return(False)

	def __setup(self) -> None:
		try:
			mkdir(self.__path)
			print(f"{Icons.info}Create path workspace for {self.name} tool at {self.__path}")

		except(FileExistsError):
			print(f"{Icons.info}Using {self.__path} for {self.name} workspace already exist")

		except(PermissionError):
			print(f"{Icons.warn}Permission denied: Unable to create '{self.__path}'.")

		except(Exception) as e:
			print(f"{Icons.err}An error occurred: {e}")

	def _create(self, args: list[str]) -> None:
		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])
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

			if(self.__ask("Did you want to start it ?")):
				self._start(args)

		except(FileExistsError):
			print(f"{Icons.warn}Wsl distribution already exist on workspace")

		except(Exception) as e:
			print(f"{Icons.err}{e}")
			rmdir(__distroPath)

	def _delete(self, args: list[str]) -> None:
		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])
		__distroPath = abspath(f"{self.__path}/{__distroName}")

		if(self.__checkExistDistro(__distroName)):
			if(("-f" in args) or self.__ask(f"Confirm the deletion of {args[0]} ?")):
				shell(f"wsl --unregister {__distroName}")
				remove(f"{__distroPath}/{__distroName}.tar")
				rmdir(f"{__distroPath}")

	def _fullDelete(self, args: list[str]) -> None:
		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])

		if(self.__ask(f"Confirm the deletion of {args[0]} ?")):
			shell(f"wsl docker rm {__distroName}")
			shell(f"wsl docker rmi {args[0]}")

			self._delete(args[:] + ["-f"])

	def _export(self, args: list[str]) -> None:
		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])
		__distroPath = abspath(f"{self.__path}/{__distroName}")

		if(
			self.__checkExistDistro(__distroName)
			and self.__checkActiveDistro(__distroName)
		):
			shell(f"wsl --export {__distroName} {__distroPath}/{__distroName}.tar")

	def _install(self, args: list[str]) -> None:
		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])
		__distroPath = abspath(f"{self.__path}/{__distroName}")

		try:
			if(not isdir(__distroPath)):
				raise(FileNotFoundError)

			if(not self.__checkActiveDistro(__distroName)):
				shell(f"wsl --import {__distroName} {__distroPath} {abspath(f'{__distroPath}/{__distroName}.tar')}")

			if(self.__ask("Did you want to start it ?")):
				self._start(args)

		except(FileNotFoundError):
			print(f"{Icons.err}{__distroName} isn't found in {self.__path}")
			print(f"{Icons.tips}Make sure you have {__distroName} in {self.__path} with {__distroName}.tar inside")

	def _init(self) -> None:
		__libspath = abspath(f"{self.__path}/../libs/wslbuilder")

		try:
			if(not isdir(__libspath)):
				raise(FileNotFoundError)

			shell(f"wsl --import wslbuilder {__libspath} {__libspath}/wslbuilder.tar")
			shell("wsl -s wslbuilder")
			shell("wsl apk update")
			shell("wsl apk add docker openrc")

			if(self.__checkDockerStatus()):
				if(shell("wsl service docker start")):
					shell('wsl touch "/../run/openrc/softlevel"')
					shell("wsl service docker start")

		except(FileNotFoundError):
			print(f"{Icons.err}WSLBuilder libs doesn't exist at {__libspath}")
			print(f'{Icons.tips}Don\'t forget to run "python setup.py" to unpack the libs')

	def _list(self) -> None:
		__distros = listdir(self.__path)

		table = list[str]([ f" *  Name{' '*(18-len('Name'))}Size{' '*(12-len('Size'))}Path" ])
		for i, distro in enumerate(__distros, start=1):
			try:
				size = stringSize(getsize(abspath(f"{self.__path}/{distro}/ext4.vhdx")))

			except(FileNotFoundError):
				size = f"INACTIVE"

			table.append("".join([
				f"{' '*(2-len(str(i)))}{Colors.green}{i}{Colors.end}.",
				f"{' '*1}{Colors.cyan}{distro.replace('-', ':')}{Colors.end}",
				f"{' '*(18-len(distro))}{Colors.red if(size == "INACTIVE") else Colors.purple}{size}{Colors.end}",
				f"{' '*(12-len(size))}{Colors.yellow}{abspath(f'{self.__path}/{distro}')}{Colors.end}"
			]))

		print(f"\n{'\n'.join([ f" {t}" for t in table ])}")

	def _stat(self, args: list[str]) -> None:
		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])

		if(self.__checkExistDistro(__distroName)):
			__distroPath		= abspath(f"{self.__path}/{__distroName}")
			__distroImageName	= str(f"{__distroName}.tar")
			__distroImagePath	= abspath(f"{__distroPath}/{__distroImageName}")
			__distroImageSize	= stringSize(getsize(__distroImagePath))

			table = list[str]([
				f"* Name{' '*(8-len('Name'))}: {Colors.cyan}{args[0]}{Colors.end}",
				f"* Path{' '*(8-len('Path'))}: {Colors.yellow}{__distroPath}{Colors.end}",
				f"* Image{' '*(8-len('Image'))}: [ {Colors.purple}{__distroImageSize}{Colors.end} ] {__distroImageName}"
			])

			if(self.__checkActiveDistro(__distroName)):
				__distroDiskName	= str("ext4.vhdx")
				__distroDiskPath	= abspath(f"{__distroPath}/{__distroDiskName}")
				__distroDiskSize	= stringSize(getsize(__distroDiskPath))

				table.append(f"* Disk{' '*(8-len('Disk'))}: [ {Colors.purple}{__distroDiskSize}{Colors.end} ] {__distroDiskName}")

			else:
				table[0] += f" [ {Colors.red}INACTIVE{Colors.end} ]"

			print(f"\n{'\n'.join([ f"  {t}" for t in table ])}")

	def _start(self, args: list[str]) -> None:
		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])

		if(
			self.__checkExistDistro(__distroName)
			and self.__checkActiveDistro(__distroName)
		):
			shell(f"wsl -d {__distroName}")
