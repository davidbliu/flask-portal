from flask import Flask
from flask import Flask, request, jsonify, render_template
from seeds import *

app = Flask(__name__)

@app.route("/")
def go_home():
	golinks = all_golinks()
	return render_template('golinks.html', golinks = golinks)

@app.route('/members')
def members_home():
	members = [x.name for x in ParseMember.Query.all()]
	attendance = ParseEventMember.Query.all()
	return render_template('members.html', members = members, attendance = attendance)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
    #app.run()
