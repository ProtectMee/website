from flask import Flask, render_template, Response, request
from dotenv import dotenv_values, load_dotenv
from feedgen.feed import FeedGenerator
from pymongo import MongoClient
from datetime import datetime
import markdown, base64
import json, os, sys
app = Flask(__name__)

class DBException(Exception):
    pass

class env:
    try:
        load_dotenv("./.env")
    except Exception as e:
        raise(f"an error occurred while loading environment file! Exception: {e}")
    config = dotenv_values()

    ip = config.get("DB_IP")
    port = config.get("DB_PORT")
    username = config.get("DB_USERNAME")
    password = config.get("DB_PASSWORD")
    db_name = config.get("DB_NAME")
    version = config.get("VERSION")
    maintenance = config.get("MAINTENANCE")

maintenance = True if env.maintenance == "True" else False
version = env.version

class DB():

    def __init__(self, ip:str, port:str, username:str, password:str, db_name:str ,authentication=True):
        c = ""
        
        if authentication:
            c = f"{username}:{password}@"
        
        try:
            client = MongoClient(f"mongodb://{c}{ip}:{port}/{db_name}")[db_name]
        except Exception as e:
            print(f"[!] An error occurred while connecting to the database, exception: {e}")
            exit(1)
        self.posts = client.get_collection("posts")
        self.users = "" # TO DO

    def get_post(self, postn: int) -> dict:
        p: dict = self.posts.find_one({"post_id":postn})
        if not p == None:
            p.pop("_id")
            return p
        raise DBException("The post id inserted was not found")

db = DB(env.ip, env.port, env.username, env.password, env.db_name)

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
        n = int(n)
        p: list[dict] = []
        for i in range(1, n):

            try:
                p.append(db.get_post(i))
            except:
                pass
        return Response(json.dumps({"status":"Ok", "output":"success", "message":p}), 200)
    except ValueError:
        return Response(json.dumps({"status":"Ok", "output":"error", "message":"Impossibile recuperare gli articoli senza una quantità specifica!!"}), 500)
    


@app.route("/post", methods=["GET"])
def post():
    
    try:
        n = request.args["n"]
    except Exception:
        return Response("C'e' stato un errore durante la richiesta del post!", 500)

    try:
        int(n)
    except ValueError:
        return Response(json.dumps({"status":"Ok", "output":"error", "message":"Il numero dell'articolo non e' valido"}), 500)
    n = int(n)
    #Prendo dal database il contenuto del post, nel caso il post non venga trovato restituisco un errore!
    
    try:
        post = db.get_post(n)
    except DBException as e:

        print(f"Il post {n} non e' stato strovato, exception: {e}")
        return Response(json.dumps({"status":"Ok", "output":"error", "message":"Il numero dell'articolo non e' valido"}), 500)

    content = post["content"]
    title = post["title"]
    author = post["author"]
    post_img = post["post_img"]
    #Converto il testo da markdown in html, dopo averlo decodificato dal base64
    html = markdown.markdown(
        base64.b64decode(content).decode(),
        extensions=["extra", "codehilite", "toc"]
    )
    
    #Renderizzo il template base e lo invio all'utente finale
    return render_template(
        "post.html",
        title=title,
        post_img=post_img,
        content=html,
        author=author,
        version=version
    )
if __name__ == "__main__":
    app.debug = True
    app.run()