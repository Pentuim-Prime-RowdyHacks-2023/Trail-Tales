import json
from quart import jsonify, request
from quart_openapi import Pint, Resource

import newDBHandler as ndbh

app = Pint(__name__, title='TrailTalesAPI')

with open(r'./dbSkel.json' , 'r') as f:
    TableSkels = json.load(f)

@app.route('/<str:uid>')
class Root(Resource):
    
    async def get(self, uid) -> jsonify.Response:
        data = await ndbh.fetch_data(uid)
        return jsonify(data)

@app.route('/Bio/<str:uid>')
class Bio(Resource):
    
    async def get(self, uid) -> jsonify.Response:
        data = await ndbh.fetch_data(uid, 'Bio')
        return jsonify(data)
    
    @app.expect(app.create_validator('Bio POST', TableSkels['Bio'] ))
    async def post(self, uid) -> jsonify.Response:
        data = request.get_json()
        await ndbh.post_data(data.__dict__, 'Bio')
        return data.__dict__, 200
    
    @app.expect(app.create_validator('Bio PUT', TableSkels['Bio'] ))
    async def put(self, uid) -> jsonify.Response:
        data = request.get_json()
        await ndbh.update_data(uid, data.__dict__, 'Bio')
        return data.__dict__, 200


@app.route('Tales/<str:uid>')
class Tales(Resource):

    async def get(self, uid) -> jsonify.Response:
        TaleId = (await request.form)['TaleId']
        if TaleId is not None:
            data = await ndbh.fetch_data(uid, 'Tales', TaleId)
        else:
            data = await ndbh.fetch_data(uid, 'Tales')
        return jsonify(data)
    
    @app.expect(app.create_validator('Tales POST', TableSkels['Tales'] ))
    async def post(self, uid) -> jsonify.Response:
        data = request.get_json()
        await ndbh.post_data(data.__dict__, 'Tales')
        return data.__dict__, 200
    
    @app.expect(app.create_validator('Tales PUT', TableSkels['Tales'] ))
    async def put(self, uid) -> jsonify.Response:
        data = request.get_json()
        await ndbh.update_data(uid, data.__dict__, 'Tales')
        return data.__dict__, 200

if __name__ == "__main__":
    app.run(debug=True)