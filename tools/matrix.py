#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tools/matrix.py

from os import system as shell
from random import randrange
from time import sleep
from traceback import format_exc

from core.colors import Colors
from core.tool import Tool

class Matrix(Tool):
	command	= (("matrix", "mat"), "(mat)rix")
	name	= "Matrix"
	path	= __file__
	version	= "0.1a"

	def __init__(self, args: list[str]):
		super().__init__()

		self._args	= [
			(("-n", "--new", "<x> <y>"), "Create a matrix with custom dimensions"),
			(("-r", "--random", "<x> <y> <i>"), "Create a matrix with placed random point")
		] + self._args[:]

		self._execs = [
			lambda x:self._new(x),
			lambda x:self._random(x)
		] + self._execs[:]

		self._run(args)

	def _new(self, args: list[str]) -> list[list[int]]:
		shell("clear")
		matrix = self.__createMatrix(int(args[0]), int(args[1]))
		self.__displayMatrix(matrix)

		return(matrix)

	def _random(self, args: list[str]) -> None:
		try:
			matrix = self._new(args)
			input("\nPress key to start ...")

			_exec = (
				lambda x:self.__addRandomPoint(x),
				lambda x:self.__removeRandomPoint(x)
			)

			x = int(args[2] if(len(args) == 3) else 3)
			for i in range(0, x):
				stats = {
					"Iterations": f"{i+1}/{x}"
				}

				while(sum([ value for x in matrix for value in x ]) != (len(matrix)*len(matrix[0]), 0)[i%2]):
					shell("clear")
					matrix = _exec[i%2](matrix)
					self.__displayMatrix(matrix, stats)
					sleep(.05)

		except:
			print(format_exc())

	def __setPoint(self, matrix: list[list[int]], x: int, y: int, value: int = 1) -> list[list[int]]:
		matrix[y][x] = round(value, 2)

		return(matrix)

	def __randomXY(self, xMax: int = 5, yMax: int = 5):
			x = randrange(0, xMax)
			y = randrange(0, yMax)

			return x, y

	def __addRandomPoint(self, matrix: list[list[int]]) -> list[list[int]]:
		dim = (len(matrix[0]), len(matrix))
		x, y = self.__randomXY(dim[0], dim[1])

		while(True):
			x, y = self.__randomXY(dim[0], dim[1])

			if(not matrix[y][x]):
				matrix = self.__setPoint(matrix, x, y, 1)
				break

		return(matrix)
	
	def __removeRandomPoint(self, matrix: list[list[int]]) -> list[list[int]]:
		dim = (len(matrix[0]), len(matrix))
		x, y = self.__randomXY(dim[0], dim[1])

		while(True):
			x, y = self.__randomXY(dim[0], dim[1])

			if(matrix[y][x]):
				matrix = self.__setPoint(matrix, x, y, 0)
				break

		return(matrix)

	def __createMatrix(self, x: int, y: int) -> list[list[int]]:
		matrix = list[list[int]]([])

		for i in range(0, int(y)):
			matrix.append([])

			for j in range(0, int(x)):
				matrix[i].append(0)

		return(matrix)

	def __displayMatrix(self, matrix: list[list[int]], stats: dict = {}) -> None:
		output = list[str]([])
		values = sum([ value for x in matrix for value in x ])
		cells  = int(len(matrix)*len(matrix[0]))
		_ = str(" "*2)
		_fill = str(round((values/cells)*100, 2))

		for i, row in enumerate(matrix):
			output.append("")
			_sum = sum(row)

			output[i] += f" {row} = {Colors.red if(_sum < (len(matrix[0])/3)) else Colors.green}{_sum}{Colors.end}{' '*(2-len(str(_sum)))}"

		if(len(matrix) > 2):
			output[-3] += f"{_}Points : {values}"
			output[-2] += f"{_}Cells  : {cells}"
			output[-1] += f"{_}Filled : {_fill}{' '*(3-len(_fill))} %"

		if(stats):
			output[0] += f"{_}Iteration(s) : {stats['Iterations']}"

		print(f"\n".join(output))