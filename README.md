# PBL Portal: Flask Edition

this is mainly a proof of concept: that a detached flask frontent server can serve the same views that the main rails portal does. 

our next play is likely to phase out the rails app for serving views and only use it as an api server for json.

we will have some other app (maybe this flask app, maybe something else) serving the frontend

## Benefits of this approach
* modularity
* easy to ramp up as a developer: learn either front end, middle tier, or back end
* clean, craftsmanship

## what's in this repo

* /ngApp : sample angular app for PBL Links Explorer
* app.py : main flask appp
* seeds.py : data, gets data from parse

# Running the /ngApp
start a dummy python server: "python -m SimpleHTTPServer 8000"

navigate to localhost:8000 in the browser, click the mainpage.html
