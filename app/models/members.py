import config
import json
from ..drivers import parse_driver
import sys

# class Member:
    # def __init__(self, obj):
        # self.name = obj.get('name')
        # self.email = obj.get('email')
        # self.id = obj.get('objectId')
        # self.phone = obj.get('phone')
        # self.committee = obj.get('committee')

def member_email_hash():
    params = {'limit':sys.maxint}
    result =  parse_driver.make_parse_request('GET', '/1/classes/ParseMember', params)
    members = result['results']
    return dict((x['email'], x) for x in members if 'email' in x.keys())

def current_members():
    params = {}
    params['limit'] = sys.maxint
    where = {'latest_semester': config.CURRENT_SEMESTER}
    params['where'] = json.dumps(where)
    result =  parse_driver.make_parse_request('GET', '/1/classes/ParseMember', params)
    return result['results']

def get_committee_members(committee):
    params = {'where': json.dumps({'committee':committee})}
    result =  parse_driver.make_parse_request('GET', '/1/classes/ParseMember', params)
    return result['results']

