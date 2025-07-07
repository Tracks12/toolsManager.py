#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Translator - CSV to multilingual JSON translation manager.

	This module provides a `Tool` for managing translation projects.
	It allows you to create translation workspaces from CSV files, 
	transform them into JSON locale files, check translations, 
	and manage their lifecycle (create, translate, list, check, delete).

	Features:
	- Create new translation projects with default or remote CSV sources.
	- Parse CSV files and generate well-structured JSON region files.
	- Check all translations by locale or search for specific labels.
	- Delete or list existing projects in the workspace.
	- Integrate easily with web or desktop applications to load regions dynamically.

	Note:
		Each project is stored in a dedicated workspace folder.
		Use `$ python translator.py --help` for usage examples.

"""

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

	""" Tool to manage multilingual translation projects from CSV files.

		Translator helps you automate the process of:
		- Creating translation projects with a CSV source.
		- Importing remote CSV files (e.g., Google Sheets export).
		- Generating JSON locale region files for web/desktop apps.
		- Checking translations by project and locale, with search.
		- Managing projects easily (create, delete, list, translate).

		Commands:
		- `-n, --new`: Create a new translation project (optionally from remote CSV).
		- `-t, --translate`: Parse CSV and generate JSON locale files.
		- `-c, --check`: Check translations for a project and locale (search labels).
		- `-l, --list`: List all translation projects in the workspace.
		- `-d, --delete`: Delete a project (with optional force flag).

		Example:
			`~$ translator --new myproject`
			`~$ translator --translate myproject`
			`~$ translator --check myproject en`

	"""

	command	= (("translator", "tr"), "(tr)anslator")
	name	= "Translator"
	path	= __file__
	version	= "1.1"

	def __init__(self, args: list[str]):
		self.__cfg = Config()
		self.__path = str(abspath(f"{dirname(abspath(__file__))}/../{self.name}"))
		self.__setup()

		self._args	= [
			(("-c", "--check", "<project> <locale> *"), ("Show all translations contain in locale file", "opt: -s, --search to search a specific label in locale")),
			(("-d", "--delete", "<project> *"), ("Delete a project from workspace", "opt: -f to delete without asking")),
			(("-l", "--list", ""), "List all projects in workspace"),
			(("-n", "--new", "<project> *"), ("Create a blank project in workspace", "opt: -r, --remote to specify a remote file to download")),
			(("-t", "--translate", "<project>"), "Run a translation process by project")
		]

		self._execs = [
			lambda x:self._check(x),
			lambda x:self._delete(x),
			lambda x:self._list(),
			lambda x:self._new(x),
			lambda x:self._translate(x)
		]

		super().__init__()
		self._run(args, lambda:self._helper())

	def __checkExistProject(self, distroName: str) -> bool:
		""" Checks if a translation project exists in the workspace.

			Args:
				distroName (str): The name of the project to check.

			Returns:
				bool: True if the project exists, False otherwise.

		"""

		__distros = listdir(self.__path)

		if(distroName in __distros):
			return(True)

		return(False)

	def __setup(self) -> None:
		""" Sets up the translator workspace by creating the directory if it does not exist.

			Prints an informational or error message depending on the outcome.

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

	def _check(self, args: list[str]) -> None:
		""" Displays the translations of a project for a given locale, with optional label search.

			Args:
				args (list[str]): Expected arguments:
					- args[0]: project name
					- args[1]: locale code (optional)
					- additional options (e.g., -s to search for a specific label)

			Features:
			- Lists available locales if no locale is specified.
			- Shows all translations for the specified locale.
			- Searches and displays translations containing a given label.
			- Handles errors gracefully, such as project not found or locale not available.

		"""

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
					print(f"{Icons.info}Checking {__regionPath} file ...")

					with open(__regionPath, "r", encoding=self.__cfg.getEncoding()) as json:
						__translations = load(json)

					try:
						if(any(a in ("-s", "--search") for a in args)):
							print(f"{Icons.info}Label matching with {args[3]} in {__regionPath} ...")
							__results = [ t for t in __translations if args[3] in t ]

							if(len(__results)):
								for r in __results:
									print(f" {r}{' '*(30-len(r))}: {__translations[r]}")
							
							else:
								print(f"{Icons.warn}No label matching")

							return

						for r in __translations:
							print(f" {r}{' '*(30-len(r))}: {__translations[r]}")

					except(IndexError):
						print(f"{Icons.warn}No label was specified !")

					except(KeyError):
						print(f"{Icons.warn}Label isn't found on selected locale")

					return

			print(f"{Icons.warn}Locale not found in {__projectPath}")

		except(FileNotFoundError) as e:
			print(f"{Icons.warn}{e}")

		except(IndexError):
			print(f"{Icons.warn}No project wasn't specified !")

	def _delete(self, args: list[str]) -> None:
		""" Deletes a translation project from the workspace.

			Args:
				args (list[str]): Expected arguments:
					- args[0]: name of the project to delete
					- additional options (e.g., -f to force deletion without confirmation)

			Asks for confirmation before deletion unless forced.

		"""

		try:
			if(not self.__checkExistProject(args[0])):
				raise(FileNotFoundError("Project doesn't exist on workspace"))

			if(("-f" in args) or self.ask(f"Confirm the deletion of {args[0]} ?")):
				rmtree(abspath(f"{self.__path}/{args[0]}"))
				print(f'{Icons.info}"{args[0]}" was deleted from {self.__path}')

		except(FileNotFoundError) as e:
			print(f"{Icons.warn}{e}")

	def _list(self) -> None:
		""" Lists all translation projects present in the workspace.

			Displays for each project:
			- Its name
			- The number of locale JSON files
			- The full path of the project

		"""

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
		""" Creates a new translation project in the workspace.

			Args:
				args (list[str]): Expected arguments:
					- args[0]: name of the new project
					- additional options (e.g., -r followed by a URL to import a remote CSV)

			Features:
			- Creates the project folder.
			- Downloads a CSV file from a URL if requested.
			- Creates a default CSV if no external source is provided.
			- Offers to launch the JSON files generation after import.

		"""

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
			print(f"{Icons.warn}No project name wasn't specified !")

		except(FileExistsError) as e:
			print(f"{Icons.warn}{e}")

		except(Exception, RequestError) as e:
			print(f"{Icons.err}{e}")
			self._delete(args)

	def _translate(self, args: list[str]) -> None:
		""" Generates locale JSON files from a project's CSV file.

			Args:
				args (list[str]): Expected arguments:
					- args[0]: name of the project to translate

			Workflow:
			- Reads the project's CSV file.
			- For each locale column (except 'label'), creates a JSON file with translations.
			- Displays progress and any errors encountered.

		"""

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
