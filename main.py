from flask import Flask 
from public import public
from user import user
from agent import agent

app=Flask(__name__)
   
app.secret_key='key'

app.register_blueprint(public)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(agent,url_prefix='/agent')

app.run(debug=True,port=5896) 