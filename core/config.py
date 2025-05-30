#!/bin/python3
# -*- coding: utf-8 -*-

from json import dump, load
from os.path import abspath

from core.icons import Icons

class Config:
	ACCEPT_ENCODING	: tuple[str] = ("ascii", "utf-8", "utf-16", "utf-32")

	__encoding	: str	= "utf-8"
	__path		: str	= abspath("config.json")
	__splash	: bool	= True

	def __init__(self):
		self.loaded		: bool	= self.__load()

	def __load(self) -> bool:
		try:
			with open(self.__path, "r", encoding=self.__encoding) as cfgFile:
				_ = dict[str, str | bool](load(cfgFile))

				self.__encoding	= str(_["encoding"])
				self.__splash	= bool(_["splash"])

		except Exception:
			print(f"{Icons.warn}Config file loading failed")
			return(False)

		return(True)

	def __save(self) -> bool:
		try:
			with open(self.__path, "w", encoding=self.__encoding) as cfgFile:
				_ = dict({
					"encoding"	: self.__encoding,
					"splash"	: self.__splash
				})

				dump(dict(_), cfgFile, sort_keys=True, indent=2)

		except Exception:
			print(f"{Icons.warn}Config file saving failed")
			return(False)

		return(True)

	def getEncoding(self) -> str:
		return(self.__encoding)

	def getSplash(self) -> bool:
		return(self.__splash)

	def setEncoding(self, encoding: str = "utf-8") -> bool:
		if(encoding.lower() in self.ACCEPT_ENCODING):
			self.__encoding = encoding
			self.__save()

			return(True)

		return(False)

	def setSplash(self, splash: bool = True) -> bool:
		self.__splash = splash
		self.__save()

		return(True)
