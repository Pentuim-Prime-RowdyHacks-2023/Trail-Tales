import json
from flask import Flask, jsonify, request

import DataBaseHandler as dbh

app = Flask(__name__)

@app.route('/<int:uid>', methods=['GET'])
def get_all_data(uid) -> jsonify.Response:
    table = request.form['table']
    return jsonify(dbh.fetch_data(uid, table))

@app.route('/<int:uid>', methods=['POST'])
def post_data(uid) -> jsonify.Response:
    table = request.form['table']
    return jsonify(dbh.fetch_data(uid, table))

@app.route('/<int:uid>/<int:postid>', methods=['PUT'])
def update_user_post(uid, postid) -> jsonify.Response:
    table = 'Posts'
    data = request.form
    return jsonify(dbh.update_table(uid, table, postid, data))

app.run(debug=True)