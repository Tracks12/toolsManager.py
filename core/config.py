#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Configuration management for tools.

	This module provides functions to load, validate, and access configuration parameters essential
	for the proper operation of tools. It supports various configuration formats and allows centralized
	management of settings.

"""

from json import dump, load
from os.path import abspath

from core.icons import Icons

class Config:
	ACCEPT_ENCODING	: tuple[str] = ("ascii", "utf-8", "utf-16", "utf-32")

	__colors	: bool	= False
	__encoding	: str	= "utf-8"
	__path		: str	= abspath("config.json")
	__splash	: bool	= True

	def __init__(self):
		self.loaded		: bool	= self.__load()

	def __load(self) -> bool:
		""" Private method to load the configuration file

			Returns the loading success statement, e.g. True or False.

		"""

		try:
			with open(self.__path, "r", encoding=self.__encoding) as cfgFile:
				_ = dict[str, str | bool](load(cfgFile))

				self.__colors	= bool(_["colors"])
				self.__encoding	= str(_["encoding"])
				self.__splash	= bool(_["splash"])

		except(Exception):
			print(f"{Icons.err}Config file loading failed")
			return(False)

		return(True)

	def __save(self) -> bool:
		""" Private method to save the current configuration

			Returns the saving success statement, e.g. True or False.

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
		""" Returns the colors display state, e.g. True or False.
		"""

		return(self.__colors)

	def getEncoding(self) -> str:
		""" Returns the encoding state, e.g. "ascii", "utf-8", "utf-16" or "utf-32"
		"""

		return(self.__encoding)

	def getSplash(self) -> bool:
		""" Returns the splash display state, e.g. True or False.
		"""

		return(self.__splash)

	def setColors(self, colors: bool = False) -> bool:
		""" Apply new colors state display on the whole cli

			Parameters:

				colors bool
					the state between True or False

			Return a bool to validate the updating

		"""

		self.__colors = bool(colors)
		self.__save()

		return(True)

	def setEncoding(self, encoding: str = "utf-8") -> bool:
		""" Apply new encoding value on settings

			Parameters:

				encoding str
					the string of the new encoding to use

			Return a bool to validate the updating

		"""

		if(encoding.lower() in self.ACCEPT_ENCODING):
			self.__encoding = str(encoding)
			self.__save()

			return(True)

		return(False)

	def setSplash(self, splash: bool = True) -> bool:
		""" Apply new splash state display on main prompt

			Parameters:

				splash bool
					the state between True or False

			Return a bool to validate the updating

		"""

		self.__splash = bool(splash)
		self.__save()

		return(True)
