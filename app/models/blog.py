
import config
import json
from ..drivers import parse_driver
import sys

def get_all_posts():
    params = {'limit':sys.maxint, 'order': '-updatedAt'}
    result = parse_driver.make_parse_request('GET','/1/classes/BlogPost', params)
    return result['results']

