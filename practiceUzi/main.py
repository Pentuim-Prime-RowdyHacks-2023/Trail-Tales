# import modules to use
from email import message
from typing_extensions import Required
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from requests import request
from flask_sqlalchemy import SQLAlchemy

# Initiallizing an instance for an api
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)

# this code block makes it mandatory for the
# following parameters to have to be inputted in your put-request
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the Video are required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the Video are required", required=True)

videos = {}

# abort messages
def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Video ID is invalid")

def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message="Video already exists with that ID")

# Making a simple Flask-RESTful resource that defines a GET method that
# will return a JSON response. Basically this will, once properly 
# written, get a JSON data response from the backend side of things
# which will then return a response that will be displayed at the 
# frontend
class Video(Resource):
    def get(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        return videos[video_id]

    def put(self, video_id):
        abort_if_video_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201
    
    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204


# To register the earlier code as a resource
# basically when the user sends a request to 
# the server that will be accessible to /helloworld
# what /helloworld/<string:name> is saying is
# that I want the user add a string parameter 
# called name after the helloworld
api.add_resource(Video, "/video/<int:video_id>")   #this is an endpoint

if __name__ == "__main__":
    app.run(debug=True)