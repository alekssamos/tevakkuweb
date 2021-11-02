import os
import os.path
from tevakku import Tevakku
from flask import Flask
from flask import request
from flask import render_template

filename = os.path.join(os.path.dirname(__file__), "tevakku.db")
tv = Tevakku()

app = Flask(__name__)

@app.route("/", methods=['GET', 'HEAD'])
def index_page():
    requested=False
    response = {}
    q = request.args.get("q", "").strip()
    if q != "" and len(q) > 1:
        requested=True
        response = api_search()
    return render_template("index.html", requested=requested, response=response, q=q)

@app.route("/api/search", methods=['GET', 'HEAD'])
def api_search():
        q = request.args.get("q", "").strip()
        if q == "":
            return {"status":"error","results":{},"error_message":"GET q search query string parameter required"}
        return {
            "status":"ok",
            "results":{
                "sentences": tv.sentences(q),
                "tevakku": tv.tevakku(q),
                "tevakku_fts": tv.tevakku_fts(q)
            }
        }
