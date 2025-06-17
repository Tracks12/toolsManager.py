#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Module to allow developers to generate a new tool skeleton.

	This script creates a Python file in the `tools/` directory with a template
	class inheriting from `Tool`. It prompts the user for the tool name, CLI
	argument, and alias, and inserts them into the class definition.

	The generated file is ready to be customized and integrated into the main project.

"""

from os import listdir
from os.path import abspath, basename, dirname

from core.icons import Icons
from core.config import Config

TOOL_TEMPLATE = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/hello.py

from core.tool import Tool

class Hello(Tool):
	""" Say hello to the user
	"""

	command	= (("{argument}", "{alias}"), "{concat}")
	name	= "{name}"
	path	= __file__
	version	= "0.1a"

	def __init__(self, args: list[str]):
		super().__init__()

		self._args	= [
			(("-s", "--say-hello", ""), "Say a hello world")
		] + self._args[:]

		self._execs = [
			lambda x:self._sayHello(x)
		] + self._execs[:]

		self._run(args)

	def _sayHello(self, args: list[str]) -> bool:
		print(f"Hello world :D")
		return(True)
'''

class Generate:

	""" Handles the creation of a new tool template file inside the `tools/` directory.

		Attributes:
			__cfg (Config): Configuration instance used to get encoding settings.
			__encoding (str): File encoding used to write the new tool.
			__path (str): Full path to the newly generated tool file.
			__defaultName (str): Default tool name if none is provided by the user.

		Workflow:
			1. Prompt the user for tool name, argument, and alias.
			2. Format and inject them into a Python class template.
			3. Save the new file in the `tools/` directory.

		Raises:
			Exception: If the target tool file already exists.

		Example:
			>>> Generate()
			Tool Name [Hello]: Hello
			Tool Argument [hello]: greet
			Tool Alias [hel]: grt
			# → tools/hello.py generated with CLI command (grt)greet

	"""

	__cfg			= Config()
	__encoding		= "utf-8"
	__path			= abspath("tools/")

	__defaultName	= "Hello"

	def __init__(self):
		__name		= str(input(f" Tool Name [{self.__defaultName}]: ")) or self.__defaultName
		__argument	= str(input(f" Tool Argument [{__name.lower()}]: ")) or __name.lower()
		__alias		= str(input(f" Tool Alias [{__name.lower()[0:3]}]: ")) or __name.lower()[0:3]
		__concat	= f"({__alias}){__argument[3 if(__alias in __argument) else 0:len(__argument)]}"
		__template	= self.__createTemplate(__name, __argument, __alias, __concat)

		self.__encoding	= self.__cfg.getEncoding()
		self.__path		= abspath(f"{self.__path}/{__name.lower()}.py")

		self.__save(__template)

	def __createTemplate(self, name: str, argument: str, alias: str, concat: str) -> str:
		""" Builds the Python class template with user-defined values injected.

			Args:
				name (str): Name of the tool class.
				argument (str): CLI argument associated with the tool.
				alias (str): Short alias for the CLI command.
				concat (str): Concatenation of alias and argument for the command pattern.

			Returns:
				str: A string representing the complete Python file content ready to be written.

		"""

		template = TOOL_TEMPLATE
		template = template.replace("{name}", name)
		template = template.replace("{argument}", argument)
		template = template.replace("{alias}", alias)
		template = template.replace("{concat}", concat)

		return(template)

	def __save(self, template: str) -> bool:
		""" Saves the generated template into the tools directory.

			Args:
				template (str): The full Python code to be written to a new `.py` file.

			Returns:
				bool: True if file was created successfully, False otherwise.

		"""

		try:
			__tools	= listdir(abspath(dirname(self.__path)))
			__tool	= basename(self.__path)

			if(__tool in __tools):
				raise(Exception(f"Tool file {self.__path} already exist"))

			with open(self.__path, "w", encoding=self.__encoding) as toolFile:
				toolFile.write(template)

		except(Exception) as e:
			print(f"{Icons.err}{e}")
			return(False)

		return(True)