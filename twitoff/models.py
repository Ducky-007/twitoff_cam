from flask_sqlalchemy import SQLAlchemy

# create conn to sqlalchemy
DB = SQLAlchemy()

# create class using DB Model REMEMBER TO CAPITALIZE M in Models!!!!!!!!
class User(DB.Model):
    # user will have 2 attributes: id, username
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    username = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    text = DB.Column(DB.Unicode(300), nullable=False)
    vect = DB.Column(DB.PickleType, nullable=False)

    # creating a relationship between users and tweets
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # create a whole list of tweets to be attached to the user
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)