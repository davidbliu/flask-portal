def test():
    where = {}
    where['email'] = {'$in': ['davidbliu@gmail.com', 'alice.sun94@gmail.com']}
    where = json.dumps(where)
    params = {}
    params['where'] = where

    result = make_parse_request('GET', '/1/classes/ParseMember', params)
    print result['results']
    print len(result['results'])

    r = make_parse_request('GET', '/1/classes/ParseEvent')
    print r['results']


if __name__ == '__main__':
    print 'Running parse_driver.py'
    test()
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

def count_golinks():
    params = {'count':1}
    r = parse_driver.make_parse_request('GET', '/1/classes/ParseGoLink', params)
    return r['count'] 

def get_with_tags(tags):
    params = {}
    where = {}
    where['tags'] = {'$all':tags}
    where = json.dumps(where)
    params['where']=where
    results = parse_driver.make_parse_request('GET', '/1/classes/ParseGoLink', params)
    return results['results']

def recent_golinks(page = 0):
    params = {}
    params['order'] = '-createdAt'
    params['skip']=page*100
    r = parse_driver.make_parse_request('GET', '/1/classes/ParseGoLink', params)
    results = r['results']
    for x in results:
        if 'num_clicks' not in x.keys():
            x['num_clicks']=0
    return results

def popular_golinks():
    params = {'order': '-num_clicks'}
    results = parse_driver.make_parse_request('GET', '/1/classes/ParseGoLink', params)
    return results['results']

def search_golinks(searchTerm):
    where = {'$or':[{'key':{'$regex':searchTerm}},
        {'description':{'$regex':searchTerm}},
        {'tags':{'$in':[searchTerm]}}
        ]}
    params = {'where':json.dumps(where)}
    results = parse_driver.make_parse_request('GET', '/1/classes/ParseGoLink', params)
    return results['results']


""" POST Requests """

def create_golink(form):
    print 'this is form'
    print form
    print form.get('key')
    print form['key']
    print 'for mke '
    golink = {'key': form.get('key'),
            'url': form.get('url'),
            'member_email': form.get('member_email'),
            'description': form.get('description'),
            'permissions': form.get('permissions', 'Anyone'),
            'tags': form.get('tags', [])
            }
    parse_driver.make_parse_post_request('/1/classes/ParseGoLink', golink)

def update_golinks(updates):
    pass


