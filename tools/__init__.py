#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Tool registry for `tools`.

	This module registers the available tools by importing them and adding them to a central registry.
	It ensures that all tools are accessible through the `tools` package.

	Constants:
	- TOOLS: A list of `Tool` instances representing all registered tools available in the package.

"""

from core.tool import Tool

from tools.matrix import Matrix
from tools.shell import Shell
from tools.translate import Translate
from tools.wslbuilder import WslBuilder

TOOLS: tuple[Tool] = (
	Matrix,
	Shell,
  Translate,
	WslBuilder,
)
""" Tools registry """
