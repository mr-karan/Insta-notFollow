import requests
from flask import Flask
from flask import request, render_template

app = Flask(__name__)

from instafollow import (get_user_id,get_unique)

@app.route('/')
def index():
    error_message = 'Username not found'
    username = request.values.get('username')
    if not username:
        return render_template('index.html')
    user_id = get_user_id(username)
    result = get_unique(user_id)
    if result:
        return render_template('result.html', username=username,
                               result=result)
    return render_template('index.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)