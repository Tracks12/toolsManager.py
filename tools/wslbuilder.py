#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" WSLBuilder - Docker image management for Windows Subsystem for Linux (WSL).

	This module provides a `Tool` for managing Docker images and WSL distributions.
	It allows you to pull Docker images, convert them into WSL distributions, export them,
	and manage their lifecycle (create, delete, export, list, inspect, and launch).

	Features:
	- Pull Docker images and transform them into custom WSL distributions.
	- Initialize a WSL environment with Docker support.
	- Export WSL distributions to `.tar` archives.
	- List all distributions, show stats, and remove them cleanly.
	- Integrate easily in an automated toolchain with your tools manager.

	Projects are saved in a dedicated workspace directory:
		<workspace_root>/WSLBuilder/<image_name>/

	Note:
		Run `$ python setup.py` to unpack dependencies required by WSLBuilder.
		You can skip this step if you already have a default WSL instance with Docker running.

"""

# tools/wslbuilder.py

from os import listdir, mkdir, remove, rmdir, system as shell
from os.path import abspath, dirname, getsize, isdir

import re

from core import stringSize
from core.colors import Colors
from core.constants import EXTRACT_PATH
from core.icons import Icons
from core.tool import Tool

DISTRONAME_REGEX = str("(\\s)|([/:])")

class WslBuilder(Tool):

	""" Tool to manage custom WSL distributions built from Docker images.

		WSLBuilder helps you automate the process of:
		- Pulling Docker images and converting them to WSL distros.
		- Managing distros (create, delete, export, list, stats, start).
		- Initializing a workspace for custom WSL builds.
		- Ensuring Docker daemon runs inside WSL when needed.

		Commands:
		- `-n, --new`: Create a new WSL distro from a Docker image.
		- `-d, --delete`: Delete a WSL distro (with optional force flag).
		- `-D, --full-delete`: Delete a distro and clean up Docker containers/images.
		- `-e, --export`: Export a WSL distro to a `.tar` archive.
		- `-i, --install`: Import/install a WSL distro from a `.tar`.
		- `-I, --init`: Initialize the builder environment with Docker.
		- `-l, --list`: List all existing distros in the workspace.
		- `-S, --stat`: Show detailed stats about a distro.
		- `-s, --start`: Launch a WSL instance of a distro.

		Example:
			`~$ wslbuilder --new ubuntu:latest`
			`~$ wslbuilder --list`
			`~$ wslbuilder --export mydistro`

	"""

	command	= (("wslbuilder", "wb"), "(wb)wslbuilder")
	name	= "WSLBuilder"
	path	= __file__
	version	= "1.1"

	def __init__(self, args: list[str]):
		self.__path = str(abspath(f"{dirname(abspath(__file__))}/../{self.name}"))
		self.__setup()

		self._args = [
			(("-d", "--delete", "<distro> *"), ("Remove a wsl distribution image and disk", "opt: -f to delete without asking")),
			(("-D", "--full-delete", "<distro> *"), ("Remove a wsl distribution image and disk with docker traces", "opt: -f to delete without asking")),
			(("-e", "--export", "<distro>"), "Export a wsl distribution into a tar image"),
			(("-i", "--install", "<distro>"), "Install a wsl distribution to workspace"),
			(("-I", "--init", ""), "Init a wsl builder instance with docker"),
			(("-l", "--list", ""), "List all wsl distributions"),
			(("-n", "--new", "<distro>"), "Create a wsl distribution"),
			(("-S", "--stat", "<distro>"), "Show statistics about a wsl distributions"),
			(("-s", "--start", "<distro>"), "Launch a wsl instance")
		]

		self._execs= [
			lambda x:self._delete(x),
			lambda x:self._fullDelete(x),
			lambda x:self._export(x),
			lambda x:self._install(x),
			lambda x:self._init(),
			lambda x:self._list(),
			lambda x:self._new(x),
			lambda x:self._stat(x),
			lambda x:self._start(x)
		]

		super().__init__()
		self._run(args, lambda:self._helper())

	def __checkActiveDistro(self, distroname: str) -> bool:
		"""Check if a WSL distribution has an active disk (ext4.vhdx).

			Args:
				distroname (str): The name of the distribution to check.

			Returns:
				bool: True if active, False otherwise.

		"""

		__distroPath = abspath(f"{self.__path}/{distroname}")
		__distroRepo = listdir(__distroPath)

		if("ext4.vhdx" in __distroRepo):
			return(True)

		print(f"{Icons.warn}Wsl distribution is inactive")
		return(False)

	def __checkDockerStatus(self) -> bool:
		"""Check if the Docker daemon is running inside WSL.

			Returns:
				bool: True if running, False otherwise.

		"""

		return(bool(shell(f"wsl service docker status")))

	def __checkExistDistro(self, distroName: str) -> bool:
		"""Check if a given WSL distribution exists in the workspace.

			Verifies if the specified distro directory is present.

			Args:
				distroName (str): The name of the distribution to check.

			Returns:
				bool: True if the distribution exists, False otherwise.

		"""

		__distros = listdir(self.__path)

		if(distroName in __distros):
			return(True)

		print(f"{Icons.warn}Wsl distribution doesn't exist on workspace")
		return(False)

	def __setup(self) -> None:
		""" Ensure the workspace directory exists for storing WSL distributions.

			Creates the workspace path if it does not exist.
			Prints informative messages depending on the outcome.

		"""

		try:
			mkdir(self.__path)
			print(f"{Icons.info}Create path workspace for {self.name} tool at {self.__path}")

		except(FileExistsError):
			print(f"{Icons.info}Using {self.__path} for {self.name} workspace")

		except(PermissionError):
			print(f"{Icons.warn}Permission denied: Unable to create '{self.__path}'.")

		except(Exception) as e:
			print(f"{Icons.err}An error occurred: {e}")

	def _new(self, args: list[str]) -> None:
		""" Create a new WSL distribution from a Docker image.

			Steps:
			1. Pull the specified Docker image.
			2. Export the container as a `.tar` archive.
			3. Import it as a new WSL distribution.
			4. Optionally start it immediately.

			Args:
				args (list[str]): A list containing the Docker image name/tag (e.g., 'ubuntu:latest').

			Raises:
				Exception: If Docker is not running or the image is not found.

		"""

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

			if(self.ask("Did you want to start it ?")):
				self._start(args)

		except(FileExistsError):
			print(f"{Icons.warn}Wsl distribution already exist on workspace")

		except(Exception) as e:
			print(f"{Icons.err}{e}")
			rmdir(__distroPath)

	def _delete(self, args: list[str]) -> None:
		""" Remove a WSL distribution and its associated files.

			Steps:
			- Unregister the WSL distro.
			- Remove the `.tar` archive.
			- Remove the distro workspace directory.

			Args:
				args (list[str]): A list with the distro name to delete. Use '-f' to force without confirmation.

			Asks for confirmation before deletion unless forced.

		"""

		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])
		__distroPath = abspath(f"{self.__path}/{__distroName}")

		if(self.__checkExistDistro(__distroName)):
			if(("-f" in args) or self.ask(f"Confirm the deletion of {args[0]} ?")):
				shell(f"wsl --unregister {__distroName}")
				remove(f"{__distroPath}/{__distroName}.tar")
				rmdir(f"{__distroPath}")

	def _fullDelete(self, args: list[str]) -> None:
		""" Remove a WSL distribution and clean up related Docker resources.

			Steps:
			- Remove the Docker container and image.
			- Delete the WSL distribution and its files.

			Args:
				args (list[str]): A list with the distro name to delete. Use '-f' to force.

			Asks for confirmation before deletion unless forced.

		"""

		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])

		if(("-f" in args) or self.ask(f"Confirm the deletion of {args[0]} ?")):
			shell(f"wsl docker rm {__distroName}")
			shell(f"wsl docker rmi {args[0]}")

			self._delete(args[:] + ["-f"])

	def _export(self, args: list[str]) -> None:
		""" Export an existing WSL distribution to a `.tar` archive.

			This allows you to back up or share the distribution.

			Args:
				args (list[str]): A list with the distro name to export.

		"""

		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])
		__distroPath = abspath(f"{self.__path}/{__distroName}")

		if(
			self.__checkExistDistro(__distroName)
			and self.__checkActiveDistro(__distroName)
		):
			shell(f"wsl --export {__distroName} {__distroPath}/{__distroName}.tar")

	def _install(self, args: list[str]) -> None:
		""" Import and install a WSL distribution from a `.tar` archive.

			If the distro is inactive, it re-imports it using its archive.

			Args:
				args (list[str]): A list with the distro name to install.

			Raises:
				FileNotFoundError: If the `.tar` archive or distro directory is missing.

		"""

		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])
		__distroPath = abspath(f"{self.__path}/{__distroName}")

		try:
			if(not isdir(__distroPath)):
				raise(FileNotFoundError)

			if(not self.__checkActiveDistro(__distroName)):
				shell(f"wsl --import {__distroName} {__distroPath} {abspath(f'{__distroPath}/{__distroName}.tar')}")

			if(self.ask("Did you want to start it ?")):
				self._start(args)

		except(FileNotFoundError):
			print(f"{Icons.err}{__distroName} isn't found in {self.__path}")
			print(f"{Icons.tips}Make sure you have {__distroName} in {self.__path} with {__distroName}.tar inside")

	def _init(self) -> None:
		""" Initialize a WSLBuilder environment with Docker support.

			- Imports the base builder instance into WSL.
			- Installs Docker and required services.
			- Starts Docker if not running.

			Notes:
				Make sure `setup.py` has unpacked the required files.

		"""

		__libspath = abspath(f"{EXTRACT_PATH}/wslbuilder")

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
		""" List all WSL distributions managed in the workspace.

			Shows:
			- Distro name
			- Size
			- Path
			- Active/inactive status

		"""

		__distros = listdir(self.__path)

		table = list[str]([ f" *  {'Name':<{18}}{'Size':<{12}}Path" ])
		for i, distro in enumerate(__distros, start=1):
			try:
				size = stringSize(getsize(abspath(f"{self.__path}/{distro}/ext4.vhdx")))

			except(FileNotFoundError):
				size = f"INACTIVE"

			table.append("".join([
				f"{' '*(2-len(str(i)))}{Colors.green}{i}{Colors.end}. ",
				f"{Colors.cyan}{distro.replace('-', ':'):<{18}}{Colors.end}",
				f"{Colors.red if(size == 'INACTIVE') else Colors.purple}{size:<{12}}{Colors.end}",
				f"{Colors.yellow}{abspath(f'{self.__path}/{distro}')}{Colors.end}"
			]))

		_ = "\n".join([ f' {t}' for t in table ])
		print(f"\n{_}")

	def _stat(self, args: list[str]) -> None:
		""" Show detailed stats about a specific WSL distribution.

			Displays:
			- Name
			- Path
			- Image size
			- Disk size (if active)

			Args:
				args (list[str]): A list with the distro name to inspect.

		"""

		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])

		if(self.__checkExistDistro(__distroName)):
			__distroPath		= abspath(f"{self.__path}/{__distroName}")
			__distroImageName	= str(f"{__distroName}.tar")
			__distroImagePath	= abspath(f"{__distroPath}/{__distroImageName}")
			__distroImageSize	= stringSize(getsize(__distroImagePath))

			table = list[str]([
				f"{'Name':<{8}}: {Colors.cyan}{args[0]}{Colors.end}",
				f"{'Path':<{8}}: {Colors.yellow}{__distroPath}{Colors.end}",
				f"{'Image':<{8}}: [ {Colors.purple}{__distroImageSize}{Colors.end} ] {__distroImageName}"
			])

			if(self.__checkActiveDistro(__distroName)):
				__distroDiskName	= str("ext4.vhdx")
				__distroDiskPath	= abspath(f"{__distroPath}/{__distroDiskName}")
				__distroDiskSize	= stringSize(getsize(__distroDiskPath))

				table.append(f"{'Disk':<{8}}: [ {Colors.purple}{__distroDiskSize}{Colors.end} ] {__distroDiskName}")

			else:
				table[0] += f" [ {Colors.red}INACTIVE{Colors.end} ]"

			_ = "\n".join([ f' * {t}' for t in table ])
			print(f"\n{_}")

	def _start(self, args: list[str]) -> None:
		""" Launch a WSL instance for the specified distribution.

			Args:
				args (list[str]): A list with the distro name to start.

		"""

		__distroName = re.sub(DISTRONAME_REGEX, "-", args[0])

		if(
			self.__checkExistDistro(__distroName)
			and self.__checkActiveDistro(__distroName)
		):
			shell(f"wsl -d {__distroName}")
