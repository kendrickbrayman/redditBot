import os
import praw

def bot_login():
    print("Attempting Login...")
    try:
        r = praw.Reddit(
            username = os.environ['USERNAME'],
            password = os.environ['PASSWORD'],
            client_id = os.environ['CLIENTID'],
            client_secret = os.environ['SECRET'],
            user_agent = "bot"
        )
        print("Login Successful")
    except:
        print("Login Failed")
    return r