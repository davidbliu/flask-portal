from ..drivers import parse_driver

def test():
    r = parse_driver.make_parse_request('GET', '/1/classes/ParseMember')
    print r['results']


