from bs4 import BeautifulSoup
import requests
import json
import query

FROM_URL = 'http://friendorfollow.com/twitter/most-followers/'

# gets 500 most recent tweets from a user post-2010 (the text)
def get_user_tweets_text(username):
    tweets = query.query_tweets_once("from:"+username, 500)
    ret = []
    for tweet in tweets:
        if len(tweet.text) > 0 and tweet.text[0] != '@':
            ret.append(tweet.text)
    return ret

# gets a list of strings representing the twitter handles of the
# celebs with the 100 most visited twitter pages
def get_celeb_usernames():
    webpage = requests.get(FROM_URL).content
    soup = BeautifulSoup(webpage, 'html.parser')
    links = soup.find_all("a", target='f', class_='tUser')
    users = []
    for a in links:
        users.append(a.contents[0][1:])
    return users

# updates celebs.json, which holds the data on celebrity twitter names
def update_db():
    cur_json_dict = {}
    users = get_celeb_usernames()
    i = 0
    for name in users:
        print("Working on number:", i)
        cur_json_dict[name] = get_user_tweets_text(name)
        i += 1
    open('celebs.json', 'w').write(json.dumps(cur_json_dict))

# gets the link to a given user's profile picture
def get_prof_pic(user):
    profile = requests.get('http://twitter.com/'+user).content
    soup = BeautifulSoup(profile, 'html.parser')
    link = soup.find("img", class_='ProfileAvatar-image')['src']
    return link
