import query
import random

most_used_words = ['the', 'be', 'and', 'of', 'a', 'in', 'to', 'have', 'it', 'i',
 'that', 'for', 'you', 'he', 'with', 'on', 'do', 'say', 'this', 'they', 'at',
 'but', 'we', 'his', 'from', 'that', 'not', 'by', 'she', 'or', 'as', 'what',
 'go', 'their', 'can', 'who', 'get', 'if', 'would', 'her', 'all', 'my', 'make',
 'about', 'know', 'will', 'as', 'up', 'one', 'there', 'so', 'when', 'which'
 'them', 'me', 'him', 'could', 'like', 'how', 'then', 'than', 'how', 'its'
 'our', 'these', 'new', 'because', 'thing', 'those', 'well', 'here', 'her',
 'there', 'an', 'is', 'isn\'t', 'the', 'a', 'won\'t', '-', '...', 'was',
 'are', 'which', 'was', 'has', '–', '…', '&', 'into']

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

    ret = " ".join(words)

    return ret

# remove all instances of string in strings
def removeAll(string, strings):
    while string in strings:
        strings.remove(string)

# finds the top ten most used words from a list of tweets
def find_most_used(tweets):
    currentWordCounts = {}
    boring_words = []
    for tweet in tweets:
        toParse = trim_uninteresting(tweet)
        words = map(lambda x: x.lower(), toParse.split())
        for word in words:
            if word in currentWordCounts:
                currentWordCounts[word] += 1
            else:
                currentWordCounts[word] = 1
    for word, value in sorted(currentWordCounts.items(), key=lambda tuple: (tuple[1], tuple[0])):
        boring_words.append(word)
    return boring_words


# finds related popular tweets to one of a person's top 10 tweets, chosen at random
def find_related_tweets(username):
    top_tweets = sort_tweets_by_activity(get_tweets(username))
    if (len(top_tweets)) >= 10:
        top_tweets = top_tweets[:9]
        i = random.randint(0, 9)
        chosen_tweet = top_tweets[i]
    top_words = find_most_used([chosen_tweet])
