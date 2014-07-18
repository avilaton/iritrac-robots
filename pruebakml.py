import simplekml
kml = simplekml.Kml()
pnt = kml.newpoint(name='A Point')
pnt.coords = [(31 0.084 S,064 51.700 W)]
print kml.kml()