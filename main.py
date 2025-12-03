from flask import Flask, render_template, Response, request
from feedgen.feed import FeedGenerator
from datetime import datetime
import markdown, base64
import json, os, sys


app = Flask(__name__)

maintenance = False
version = 0.1
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
def get_articles():

    if maintenance:
        return Response(json.dumps({"status":"Ok", "output":"error", "message":"Impossibile recuperare gli articoli senza una quantità specifica!"}), 500)


    try:
        
        n = request.args["n"]
        ...
        # BISOGNA AGGIUNGERE LA FUNZIONE DEGLI ARTICOLI!
        return Response(json.dumps({"status":"Ok", "output":"success", "message":[]}), 200)
    except:
        return Response(json.dumps({"status":"Ok", "output":"error", "message":"Impossibile recuperare gli articoli senza una quantità specifica!"}), 500)
    


@app.route("/post", methods=["GET"])
def post():
    n = request.args["n"]
    try:
        int(n)
    except ValueError:
        return Response(json.dumps({"status":"Ok", "output":"error", "message":"Il numero dell'articolo non e' valido"}), 500)

    title = "Hello world!"
    content = "IyBIZWxsbyB3b3JsZCEKCkluY3JlZGliaWxlIHJhZ2F6emksIGNpIHNpYW1vIHJpdXNjaXRpIQoKcXVlc3RvIGUnIGlsIHByaW1vIHBvc3QgZGVsIGJsb2csIGRvcG8gYW5uaSBkaSBwcmVwYXJhemlvbmUgc2lhbW8gZmluYWxtZW50ZSBvbmxpbmUhCgpub24gdmVkbyBsJ29yYSBkaSBwb3J0YXJ2aSB1biBzYWNjbyBkaSBjb250ZW51dGkgZGkgKip0dXR0aSoqIGkgdGlwaS4KCm5laSBwcm9zc2ltaSBnaW9ybmkgdmkgdGVuZ28gYWdnaW9ybmF0aSBzdSB0dXR0aSBnbGkgYWdnaW9ybmFtZW50aSBkZWwgc2l0byB3ZWIsIG1hIHBvdGV0ZSBjb250YXJlIHF1ZXN0YSB2ZXJzaW9uZSBjb21hIGxhIHByaW1hIHZlcnNpb25lIGRlbCBzaXRvIAoKQnkgKipPbm9mcmlvKiogb24gKipQcm90ZWN0TWVlLnh5eiBWMC4xKio="
    author = "Onofrio"
    #Converto il testo da markdown in html, dopo averlo decodificato dal base64
    html = markdown.markdown(
        base64.b64decode(content).decode(),
        extensions=["extra", "codehilite", "toc"]
    )
    
    #Renderizzo il template base e lo invio all'utente finale
    return render_template(
        "post.html",
        title=title,
        post_img="1.png",
        content=html,
        author=author,
        version=version
    )
if __name__ == "__main__":
    app.debug = True
    app.run()