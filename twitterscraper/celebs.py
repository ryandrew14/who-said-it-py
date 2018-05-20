from bs4 import BeautifulSoup
import requests
import json
import query

FROM_URL = 'http://friendorfollow.com/twitter/most-followers/'


# order tweets by activity
def sort_tweets_by_activity(tweets):
    def activityKey(tweet):
        return int(tweet.likes) + int(tweet.retweets) + int(tweet.replies)

    return sorted(tweets, key=activityKey, reverse=True)


# gets 500 most recent tweets from a user post-2010 (the text), sorted
def get_user_tweets_text(username):
    tweets = sort_tweets_by_activity(query.query_tweets_once("from:" + username, 500))
    ret = []
    for tweet in tweets:
        if len(tweet.text) > 0 and tweet.text[0] != '@':
            ret.append(tweet.text)
    for text in ret:
        list = text.split()
        for word in list:
            if len(word) > 4 and word[0:3] == "http":
                list.remove(word)
        " ".join(list)
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
    return users[:100]


# updates celebs.json, which holds the data on celebrity twitter names
def update_db(filename="celebs.json", users=get_celeb_usernames()):
    with open(filename, 'r+') as f:
        data = f.read()
        cur_json_dict = {}
        if(data != ''):
            cur_json_dict = json.loads(data)
        f.seek(0)
        for name in users:
            if name not in cur_json_dict:
                print("Fetching tweets for " + name)
                cur_json_dict[name] = get_user_tweets_text(name)
            else:
                print("Already have tweets for " + name)
        f.write(json.dumps(cur_json_dict))
        f.truncate()


# gets the link to a given user's profile picture
def get_prof_pic(user):
    profile = requests.get('http://twitter.com/' + user).content
    soup = BeautifulSoup(profile, 'html.parser')
    link = soup.find("img", class_='ProfileAvatar-image')['src']
    return link


if __name__ == '__main__':
    quoatable_users = ["colesprouse","rickygervais","bjnovak","mindykaling","VancityReynolds","chrissyteigen",
                       "AnnaKendrick47","prattprattpratt","StephenAtHome","ConanOBrien"]
    update_db("quotable.json", users=quoatable_users)
