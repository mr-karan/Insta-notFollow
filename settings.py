import os

access_token = os.environ['INSTA_ACCESS_TOKEN']
client_id = os.environ['INSTA_CLIENT_ID']
base_url='https://api.instagram.com/v1'
client_secret=os.environ['INSTA_CLIENT_SECRET']
secret_key=os.environ['FLASK_SECRET_KEY']
REDIRECT_URI='http://insta-notfollow.herokuapp.com/instagram_callback'