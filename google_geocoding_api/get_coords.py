#! /usr/bin/python
# coding=utf-8
"""
Usage:
python get_coords.py _address_

Prerequisites:

1. Obtain a valid API Key from Google.
2. Set the key into GOOGLE_GEOCODING_API_KEY environment variable.

Documentation:
https://developers.google.com/maps/documentation/geocoding/
"""
import os, sys, requests

GOOGLE_GEOCODING_API_KEY = os.getenv('GOOGLE_GEOCODING_API_KEY')
ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json"

payload = dict(key=GOOGLE_GEOCODING_API_KEY, address=sys.argv[1])

r = requests.get(ENDPOINT, params=payload)
print(r.text)

