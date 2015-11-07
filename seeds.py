from parse_rest.datatypes import Object
from parse_rest.connection import register
import sys
import config 

register(config.PARSE_APP_ID, config.PARSE_REST_API_KEY)

""" Data @ WD Models """
class ParseMember(Object):
	def to_dict(self):
		return self.__dict__
	def to_json(self):
		d = self.to_dict()
		return {
			'name': str(d['name']), 
			'email': str(d['email']) if 'email' in d.keys() else 'none', 
			'committee': str(d['committee']) if 'committee' in d.keys() else 'none'
		}
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

