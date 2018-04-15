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

most_visited_users = json.loads(open('celebs.json', 'r').read())['usernames']

# gets 500 most recent tweets from a user post-2010
def get_user_tweets(username):
    return query.query_tweets_once("from:"+username, 500)

# order tweets by activity
def sort_tweets_by_activity(tweets):
    def activityKey(tweet):
        return int(tweet.likes) + int(tweet.retweets) + int(tweet.replies)
    return sorted(tweets, key=activityKey)

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

# finds the top ten most used words from a list of tweets
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
    print("top words: "+" ".join(top_words))
    celeb_tweets = find_tweets_with(top_words)
    return (chosen_tweet, find_tweets_with)

# finds related popular celebrity tweets to a given set of words
def find_tweets_with(words):
    to_use = random.randint(0, len(words) - 1)
    final_word = words[to_use]
    print(final_word)
    tweet_1 = find_tweet_from_user(final_word)
    print(tweet_1.text)

# finds a tweet from a popular user that uses a specific word
def find_tweet_from_user(word):
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
