import instaloader
import getpass

# need "pip install instaloader"
Loader = instaloader.Instaloader()

username = input("Please input your id : ")
password = getpass.getpass("Please input your password : ")
Loader.login(username, password)

profile = instaloader.Profile.from_username(Loader.context, username)

follower_list = []
for f in profile.get_followers():    
    follower_list.append([f.username, f.full_name])

following_list = []
for f in profile.get_followees():    
    following_list.append([f.username, f.full_name])

not_following = []
for i in range(len(following_list)):
    if not following_list[i] in follower_list:
        not_following.append(following_list[i])

not_follower = []
for i in range(len(follower_list)):
    if not follower_list[i] in following_list:
        not_follower.append(follower_list[i])

print("follwer : %d, following : %d" % (len(follower_list), len(following_list)))

print('나는 팔로우하지만 상대방은 날 팔로우하지 않는 사람 -> ')
for i in range(len(not_following)):
    print("id : \033[32m%s\033[0m, name : \033[32m%s\033[0m" % (not_following[i][0], not_following[i][1]))

print('나는 팔로우하지 않지만 상대방은 날 팔로우하는 사람 -> ')
for i in range(len(not_follower)):
    print("id : \033[32m%s\033[0m, name : \033[32m%s\033[0m" % (not_follower[i][0], not_follower[i][1]))
