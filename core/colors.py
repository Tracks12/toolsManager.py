#!/bin/python3
# -*- coding: utf-8 -*-

from platform import system

class Colors:
	if(system() == "Linux"):
		bold	: str	= "\033[1m"
		italic	: str	= "\033[3m"

		red		: str	= "\033[31m"
		green	: str	= "\033[32m"
		yellow	: str	= "\033[33m"
		blue	: str	= "\033[34m"
		purple	: str	= "\033[35m"
		cyan	: str	= "\033[36m"
		white	: str	= "\033[37m"

		end		: str	= "\033[0m"

	else:
		bold = italic = end = str("")
		red = green = yellow = blue = purple = cyan = white = str("")