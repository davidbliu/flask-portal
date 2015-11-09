# PBL API Docs

Guide to using PBL's APIs

## Authentication

You need an authentication token to use the APIs. These can be obtained at http://pbl.link/api-token.

Append the api token to each api request. ex: `/some_route?token=<<YOUR TOKEN HERE>>`

# Routes
## PBL Links
Routes:
- `/go/<<key>>`
- `/recent_golinks`
- `/search_golinks?searchTerm=<<searchTerm here>>`
- `/create_golink` (POST)
- `/update_golink` (POST) 

```python
# golinks are returned as dicts that look like
{
  'key': 'portal',
  'url': 'http://portal.berkeley-pbl.com',
  'description': 'PBL\'s members portal',
  'tags': ['wd', 'tools'],
  'permissions': 'Only PBL',
  'createdAt': <<some time string>>,
}

# gets list of recent golinks
/recent_golinks
# gets search results (that you have permissions for)
# expects searchTerm url parameter (?searchTerm=<<something>>)
/search_golinks

```
## Members

Routes: 
- `/current_members`
- `/member_email_hash`



```python
# members are dicts that look like
{
  'name': 'David Liu',
  'email': 'davidbliu@gmail.com',
  'position': 'chair',
  'phone': '7142991786',
  'major': 'EECS',
  'committee': 'HT'
}
# return list of current members (dictionaries like above)
/current_members
# return dictionary, keys are emails and values are members (dictionaries)
/member_email_hash
```
