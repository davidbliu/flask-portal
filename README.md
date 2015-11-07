# PBL Portal: Flask Edition

next generation of the portal



## installing

this is a non comprehensive list of dependencies
most are listed in install.sh

- oauth
- parsepy

## resources

how to navigate this repo
- https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

how to use parse rest api
- https://parse.com/docs/rest/guide

fulltext search

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

### caching

figure out how caching should work. some requirements
- easy to use/configure/install on machines
- we will run multiple flask webservers. they need to be able to share the same cache.
  - ex: redis



