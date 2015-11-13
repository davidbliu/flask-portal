import config
from flask import Flask, request, jsonify, render_template,redirect, url_for, session, Response, make_response
from flask.ext.cors import CORS
from flask_oauth import OAuth
import sys,json,datetime

# WD made scripts
import parse_driver as ParseDriver
import utils
import scripts # phase out. basically a constants that only change each semester

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
     members = ParseDriver.make_parse_get_request('/1/classes/ParseMember', params)['results']
     return Response(json.dumps(members), mimetype='application/json')

@app.route('/member_email_hash')
def member_email_hash():
     params = {'limit': sys.maxint}
     params['where'] = json.dumps({'email': {'$exists':True}})
     members = ParseDriver.make_parse_get_request('/1/classes/ParseMember', params)['results']
     h= dict((x['email'], x) for x in members)
     return Response(json.dumps(h), mimetype = 'application/json')

""" Tabling """

@app.route('/tabling_slots')
def tabling_slots():
     params = {'limit': sys.maxint}
     tabling_slots = ParseDriver.make_parse_get_request('/1/classes/ParseTablingSlot', params)['results']
     for slot in tabling_slots:
          slot['member_emails'] = slot['member_emails'].split(',')
     return Response(json.dumps(tabling_slots), mimetype = 'application/json')


@app.route('/schedule')
def schedule():
    myEmail = utils.get_email_from_token(request.args.get('token'))
    params = {'where':json.dumps({'member_email': myEmail})}
    schedule = ParseDriver.make_parse_get_request('/1/classes/Commitments', params)['results']
    if len(schedule) == 0:
         return 'no schedule found', 404
    schedule = schedule[0]
    return utils.get_response(schedule['commitments'])

@app.route('/save_schedule', methods = ['POST'])
def save_schedule():
    myEmail = utils.get_email_from_token(request.args.get('token'))
    times = request.get_json().get('schedule')
    params = {'where':json.dumps({'member_email': myEmail})}
    schedule = ParseDriver.make_parse_get_request('/1/classes/Commitments', params)['results']
    s = {'member_email': myEmail, 'commitments': times}
    print 'schedule was '+str(s)
    if len(schedule) == 0:
        ParseDriver.make_parse_post_request('/1/classes/Commitments', s)
    else:
        sid = schedule[0].get('objectId')
        ParseDriver.make_parse_put_request('/1/classes/Commitments/'+sid, s)
    return 'ok'

""" Points """

def get_attendance(email):
     params = {'limit': sys.maxint}
     params['where'] = json.dumps({
          'member_email': email
          })
     result = ParseDriver.make_parse_get_request('/1/classes/ParseEventMember', params)
     return result['results']

def get_events_by_id(eids):
     params = {'limit':sys.maxint,
                'where': json.dumps( {'google_id': {'$in': eids}})}

     result = ParseDriver.make_parse_get_request('/1/classes/ParseEvent', params)
     return result['results']


@app.route('/get_member_points')
def get_member_points():
     email = request.args.get('email')
     attendance = get_attendance(email)
     eids = [x['event_id'] for x in attendance]
     events = get_events_by_id(eids)
     points = sum([x['points'] for x in events if 'points' in x.keys()])
     p = {'points':points, 'attendance':events}
     return utils.get_response(p)

@app.route('/events')
def get_events():
     params = {'limit':sys.maxint}
     params['where'] = json.dumps({'semester_name': config.CURRENT_SEMESTER})
     events = ParseDriver.make_parse_get_request('/1/classes/ParseEvent', params)['results']
     return utils.get_response(events)

@app.route('/attendance')
def attendance():
     requesterEmail = utils.get_email_from_token(request.args.get('token'))
     me = scripts.load_pickle_key('member_email_hash')[requesterEmail]
     emails = scripts.load_pickle_key('committee_members_hash')[me['committee']]
     emails = [x['email'] for x in emails]
     params = {'limit':sys.maxint, 'where': json.dumps({'member_email': {'$in':emails}})}
     event_members = ParseDriver.make_parse_get_request('/1/classes/ParseEventMember', params)['results']
     # return a dictionary with keys emails, values list of attended events
     h = {}
     seen = []
     for em in event_members:
          if em['member_email'] not in seen:
                seen.append(em['member_email'])
                h[em['member_email']] = []
          h[em['member_email']].append({'event_id': em['event_id'], 'type': em['type']})
     return utils.get_response(h)

@app.route('/record_attendance', methods = ['POST'])
def record_attendance():
     form = request.get_json()
     myEmail = utils.get_email_from_token(request.args.get('token'))
     event_id = form.get('event_id')
     email = form.get('email')
     params = {'where': json.dumps({'event_id': event_id, 'member_email': email})}
     ems = ParseDriver.make_parse_get_request('/1/classes/ParseEventMember', params)['results']
     myPosition = utils.get_position_from_email(myEmail)
     if myPosition == 'exec':
          myPosition = 'chair'
     if len(ems) == 0:
          print 'there are no ems that match'
          data = {'event_id': event_id, 'member_email': email, 'type': myPosition}
          ParseDriver.make_parse_post_request('/1/classes/ParseEventMember', data)
     else:
          print 'there are matching ems ('+str(len(ems))+')'
          em = ems[0]
          url = '/1/classes/ParseEventMember/'+em['objectId']
          data = {'type':myPosition}
          ParseDriver.make_parse_put_request(url,  data)

     return 'ok'

@app.route('/all_points')
def all_points():
     return 'not implemented yet'

""" Blog """
@app.route('/all_blogposts')
def all_blogposts():
     params = {'limit':sys.maxint, 'order': '-updatedAt'}
     posts = ParseDriver.make_parse_get_request('/1/classes/BlogPost', params)['results']
     return utils.get_response(posts)

@app.route('/get_blogpost')
def get_blogpost():
     post_id = request.args.get('id')
     post = ParseDriver.make_parse_get_request('/1/classes/BlogPost/'+str(post_id), '')
     print post
     return utils.get_response(post)

@app.route('/delete_blogpost')
def delete_blogpost():
     post_id = request.args.get('id')
     ParseDriver.make_parse_delete_request('/1/classes/BlogPost/'+str(post_id))
     return 'ok'

@app.route('/save_blogpost', methods = ['POST'])
def save_blogpost():
     myEmail =utils.get_email_from_token(request.args.get('token')) 
     post = request.get_json()
     post['last_editor'] = myEmail
     # date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%M:%S.000Z')
     # post['timestamp'] = {'__type': 'Date', 'iso': date}
     objectId = post.get('objectId')
     if objectId != None and objectId != '':
          print 'this is an existing post'
          url = '/1/classes/BlogPost/'+objectId
          ParseDriver.make_parse_put_request(url, post)
     else: 
          print 'this is a new post'
          post['author'] = myEmail
          print post
          resp = ParseDriver.make_parse_post_request('/1/classes/BlogPost', post)
          print resp
     return 'ok'

""" GoLinks """

@app.route('/go/<key>')
def go(key):
     params = {'where': json.dumps({'key':key})}
     golinks = ParseDriver.make_parse_get_request('/1/classes/ParseGoLink',params)['results']
     if len(golinks)==0:
          return 'not a valid key'
     else:
          return redirect(golinks[0]['url'])

@app.route('/create_golink',methods=['POST'])
def create_golink():
     senderEmail = utils.get_email_from_token(request.args.get('token'))
     form = request.get_json()
     golink = {'key': form.get('key'),
                'url': form.get('url'),
                'member_email': form.get('member_email'),
                'description': form.get('description'),
                'permissions': form.get('permissions', 'Anyone'),
                'tags': form.get('tags', [])
                }
     ParseDriver.make_parse_post_request('/1/classes/ParseGoLink', golink)
     return 'ok'


@app.route('/save_golink',methods=['POST'])
def save_golink():
     myEmail = utils.get_email_from_token(request.args.get('token'))
     golink = request.get_json()
     golink_id = golink.get('objectId')
     golink['member_email'] = myEmail
     permissions = golink.get('permissions')
     if permissions == None or permissions == '':
         golink['permissions'] = 'Anyone'
     if golink_id == None or golink_id == '':
         print 'creating a new golink'
         ParseDriver.make_parse_post_request('/1/classes/ParseGoLink', golink)
     else:
         print 'editing an existing golink'
         ParseDriver.make_parse_put_request('/1/classes/ParseGoLink/'+golink_id, golink)
     return 'ok'

@app.route('/recent_golinks')
def recent_golinks():
     email = utils.get_email_from_token(request.args.get('token'))
     page = int(request.args.get('page', '0'))
     params = {}
     params['order'] = '-createdAt'
     params['skip']=page*100
     r = ParseDriver.make_parse_get_request('/1/classes/ParseGoLink', params)
     results = r['results']
     for x in results:
          if 'num_clicks' not in x.keys():
                x['num_clicks']=0
     return utils.get_response(results)


@app.route('/my_links')
def my_links():
     email = utils.get_email_from_token(request.args.get('token'))
     page = int(request.args.get('page', '0'))
     params = {}
     params['order'] = '-createdAt'
     params['skip']=page*100
     params['where']= json.dumps({'member_email': email})
     r = ParseDriver.make_parse_get_request('/1/classes/ParseGoLink', params)
     results = r['results']
     for x in results:
          if 'num_clicks' not in x.keys():
                x['num_clicks']=0
     return utils.get_response(results)


@app.route('/popular_golinks')
def popular_golinks():
     email = utils.get_email_from_token(request.args.get('token'))
     page = int(request.args.get('page', '0'))
     params = {}
     params['order'] = '-num_clicks'
     params['skip']=page*100
     params['where']= json.dumps({'member_email': email})
     r = ParseDriver.make_parse_get_request('/1/classes/ParseGoLink', params)
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
     results = ParseDriver.make_parse_get_request('/1/classes/ParseGoLink', params)
     results = results['results']
     return Response(json.dumps(results), mimetype='application/json')
     

@app.route('/count_golinks')
def count_golinks():
     params = {'count':1}
     r = ParseDriver.make_parse_get_request('/1/classes/ParseGoLink', params)
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
          app.run(host='0.0.0.0', port=port, debug=False)
     except:
          port = 3000
          app.run(host='0.0.0.0', port=port, debug=True)


