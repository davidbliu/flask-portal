import json
from ..drivers import parse_driver

def test():
    r = parse_driver.make_parse_request('GET', '/1/classes/ParseMember')
    print r['results']

def create_golink(key, url, member_email, description = '', tags = [], permissions = 'Anyone'):
    golink = {}
    golink['key'] = key
    golink['url'] = url
    golink['tags'] = tags
    golink['permissions'] = permissions
    golink['member_email'] = member_email
    results = parse_driver.make_parse_post_request('/1/classes/ParseGoLink', golink)

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
