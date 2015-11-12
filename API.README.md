<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [PBL API Docs](#pbl-api-docs)
  - [Authentication](#authentication)
- [Routes](#routes)
  - [Members](#members)
  - [Tabling](#tabling)
  - [Points](#points)
  - [PBL Links](#pbl-links)
  - [Blog](#blog)
- [html content here](#html-content-here)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# PBL API Docs

Guide to using PBL's APIs

## Authentication

You need an authentication token to use the APIs. These can be obtained at http://pbl.link/api-token.

Append the api token to each api request. ex: `/some_route?token=<<YOUR TOKEN HERE>>`

# Routes

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

## Tabling
Routes:
- `/tabling_slots`
- `/schedule`
- `/save_schedule` (POST) (take 'schedule': list of available slots)

```python
# the post request to save_schedule needs a dict looking like this
{
  'schedule': ['8', '9', '10', .... ]
}

# a tabling slot looks like this
{
  'time': 10,
  'member_emails': [
      'davidbliu@gmail.com',
      'alice.sun94@gmail.com',
      'berkeleypbl.webdev@gmail.com'
  ]
}
```

## Points
Routes: 
- `/all_points`
- `/get_member_points`
- `/events`
- `/attendance`
- `/record_attendance`

```python
# an event looks like this
{
  'name': '[PD] Alumni Speaker Panel'
  'google_id': 47rmm863s6c0v13qphr705jv50'
  'semester_name': 'Fall 2015',
  'points': 10,
  'location': '126 Barrows',
  'start_time': '2015-09-04T02:00:00Z'
  'end_time': '2015-09-04T05:00:00Z',
  'description': 'Come hear PBL alumni talk about their experience in PBL...'
}

# get_member_points returns a members points (int) and attendance (list of events)
/get_member_points
# result looks like:
{
  'points': 121,
  'attendance': [
    { <<event1>>},
    { <<event2>>},
    ...
  ]
}

# all points returns a list of point dictionaries like above
/all_points  

# attendance returns a dictionary with keys being emails for your co-cms and values being a list of dictionary objects that look like
{
  'event_id': '123lk23j1l'
  'type': 'chair'
}
# valid types are cm and chair
/attendance

# record attendance takes in a dict looking like
{
  'event_id': 'l24kjl23k4',
  'email': 'davidbliu@gmail.com'
}
```

## PBL Links
Routes:
- `/go/<<key>>` (used in redirects, not important)
- `/recent_golinks`
- `/search_golinks?searchTerm=<<searchTerm here>>`
- `/create_golink` (POST)
- `/update_golink` (POST) (TODO)
- `/my_links`
- `/popular_golinks`

recent, my, and popular take no parameters except optional page=?<<page>> param

search takes searchTerm param

create and update take golink objects as param. 

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
# POST: params dictionary of attributes
/create_golink
# params should look like
{
  'key': 'test-key',
  'url': 'http://www.google.com',
  'description': 'test link',
  'permissions': 'Only Me'
}
# updates an existing golink
# params should be same as above but include objectId
/update_golink
{
  'key': 'test-key', 
  ...
  'objectId': 'ptRdXhFHzS'
}
```


## Blog

Routes: 
- `/all_blogposts`
- `/save_blogpost` (POST)
- `/get_blogpost`
- `/delete_blogpost`

delete, and get take id as a request param (?id=<<id here>>)

save takes a post json object in the request params

```python
# a blogpost is a dictionary that looks like this
{
  'title': 'Example Title',
  'content': '<h1>html content here</h1>',
  'author': 'davidbliu@gmail.com',
  'last_editor': 'berkeleypbl.webdev@gmail.com',
  'view_permissions': 'Anyone',
  'edit_permissions': 'Only Me', 
  'timestamp': '<<some time string>>',
  'createdAt': '<<some time string>>',
  'updatedAt': '<<some time string>>'
}

# possible view and edit permissions are the same as for golinks, they include
['Only Me', 'Only Execs', 'Only Officers', 'Only PBL', 'Anyone']

```
