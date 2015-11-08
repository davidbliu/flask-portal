import config
import json
from ..drivers import parse_driver
import sys

def get_tabling_slots():
    params = {}
    r = parse_driver.make_parse_request('GET', '/1/classes/ParseTablingSlot', params)
    return r['results']
