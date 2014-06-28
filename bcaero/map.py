#!/usr/bin/env python
"""
bcaero.map
Gets mapping data from BoardConnect

Copyright 2014 Michael Farrell <http://micolous.id.au>

Tile server: http://map.boardconnect.aero/tiles/

"""

import requests

class Position(object):
	def __init__(self, input_data):
		self._data = input_data

	@property
	def latitude(self):
		return self._data['lat']

	@property
	def longitude(self):
		return self._data['lon']

	# TODO: implement __geo__ interface
	def __str__(self):
		return '<Position: %f,%f>' % (self.latitude, self.longitude)

class FlightStatus(Position):
	@property
	def altitude_ft(self):
		"""
		Returns the current altitude of the plane, in feet.
		"""
		return int(self._data['altitude'])

	@property
	def altitude_m(self):
		return int(self.altitude_ft * 0.3048)

	@property
	def ground_speed_kt(self):
		"""
		Returns the current ground speed of the aircraft, in knots.
		"""
		return int(self._data['groundSpeed'])

	@property
	def ground_speed_mph(self):
		return self.ground_speed_kt * 1.15078

	@property
	def ground_speed_kmh(self):
		return self.ground_speed_kt * 1.852

	@property
	def flight_number(self):
		"""
		Returns the flight number of the aircraft.
		"""
		return self._data['flightNumber']

	@property
	def heading(self):
		"""
		Returns the heading of the aircraft, in degrees.
		"""
		return self._data['heading']

	@property
	def temperature_c(self):
		"""
		External aircraft temperature, in Celsius (MovingMap.js:35)
		"""
		return self._data['temperature']

	@property
	def temperature_f(self):
		return self.temperature_c * (9./5.) + 32

	def __str__(self):
		return '<FlightStatus: flight=%r, temp=%.2f C, hdg=%.2f, spd=%d kt, alt=%d ft, pos=%f,%f>' % (
			self.flight_number,
			self.temperature_c,
			self.heading,
			self.ground_speed_kt,
			self.altitude_ft,
			self.latitude,
			self.longitude
		)


def current_position():
	"""
	Gets the current position of the flight.
	
	Throws exceptions if you are not on a flight or the data is not available.
	
	:returns: :class:`FlightStatus` indicating the current status of the flight
	"""
	response = requests.get('http://map.boardconnect.aero/api/flightdata')

	# NOTE: the ASP.net web service providing this data passes the heading,
	# latitude and longitude of the aircraft as a float, not a decimal type.
	# As a result, the accuracy of the data is reduced and so don't bother
	# putting it in a Decimal in our code.
	flight_data = response.json()

	return FlightStatus(flight_data)


def route():
	"""
	Gets the route of the flight.
	
	:returns: List of :class:`Position`
	"""
	response = requests.get('http://map.boardconnect.aero/api/route')
	return [Position(x) for x in response.json()]


def ping():
	"""
	"Pings" the API endpoint.
	
	Throws an exception on connectivity error or bad response.
	"""
	response = requests.get('http://map.boardconnect.aero/api/ping').read()
	assert response == '"ping"', 'Unexpected response: %r' % response


if __name__ == '__main__':
	print current_position()