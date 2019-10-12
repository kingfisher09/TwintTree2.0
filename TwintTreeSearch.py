import twint.output
from TreeUser import *
import twint.user

def retconfig(username):
    c = twint.Config
    c.Username = username
    c.Hide_output = True
    c.Store_object = True
    c.User_full = True
    return c


def getsingleuser(username):
    c = retconfig(username)
    twint.run.Lookup(c)
    return TreeUser(twint.output.users_list[0])


def searchfollowers(user):
    c = retconfig(user.username)
    twint.output.users_list.clear()
    twint.run.Followers(c)
    for userout in twint.output.users_list:
        user.followerslist.add(userout.username)
    return [TreeUser(tuser) for tuser in twint.output.users_list]


def searchfollowing(user):
    c = retconfig(user.username)
    twint.output.follows_list.clear()
    twint.run.Following(c)

    for userout in twint.output.users_list:
        user.followinglist.add(userout.username)
    return [TreeUser(tuser) for tuser in twint.output.users_list]


def searchtweets(user):
    c = retconfig(user.username)
    twint.output.tweets_list.clear()
    twint.run.Search(c)
    hashtags = dict()

    for hashtag in [tags for tweet in twint.output.tweets_list for tags in tweet.hashtags]: # combine all hashtags from tweets
        if hashtag in user.tweetedhashtags.keys():
            hashtags += 1
        else:
            hashtags[hashtag] = 1

    return twint.output.tweets_list, hashtags


def searchfavourites(user):
    twint.output.tweets_list.clear()
    c = retconfig(user.username)

    return twint.output.tweets_list
