#!/bin/python3
# -*- coding: utf-8 -*-

from core.tool import Tool

from tools.matrix import Matrix
from tools.shell import Shell
from tools.wslBuilder import WslBuilder

TOOLS: list[Tool] = [
	Matrix,
	Shell,
	WslBuilder,
]
