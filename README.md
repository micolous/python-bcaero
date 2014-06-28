# python-bcaero #

Library/tools to get data from Virgin Australia (and possibly other [Lufthansa oardConnect](https://www.lhsystems.com/solutions-services/airline-solutions-services/inflight-entertainment/boardconnect.html) systems) in-flight tracking systems.

Normally this is available at http://map.boardconnect.aero/

Flight destination tracking is currently unsupported, as VA do not enable this on their flights.

You will need to connect to the plane's WiFi network (normally named the same as your airline) and wait for the plane to reach cruising altitude before this information will be available.  Due to CASA regulations, I have not tested this system during takeoff or landing.

## API ##

Various map functions are available via the `bcaero.map` module.

### `bcaero.map.current_position()` ###

Gets the current position of the aircraft, as `bcaero.map.FlightStatus`.

### `bcaero.map.route()` ###

Returns the route of the aircraft, as a `list` of `bcaero.map.Position`.

### `bcaero.map.ping()` ###

"Pings" the API endpoint.  Throws exceptions on failure.

## Command-line tools / test programs ##

Several tools are available by using `python -m bcaero...` syntax.

### `bcaero.map` ###

*Usage*: `python -m bcaero.map`

Displays the flight number, current location, heading, speed, altitude, and outside temperature of the plane.

### `bcaero.route_export` ###

*Usage*: `python -m bcaero.route_export track.geojson`

This tool can export your plane's current track as a GeoJSON shapefile, with the route as a `LineString`.  This can then be used inside of other applications, for example, QGIS.

Because this information is not available inside of the web service, there is no information about times or speeds on the tracks.
