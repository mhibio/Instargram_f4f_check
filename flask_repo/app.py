from flask import Flask, render_template, request, redirect
import instaloader

WRONGPASSWORD = 0xdead
PLEASEWAIT = 0xbeef
USERNOTFOUND = 0xcafe
OTHER = 0xbabe


app = Flask(__name__)

def get_insta_f4f(username, password):
    Loader = instaloader.Instaloader()
    
    try:
        Loader.login(username, password)

    except instaloader.exceptions.BadCredentialsException:
        return WRONGPASSWORD

    except instaloader.exceptions.InvalidArgumentException:
        return USERNOTFOUND

    except instaloader.exceptions.ConnectionException:
        return PLEASEWAIT

    except:
        return OTHER

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

    return not_following, not_follower

@app.errorhandler(404)
def page_not_found(error):
    return render_template('./error/404.html')

@app.route('/')
def routing(): 
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def index(num=None):
    if request.method == "POST":
        id = request.form.get('id')
        pw = request.form.get('pw')
        res = get_insta_f4f(id, pw)
        if res == WRONGPASSWORD:
            return render_template('./error/wrong_password.html')

        elif res == PLEASEWAIT:
            return render_template('./error/please_wait.html')

        elif res == USERNOTFOUND:
            return render_template('./error/usernot_found.html')

        elif res == OTHER:
            return render_template('./error/other_error.html')

        return render_template('form_result.html', result1 = res[0], result2=res[1])

    else:
        return render_template('./error/400.html')
        
if __name__ == '__main__':
	app.run(debug=True, threaded=True)
    
'''
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
'''