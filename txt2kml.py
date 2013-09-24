#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   tra2gpx.py
#	   
#	   Copyright 2012 Gaston Avila <avila.gas@gmail.com>
#	   
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 2 of the License, or
#	   (at your option) any later version.
#	   
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#	   
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.

import os
import optparse
import codecs
import csv
import pystache
import datetime

def getDecimalDegrees(sexDegrees):
	signs = {'S': -1, 'N': 1, 'E':1,'W':-1}
	sign = signs[sexDegrees[-1]]
	sexDegrees = sexDegrees[:-1]
	degrees, minutes = map(float,sexDegrees.split('x'))
	minutes = minutes
	decDegrees = sign*(degrees+1/60.0*minutes)

	return decDegrees

def getTimeStamp(Date, Heure, Mil):
	tstamp = datetime.datetime.strptime(Date+'-'+Heure+'.'+Mil,'%d/%m/%y-%H:%M:%S.%f')
	gpxtstamp = datetime.datetime.strftime(tstamp, "%Y-%m-%dT%H:%M:%S.%fZ")

	return gpxtstamp

def render(values):
	renderer = pystache.Renderer()
	with codecs.open('template.mustache', 'r', 'utf-8') as templateFile:
		template = templateFile.read()
		parsed = pystache.parse(template)

	return renderer.render(parsed, values)

def parse(filename):
	points = []

	with codecs.open(filename,'r') as inFile:
		content = inFile.readlines()
		comment = content.pop(0)
		reader = csv.DictReader(content)
		for dic in reader:
		 	lat, lon = map(getDecimalDegrees,[dic['Latitude'], dic['Longitude']])
		 	timestamp = getTimeStamp(dic['Date'], dic['Heure'], dic['Mil'])
		 	points.append({
		 		'lat': lat, 'lon': lon,
		 		'timestamp': timestamp,
		 		'time': dic['Heure'],
		 		'speed': dic['Vitesse'],
		 		'date': dic['Date'],
		 		'mil': dic['Mil'],
		 		'numtrace': dic['NumTrace']
		 		})

	return comment, points

def convert(filename):
	comment, points = parse(filename)

	print "File header discarded \n"
	
	outFilename = filename.replace('.txt', '.kml')

	with codecs.open(outFilename, 'w', 'utf-8') as outFile:
		outFile.write(render({
			'points': points, 
			'filename': filename,
			'comment': comment
			}))

def main():
	desc = """Transforma TXT de Matias a KML"""
	parser = optparse.OptionParser(description=desc)

	parser.add_option('-t','--todos', dest='todos', default=False, action='store_true', help='Transforma todos los TXT en el directorio')
	parser.add_option('-f','--filename', help='Convierte el archivo a KML',dest='filename')
	(opts, args) = parser.parse_args()
	
	if opts.todos:
		listDir = os.listdir('.')
		for filename in listDir:
			if filename[-4:] == '.txt':
				print 'Convirtiendo: ',filename
				convert(filename)
				
	elif opts.filename:
		gpx = convert(opts.filename)
		return 0
	else:
		print desc,'\n\n Escriba tra2gpx.py -h para ver ayuda\n\n'

if __name__ == '__main__':
	main()
