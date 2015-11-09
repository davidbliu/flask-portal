import config
from flask import Flask
from flask import Flask, request, jsonify, render_template
from flask.ext.cors import CORS
from flask import redirect, url_for, session
from flask_oauth import OAuth
from flask import Response
# set cookies
from flask import request
from flask import make_response

# import models 
import models.golinks as GoLinks
import models.members as Members
import models.tabling as Tabling
import models.points as Points
import models.blog as Blog

import sys
import json

app = Flask(__name__)
app.secret_key = 'aslkdfjlsfj'
CORS(app)


@app.route('/')
def home():
    return 'hello world'

@app.route('/test')
def test():
    golinks = GoLinks.recent_golinks()
    result = {}
    result['golinks'] = golinks
    # return jsonify(**result)
    return json.dumps(golinks)

@app.route('/test2')
def test2():
    import models.members as Mem
    members = Mem.all_members()
    return Response(json.dumps(members),  mimetype='application/json')


@app.route('/cookie')
def cookie():
    return request.cookies.get('email')

""" Members """
@app.route('/current_members')
def current_members():
    members = Members.current_members()
    return Response(json.dumps(members), mimetype='application/json')

@app.route('/member_email_hash')
def member_email_hash():
    h = Members.member_email_hash()
    return Response(json.dumps(h), mimetype = 'application/json')

""" Tabling """
@app.route('/tabling_slots')
def tabling_slots():
    tabling_slots = Tabling.get_tabling_slots()
    for x in tabling_slots:
        x['member_emails']=x['member_emails'].split(',')
    return Response(json.dumps(tabling_slots), mimetype = 'application/json')

""" Points """
@app.route('/get_member_points')
def get_member_points():
    email = request.args.get('email')
    return Response(json.dumps(Points.get_member_points(email)), mimetype='application/json')

@app.route('/get_all_points')
def get_all_points():
    return 'not implemented yet'

""" Blog """
@app.route('/all_blogposts')
def all_blogposts():
    posts = Blog.get_all_posts()
    return Response(json.dumps(posts), mimetype='application/json')

""" GoLinks """

@app.route('/go/<key>')
def go(key):
    golinks = GoLinks.get_with_key(key)
    if len(golinks) > 0:
        return redirect(golinks[0]['url'])
    else:
        return 'that key doesnt exist'

@app.route('/create_golink',methods=['POST'])
def create_golink():
    GoLinks.create_golink(request.get_json())
    return 'ok'

@app.route('/recent_golinks')
def recent_golinks():
    page = int(request.args.get('page', '0'))
    golinks = GoLinks.recent_golinks(page)
    return Response(json.dumps(golinks), mimetype = 'application/json')

@app.route('/search_golinks')
def search_golinks():
    searchTerm = request.args.get('searchTerm')
    golinks = GoLinks.search_golinks(searchTerm)
    return Response(json.dumps(golinks), mimetype = 'application/json')

""" Google Oauth """
# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
REDIRECT_URI = '/auth/google_oauth2/callback'  
oauth = OAuth()

google = oauth.remote_app('google',
  base_url='https://www.google.com/accounts/',
  authorize_url='https://accounts.google.com/o/oauth2/auth',
  request_token_url=None,
  request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                        'response_type': 'code'},
  access_token_url='https://accounts.google.com/o/oauth2/token',
  access_token_method='POST',
  access_token_params={'grant_type': 'authorization_code'},
  consumer_key=config.GOOGLE_CLIENT_ID,
  consumer_secret=config.GOOGLE_CLIENT_SECRET)

@app.route('/handle_auth')
def handle_auth():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()
    data = json.loads(res.read())
    email = data['email']
    resp = make_response('you have been logged in as '+email)
    resp.set_cookie('email', email)
    return resp
    # return data

@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('handle_auth'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug = True)
