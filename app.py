import flask
from flask import jsonify

app = flask.Flask(__name__)

@app.route('/api/v1/record', methods=['POST'])
def apiRecord():
    return jsonify({'status' : 'success'})

if __name__ == "__main__":
    app.run(host='127.0.0.1')
