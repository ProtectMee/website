from flask import Flask, render_template, Response, request
from feedgen.feed import FeedGenerator
from datetime import datetime
import json, os, sys


app = Flask(__name__)

maintenance = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rss")
def readrss():
    fg = FeedGenerator()
    fg.title('ProtectMee Feed')
    fg.link(href='https://protectmee.xyz/rss', rel='self')
    fg.description('Articoli sulla cybersicurezza pubblicati su ProtectMee')
    fg.language('it')

    # Aggiungi gli articoli
    for articolo in []:
        fe = fg.add_entry()
        fe.title(articolo['title'])
        fe.link(href=articolo['link'])
        fe.description(articolo['description'])
        fe.pubDate(datetime.fromisoformat(articolo['pubDate']))

    # Genera XML
    rss_feed = fg.rss_str(pretty=True)
    return Response(rss_feed, mimetype='application/rss+xml')

@app.route("/get_articles", methods=["GET"])
def get_article():

    if maintenance:
        return Response(json.dumps({"status":"Ok", "output":"error", "message":"Impossibile recuperare gli articoli senza una quantità specifica!"}), 500)


    try:
        
        n = request.args["n"]
        ...
        # BISOGNA AGGIUNGERE LA FUNZIONE DEGLI ARTICOLI!
    except:
        return Response(json.dumps({"status":"Ok", "output":"error", "message":"Impossibile recuperare gli articoli senza una quantità specifica!"}), 500)
    
    return Response(json.dumps({"status":"Ok", "output":"success", "message":[]}), 200)

if __name__ == "__main__":
    app.debug = False
    app.run()