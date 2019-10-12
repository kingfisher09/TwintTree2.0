import twint.output
from TreeUser import *
from TwintTreeSearch import *
import twint.user
import pandas as pd
import numpy as np
import re

#set up dataframe
userlist = pd.DataFrame(columns=["user", "search", "layer"])
userlist.set_index("user")

rellist = set() # rellist and searchdata could make a nice class too


def searchfilter(user, layer): # This obviously needs work
    global rellist

    filtersalwayssearch = {"user": (),
                           "biowords": (),
                           "location": ()
                           }

    filtersmustcontain = {"biowords": (),
                          "location": (),
                          }
    filtlayers = []
    minconnections = np.inf

    filterswithin = {"followers": (0, 200),
                     "following": (0, np.inf),
                     "tweets": (0, np.inf),
                     "favourites": (0, np.inf),
                     "connections": (0, np.inf),
                     "layer": (0, 2)
                     }

    #get bio words
    regex = re.compile("[^a-zA-Z'-]")
    biowords = tuple(set(regex.sub(" ", user.bio.lower()).split()))

    connections = [u for rel in rellist for u in rel].count(user.username) # check this

    values = {"user": user.username,
              "biowords": biowords,
              "location": user.location,
              "followers": user.follwers,
              "following": user.following,
              "favourites": user.likes,
              "connections": connections,
              "layer": layer}


    for filter in filtersalwayssearch:
        if values[filter] in filtersalwayssearch[filter]:
            return True

    for filter in filtersmustcontain:
        if len([i for i in values[filter] if i in filtersmustcontain[filter]]) == 0 < len(filtersmustcontain[filter]):  # check length intersection of lists is greater than 0 and there are items in filter
            return False

    for filter in filterswithin:
        if not filterswithin[filter][0] <= values[filter] <= filterswithin[filter][1]:
            return False


    return True


def AddUser(listin, listfollows = None, listfollowedby = None):
    global userlist
    global rellist

    if listfollows != None and listfollowedby != None:
        raise Exception("Both listfollowed and listfollowedby used")


    if listfollows != None:  # check to see if this comes from a follows search
        searchdirection = "down"

    elif listfollowedby != None:
        searchdirection = "up"

    else:
        searchdirection = "flat"


    for user in listin:
        if not user.username in userlist.index.values.tolist():
            userdict = dict()
            layer = 0

            if searchdirection == "up":
                layer = userlist.loc[listfollowedby].layer - 1
            if searchdirection == "down":
                layer = userlist.loc[listfollows].layer + 1

            userlist.loc[user.username] = {"user": user, "search": searchfilter(user, layer), "layer": layer}


        if searchdirection == "up": # check to see if this comes from a follows search
            rellist.add((user.username, listfollows))

        if searchdirection == "down":
            rellist.add((listfollowedby, user.username))


topuser = getsingleuser("ofisher")
AddUser([topuser])

print(userlist)


AddUser(searchfollowers(topuser), listfollows=topuser.username) # would be good to fix this so list follows is automatically passed
print("searched followers")
AddUser(searchfollowing(topuser), listfollowedby=topuser.username)

print(userlist)