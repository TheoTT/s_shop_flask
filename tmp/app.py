from flask import Flask
from marshmallow import fields
from flask_apispec import use_kwargs
from flask_cors import CORS, cross_origin

app = Flask(__name__)
#CORS(app)
#cors = CORS(app, resources=r"/api/*", origins="*", supports_credentials=True)
cors = CORS(app, resources=r"/*", origins=r"*", )


@app.route('/api/login/', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
@use_kwargs({'username': fields.Str(), 'password': fields.Str()})
def login(username, password):
    print(username, password)
    return {
        "id": 1,
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODczNjk2MjksImlhdCI6MTU4NDc3NzYyOSwibmJmIjoxNTg0Nzc3NjI5LCJpZGVudGl0eSI6MX0.tRz2r1C1aKaR0BWrgTDavYlPFQbQnsYPxIXwwjyCbAo",
        "username": "admin"
}
