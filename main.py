import requests
from instagram.client import InstagramAPI
from flask import Flask, request, render_template, session, redirect, abort, flash, jsonify
import os
app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

# configure Instagram API
instaConfig = {
    'client_id':os.environ['INSTA_CLIENT_ID'],
    'client_secret':os.environ['INSTA_CLIENT_SECRET'],
    'redirect_uri' : os.environ['INSTA_REDIRECT_URI']
}
api = InstagramAPI(**instaConfig)
'''
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
'''
@app.route('/')
def index():

    # if instagram info is in session variables, then display user photos
    if 'instagram_access_token' in session and 'instagram_user' in session:
        userAPI = InstagramAPI(access_token=session['instagram_access_token'])
        follows = []
        follows, next_ = userAPI.user_follows(user_id=session['instagram_user'].get('id'))
        while next_:
            more_follows, next_ = userAPI.user_follows(with_next_url=next_)
            follows.extend(more_follows)
        
        followed_by = []
        followed_by, _ = userAPI.user_followed_by(user_id=session['instagram_user'].get('id'))
        while _:
            more_followed_by, _ = api.user_followed_by(with_next_url=_)
            followed_by.extend(more_followed_by)

        followers_names=list(map(str,follows))
        followed_by_names=list(map(str,followed_by))
        unique_people=list(set(followers_names) - set(followed_by_names))
        clean_list=[i.replace("User: ","") for i in unique_people]
        result=[i for i in follows if i.username in clean_list]
        resultattr = {}
        for i in result:
            resultattr[i.username]=i.profile_picture


        return render_template('result.html', result = resultattr)
        

    else:

        return render_template('index.html')

@app.route('/connect')
def main():

    url = api.get_authorize_url(scope=["follower_list"])
    return redirect(url)

@app.route('/instagram_callback')
def instagram_callback():

    code = request.args.get('code')

    if code:

        access_token, user = api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'

        app.logger.debug('got an access token')
        app.logger.debug(access_token)

        # Sessions are used to keep this data 
        session['instagram_access_token'] = access_token
        session['instagram_user'] = user

        return redirect('/') # redirect back to main page
        
    else:
        return "Uhoh no code provided"


    
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)