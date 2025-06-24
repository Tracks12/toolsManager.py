#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/translator.py

from csv import DictReader, DictWriter
from json import dumps
from os import listdir, mkdir
from os.path import abspath, dirname, realpath
from shutil import rmtree
from time import sleep
from traceback import format_exc

from core.colors import Colors
from core.config import Config
from core.icons import Icons
from core.tool import Tool

class Translator(Tool):
	""" Say hello to the user
	"""

	command	= (("translator", "tr"), "(tr)anslator")
	name	= "Translator"
	path	= __file__
	version	= "1.0"

	def __init__(self, args: list[str]):
		super().__init__()

		self.__cfg = Config()
		self.__path = str(abspath(f"{dirname(abspath(__file__))}/../{self.name}"))
		self.__setup()

		self._args	= [
			(("-c", "--create", "<project>"), "Create a blank project in workspace"),
			(("-d", "--delete", "<project>"), "Delete a project from workspace"),
			(("-t", "--translate", "<project>"), "Run a translation process by project"),
		] + self._args[:]

		self._execs = [
			lambda x:self._create(x),
			lambda x:self._delete(x),
			lambda x:self._translate(x)
		] + self._execs[:]

		self._run(args)

	def __checkExistProject(self, distroName: str) -> bool:
		__distros = listdir(self.__path)

		if(distroName in __distros):
			return(True)

		print(f"{Icons.warn}Project doesn't exist on workspace")
		return(False)

	def __setup(self) -> None:
		try:
			mkdir(self.__path)
			print(f"{Icons.info}Create path workspace for {self.name} tool at {self.__path}")

		except(FileExistsError):
			print(f"{Icons.info}Using {self.__path} for {self.name} workspace")

		except(PermissionError):
			print(f"{Icons.warn}Permission denied: Unable to create '{self.__path}'.")

		except(Exception) as e:
			print(f"{Icons.err}An error occurred: {e}")

	def _create(self, args: list[str]) -> None:
		try:
			if(self.__checkExistProject(args[0])):
				raise(FileExistsError(f'Project "{args[0]}" already exist in {self.__path}'))

			__projectPath	= abspath(f"{self.__path}/{args[0]}")

			mkdir(__projectPath)

			with open(abspath(f"{__projectPath}/{args[0]}.csv"), "w", encoding=self.__cfg.getEncoding(), newline='') as csvFile:
				__header	= [ "label", "en", "fr" ]
				__writer	= DictWriter(csvFile, __header)
				__rows		= list[dict[str, str]]([
					{ "label": "HELLO_WORLD", "en": "Hello World", "fr": "Bonjour Monde" }
				])

				if(not csvFile.tell()):
					__writer.writeheader()

				__writer.writerows(__rows)

			print(f'"{args[0]}" was created in {self.__path}')

		except(IndexError):
			print(f"{Icons.warn}No schedule name was specified !")

		except(FileExistsError) as e:
			print(f"{Icons.warn}{e}")

		except(Exception) as e:
			print(f"{Icons.err}{e}")

	def _delete(self, args: list[str]) -> None:
		if(self.__checkExistProject(args[0])):
			rmtree(abspath(f"{self.__path}/{args[0]}"))
			print(f'"{args[0]}" was deleted from {self.__path}')

	def _translate(self, args: list[str]) -> None:
		__projectPath	= abspath(f"{self.__path}/{args[0]}")
		__datas			= list[str]([])
		__regions		= dict({})

		with open(f"{__projectPath}/{args[0]}.csv", 'r', newline='') as file:
			print(f"{Icons.play}Reading CSV file and load translation ...")
			lines = DictReader(file, delimiter=',')

			for line in lines:
				__datas.append(line)

		print(f"{Icons.play}Wrapping data in new format ...")
		for field in lines.fieldnames:
			if(field != 'label'):
				__regions[field] = dict({})

				try:
					print(f'{Icons.play}PROCESSING "{field}" [ {Colors.yellow}...{Colors.end} ]', end="\r")

					for data in __datas:
						__regions[field].update({ data["label"]: data[field] })

					sleep(.05)

				except(Exception):
					print(f'{Icons.warn}PROCESSING "{field}" [ {Colors.red}FAILED{Colors.end} ]')
					print(f"{Icons.warn}{format_exc()}")

		print(f"{Icons.play}Writing new regions json files ...")

		for key in __regions:
			__regionPath = abspath(f"{__projectPath}/{key}.json")

			try:
				print(f'{Icons.play}WRITTING "{__regionPath}" [ {Colors.yellow}...{Colors.end} ]', end="\r")

				with open(__regionPath, 'w') as regionFile:
					string = str(dumps(__regions[key], indent=2, sort_keys=True))
					regionFile.write(string)

				sleep(.05)
				print(f'{Icons.info}WRITTING "{__regionPath}" [ {Colors.green}OK{Colors.end} ] ')

			except(Exception):
					print(f'{Icons.warn}WRITTING "{__regionPath}" [ {Colors.red}FAILED{Colors.end} ]')
					print(f"{Icons.warn}{format_exc()}")

		print(f"{Icons.info}Translations created with success !")
