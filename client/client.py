import json
import hashlib
import time
import random, string, requests


gold = "0000"

node_ips = [
    '84.211.93.161:5000'
]

def constructBlock():
    r = requests.get(node_ips[0])
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
            response = requests.post(node_ips[0], data)
            print(response)
            break
        else:
            print("Wrong hash | " + result.hexdigest())
            iteration += 1
    
    startMine()


startMine()