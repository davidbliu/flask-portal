import app.models.golinks as gl
import app.test as t
import app.models.members as mem
import app.drivers.redis_driver as redis
def test_gl():
    golinks = gl.recent_golinks()
    print [x.url for x in golinks]

test_gl()
print redis.get('alskfjls')
print 'recent golinks:'
print redis.get('recent_golinks')
