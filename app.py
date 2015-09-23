from flask import Flask
from flask import Flask, request, jsonify, render_template
from seeds import *
import sys
import json
app = Flask(__name__)

""" DEMO Routes """
@app.route("/")
def go_home():
	golinks = all_golinks()
	return render_template('golinks.html', golinks = golinks, num_golinks = len(golinks))

@app.route('/angular')
def angular_home():
	return render_template('angular_index.html', members = [x.to_json() for x in ParseMember.Query.all()])

@app.route('/members')
def members():
	members = all_members()
	attendance = ParseEventMember.Query.all().limit(sys.maxint)
	return render_template('members.html', members = members, attendance = attendance)

@app.route('/events')
def events():
	events = ParseEvent.Query.all().limit(sys.maxint)
	return render_template('events.html', events = events)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug = True)
    #app.run()
