import numpy as np
from .models import User
from sklearn.linear_model import LogisticRegression
from.twitter import vectorize_tweet


def predict_user(user0, user1, hypo_tweet):

    user0 = User.query.filter(User.username==user0).one()
    user1 = User.query.filter(User.username==user1).one()

    # 2D numpy arrays
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])
    
    # X Matrix for training the logistic regression
    vects = np.vstack([user0_vects, user1_vects])

    # 1D numpy arrays
    zeros = np.zeros(len(user0.tweets))
    ones = np.ones(len(user1.tweets))

    # y vector (target) for training logistic regression
    labels = np.concatenate([zeros, ones])

    # instantiate logistic regression model
    log_reg = LogisticRegression()
    # training our logistic regression model
    log_reg.fit(vects, labels)

    # vectorize word embeddings for the hypo_tweet
    hypo_tweet_vect = vectorize_tweet(hypo_tweet)

    # get prediction for which user is more likely to have said the hypo_tweet
    prediction = log_reg.predict(hypo_tweet_vect.reshape(1,-1))

    return prediction[0]
