import parse_driver
import config
import sys, pickle, json

PICKLE_FILE = 'pickle_data.p'


def save_events_hash():
    events_hash = {}
    params = {'limit':sys.maxint, 'where':json.dumps({'google_id':{'$exists':True}})}
    events = parse_driver.make_parse_get_request('/1/classes/ParseEvent', params)['results']
    print events
    for e in events:
        events_hash[e['google_id']] = e
    save_pickle_key('events_hash', events_hash)
    pass

def save_committee_members_hash():
    h = {}
    params = {'limit':sys.maxint}
    params['where'] = json.dumps({'latest_semester': 'Fall 2015'})
    members = parse_driver.make_parse_get_request('/1/classes/ParseMember', params)['results']
    for m in members:
        if m['committee'] not in h.keys():
            h[m['committee']] = []
        h[m['committee']].append(m)
    save_pickle_key('committee_members_hash', h)

def save_member_hash():
    h = {}
    params = {'limit':sys.maxint}
    params['where'] = json.dumps({'email': {'$exists': True}})
    members = parse_driver.make_parse_get_request('/1/classes/ParseMember', params)['results']
    for m in members:
        h[m['email']] = m
    save_pickle_key('member_email_hash', h)

def save_pickle_key(key, obj):
    data = pickle.load(open(PICKLE_FILE, 'rb'))
    data[key] = obj
    pickle.dump(data, open(PICKLE_FILE, 'wb'))

def load_pickle_key(key):
    data = pickle.load(open(PICKLE_FILE, 'rb'))
    return data[key]


if __name__=='__main__':
    save_member_hash()
    # save_committee_members_hash()
    # save_events_hash()
    # h = load_pickle_key('member_email_hash')
    # print h.keys()
