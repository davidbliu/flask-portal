from parse_rest.datatypes import Object
from parse_rest.connection import register
import sys
application_id = 'XIpP60GkEQF4bQtKFOcceguywNhzOs3Lpsw1H17Z'
client_key = '7otfMUAoJ7v5EjhLNMiwqKbSRUi9UOA7xnZp6zOO'
register(application_id, client_key)

""" Data @ WD Models """
class ParseMember(Object):
	pass

class ParseGoLink(Object):
	def get_tags(self):
		try:
			return self.tags
		except:
			return []
	pass

class ParseGoLinkClick(Object):
	pass

class BlogPost(Object):
	pass

class ParseTablingSlot(Object):
	pass

class ParseEvent(Object):
	pass

class ParseEventMember(Object):
	pass

""" convenient access methods: examples  """

""" members access methods """
def all_members():
	return [x for x in ParseMember.Query.all().limit(sys.maxint)]
""" blog access methods """
def all_blogposts():
	return BlogPost.Query.all().limit(sys.maxint)

""" Points access methods """

def event_members():
	return ParseEventMember.Query.all()

def events():
	return ParseEvent.Query.all()

""" PBL Links accessing methods """
def all_golinks():
	return ParseGoLink.Query.all().limit(sys.maxint)

def tag_query(tag):
	return [x for x in all_golinks() if tag in x.get_tags()]

if __name__=='__main__':
	#members = ParseMember.Query.all().limit(100000)
	#member_names = [x.name for x in members]
	#print members
	#print member_names
	#print all_golinks()
	#blogposts = [x.title for x in all_blogposts()]
	#print blogposts
	t = tag_query('articles')
	print [x.key for x in t]

