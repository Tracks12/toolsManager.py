#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Abstract base class for color handling.

	Defines abstract classes and interfaces to standardize color management
	across tools. It provides a foundation for implementing color schemes
	and palettes compatible with different output formats.

"""

from json import load
from os.path import abspath

from core.constants import ENABLE_COLOR

try:
	with open(abspath("config.json"), "r", encoding="utf-8") as cfgFile:
		_ = dict[str, str | bool](load(cfgFile))
		ENABLE_COLOR = _["colors"] or ENABLE_COLOR

except(Exception):
	pass

class Colors:

	""" CLI ASCII colors

		Note:
			Colors was disabled if the `colors` of `config.json` was in False or system is Windows

		Attributes:
			bold (str):
			italic (str):
			red (str):
			green (str):
			yellow (str):
			blue (str):
			purple (str):
			cyan (str):
			white (str):
			end (str):

	"""

	bold	= str("\033[1m"		if(ENABLE_COLOR) else "")
	italic	= str("\033[3m"		if(ENABLE_COLOR) else "")

	red		= str("\033[31m"	if(ENABLE_COLOR) else "")
	green	= str("\033[32m"	if(ENABLE_COLOR) else "")
	yellow	= str("\033[33m"	if(ENABLE_COLOR) else "")
	blue	= str("\033[34m"	if(ENABLE_COLOR) else "")
	purple	= str("\033[35m"	if(ENABLE_COLOR) else "")
	cyan	= str("\033[36m"	if(ENABLE_COLOR) else "")
	white	= str("\033[37m"	if(ENABLE_COLOR) else "")

	end		= str("\033[0m"		if(ENABLE_COLOR) else "")
