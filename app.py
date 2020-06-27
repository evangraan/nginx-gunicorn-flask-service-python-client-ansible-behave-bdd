import flask
from flask import jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/record', methods=['POST'])
def apiRecord():
    return jsonify({'status' : 'success'})

app.run()
