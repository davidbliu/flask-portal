import json
from ..drivers import parse_driver
from ..drivers import redis_driver

class GoLink:
    def __init__(self, obj):
        print obj
        self.id = obj.get('objectId')
        self.key = obj.get('key')
        self.url = obj.get('url')
        self.permissions = obj.get('permissions')
        self.createdAt = obj.get('createdAt')
        self.tags = obj.get('tags')
        self.member_email = obj.get('member_email')
    def to_json(self):
        js = {}
        js['id'] = self.id
        js['key'] = self.key
        js['url'] = self.url
        js['permissions'] = self.permissions
        js['createdAt'] = self.createdAt
        js['tags'] = self.tags
        js['member_email'] = self.member_email
        return js
    def __repr__(self):
        return self.key

def test():
    r = parse_driver.make_parse_request('GET', '/1/classes/ParseMember')
    print r['results']

# return golinks that this member has permissions to view
def filter_permissions(golinks, email, position):
    return golinks

def get_with_key(key):
    params = {}
    where = {'key': key}
    params['where'] = json.dumps(where)
    r = parse_driver.make_parse_request('GET', '/1/classes/ParseGoLink', params)
    return r['results']

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
    params['order'] = '-createdAt'
    r = parse_driver.make_parse_request('GET', '/1/classes/ParseGoLink', params)
    objs = r['results']
    redis_driver.r.set('recent_golinks', [GoLink(x) for x in objs])
    return [GoLink(x) for x in objs]

def popular_golinks():
    params = {'order': '-num_clicks'}
    results = parse_driver.make_parse_request('GET', '/1/classes/ParseGoLink', params)
    return results['results']

def search_golinks(searchTerm):
    params = {}
    results = parse_driver.make_parse_request('GET', '/1/classes/ParseGoLink', params)
    return results['results']


""" POST Requests """

def create_golink(key, url, member_email, description = '', tags = [], permissions = 'Anyone'):
    golink = {}
    golink['key'] = key
    golink['url'] = url
    golink['tags'] = tags
    golink['permissions'] = permissions
    golink['member_email'] = member_email
    results = parse_driver.make_parse_post_request('/1/classes/ParseGoLink', golink)

def edit_golinks(key, data):
    print 'not implemented yet'

