#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Custom exception classes for application-level error handling.

	This module provides a centralized place to define and manage reusable
	exceptions across the codebase. These exceptions are intended to replace
	standard Python or third-party exceptions with more meaningful, context-aware
	errors suited to the specific needs of the application.

	Can include (but is not limited to):
	- Request/HTTP errors
	- Validation or input errors
	- Configuration errors

"""

class RequestError(Exception):

	""" Raised when an HTTP request fails or returns an unexpected response.

		Attributes:
			message (str): Description of the error.
			url (str): URL that triggered the exception.
			status_code (int): HTTP status code (if available).

	"""

	def __init__(self, message: str, url: str = None, status_code: int = None):
		super().__init__(message)

		self.message		= str(message)
		self.url			= str(url)
		self.status_code	= int(status_code)

	def __str__(self) -> str:
		parts = list[str]([ f"RequestError: {self.message}" ])

		if(self.url):
			parts.append(f"URL: {self.url}")

		if(self.status_code):
			parts.append(f"Status: {self.status_code}")

		return("\n\t| ".join(parts))

class ToolInitError(Exception):

	""" Raised when a tool fails to initialize properly.

		Attributes:
			tool_name (str): Name of the tool.
			details (str): Explanation of the failure.

	"""

	def __init__(self, tool_name: str, details: str):
		super().__init__(f"Failed to initialize tool '{tool_name}': {details}")

		self.tool_name	= str(tool_name)
		self.details	= str(details)

class ValidationError(Exception):

	""" Raised when an input or configuration value is invalid.

		Attributes:
			field (str): Name of the field or parameter in error.
			reason (str): Explanation of why the value is invalid.

	"""

	def __init__(self, field: str, reason: str):
		super().__init__(f"Validation failed for '{field}': {reason}")

		self.field	= str(field)
		self.reason	= str(reason)