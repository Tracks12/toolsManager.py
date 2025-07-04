#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Tool registry for `tools`.

	This module registers the available tools by importing them and adding them to a central registry.
	It ensures that all tools are accessible through the `tools` package.

	Constants:
	- TOOLS: A list of `Tool` instances representing all registered tools available in the package.

"""

from importlib import import_module
from inspect import getmembers, isclass
from pkgutil import iter_modules

from core.constants import DEBUG
from core.tool import Tool

if(DEBUG):
	print("🔍 [tools] Starting dynamic tool discovery...")

TOOLS: list[Tool] = []

for _, module, _ in iter_modules(__path__):
	if(module == "__init__"):
		continue

	tool = str(f"{__name__}.{module}")
	
	try:
		module = import_module(tool)

		for _, obj in getmembers(module, isclass):
			if(issubclass(obj, Tool) and obj is not Tool):
				TOOLS.append(obj)

				if(DEBUG):
					print(f"🔧 [tools] Registered tool: {obj.__name__}")
	
	except(Exception) as e:
		if(DEBUG):
			print(f"❌ [tools] Failed to import tool '{tool}': {e}")

TOOLS: tuple[Tool] = tuple(TOOLS)
""" Tools registry
"""

if(DEBUG):
	print(f"📦 [tools] Total tools loaded: {len(TOOLS)}\n")
