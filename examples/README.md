
# Examples

this directory contains a bunch of examples. look at them to get started

## Parse rest api

the formal documentation is at pbl.link/parse-rest-api

you can make parse requests using standard python rest calls
```python

def make_parse_request(req_type, url, params = {}):
    params = urllib.urlencode(params)
    connection.request(
        req_type, 
        url+'?%s' % params, 
        '', 
        {
            "X-Parse-Application-Id": config.PARSE_APP_ID,
            "X-Parse-REST-API-Key": config.PARSE_REST_API_KEY
        }
    )
    result = json.loads(connection.getresponse().read())
    return result

```

as an example of what params could be

```python
# example 0: limit
params ={}
params['limit'] = 500

# example 1: where query
params = {}
where = {}
where['tags'] = {$all': ['wd', 'articles']}
params['where'] = json.dumps(where)
```

## authentication

- see google.py
- search flask oauth google 

