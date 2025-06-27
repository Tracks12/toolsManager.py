# CONTRIBUTING

[Back to index](README.md)

## Coding Guidelines – toolsManager.py

This document defines the best development practices to follow when contributing to the project.

### 📁 Project Structure

- `main.py`: Main entry point.
- `setup.py`: Installer for project-specific dependencies (`.rar` file).
- `core/`: Contains the core modules (configuration, tool management, etc.).
- `tools/`: Contains each tool, 1 `.py` file per tool.
- `dev`: Continuous development branch.
- `master`: Stable branch only.

### 🧱 Tool Writing Convention

- Each tool must:
	- be in a separate file under `tools/`,
	- have the same name as the class (in PascalCase),
	- inherit from core.tool.Tool,
	- must implement the run() method.

- Inheriting from Tool ensures consistent behavior and facilitates the overall management of tool modules.

#### ✅ Minimum valid example:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/hello.py

from core.tool import Tool

class Hello(Tool):
	""" Say hello to the user
	"""

	command	= (("hello", "hel"), "(hel)lo")
	name	= "Hello"
	path	= __file__
	version	= "0.1a"

	def __init__(self, args: list[str]):
		self._args	= [
			(("-s", "--say-hello", "<user>"), "Say hello to the user")
		]

		self._execs = [
			lambda x:self._sayHello(x)
		]

		super().__init__()
		self._run(args)

	def _sayHello(self, args: list[str]) -> bool:
		print(f"Hello world :D")
		return(True)
```

#### 🚨 Non-compliant example:

```python
# ❌ Missing environment & encoding declarations

# tools/hello.py

# ❌ Missing inheritance from Tool
class Hello:

	# ❌ Missing Tool porperties command, name, path & version

	def __init__(self, a: list[str]): # ❌ Naming mistake on args parameters
		super().__init__() # ❌ Bad super init position

		# ❌ Missing init properties _args & _execs

		self.hey(a) # ❌ Missing _run(args) method

	# ❌ Bad name compliance
	def hey(self, args: list[str]) -> bool:
		print(f"Goodbye world :(")
		return(True)
```

> [!Tip]
> You can create you own tool by typing `$ python main.py -g`

## 🧪 Tests

- Tests are currently manual.
- Adding a tool must be followed by a test in main.py or CLI.
- Errors must be handled properly via try/except.

## 🧰 Coding Conventions

- Follow PEP8 conventions.
- Strong typing is recommended (str, bool, etc.).
- Each public method must have a clear docstring. - Preferred use of logging over print() (if applicable).

## 🔁 GitFlow

- Each new tool or feature must start from a dedicated branch from dev.
- Branches must be named `feature/tool-name` or `hotfix/issue`.
- Commit must be named like these:
  - `doc(scope): ...` for documentation updates
  - `feat(scope): ...` for feature developed
  - `fix(scope): ...` for fix applied
  - `refacto(scope): ...` for refactoring or code optimization
- Always rebase before merging to dev.
- The master branch should only receive tested and stable code.
- Each merge to master must be accompanied by a versioned tag (v1.2.0, etc.).

## 🚀 Release

- When merging to master, add a Git tag and a GitHub release if possible.
- Releases must contain:
	- a brief changelog,
	- a list of added/modified tools,
	- a version number.

## 🤝 Contribution

- Forks, pull requests, and issues welcome.
- Please respect the structure and naming, and keep the code readable.

[Back to index](README.md)
