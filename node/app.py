from flask import Flask, redirect, url_for, session, request
import json

from flask.templating import render_template


app = Flask(__name__)

def getLocalBlockchain():
    f = open("./data/blockchain.json")
    x = json.load(f)
    return x


@app.route("/")
def index():
    localBlockchain = getLocalBlockchain()
    return json.dumps(localBlockchain)

@app.route("/registerNewBlock", methods = ['POST'])
def registerNewBlock():
    # Get data from request
    # Check if block fits on any of the current local blockchains.
    # If it does not, query other nodes for blockchains. If it does, add block to blockchain.
    # Check if block fits on any of the queried blocks.
    # If it does, create new alternative local blockchain and add new block.
    # Flag as conflicted, wait for new blocks to come in and do checks.

    if request.method == "POST":
        if request.form.get("block"):
            block = request.form.get("block")
            localBlockchain = getLocalBlockchain()
            b = json.loads(block)
            localBlockchain.append(b[0])
            f = open("data/blockchain.json", "w")
            f.write(json.dumps(localBlockchain))
            return "Success."
    return "Failure"

@app.route("/gui")
def gui():
    try:
        lbc = getLocalBlockchain()
    except:
        pass
    iters = 0
    for b in lbc:
        iters += 1
        print(iters)
    return render_template("index.html", lbc = lbc)