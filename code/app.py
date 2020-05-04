from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

app=Flask(__name__)
app.secret_key='Pratik'
api=Api(app)


app.run(port=5000,debug=True)