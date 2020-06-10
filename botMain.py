import praw
import json
import requests
import bot_login
import card_fetcher
import time

def reply_to_comment(r, comment_id, comment_reply):
    try:
        parent_comment = r.comment(comment_id)
        parent_comment.reply(comment_reply)
        print("Fetch details: /n{}".format(comment_reply))
    except Exception as e:
        print (str(e.__class__.__name__) + ": " + str(e))
        time_remaining = 15
        for i in range(time_remaining, 0, -5):
            print("Retrying in", i, "seconds..")
            time.sleep(5)

def get_recent_utc(subreddit):
    try:
        t = requests.get("https://api.pushshift.io/reddit/search/comment/?",{"subreddit":subreddit,"size":1,"fields":"created_utc"}).json()['data'][0]['created_utc']
    except Exception as e:
        print (str(e.__class__.__name__) + ": " + str(e))
        t = None
    return t

def get_comments(subreddit, created_utc):
    print("\nFetching comments...")
    try:
        comments_data = requests.get("https://api.pushshift.io/reddit/search/comment/?fields=body,created_utc,id",{"subreddit":subreddit,"after":created_utc}).json()
    except Exception as e:
        print (str(e.__class__.__name__) + ": " + str(e))
        comments_data = None

    return comments_data


def bot_function(r,function_param):

    try:
        if function_param == "mtgbot":
            created_utc = get_recent_utc("magictcg")
            comment_data = get_comments("magictcg", created_utc)
            resp = card_fetcher.card_bot_main(comment_data)



        for id,response in resp.items():
            reply_to_comment(r,id,response)

    except Exception as e:
        print (str(e.__class__.__name__) + ": " + str(e))

    return created_utc


if __name__ == "__main__":
    while True:
        try:
            r = bot_login.bot_login()
            function_param = input("Enter function parameter option: \nmtgbot\n")

            while True:
                created_utc = bot_function(r, function_param)
                time.sleep(15)

        except Exception as e:
            print (str(e.__class__.__name__) + ": " + str(e))
            time.sleep(10)