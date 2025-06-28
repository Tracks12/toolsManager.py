#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/translator.py

from csv import DictReader, DictWriter
from json import dumps, load
from os import listdir, mkdir
from os.path import abspath, dirname
from requests import get
from shutil import rmtree
from time import sleep

from core.colors import Colors
from core.config import Config
from core.exceptions import RequestError
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
		self.__cfg = Config()
		self.__path = str(abspath(f"{dirname(abspath(__file__))}/../{self.name}"))
		self.__setup()

		self._args	= [
			(("-c", "--check", "<project> <locale>"), "Run a translation process by project"),
			(("-d", "--delete", "<project> <opt>"), ("Delete a project from workspace", "opt: -f to delete without asking")),
			(("-l", "--list", ""), "List all projects in workspace"),
			(("-n", "--new", "<project> <opt>"), ("Create a blank project in workspace", "opt: -r, --remote to specify a remote file to download")),
			(("-t", "--translate", "<project>"), "Run a translation process by project"),
		]

		self._execs = [
			lambda x:self._check(x),
			lambda x:self._delete(x),
			lambda x:self._list(),
			lambda x:self._new(x),
			lambda x:self._translate(x)
		]

		super().__init__()
		self._run(args)

	def __checkExistProject(self, distroName: str) -> bool:
		__distros = listdir(self.__path)

		if(distroName in __distros):
			return(True)

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

	def _delete(self, args: list[str]) -> None:
		try:
			if(not self.__checkExistProject(args[0])):
				raise(FileNotFoundError("Project doesn't exist on workspace"))

			if(("-f" in args) or self.ask(f"Confirm the deletion of {args[0]} ?")):
				rmtree(abspath(f"{self.__path}/{args[0]}"))
				print(f'{Icons.info}"{args[0]}" was deleted from {self.__path}')

		except(FileNotFoundError) as e:
			print(f"{Icons.warn}{e}")

	def _list(self) -> None:
		__projects = listdir(self.__path)

		table = list[str]([ f" *  Name{' '*(18-len('Name'))}Region(s){' '*(12-len('Region(s)'))}Path" ])
		for i, project in enumerate(__projects, start=1):
			__regions = [ r for r in listdir(abspath(f"{self.__path}/{project}")) if(".json" in r) ]

			table.append("".join([
				f"{' '*(2-len(str(i)))}{Colors.green}{i}{Colors.end}.",
				f"{' '*1}{Colors.cyan}{project.replace('-', ':').split('.')[0]}{Colors.end}",
				f"{' '*(18-len(project.split('.')[0]))}{Colors.purple}{len(__regions)}{Colors.end}",
				f"{' '*(12-len(str(len(__regions))))}{Colors.yellow}{abspath(f'{self.__path}/{project}')}{Colors.end}"
			]))

		_ = "\n".join([ f' {t}' for t in table ])
		print(f"\n{_}")

	def _new(self, args: list[str]) -> None:
		try:
			if(self.__checkExistProject(args[0])):
				raise(FileExistsError(f'Project "{args[0]}" already exist in {self.__path}'))

			__projectPath	= abspath(f"{self.__path}/{args[0]}")
			mkdir(__projectPath)

			for i, arg in enumerate(args):
				if(arg in ("-r", "--remote")):
					__url = f"{args[i+1]}/export?format=csv"
					print(f"{Icons.play}Downloading from remote [ {Colors.yellow}...{Colors.end} ]", end="\r")
					__req = get(__url)
					print(f"{Icons.info}Downloading from remote [ {Colors.green}OK{Colors.end} ]{' '*10}")

					if(__req.status_code == 200):
						__filePath = abspath(f"{__projectPath}/translations.csv")

						with open(__filePath, "wb") as csvFile:
							print(f"{Icons.play}Importing CSV file with translations ...")
							csvFile.write(__req.content)

						print(f'{Icons.info}"{args[0]}" was imported in {self.__path}')

						if(self.ask("Did you want to process translations ?")):
							self._translate([ args[0] ])

					else:
						raise(RequestError(f"Error when downloading Google Sheet", __url, __req.status_code))

					return

			with open(abspath(f"{__projectPath}/translations.csv"), "w", encoding=self.__cfg.getEncoding(), newline='') as csvFile:
				print(f"{Icons.play}Create new CSV file with default translations ...")

				__header	= [ "label", "en", "fr" ]
				__writer	= DictWriter(csvFile, __header)
				__rows		= list[dict[str, str]]([
					{
						"label": "HELLO_WORLD",
						"en": "Hello World",
						"fr": "Bonjour Monde"
					}
				])

				if(not csvFile.tell()):
					__writer.writeheader()

				__writer.writerows(__rows)

			print(f'"{args[0]}" was created in {self.__path}')

		except(IndexError):
			print(f"{Icons.warn}No project name was specified !")

		except(FileExistsError) as e:
			print(f"{Icons.warn}{e}")

		except(Exception, RequestError) as e:
			print(f"{Icons.err}{e}")
			self._delete(args)

	def _translate(self, args: list[str]) -> None:
		try:
			if(not self.__checkExistProject(args[0])):
				raise(FileNotFoundError("Project doesn't exist on workspace"))

			__projectPath	= abspath(f"{self.__path}/{args[0]}")
			__datas			= list[str]([])
			__regions		= dict({})

			with open(f"{__projectPath}/translations.csv", 'r', encoding=self.__cfg.getEncoding(), newline='') as file:
				print(f"{Icons.play}Reading CSV file and load translations ...")
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

					except(Exception) as e:
						print(f'{Icons.warn}PROCESSING "{field}" [ {Colors.red}FAILED{Colors.end} ] (ERR: {e})')

			print(f"{Icons.play}Writing new regions json files ...")

			for key in set(__regions):
				__regionPath = abspath(f"{__projectPath}/{key}.json")

				try:
					with open(__regionPath, 'w', encoding=self.__cfg.getEncoding()) as regionFile:
						print(f'{Icons.play}WRITTING "{__regionPath}" [ {Colors.yellow}...{Colors.end} ]', end="\r")
						string = str(dumps(__regions[key], indent=2, sort_keys=True))
						regionFile.write(string)

					sleep(.05)
					print(f'{Icons.info}WRITTING "{__regionPath}" [ {Colors.green}OK{Colors.end} ] ')

				except(Exception) as e:
						print(f'{Icons.warn}WRITTING "{__regionPath}" [ {Colors.red}FAILED{Colors.end} ] (ERR: {e})')

			print(f"{Icons.info}Translations created with success !")

		except(FileNotFoundError) as e:
			print(f"{Icons.warn}{e}")

	def _check(self, args: list[str]) -> None:
		try:
			if(not self.__checkExistProject(args[0])):
				raise(FileNotFoundError("Project doesn't exist on workspace"))

			__projectPath	= abspath(f"{self.__path}/{args[0]}")
			__regions		= [ r for r in listdir(__projectPath) if(".json" in r) ]

			if(len(args) == 1):
				print(f"{Icons.warn}No locale was specified !")
				print(f"{Icons.tips}Here the list of locales present in {__projectPath}")
				print("".join([
					"Locales: ",
					" | ".join([ f"{Colors.purple}{r.split('.')[0]}{Colors.end}" for r in __regions ]) or f"{Colors.red}No locales{Colors.end}"
				]))

				return

			for region in __regions:
				if(args[1] in region):
					__regionPath = abspath(f"{__projectPath}/{region}")
					print(f"{Icons.info}Viewing {__regionPath} file ...")

					with open(__regionPath, "r", encoding=self.__cfg.getEncoding()) as json:
						__translations = load(json)

					for t in __translations:
						print(f" {t}{' '*(30-len(t))}: {__translations[t]}")
					
					return

			print(f"{Icons.warn}Locale not found in {__projectPath}")

		except(FileNotFoundError) as e:
			print(f"{Icons.warn}{e}")

		except(IndexError):
			print(f"{Icons.warn}No project was specified !")
