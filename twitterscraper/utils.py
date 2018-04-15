import query
import random
import celebs
import json

most_used_words = ['the', 'be', 'and', 'of', 'a', 'in', 'to', 'have', 'it', 'i',
 'that', 'for', 'you', 'he', 'with', 'on', 'do', 'say', 'this', 'they', 'at',
 'but', 'we', 'his', 'from', 'that', 'not', 'by', 'she', 'or', 'as', 'what',
 'go', 'their', 'can', 'who', 'get', 'if', 'would', 'her', 'all', 'my', 'make',
 'about', 'know', 'will', 'as', 'up', 'one', 'there', 'so', 'when', 'which'
 'them', 'me', 'him', 'could', 'like', 'how', 'then', 'than', 'how', 'its'
 'our', 'these', 'new', 'because', 'thing', 'those', 'well', 'here', 'her',
 'there', 'an', 'is', 'isn\'t', 'the', 'a', 'won\'t', '-', '...', 'was',
 'are', 'which', 'was', 'has', '–', '…', '&', 'into']

celebs = open('celebs.json', 'r').read()

most_visited_users = []#json.loads(open('../celebs.json', 'r').read())['usernames']

for user in json.loads(celebs)[fake].keys():
    most_visited_users.append(user)

for user in json.loads(celebs)[real].keys():
    most_visited_users.append(user)

# random integer object ensuring that the next random called is not equal to the
# previous or the second-previous or third-previous random number
class Random(object):
    def __init__(self, lower, upper):
        self.third_to_last = None
        self.second_to_last = None
        self.last = None
        self.lower = lower
        self.upper = upper

    def __call__(self):
        r = random.randint(self.lower, self.upper)
        while r == self.last or r == self.second_to_last or r == self.third_to_last:
            r = random.randint(self.lower, self.upper)
        self.second_to_last = self.last
        self.last = r
        return r

# gets 500 most recent tweets from a user post-2010 (the text)
def get_user_tweets(username):
    tweets = query.query_tweets_once("from:"+username, 500)
    ret = []
    for tweet in tweets:
        if len(tweet.text) > 0 and tweet.text[0] != '@':
            ret.append(tweet)
    return ret

# order tweets by activity
def sort_tweets_by_activity(tweets):
    def activityKey(tweet):
        return int(tweet.likes) + int(tweet.retweets) + int(tweet.replies)
    return sorted(tweets, key=activityKey, reverse=True)

# trim out uninteresting words from a tweet
def trim_uninteresting(tweet):
    toParse = tweet.text
    words = list(map(lambda x: x.lower(), toParse.split()))

    for word in most_used_words:
        words = list(filter(lambda x: x.lower() != word, words))

    for word in words:
        if word[0] == '@':
            words.remove(word)

    ret = " ".join(words)

    return ret

# remove all instances of string in strings
def removeAll(string, strings):
    while string in strings:
        strings.remove(string)

# finds the most used words from a list of tweets
def find_most_used(tweets):
    currentWordCounts = {}
    frequent_words = []
    for tweet in tweets:
        toParse = trim_uninteresting(tweet)
        words = map(lambda x: x.lower(), toParse.split())
        for word in words:
            if word in currentWordCounts:
                currentWordCounts[word] += 1
            else:
                currentWordCounts[word] = 1
    for word, value in sorted(currentWordCounts.items(), key=lambda tuple: (tuple[1], tuple[0])):
        frequent_words.append(word)
    return frequent_words

# returns a pair, with the first element being the given user's popular tweet
# and the second being a list of three celebrity tweets to go along with it
def find_related_tweets(username):
    top_tweets = sort_tweets_by_activity(get_user_tweets(username))
    if (len(top_tweets)) >= 10:
        top_tweets = top_tweets[:9]
        i = random.randint(0, 9)
        chosen_tweet = top_tweets[i]
    top_words = find_most_used([chosen_tweet])
    celeb_tweets = find_tweets_with(top_words)
    return (chosen_tweet, find_tweets_with)

# finds related popular celebrity tweets to a given set of words
def find_tweets_with(words):
    to_use = random.randint(0, len(words) - 1)
    final_word = words[to_use]
    tweet_1 = find_tweet_with(final_word)

# finds a tweet from a popular user that uses a specific word
def find_tweet_with(word):
    ret = None
    tweets = ['']
    while ret == None and len(tweets) > 0:
        curUser = most_visited_users[random.randint(0, len(most_visited_users) - 1)]
        tweets = sort_tweets_by_activity(get_user_tweets(curUser))
        for tweet in tweets:
            if word in tweet.text.split():
                ret = tweet
            else:
                tweets.remove(tweet)
        word = word[1:-1]
    return ret

# returns a random popular tweet from a user
def find_tweet_from_user(user):
    user_tweets = sort_tweets_by_activity(get_user_tweets(user))
    i = random.randint(0, 19)
    return user_tweets[i]


# returns four celebrity tweets as a json in the format:
# {real:{'user':'tweet'}, fake:{'user1':'tweet1', 'user2':'tweet2', 'user3':'tweet3'}
def find_four():
    json_ret = {}
    rand = Random(0, 99)
    true_user = most_visited_users[rand()]
    true_tweet = find_tweet_from_user(true_user)
    fake_1 = most_visited_users[rand()]
    fake_2 = most_visited_users[rand()]
    fake_3 = most_visited_users[rand()]
    ftweet_1 = find_tweet_from_user(fake_1)
    ftweet_2 = find_tweet_from_user(fake_2)
    ftweet_3 = find_tweet_from_user(fake_3)
    fake = {fake_1:ftweet_1.text, fake_2:ftweet_2.text, fake_3:ftweet_3.text}
    json_ret['real'] = {true_user:true_tweet.text}
    json_ret['fake'] = fake
    pics = {
        true_user:celebs.get_prof_pic(true_user),
        fake_1:celebs.get_prof_pic(fake_1),
        fake_2:celebs.get_prof_pic(fake_2),
        fake_3:celebs.get_prof_pic(fake_3)
    }
    json_ret['pics'] = pics
    return json.dumps(json_ret)
