<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [PBL Portal: Flask Edition](#pbl-portal-flask-edition)
  - [Setting up to develop](#setting-up-to-develop)
  - [Dependencies](#dependencies)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# PBL Portal: Flask Edition

Portal API Server here. See http://pbl.link/pbl-front-end for the Frontend counterpart.

or...use APIs and build your own


## Setting up to develop

1. Clone this repo
  * `git clone https://github.com/davidbliu/flask-portal.git`
2. Install dependencies (see section on dependencies)
  * tl;dr is to run `sh install.sh`
3. Set up config.py
  * config.py contains sensitive app keys etc that we dont want to commit
  * see example.config.py for what app keys and ids you need
  * see http://pbl.link/wiki for our keys
  * or ask chairs (davidbliu@gmail.com)
4. Run the flask server
  * `sh run.sh` from the root directory
5. see api.README.md and read docs on the files in this repo
 
## Dependencies 

* Flask
* Database: Parse (using the rest api http://pbl.link/parse-rest-api)
* Caching: Saving some things in pickle (see scripts.py)
* Caching: considering using Redis
  * `pip install redis`
* Oauth  
  * `pip install Flask-Oauth`
* CORS
  * `pip install -U flask-cors`

## Files

read this to understand what files are being used and for what in this repository 

### app.py

Add new routes here. imports all helper files (like `import parse_driver as ParseDriver` for example)

### parse_driver.py

handles making GET, POST, PUT, DELETE requests to parse, etc.

for most requests, you need only pass in the url (ex `/1/classes/ParseMember`) and a dictionary of params (see ex below)
see http://pbl.link/parse-rest-api for more about how to construct valid params

```python
{
  'limit': sys.maxint,
  'where': json.dumps({
      'email': 'davidbliu@gmail.com',
   }),
}
```

### utils.py

has the following convenience methods
```python
get_response(obj):
  # returns json response, obj can be python list or dict

get_email_from_token(token):
  # gets string from token
  # ex token: 6461766964626c697540676d61696c2e636f6d
```

### mail_driver.py




