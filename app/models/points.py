
import config
import json
from ..drivers import parse_driver
import sys


def get_member_attendance(email):
    params = {'limit': sys.maxint}
    params['where'] = json.dumps({
        'member_email': email
        })
    result = parse_driver.make_parse_request('GET','/1/classes/ParseEventMember', params)
    return result['results']

def get_events_by_id(eids):
    params = {'limit':sys.maxint,
            'where': json.dumps( {'google_id': {'$in': eids}})}

    result = parse_driver.make_parse_request('GET','/1/classes/ParseEvent', params)
    return result['results']

def get_member_points(email):
    attendance = get_member_attendance('davidbliu@gmail.com')
    eids = [x['event_id'] for x in attendance]
    events = get_events_by_id(eids)
    points = sum([x['points'] for x in events if 'points' in x.keys()])
    return {'points':points, 'attendance':events}

