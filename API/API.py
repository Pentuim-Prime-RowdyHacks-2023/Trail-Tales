import json
from flask import Flask, jsonify, request

import DataBaseHandler as dbh

app = Flask(__name__)

@app.route('/<int:uid>', methods=['GET'])
def get_all_data(uid) -> jsonify.Result:
    table = request.form['table']
    dbh.fetch_data(uid, table)

app.run(debug=True)