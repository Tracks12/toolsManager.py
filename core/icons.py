#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Abstract base class for icon handling.

	Defines abstract classes to represent icons used in tools.
	Provides a structure for consistent icon management and allows
	extension for various icon sets or formats.

"""

from core.colors import Colors

class Icons:
	err: str = f" {Colors.bold}{Colors.red}[!]{Colors.end} - "
	warn: str = f" {Colors.bold}{Colors.yellow}/!\\{Colors.end} - "
	info: str = f" {Colors.bold}{Colors.blue}(i){Colors.end} - "
	tips: str = f" {Colors.bold}{Colors.green}(?){Colors.end} - "
	play: str = f" {Colors.bold}{Colors.green}(>){Colors.end} - "