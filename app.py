from flask import Flask
from flask import Flask, request, jsonify, render_template
from seeds import *
app = Flask(__name__)

@app.route("/")
def go_home():
	golinks = all_golinks()
	return render_template('golinks.html', golinks = golinks)
if __name__ == "__main__":
    app.run()
