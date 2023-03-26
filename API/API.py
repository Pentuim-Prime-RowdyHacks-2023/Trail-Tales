import json
from flask import Flask, jsonify, request

import DataBaseHandler as dbh

app = Flask(__name__)

@app.route('/<int:uid>', methods=['GET'])
def get_all_data(uid) -> jsonify.Result:
    table = request.form['table']
    return jsonify(dbh.fetch_data(uid, table))

@app.route('/<int:uid>', methods=['POST'])
def post_data(uid) -> jsonify.Result:
    table = request.form['table']
    return jsonify(dbh.fetch_data(uid, table))

app.run(debug=True)