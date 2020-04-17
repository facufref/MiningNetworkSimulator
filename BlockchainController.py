from argparse import ArgumentParser
from uuid import uuid4
from flask import Flask, jsonify, request
from Blockchain import Blockchain

# Instantiate our Node
app = Flask(__name__)

# Instantiate the Miner
blockchain = Blockchain()


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/get', methods=['GET'])
def get_nodes():
    response = {
        'message': 'Returning existing nodes',
        'nodes': list(blockchain.nodes)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
