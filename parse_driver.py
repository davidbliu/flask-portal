import config
import json, httplib, urllib
connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()

def make_parse_request(req_type, url, params = {}):
    params = urllib.urlencode(params)
    connection.request(
        req_type, 
        url+'?%s' % params, 
        '', 
        {
            "X-Parse-Application-Id": config.PARSE_APP_ID,
            "X-Parse-REST-API-Key": config.PARSE_REST_API_KEY
        }
    )
    result = json.loads(connection.getresponse().read())
    return result

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
