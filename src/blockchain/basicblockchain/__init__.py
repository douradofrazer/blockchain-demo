# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 19:26:38 2021

@author: doura
"""

from src.blockchain import Blockchain
from flask import Flask, jsonify

# Mining our Blockchain

# Creating a web app
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a Blockchain
blockchain = Blockchain()


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200


# Getting the full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid_chain():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    response = {'is_blockchain_valid': is_valid}
    return jsonify(response), 200


# Running the app
app.run(host='0.0.0.0', port=5000)
