# Python travelling library

![GitHub License](https://img.shields.io/github/license/diagmatrix/py-travel)
![Python ^3.10](https://img.shields.io/badge/Python-3.10%2B-blue)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/diagmatrix/py-travel/commit.yml)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/diagmatrix/py-travel)
![PyPI - Status](https://img.shields.io/pypi/status/py_travel)


This is a Python library to use in conjunction with the 
[Google Maps API](https://github.com/googlemaps/google-maps-services-python) (at least for now) in order to plan trips
and much more! It tries to bring a less JSON-oriented way of using the API.

## Roadmap

 1. Distance and timing calculations for trips. ✔️
 2. Geocoding and decoding locations in the globe.
 3. Support for static map images.
 4. Drop `googlemaps` dependency.
 5. Investigate other APIs to use.
 6. ...


## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

### Local installation

#### Prerequisites

You will need the following:

 - Python >= 3.10
 - A Google Maps API key (for testing outside the testing environment)

#### Installing

For a local installation, just clone this repository inside the parent directory of your project.

````bash
git clone https://github.com/diagmatrix/py-travel.git
git checkout main
````

Then install the dependencies of **py-travel**.

````bash
pip install -r requirements.txt
````

And there you have it! You can now use this library freely.

### Installation

This project is available in [PyPy](https://pypi.org/project/py-travel/), so you can install it using
pip.

````bash
pip install py-travel
````

## Usage

There are currently two ways of using the classes provided in the package: by using the built-in
Google Maps API clients or by using the `googlemaps` client directly. The first method will initialize an API client for
each of the classes of **py-travel** that use them, while the second approach will give you more control on which ones
can access it.

### Using built-in client

````python
from py_travel import init_clients
from py_travel.trip import Trip

init_clients(api_key="<API KEY>")  # Initialize all API clients
my_trip = Trip(origin=(39.25, -4.47), destination="Aveiro, Portugal", config={'mode': 'walking'})

# Get the kms between the points
kms = my_trip.distance
````

### Using `googlemaps` directly

````python
from py_travel.trip import Trip
import googlemaps

cli = googlemaps.Client(key="<API KEY>")
Trip.set_client(cli)  # Initialize client for the trip class
my_trip = Trip(origin=(39.25, -4.47), destination="Aveiro, Portugal", config={'mode': 'walking'})

# Get the kms between the points
kms = my_trip.distance
````

## Running the tests

In order to run the tests you will first need to install the python package `pytest`. Then, place yourself in the parent 
branch of the repository and run the following command:

````bash
pytest
````
For linting tests, this project uses the default `ruff` configuration.

## Contributing

Work in progress
