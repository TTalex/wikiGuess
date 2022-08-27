import requests
import random

S = requests.Session()

URL = "https://fr.wikipedia.org/w/api.php"

def getRandomPages():
    PARAMS = {
    	"action": "query",
    	"format": "json",
    	"generator": "random",
    	"grnnamespace": "0",
        "grnlimit": "20",
        "prop": "pageviews",
    	"pvipmetric": "pageviews",
    	"pvipdays": "1"
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA["query"]["pages"]
    pagesList = list(filter(lambda p: ":" not in p["title"], list(PAGES.values())))
    return random.sample(pagesList, 10)

def getRandomMostViewedPages():
    PARAMS = {
    	"action": "query",
    	"format": "json",
    	"list": "mostviewed",
    	"utf8": 1,
    	"ascii": 1,
    	"pvimlimit": "100"
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA["query"]["mostviewed"]
    pagesList = list(filter(lambda p: ":" not in p["title"], PAGES))
    return random.sample(pagesList, 10)

def getBacklinks(pageTitle):
    PARAMS = {
    	"action": "query",
    	"format": "json",
    	"prop": "pageviews",
    	"pvipmetric": "pageviews",
    	"pvipdays": "1",
    	"generator": "backlinks",
    	"utf8": 1,
    	"ascii": 1,
        "gblfilterredir": "nonredirects",
        "gbltitle": pageTitle,
    	"gblnamespace": "0",
    	"gbllimit": "100"
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA["query"]["pages"]
    return PAGES.values()

def getPageView(page):
    if "pageviews" not in page:
        return 0
    pageViews = list(page["pageviews"].values())[0] or 0
    page["count"] = pageViews
    return pageViews

def game(hardMode=False):
    if hardMode:
        randomPages = getRandomPages()
        randomPages.sort(key=getPageView, reverse=True)
    else:
        randomPages = getRandomMostViewedPages()
    randomPage = random.choice(randomPages)
    backlinks = list(getBacklinks(randomPage["title"]))
    backlinks.sort(key=getPageView, reverse=True)
    return {
        "randomPages": randomPages,
        "randomPage": randomPage,
        "backlinks": backlinks[:20]
    }



if __name__ == '__main__':
    gameData = game()
    for page in gameData["backlinks"]:
        print(page)

    i = 1
    for page in gameData["randomPages"]:
        print(i, page)
        i += 1
    input()

    print(gameData["randomPage"]["title"])
else:
    from flask import Flask, url_for

    app = Flask(__name__)
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    @app.route("/api/easy")
    def easy():
        return game(False)
    @app.route("/api/hard")
    def hard():
        return game(True)
