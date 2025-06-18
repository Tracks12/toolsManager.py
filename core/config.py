#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Configuration management for tools.

	This module provides functions to load, validate, and access configuration parameters essential
	for the proper operation of tools. It supports various configuration formats and allows centralized
	management of settings.

	Constants:
	- ACCEPT_ENCODING: Contains application encoding, including "ascii", "utf-8", "utf-16", "utf-32".

"""

from json import JSONDecodeError, dump, load
from os.path import abspath

from core.icons import Icons

ACCEPT_ENCODING	: tuple[str] = ("ascii", "utf-8", "utf-16", "utf-32")
""" Contains application encoding, including "ascii", "utf-8", "utf-16", "utf-32"
"""

class Config:

	""" Configuration manager object for the program.

		This class handles the loading, saving, and manipulation of a configuration file 
		used by the program. It allows setting and retrieving parameters like CLI color usage, 
		character encoding, and splash screen visibility.

		Attributes:
			loaded (bool): Indicates whether the configuration was successfully loaded at initialization.

		Private Attributes:
			__colors (bool): Whether colored output is enabled in the CLI.
			__encoding (str): Encoding used for reading/writing the configuration file.
			__path (str): Absolute path to the JSON configuration file.
			__splash (bool): Whether the splash screen is enabled at startup.

		Methods:

			getColors() -> bool:
				Returns the current state of CLI color output.

			getEncoding() -> str:
				Returns the currently set encoding.

			getSplash() -> bool:
				Returns whether the splash screen is enabled.

			setColors(colors: bool = False) -> bool:
				Updates the CLI color state and saves the configuration.

			setEncoding(encoding: str = "utf-8") -> bool:
				Updates the encoding value if it's allowed and saves the configuration.

			setSplash(splash: bool = True) -> bool:
				Updates the splash screen setting and saves the configuration.

		Notes:
		- The configuration file must be in JSON format with the keys: "colors", "encoding", and "splash".
		- Accepted encodings are defined in the module-level constant `ACCEPT_ENCODING`.

	"""

	__colors	: bool	= False
	__encoding	: str	= "utf-8"
	__path		: str	= abspath("config.json")
	__splash	: bool	= True

	def __init__(self):
		self.loaded		: bool	= self.__load()

	def __load(self) -> bool:
		""" Private method to load the configuration file

			Returns:
				bool: the loading success statement, e.g. True or False.

		"""

		try:
			with open(self.__path, "r", encoding=self.__encoding) as cfgFile:
				_ = dict[str, str | bool](load(cfgFile))

				self.__colors	= bool(_["colors"])
				self.__encoding	= str(_["encoding"])
				self.__splash	= bool(_["splash"])

		except(FileNotFoundError):
			print(f"{Icons.err}No config file found")
			print(f"{Icons.info}Recreate config file with default settings")
			self.__save()

		except(JSONDecodeError, KeyError, Exception):
			print(f"{Icons.err}Config file loading failed")
			return(False)

		return(True)

	def __save(self) -> bool:
		""" Private method to save the current configuration

			Returns:
				bool: the saving success statement, e.g. True or False.

		"""

		try:
			with open(self.__path, "w", encoding=self.__encoding) as cfgFile:
				_ = dict({
					"colors"	: self.__colors,
					"encoding"	: self.__encoding,
					"splash"	: self.__splash
				})

				dump(dict(_), cfgFile, sort_keys=True, indent=2)

		except(Exception):
			print(f"{Icons.err}Config file saving failed")
			return(False)

		return(True)

	def getColors(self) -> bool:
		""" Get the current colors display settings

			Returns:
				bool: the colors display state, e.g. True or False.

		"""

		return(self.__colors)

	def getEncoding(self) -> str:
		""" Get the current encoding string settings

			Returns:
				str: the encoding state, e.g. "ascii", "utf-8", "utf-16" or "utf-32"

		"""

		return(self.__encoding)

	def getSplash(self) -> bool:
		""" Get the current splash display settings

			Returns:
				bool: the splash display state, e.g. True or False.

		"""

		return(self.__splash)

	def setColors(self, colors: bool = False) -> bool:
		""" Apply new colors state display on the whole cli

			Parameters:
				colors (bool): the state between True or False.

			Returns:
				bool: True to validate the updating, False otherwise.

		"""

		self.__colors = bool(colors)
		self.__save()

		return(True)

	def setEncoding(self, encoding: str = "utf-8") -> bool:
		""" Apply new encoding value on settings

			Parameters:
				encoding (str): the string of the new encoding to use

			Returns:
				bool: True to validate the updating, False otherwise.

		"""

		if(encoding.lower() in ACCEPT_ENCODING):
			self.__encoding = str(encoding)
			self.__save()

			return(True)

		return(False)

	def setSplash(self, splash: bool = True) -> bool:
		""" Apply new splash state display on main prompt

			Parameters:
				splash (bool): the state between True or False

			Returns:
				bool: True to validate the updating, False otherwise.

		"""

		self.__splash = bool(splash)
		self.__save()

		return(True)

def getConfig(cfg: Config, prop: str) -> bool:
	""" Interface to get a config displayer

		Parameters:
			cfg (Config): the config object instance
			prop (str): the string of property to show.
			
				can be "all" to display whole settings values

		Returns:
			bool: True to validate the output, False otherwise.

	"""

	__output = list[str]([])
	__gets = (
		("colors", lambda:cfg.getColors()),
		("encode", lambda:cfg.getEncoding()),
		("splash", lambda:cfg.getSplash())
	)

	if(prop == "all"):
		for r, g in __gets:
			__output.append(f"{r}: {g()}")

	elif(prop in [ r for r, g in __gets ]):
		for r, g in __gets:
			if(prop == r):
				__output.append(g())

	else:
		__output.append(f"{Icons.warn}Uknown value was entered !"[1:-1])

	print("\n".join([ f" {o}" for o in __output ]), end="\n"*2)
	return(True)

def setConfig(cfg: Config, prop: str, val: str) -> bool:
	""" Interface to set a config property on config object

		Parameters:
			cfg (Config): the config object instance
			prop (str): the string of property to update
			val (str): the new value of setting prop to update

		Returns:
			bool: True if the settings is validated, False otherwise.

		Raise an Exception if the property doen't know

	"""

	__isApplied	= bool(False)
	__sets		= (
		("colors", lambda v:cfg.setColors(v.lower() == "true")),
		("encode", lambda v:cfg.setEncoding(v)),
		("splash", lambda v:cfg.setSplash(v.lower() == "true"))
	)

	for r, s in __sets:
		if(prop == r):
			__isApplied = s(val)
			print(f'{Icons.info if(__isApplied) else Icons.err}new {prop} {"is" if(__isApplied) else "is not"} applied')
			return(__isApplied)

	raise(Exception("Uknown property !"))
