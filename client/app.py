from typing import Iterator
from flask import Flask, render_template, redirect, url_for, session, request
import json
import hashlib
import time
import random, string, requests

app = Flask(__name__)

gold = "0000"



def constructBlock():
    r = requests.get("http://127.0.0.1:5000")
    blockchain = r.json()
    block = blockchain[-1]
    data = []
    iteration = 0
    
    while True:
        s = string.ascii_lowercase
        data.append({
            "timestamp": time.time(),
            "sender": ''.join(random.choice(s) for i in range(10)),
            "recipient" : ''.join(random.choice(s) for i in range(10)),
            "amount": random.randrange(30000)
        })
        if iteration > 1000:
            break
        iteration = iteration + 1

    new_block = [{
        "block_id": int(block['block_id']) + 1,
        "previous_hash": block['hash'],
        "timestamp": time.time(),
        "data": data,
        "nounce": 0,
        "hash": ""
    }]

    to_hash = block['hash'] + json.dumps(data)

    blocks = [new_block, to_hash]
    return blocks



def mine(block, nounce):
    b = block + str(nounce)
    b = b.encode()
    return hashlib.sha256(b)




@app.route("/")
def index():
    return "Works"


@app.route("/startMine")
def startMine():

    block = constructBlock()

    iteration = 0
    while True:
        result = mine(block[1], iteration)
        if result.hexdigest().startswith(gold):
            print("--- FOUND HASH ---")
            print(result.hexdigest())
            print("Nounce: " + str(iteration))
            block[0][0]['nounce'] = iteration
            block[0][0]['hash'] = result.hexdigest()
            data = {
                "block": json.dumps(block[0])
            }
            response = requests.post("http://127.0.0.1:5000/registerNewBlock", data)
            print(response)
            return redirect(url_for("startMine"))
        else:
            print("Wrong hash | " + result.hexdigest())
            iteration += 1