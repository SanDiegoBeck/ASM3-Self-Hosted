#!/usr/bin/python

"""
    Geocoding module. Understands URLs going to Nominatim and Cloudmade.
"""

import al
import cache
import json
import threading
import urllib2
import utils
from lookups import LOCALE_COUNTRY_NAME_MAP
from sitedefs import BULK_GEO_PROVIDER, BULK_GEO_PROVIDER_KEY

lat_long_lock = threading.Lock()

CLOUDMADE_URL = "http://geocoding.cloudmade.com/{key}/geocoding/v2/find.js?query={q}"
NOMINATIM_URL = "http://nominatim.openstreetmap.org/search?format=json&q={q}"

GEO_LOOKUP_TIMEOUT = 10 # Give up trying to do geo lookup after 10 seconds to prevent blocking

def get_lat_long(dbo, address, town, county, postcode, country = None):
    """
    Looks up a latitude and longitude from an address using GEOCODE_URL
    and returns them as lat,long,(first 3 chars of address)
    Returns None if no results were found.
    NB: dbo is only used for contextual reference in logging, no database
        calls are made by any of this code.
    """

    if address.strip() == "":
        return None

    try:
        # Synchronise this process to a single thread to prevent
        # abusing our geo provider and concurrent requests for the
        # same address when opening an animal with the same
        # original/brought in by owner, etc.
        lat_long_lock.acquire()

        url = ""
        if country is None: 
            country = LOCALE_COUNTRY_NAME_MAP[dbo.locale]

        if BULK_GEO_PROVIDER == "cloudmade":
            q = normalise_cloudmade(address, town, county, postcode, country)
            url = CLOUDMADE_URL.replace("{key}", BULK_GEO_PROVIDER_KEY).replace("{q}", q)
        elif BULK_GEO_PROVIDER == "nominatim":
            q = normalise_nominatim(address, town, county, postcode, country)
            url = NOMINATIM_URL.replace("{q}", q)
        else:
            al.error("unrecognised geo provider: %s" % BULK_GEO_PROVIDER, "geo.get_lat_long", dbo)

        al.debug("looking up geocode for address: %s" % q, "geo.get_lat_long", dbo)
        
        key = "nom:" + q
        if cache.available():
            v = cache.get(key)
            if v is not None:
                al.debug("cache hit for address: %s = %s" % (q, v), "geo.get_lat_long", dbo)
                return v

        jr = urllib2.urlopen(url, timeout = GEO_LOOKUP_TIMEOUT).read()
        j = json.loads(jr)

        latlon = None
        if BULK_GEO_PROVIDER == "cloudmade":
            latlon = parse_cloudmade(dbo, jr, j, q)
        elif BULK_GEO_PROVIDER == "nominatim":
            latlon = parse_nominatim(dbo, jr, j, q)

        # Cache this address/geocode response for an hour
        if cache.available() and latlon is not None:
            cache.put(key, latlon, 3600)

        return latlon

    except Exception,err:
        al.error(str(err), "geo.get_lat_long", dbo)
        return None

    finally:
        lat_long_lock.release()

def parse_nominatim(dbo, jr, j, q):
    if len(j) == 0:
        al.debug("no response from nominatim for %s (response %s)" % (q, str(jr)), "geo.parse_nominatim", dbo)
        return None
    try:
        latlon = "%s,%s,%s" % (str(utils.strip_unicode(j[0]["lat"])), str(utils.strip_unicode(j[0]["lon"])), "na")
        al.debug("contacted nominatim to get geocode for %s = %s" % (q, latlon), "geo.parse_nominatim", dbo)
        return latlon
    except Exception,err:
        al.error("couldn't find geocode in nominatim response: %s, %s" % (str(err), jr), "geo.parse_nominatim", dbo)
        return None

def parse_cloudmade(dbo, jr, j, q):
    if not j.has_key("found") or j["found"] == "0":
        al.debug("no response from cloudmade for %s (response %s)" % (q, str(jr)), "geo.parse_cloudmade", dbo)
        return None
    try:
        point = j["features"][0]["centroid"]["coordinates"]
        latlon = "%s,%s,%s" % (str(point[0]), str(point[1]), "na")
        al.debug("contacted cloudmade to get geocode for %s = %s" % (q, latlon), "geo.parse_cloudmade", dbo)
        return latlon
    except Exception,err:
        al.error("couldn't find geocode in response: %s, %s" % (str(err), jr), "geo.parse_cloudmade", dbo)
        return None

def normalise_nominatim(address, town, county, postcode, country):
    q = address + "," + town + "," + country
    q = utils.html_to_uri(q)
    q = q.replace("&", "").replace("=", "").replace("^", "").replace(".", "")
    q = q.replace("\n", ",").replace(", ", ",").replace(" ", "+")
    q = q.lower()
    dummy = county + postcode
    return q

def normalise_cloudmade(address, town, county, postcode, country):
    q = address + "," + town + "," + county + "," + postcode + "," + country
    q = utils.html_to_uri(q)
    q = q.replace("&", "").replace("=", "").replace("^", "").replace(".", "")
    q = q.replace("\n", ",").replace(", ", ",").replace(" ", "+")
    q = q.lower()
    return q

