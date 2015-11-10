<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [PBL Portal: Flask Edition](#pbl-portal-flask-edition)
  - [Setting up to develop](#setting-up-to-develop)
  - [Dependencies](#dependencies)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# PBL Portal: Flask Edition
Portal API Server here

## Setting up to develop

1. Clone this repo
2. Install dependencies (see section on dependencies)
  * tl;dr is to run install.sh
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
