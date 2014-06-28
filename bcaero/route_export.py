#!/usr/bin/env python
"""
bcaero.route_export: GeoJSON flight route export
Copyright 2014 Michael Farrell <http://micolous.id.au>

License: 3-clause BSD, see COPYING

On-board tileserver: http://map.boardconnect.aero/tiles/
"""

from __future__ import absolute_import
from .map import route
import argparse, geojson


def route_export(output_fh):
	output_layer = geojson.FeatureCollection([])
	# assume WGS84 CRS
	output_layer.crs = geojson.crs.Named('urn:ogc:def:crs:OGC:1.3:CRS84')
	ls = geojson.LineString()

	for point in route():
		ls.coordinates.append([point.longitude, point.latitude])

	output_layer.features.append(geojson.Feature(id=1, geometry=ls))
	geojson.dump(output_layer, output_fh)


def main():
	parser = argparse.ArgumentParser()
	
	parser.add_argument('output',
		type=argparse.FileType('wb'),
		nargs=1
	)

	options = parser.parse_args()

	route_export(options.output[0])

if __name__ == '__main__':
	main()
