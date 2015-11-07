import json
from ..drivers import parse_driver

def test():
    r = parse_driver.make_parse_request('GET', '/1/classes/ParseMember')
    print r['results']


def get_with_tags(tags):
    params = {}
    where = {}
    where['tags'] = {'$all':tags}
    where = json.dumps(where)
    params['where']=where
    results = parse_driver.make_parse_request('GET', '/1/classes/ParseGoLink', params)
    return results['results']

def recent_golinks():
    params = {}
    results = parse_driver.make_parse_request('GET', '/1/classes/ParseGoLink', params)
    return results['results']
