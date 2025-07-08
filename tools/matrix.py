#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/matrix.py

from keyboard import is_pressed, on_press
from os import system as shell
from platform import system
from random import randrange
from time import sleep
from traceback import format_exc

from core.colors import Colors
from core.constants import CMD_CLEAR
from core.tool import Tool

class Matrix(Tool):
	command	= (("matrix", "mat"), "(mat)rix")
	name	= "Matrix"
	path	= __file__
	version	= "0.3a"

	__sleep = 0

	def __init__(self, args: list[str]):
		self._args	= [
			(("-n", "--new", "<x> <y>"), "Create a matrix with custom dimensions"),
			(("-r", "--random", "<x> <y> <i>"), "Create a matrix with placed random point")
		]

		self._execs	= [
			lambda x:self._new(x),
			lambda x:self._random(x)
		]

		super().__init__()
		self._run(args, lambda:self._helper())

	def __addRandomPoint(self, matrix: list[list[int]]) -> list[list[int]]:
		_dim = (len(matrix[0]), len(matrix))

		while(True):
			x, y = self.__randomXY(_dim[0], _dim[1])

			if(not matrix[y][x]):
				matrix = self.__setPoint(matrix, x, y, 1)
				break

		return(matrix)

	def __createMatrix(self, x: int, y: int) -> list[list[int]]:
		_matrix	= list[list[int]]([])

		for i in range(0, int(y)):
			_matrix.append([])

			for j in range(0, int(x)):
				_matrix[i].append(0)

		return(_matrix)

	def __displayMatrix(self, matrix: list[list[int]], stats: dict = {}) -> None:
		_output	= list[str]([])
		_values	= sum([ value for x in matrix for value in x ])
		_cells	= int(len(matrix)*len(matrix[0]))
		_		= str(" "*2)
		_fill	= str(round((_values/_cells)*100, 2))

		for i, row in enumerate(matrix):
			_output.append("")
			_sum = sum(row)
			_output[i] += f" [ {' '.join([ f'{Colors.cyan}{r}{Colors.end}' for r in row ])} ] = {Colors.red if(_sum < (len(matrix[0])/3)) else Colors.green}{_sum}{Colors.end}{' '*(2-len(str(_sum)))}"

		if(len(matrix) > 3):
			_output[-4] += f"{_}{'Dim':<{7}}: {len(matrix)}x{len(matrix[0])}"
			_output[-3] += f"{_}{'Cells':<{7}}: {_cells}"
			_output[-2] += f"{_}{'Points':<{7}}: {_values}"
			_output[-1] += f"{_}{'Filled':<{7}}: {str(_fill):<{5}} %"

			if(stats):
				_output[0] += f"{_}{'Iteration(s)':<{13}}: {stats['Iterations']}"

		print(f"\n".join(_output))

	def __label(self, text: str, dim: tuple[int] = (1, 1), color: Colors = "") -> None:
		_higher = "\x1b[A"
		_lower = "\x1b[B"

		_ = str(' '*int((dim[1]+(dim[1]-1))/2))[int((len(text)-1)/2)-(1 if(len(text)%2) else 0):-1]

		print(_higher*int(dim[0]/2), end="\r")
		print(f" [ {_}{color}{text}{Colors.end}{_}{'' if(len(text)%2) else ' '} ] ")
		print(_lower*int((dim[0]/2)-1), end="\r")

	def __onKeyPress(self, keys: list[bool]) -> None:
		keys[0] = True

	def __randomXY(self, xMax: int = 5, yMax: int = 5) -> tuple[int]:
		return(randrange(0, xMax), randrange(0, yMax))

	def __removeRandomPoint(self, matrix: list[list[int]]) -> list[list[int]]:
		_dim = (len(matrix[0]), len(matrix))

		while(True):
			x, y = self.__randomXY(_dim[0], _dim[1])

			if(matrix[y][x]):
				matrix = self.__setPoint(matrix, x, y, 0)
				break

		return(matrix)

	def __setPoint(self, matrix: list[list[int]], x: int, y: int, value: int = 1) -> list[list[int]]:
		matrix[y][x] = int(value)

		return(matrix)

	def _new(self, args: list[str]) -> list[list[int]]:
		shell(CMD_CLEAR)
		_matrix = self.__createMatrix(int(args[0]), int(args[1]))
		self.__displayMatrix(_matrix)

		return(_matrix)

	def _random(self, args: list[str]) -> None:
		try:
			_keyPressed = [ False ]
			_matrix = self._new(args)
			_dim = (len(_matrix), len(_matrix[0]))
			input("Press key to start ...")
			shell(CMD_CLEAR)

			_execs = (
				lambda x:self.__addRandomPoint(x),
				lambda x:self.__removeRandomPoint(x)
			)

			_higher = "\x1b[A"
			_hook = on_press(lambda e:self.__onKeyPress(_keyPressed))

			_iterations = int(args[2] if(len(args) == 3) else 3)
			for i in range(0, _iterations):
				_stats = {
					"Iterations": f"{i+1}/{_iterations}",
				}

				while(sum([ value for x in _matrix for value in x ]) != (len(_matrix)*len(_matrix[0]), 0)[i%2]):
					_matrix = _execs[i%2](_matrix)
					print(_higher*(len(_matrix)+1), end="\r")
					self.__displayMatrix(_matrix, _stats)

					if(_keyPressed[0]):
						_keyPressed[0] = False

						if(is_pressed("space")):
							self.__label("PAUSED", _dim, Colors.yellow)
							input("Press enter to continue ...")
							shell(CMD_CLEAR)

						if(is_pressed("esc")):
							raise(KeyboardInterrupt)

					sleep(self.__sleep)

			self.__label("FINISHED", _dim, Colors.green)

		except(KeyboardInterrupt):
			self.__label("STOPPED", _dim, Colors.red)

		except(Exception):
			print(format_exc())

		finally:
			if(_hook):
				_hook()
