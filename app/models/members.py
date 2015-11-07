from ..drivers import parse_driver
import sys

def all_members():
    params = {}
    params['limit'] = sys.maxint
    result =  parse_driver.make_parse_request('GET', '/1/classes/ParseMember', params)
    return result['results']
