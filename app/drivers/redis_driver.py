import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def set(key, obj):
    r.set(key, obj)

def get(key):
    return r.get(key)
