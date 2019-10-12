import PySimpleGUIQt as sg
import TwintTreeSearch
import threading


treedata = sg.TreeData()


print(treedata)
layout = [[sg.Text("Search Username😊"), sg.InputText(key="username"), sg.Button("Search")],
         [sg.Tree(data = treedata,
                  headings=["Name", "Following", "Followers", "Tweets", ],
                  num_rows=20,
                  key="usertree",
                  auto_size_columns=True,
                  col0_width=30)]]

window = sg.Window("Twint Tree", layout)
#window = sg.Window('Twint Tree', layout, resizable=True, finalize=True)

#window.Maximize()

def addsearch(firstuser):
    for user in firstuser.searchfollowers():
        treedata.Insert(firstuser.username + "followers", user.username, user.username,
                        [user.name, user.following, user.followers, user.tweets])
    window.Element("usertree").Update(treedata)


while True:

    event, values = window.Read()

    if event in (None, 'Cancel'):
        break

    if event == "Search":
        firstuser = TwintTreeSearch.getsingleuser(values["username"])
        treedata.Insert("", firstuser.username, firstuser.username, [firstuser.name, firstuser.following, firstuser.followers, firstuser.tweets])
        print(treedata)
        window.Element("usertree").Update(treedata)
        treedata.Insert(firstuser.username, firstuser.username + "followers", "Followers", "")
        thread = threading.Thread(target=addsearch(firstuser))
        thread.daemon = True
        thread.start()

window.Close()


