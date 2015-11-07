import app.models.golinks as gl
import app.test as t
import app.models.members as mem

golinks = gl.get_with_tags(['wd', 'articles'])
golinks = [x['key'] for x in golinks]
for k in golinks:
    print k


# print 'making golink'
# gl.create_golink('test-flask-golink', 'http://www.google.com', 'davidbliu@gmail.com')

print 'members'
names =  [x['name'] for x in mem.all_members()]
print names
print len(names)
