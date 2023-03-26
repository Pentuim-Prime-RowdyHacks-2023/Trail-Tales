import json
from quart import jsonify, request, Response
from quart_openapi import Pint, Resource

import newDBHandler as ndbh

app = Pint(__name__, title='TrailTales', no_openapi=True)

with open(r'./New-API/dbSkel.json' , 'r') as f:
    TableSkels = json.load(f)

@app.route('/')
class Root(Resource):

    expect = app.create_validator('Full POST', TableSkels) 

    @app.expect(expect)
    async def post(self) -> Response:
        data = await request.get_json()
        await ndbh.post_data(data['Bio'], 'Bio')
        await ndbh.post_data(data['Tales'], 'Tales')
        return jsonify(data)

@app.route('/<string:uid>')
class User(Resource):
    
    async def get(self, uid) -> Response:
        data = await ndbh.fetch_data(uid)
        return jsonify(data)
    
@app.route('/Bio/<string:uid>')
class Bio(Resource):
    
    async def get(self, uid) -> Response:
        data = await ndbh.fetch_data(uid, 'Bio')
        return jsonify(data)
    
    @app.expect(app.create_validator('Bio POST', TableSkels['Bio'] ))
    async def post(self, uid) -> Response:
        data = request.get_json()
        await ndbh.post_data(data.__dict__, 'Bio')
        return jsonify(data.__dict__)
    
    @app.expect(app.create_validator('Bio PUT', TableSkels['Bio'] ))
    async def put(self, uid) -> Response:
        data = request.get_json()
        await ndbh.update_data(uid, data.__dict__, 'Bio')
        return jsonify(data.__dict__)


@app.route('/Tales/<string:uid>')
class Tales(Resource):

    async def get(self, uid) -> Response:
        TaleId = (await request.form)['TaleId']
        if TaleId is not None:
            data = await ndbh.fetch_data(uid, 'Tales', TaleId)
        else:
            data = await ndbh.fetch_data(uid, 'Tales')
        return jsonify(data)
    
    @app.expect(app.create_validator('Tales POST', TableSkels['Tales'] ))
    async def post(self, uid) -> Response:
        data = request.get_json()
        await ndbh.post_data(data.__dict__, 'Tales')
        return jsonify(data.__dict__)
    
    @app.expect(app.create_validator('Tales PUT', TableSkels['Tales'] ))
    async def put(self, uid) -> Response:
        data = request.get_json()
        await ndbh.update_data(uid, data.__dict__, 'Tales')
        return jsonify(data.__dict__)

app.run(debug=True)
