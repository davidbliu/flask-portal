from parse_rest.datatypes import Object
from parse_rest.connection import register
import sys
application_id = 'XIpP60GkEQF4bQtKFOcceguywNhzOs3Lpsw1H17Z'
client_key = '7otfMUAoJ7v5EjhLNMiwqKbSRUi9UOA7xnZp6zOO'
register(application_id, client_key)

class ParseMember(Object):
	pass

class ParseGoLink(Object):
	pass

def all_golinks():
	return ParseGoLink.Query.all().limit(sys.maxint)
if __name__=='__main__':
	members = ParseMember.Query.all().limit(100000)
	member_names = [x.name for x in members]
	print members
	print member_names
	print all_golinks()
