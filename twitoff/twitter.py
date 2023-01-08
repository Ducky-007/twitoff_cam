from os import getenv
from .models import DB, User, Tweet
import tweepy
import spacy

# getting our environmental varibles
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_SECRET')

# making the connection to the twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

def add_or_update_user(username):

    try:
        twitter_user = TWITTER.get_user(screen_name=username)

        # if there's no user in the DB create one
        # if there IS one in the DB already, let that be our db_user
        db_user = (User.query.get(twitter_user.id) or User(id=twitter_user.id, username=username))

        DB.session.add(db_user)

        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             vect=tweet_vector,
                             user_id=db_user.id)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f'Error processing {username}: {e}')
        raise e
    
    else:
        DB.session.commit()

    
# take tweet text and turn it into a word embedding "vector"
nlp = spacy.load('my_model/')

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector