""" Create the Flask application """
from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/api/v1/status', methods=['GET'])
def get_status():
    """ Create a dictionary representing the status response """
    status_response = {"status": "ok"}
    return jsonify(status_response)


if __name__ == '__main__':
    app.run(host=os.environ['HBNB_API_HOST'],
            port=int(os.environ['HBNB_API_PORT']))
