import requests
import re

def card_search(cardname):
    try:
        card_data = requests.get("https://api.scryfall.com/cards/named?fuzzy=", {"fuzzy": cardname}).json()
    except:
        card_data = None
    return card_data


def card_bot_main(comment_data):
    responses = {}
    try:
        if(len(comment_data["data"]) > 0):
            for comment in comment_data["data"]:
                comment_id = comment["id"]
                comment_body = comment["body"]
                if re.search(r'\[\[.+?\]\]',comment_body) is not None:

                    cardnames = re.findall("\[\[(.+?)\]\]", comment_body)
                    cards_info = []
                    for card in cardnames:
                        cards_info.append(card_search(card))

                    comment_reply = ""
                    for card in cards_info:
                        comment_reply += "[" + card["name"] + "](" + card['image_uris']['normal'] + ")[(Gatherer link)](https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=" + str(card["multiverse_ids"][0]) + ")\n"
                    responses[comment_id] = comment_reply
                else:
                    print("no comments yet...")
        else:
            print("no comments yet...")
    except Exception as e:
        print (str(e.__class__.__name__) + ": " + str(e))

    return responses
