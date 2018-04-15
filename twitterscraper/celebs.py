from bs4 import BeautifulSoup
import requests
import json

FROM_URL = 'http://friendorfollow.com/twitter/most-followers/'

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
    cur_json_dict['usernames'] = get_celeb_usernames()
    open('celebs.json', 'w').write(json.dumps(cur_json_dict))

update_db()
