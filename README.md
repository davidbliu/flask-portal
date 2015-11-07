# PBL Portal: Flask Edition

next generation of the portal


## How to get started

- clone this repo
- add config.py from http://pbl.link/flask-drive to the root directory. this has app ids and keys and whatnot
- start working on api routes (goal of today is to finish apiserver)
  - reading over resources may help
  - see `app/models/*`

next step is to work on frontend
- http://pbl.link/pbl-front-end

## installing

this is a non comprehensive list of dependencies
most are listed in install.sh

- oauth

## resources

how to navigate this repo
- https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

how to use parse rest api
- https://parse.com/docs/rest/guide

oauth via google
- https://github.com/mitsuhiko/flask-oauth/blob/master/example/google.py

## TODO

### finish models

this app is meant to be an api server. finish writing code to serve apis for

- members
- tabling
- events
- attendance
- points
- golinks
- blog posts

#### Members
```python
def get_member(email):
  # return member object corresponding to this email (primary key)

def get_members(params):
  # if no params get current members
  # params can be used to filter results
    # ex: name like %avid%

def update_member(email, data):
  # update member data in parse

```

#### Tabling
```python
def get_tabling_schedule(params):
  # default: return current tabling schedule

def get_tabling_slot(email):
  # return this members tabling slot
```

#### Points


### caching

figure out how caching should work. some requirements
- easy to use/configure/install on machines
- we will run multiple flask webservers. they need to be able to share the same cache.
  - ex: redis



