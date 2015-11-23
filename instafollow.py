
# coding: utf-8
from settings import(access_token , client_id)
from instagram.client import InstagramAPI
from instagram.models import MediaShortcode, Media, User, Location, Tag, Comment, Relationship
import requests

api = InstagramAPI(access_token=access_token, client_secret=client_id)
def get_user_id(username):
	all_user_id=requests.get('https://api.instagram.com/v1/users/search?q='+username+'&access_token='+access_token).json()
	for i in range(len(all_user_id['data'])):
			if username == all_user_id['data'][i]['username']:
				user_id=all_user_id['data'][i]['id']
				return user_id

def get_followers(user_id):
	follows = []
	follows, next_ = api.user_follows(user_id)
	while next_:
	    more_follows, next_ = api.user_follows(with_next_url=next_)
	    follows.extend(more_follows)
	return follows

def get_followed_by(user_id):
	followed_by = []
	followed_by, _ = api.user_followed_by(user_id)
	while _:
	    more_followed_by, _ = api.user_followed_by(with_next_url=_)
	    followed_by.extend(more_followed_by)
	return followed_by

def get_unique(user_id):
	followers_user_model = get_followers(user_id)
	followers_names=list(map(str,get_followers(user_id)))
	followed_by_names=list(map(str,get_followed_by(user_id)))
	unique_people=list(set(followers_names) - set(followed_by_names))
	clean_list=[i.replace("User: ","") for i in unique_people]
	result=[i for i in followers_user_model if i.username in clean_list]
	#print(result)
	#return result
	resultattr = {}
	for i in result:
		resultattr[i.full_name]=i.profile_picture

	#print(resultattr)
	return resultattr


get_unique('1413598181')