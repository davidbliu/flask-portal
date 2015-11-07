import app.models.golinks as gl
import app.test as t

golinks = gl.get_with_tags(['wd', 'articles'])
golinks = [x['key'] for x in golinks]
for k in golinks:
    print k
