import codecs
import json
import re

import lda as lda
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors

import matplotlib.pyplot as plt

def main():
    # Get the celebrity tweets
    celebs_json = json.loads(codecs.open('celebs.json', 'r', 'utf-8').read())

    tweets = []
    usernames = []

    for celeb, celebs_tweets in celebs_json.items():
        if(len(celebs_tweets) > 20):
            # Remove all links and pics
            tweets.append(re.sub(r"(http\S+)|(pic.twitter\S+)", "",' '.join(celebs_tweets)))
            usernames.append(celeb)

    # Turn the tweets into vectors, where each dimension is a different word,
    #  and the length in each axis is the number of times the word appears.
    vectorizer = CountVectorizer(stop_words='english')
    train_count = vectorizer.fit_transform(tweets)

    # Transform the count vectors into tf-idf, where rarer words are weighed more, and the vectors are normalized.
    tfidf_transfomer = TfidfTransformer()
    train_tfidf = tfidf_transfomer.fit_transform(train_count)

    neigh = NearestNeighbors(n_neighbors=3)
    neigh.fit(train_tfidf)



    # Test with sample input
    test = ["#americanidol", "Human is a slang term for god",
            "Nihilism has deeply infected the GOP in congress, their beholdence to donors,lobbyists, and the rich has never been so blatant and cowardice"]
    test_tfidf = vectorizer.transform(test)

    res = neigh.kneighbors(test_tfidf, n_neighbors=3, return_distance=False)

    for idx, tweet in enumerate(test):
        users = [usernames[x] for x in res[idx]]
        print("\"{}\" could be from users {user[0]}, {user[1]}, {user[2]}".format(tweet,user=users))
    plotTopics(train_count, vectorizer.get_feature_names(), usernames)

# train_count is the count vector array
# vocab is the array mapping vector dimensions to words
# usernames is the list of twitter usernames
def plotTopics(train_count, vocab, usernames):
    # Visualization:
    colormap = np.array([
        "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
        "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
        "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
        "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"
    ])

    # Topic modeling using LDA
    lda_model = lda.LDA(n_topics = 10, n_iter = 400)
    train_topics = lda_model.fit_transform(train_count)

    _lda_keys = []
    for i in range(train_topics.shape[0]):
        _lda_keys += train_topics[i].argmax(),

    n_top_words = 5
    topic_summaries = []
    topic_word = lda_model.topic_word_  # all topic words
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]  # get!
        topic_summaries.append(' '.join(topic_words))  # append!

    # TSNE flattens the 20,000+ dimensional word vectors into an approximate 2D plane to visualize similarities
    tsne_model = TSNE(n_components=2, random_state=0)
    tsne_lda = tsne_model.fit_transform(train_topics)

    # Format the TSNE data for matplotlib
    x = [val[0] for val in tsne_lda]
    y = [val[1] for val in tsne_lda]

    plt.figure(figsize=(16, 16))

    # Plot the celebs
    for i in range(len(x)):
        plt.scatter(x[i], y[i],
                    color=colormap[_lda_keys[i]])
        plt.annotate(usernames[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')


    # Plot the topics
    topic_coord = np.empty((train_topics.shape[1], 2)) * np.nan
    for topic_num in _lda_keys:
        if not np.isnan(topic_coord).any():
            break
        topic_coord[topic_num] = tsne_lda[_lda_keys.index(topic_num)]

    # plot crucial words
    for i in range(train_topics.shape[1]):
        plt.annotate(topic_summaries[i],
                     xy=topic_coord[i],
                     color=colormap[i])

    plt.show()

if __name__ == '__main__':
    main()
