import config
from flask import Flask, request, jsonify, render_template,redirect, url_for, session, Response, make_response
from flask.ext.cors import CORS
from flask_oauth import OAuth
import sys,json
import parse_driver
import utils

app = Flask(__name__)
app.secret_key = 'aslkdfjlsfj'
CORS(app)

@app.route('/')
def test_route():
    return 'hello world'

""" Members """
@app.route('/current_members')
def current_members():
    params = {'limit': sys.maxint, 'where': json.dumps({'latest_semester': config.CURRENT_SEMESTER})}
    members = parse_driver.make_parse_get_request('/1/classes/ParseMember', params)['results']
    return Response(json.dumps(members), mimetype='application/json')

@app.route('/member_email_hash')
def member_email_hash():
    params = {'limit': sys.maxint}
    params['where'] = json.dumps({'email': {'$exists':True}})
    members = parse_driver.make_parse_get_request('/1/classes/ParseMember', params)['results']
    h= dict((x['email'], x) for x in members)
    return Response(json.dumps(h), mimetype = 'application/json')

""" Tabling """
@app.route('/tabling_slots')
def tabling_slots():
    params = {'limit': sys.maxint}
    tabling_slots = parse_driver.make_parse_get_request('/1/classes/ParseTablingSlot', params)['results']
    for slot in tabling_slots:
        slot['member_emails'] = slot['member_emails'].split(',')
    return Response(json.dumps(tabling_slots), mimetype = 'application/json')

""" Points """

def get_attendance(email):
    params = {'limit': sys.maxint}
    params['where'] = json.dumps({
        'member_email': email
        })
    result = parse_driver.make_parse_get_request('/1/classes/ParseEventMember', params)
    return result['results']

def get_events_by_id(eids):
    params = {'limit':sys.maxint,
            'where': json.dumps( {'google_id': {'$in': eids}})}

    result = parse_driver.make_parse_get_request('/1/classes/ParseEvent', params)
    return result['results']

@app.route('/get_member_points')
def get_member_points():
    email = request.args.get('email')
    attendance = get_attendance(email)
    eids = [x['event_id'] for x in attendance]
    events = get_events_by_id(eids)
    points = sum([x['points'] for x in events if 'points' in x.keys()])
    p = {'points':points, 'attendance':events}
    return Response(json.dumps(p), mimetype='application/json')

@app.route('/attendance')
def attendance():
    requesterEmail = utils.get_email_from_token(request.args.get('token'))
    emails = ['davidbliu@gmail.com', 'alice.sun94@gmail.com']
    params = {'limit':sys.maxint, 'where': json.dumps({'member_email': {'$in':emails}})}
    event_members = parse_driver.make_parse_get_request('/1/classes/ParseEventMember', params)['results']
    # return a dictionary with keys emails, values list of attended events
    return utils.get_response(event_members)

""" Blog """
@app.route('/all_blogposts')
def all_blogposts():
    params = {'limit':sys.maxint, 'order': '-updatedAt'}
    posts = parse_driver.make_parse_get_request('/1/classes/BlogPost', params)['results']
    return utils.get_response(posts)

""" GoLinks """

@app.route('/go/<key>')
def go(key):
    params = {'where': json.dumps({'key':key})}
    golinks = parse_driver.make_parse_get_request('/1/classes/ParseGoLink',params)['results']
    if len(golinks)==0:
        return 'not a valid key'
    else:
        return redirect(golinks[0]['url'])

@app.route('/create_golink',methods=['POST'])
def create_golink():
    form = request.get_json()
    golink = {'key': form.get('key'),
            'url': form.get('url'),
            'member_email': form.get('member_email'),
            'description': form.get('description'),
            'permissions': form.get('permissions', 'Anyone'),
            'tags': form.get('tags', [])
            }
    parse_driver.make_parse_post_request('/1/classes/ParseGoLink', golink)
    return 'ok'

@app.route('/recent_golinks')
def recent_golinks():
    email = utils.get_email_from_token(request.args.get('token'))
    page = int(request.args.get('page', '0'))
    params = {}
    params['order'] = '-createdAt'
    params['skip']=page*100
    r = parse_driver.make_parse_get_request('/1/classes/ParseGoLink', params)
    results = r['results']
    for x in results:
        if 'num_clicks' not in x.keys():
            x['num_clicks']=0
    return utils.get_response(results)

@app.route('/search_golinks')
def search_golinks():
    searchTerm = request.args.get('searchTerm')
    where = {'$or':[{'key':{'$regex':searchTerm}},
        {'description':{'$regex':searchTerm}},
        {'tags':{'$in':[searchTerm]}}
        ]}
    params = {'where':json.dumps(where)}
    results = parse_driver.make_parse_get_request('/1/classes/ParseGoLink', params)
    results = results['results']
    return Response(json.dumps(results), mimetype='application/json')
    

@app.route('/count_golinks')
def count_golinks():
    params = {'count':1}
    r = parse_driver.make_parse_get_request('/1/classes/ParseGoLink', params)
    return r['count'] 

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
    try:
        port = int(sys.argv[1])
        app.run(host='0.0.0.0', port=port, debug=True)
    except:
        port = 3000
        app.run(host='0.0.0.0', port=port, debug=True)


