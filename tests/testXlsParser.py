
import unittest
from server.services import xlsParser

class testXlsParser(unittest.TestCase):
	def testData(self):
		f = open('tests/data.xls')
		xls = xlsParser(f.read())
		d = xls.toDictArray()
		self.assertTrue(type(d), list)
