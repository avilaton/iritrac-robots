#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib
import urllib2
import cookielib

COOKIEFILE = 'cookies.lwp'

def main():
	# cj = cookielib.CookieJar()
	# this cookie jar stores the login cookie to a file. Should be checked for existence, 
	# and validity and if it is not valid, ask the user to login again.
	cj = cookielib.LWPCookieJar(COOKIEFILE)
	if os.path.isfile(COOKIEFILE):
		cj.load()
	
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	username = raw_input("Please enter your username: ")
	password = raw_input("Please enter your password: ")
	query = {'username': username,'password': password,'valid': 'OK'}
	data = urllib.urlencode(query)

	response = opener.open('http://tracking.iritrack.com/index.php', data)
	html = response.read()

	cj.save()
	query = {'page':'positions.xl','name':'positions-603','vehicle':'603',
	'date_from':1363910400,'date_to':1395532799,'time_from':1363910400,'time_to':1395532799}
	data = urllib.urlencode(query)

	excelResponse = opener.open('http://tracking.iritrack.com/index.php?'+data)
	#excelResponse = opener.open('http://tracking.iritrack.com/index.php?page=positions.xl&name=positions-603&vehicle=603&date_from=1363910400&date_to=1395532799&time_from=1363910400&time_to=1395532799')
	xls = excelResponse.read()

	with open('data.xls','wb') as f:
		f.write(xls)

if __name__ == '__main__':
	main()