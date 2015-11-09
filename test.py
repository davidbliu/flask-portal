import app.models.golinks as gl
import app.test as t
import app.models.members as mem
import app.models.tabling as Tabling
import app.models.points as Points
import app.models.blog as Blog

import app.drivers.redis_driver as redis
def test_gl():
    golinks = gl.recent_golinks()
    print [x.url for x in golinks]

def test_members():
    members = mem.get_committee_members('HT')
    print [x['name'] for x in members]

def test_tabling():
    ts = Tabling.get_tabling_slots()
    print ts

def test_points():
    p = Points.get_member_attendance('davidbliu@gmail.com')
    eids = [x['event_id'] for x in p]
    print 'eids were'+str(eids)
    p = Points.get_events_by_id(eids)
    total = sum([x['points'] for x in p if 'points' in x.keys()])
    print p
    print total

def test_blog():
    p = Blog.get_all_posts()
    print p

# test_gl()

# print redis.get('alskfjls')
# print 'recent golinks:'
# print redis.get('recent_golinks')

test_blog()
