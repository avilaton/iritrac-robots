#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib
import urllib2
import cookielib

class Iritrack(object):
	"""Login to Iritrack and make requests"""
	def __init__(self):
		COOKIEFILE = 'cookies.lwp'
		# cj = cookielib.CookieJar()
		# this cookie jar stores the login cookie to a file. Should be checked for existence, 
		# and validity and if it is not valid, ask the user to login again.
		self.cj = cookielib.LWPCookieJar(COOKIEFILE)
		if os.path.isfile(COOKIEFILE):
			self.cj.load()

	def login(self, username, password):
		self._username = username
		self._password = password
		self.connection = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		query = {'username': self._username,'password': self._password, 'valid': 'OK'}
		data = urllib.urlencode(query) 
		response = self.connection.open('http://tracking.iritrack.com/index.php', data)
		html = response.read()
		self.cj.save()
		return self

	def getData(self, fecha_desde, fecha_hasta, vehiculo):
		query = {'page':'positions.xl', 'name':'positions-1',
			'vehicle':vehiculo,
			'date_from':fecha_desde,
			'date_to':fecha_hasta,
			'time_from':fecha_desde, 
			'time_to':fecha_hasta}
		data = urllib.urlencode(query)
		request = self.connection.open('http://tracking.iritrack.com/index.php?'+data)
		return request.read()
