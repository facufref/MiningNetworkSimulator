from argparse import ArgumentParser
from flask import Flask, jsonify, request
from Miner import Miner
import requests
from GeneralSettings import host_address, blockchain_port

# Instantiate our Node
app = Flask(__name__)

# Instantiate the Miner
miner = Miner()


@app.route('/mine', methods=['GET'])
def mine():
    block = miner.mine()

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'timestamp': block['timestamp']
    }

    return jsonify(response), 200


@app.route('/mine_forever', methods=['GET'])
def mine_forever():
    block = miner.mine()

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'timestamp': block['timestamp']
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = miner.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': miner.chain,
        'length': len(miner.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST']) # TODO: Remove
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        miner.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(miner.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])  # TODO: Remove
def consensus():
    replaced = miner.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': miner.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': miner.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    #  On start, register the Miner on the blockchain
    requests.post(f'{host_address}{blockchain_port}/nodes/register', json={'nodes': [f"{host_address}{port}"]})

    app.run(host='0.0.0.0', port=port)
