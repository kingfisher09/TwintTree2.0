import twint
import twint.output
import twint.tweet
import twint.user


class TreeUser:

    def __init__(self, userin):
        for attr in [x for x in dir(userin) if not x[0] == "_"]: # copy everything out of user object
            try:
                setattr(self, attr, getattr(userin, attr))
            except:
                pass

        self.followersearched = False
        self.followingsearched = False
        self.tweetssearched = False
        self.favouritessearched = False
        self.followerslist = set()
        self.followinglist = set()
        self.tweets = []
        self.favourites = []
        self.tweetedhashtags = dict()  # dict key is hashtag, value is number of times used


    def __eq__(self, other):  # Compare instances of TreeUser
        if isinstance(other, TreeUser):
            try:
                if self.username == other.username:
                    return True
            except AttributeError:
                pass

        return False

    def __hash__(self):
        return int(self.id)


