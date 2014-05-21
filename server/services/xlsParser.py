#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd

class xlsParser(object):
	"""docstring for Parser"""

	def __init__(self, file_contents, headers=None):
		self.headers = headers
		self.doc = xlrd.open_workbook(file_contents=file_contents)

	def toDictArray(self):
		sheet = self.doc.sheet_by_index(0)
		headers = self.headers
		if not headers:
			headers = [str(sheet.cell_value(0,i)).lower() for i in range(sheet.ncols)]

		rows = []
		for i in range(sheet.nrows-1):
			rows.append([sheet.cell_value(i+1,j) for j in range(sheet.ncols)])
		
		dictArray = []
		for row in rows:
			dictArray.append({k:row[j] for j,k in enumerate(headers)})
			
		return dictArray