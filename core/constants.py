#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Constants package for `core`.

	Constants:
	- LIBS_PATH: Path to the directory where libraries are stored.
	- EXTRACT_PATH: Path to the directory where libraries are unpacked.
	- CMD_CLEAR: Command to clear the terminal screen, platform-dependent.
	- CMD_PYTHON: Command to run Python scripts, platform-dependent.
	- ENABLE_COLOR: Boolean indicating whether color output is enabled, typically set to True on Linux systems.
	- ACCEPT_ENCODING: Contains application encoding, including "ascii", "utf-8", "utf-16", "utf-32".
	- INFO: Contains application information such as version, git commit hash, and other metadata.
	- REGEX_ARGS: A regular expression pattern used to parse and split argument strings into lists.
	- UNITS: Units of measurement for bytes, including b, Kb, Mb, Gb, Tb, etc., to facilitate size conversions.
	- DEBUG: Flag to enable verbose output during tool discovery.

"""

from os import getenv
from os.path import abspath
from platform import system

__isLinux = bool(system() == "Linux")

LIBS_PATH = abspath("libs/")
""" Path to the directory where libraries are stored
"""

EXTRACT_PATH = abspath(f"{LIBS_PATH}/unpacked/")
""" Path to the directory where libraries are unpacked
"""

CMD_CLEAR = "clear" if(__isLinux) else "cls"
""" Command to clear the terminal screen, platform-dependent
"""

CMD_PYTHON = 'python3' if(__isLinux) else 'python'
""" Command to run Python scripts, platform-dependent
"""

ENABLE_COLOR = __isLinux
""" Boolean indicating whether color output is enabled, typically set to True on Linux systems
"""

ACCEPT_ENCODING	: tuple[str] = ("ascii", "utf-8", "utf-16", "utf-32")
""" Contains application encoding, including "ascii", "utf-8", "utf-16", "utf-32"
"""

INFO = dict[str, str]({
	"author": "Florian Cardinal",
	"github": "https://github.com/Tracks12/toolsManager.py",
	"name": "toolsManager.py",
	"version": "0.3",
})
""" Contains application information such as version, git commit hash, and other metadata
"""

REGEX_ARGS = str("\\s(?=(?:[^\"'`]*[\"'`][^\"'`]*[\"'`])*[^\"'`]*$)")
""" A regular expression pattern used to parse and split argument strings into lists
"""

UNITS = tuple[str](("b", "Kb", "Mb", "Gb", "Tb"))
""" Units of measurement for bytes, including b, Kb, Mb, Gb, Tb, etc., to facilitate size conversions
"""

DEBUG = bool(getenv("TM_DEBUG", "0") == "1")
""" Flag to enable verbose output during tool discovery
"""
