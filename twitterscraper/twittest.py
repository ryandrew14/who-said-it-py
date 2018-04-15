from query import query_tweets_once
import utils

if __name__ == '__main__':
    tweets_from_user = utils.sort_tweets_by_activity(query_tweets_once("from:ryandrew8", 1000))
    list_of_tweets = utils.sort_tweets_by_activity(query_tweets_once("from:realdonaldtrump", 100))

    # print the retrieved tweets to the screen:
    '''for tweet in list_of_tweets:
        print(tweet.timestamp)'''
    for word in utils.find_most_used(list_of_tweets):
        print(word)
