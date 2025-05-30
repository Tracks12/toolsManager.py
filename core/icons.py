#!/bin/python3
# -*- coding: utf-8 -*-

from core.colors import Colors

class Icons:
	warn: str = f" {Colors.bold}{Colors.red}[!]{Colors.end} - "
	info: str = f" {Colors.bold}{Colors.blue}(i){Colors.end} - "
	tips: str = f" {Colors.bold}{Colors.green}(?){Colors.end} - "
	play: str = f" {Colors.bold}{Colors.green}(>){Colors.end} - "