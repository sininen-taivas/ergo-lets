#!/usr/bin/env python3
import json
import logging
from time import time
from argparse import ArgumentParser, FileType, ArgumentTypeError

from utils.util import TARGET_SERVER, ErgoClient, setup_logger
from base58 import b58encode

def parse_cli():
    parser = ArgumentParser()
    parser.add_argument(
        '--mintojoin',
        default=10,
        help='Minimum number of ergs to be locked in the newly created member’s box'
    )
    parser.add_argument(
        '-s', '--server',
        help='Address of RPC server in format SERVER:PORT'
    )
    parser.add_argument(
        '-q', '--quiet', action='store_true', default=False,
        help='Do not show debug output'
    )
    parser.add_argument(
        '--api-key',
        required=True,
        help='API key to pass RPC node authentication',
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--mainnet', action='store_true',
                       help='Using main net, default server localhost:9053')
    group.add_argument('--testnet', action='store_true',
                       help='Using test net, default server localhost:9052')

    opts = parser.parse_args()
    return opts


def gen_random_string():
    import secrets
    # generate random 32-bytes string
    random_string = secrets.token_hex(16)
    logging.debug(f'Generate 32 random string {random_string}')
    return random_string

def main():
    opts = parse_cli()
    setup_logger(not opts.quiet)

    target_ = 'mainnet'
    if opts.testnet:
        target_ = 'testnet'

    server_ = opts.server or TARGET_SERVER[target_]
    api = ErgoClient(server_, opts.api_key)

    random_string = gen_random_string()
    member_script_hash = b58encode(random_string)
    logging.debug(f'Base58 hash {member_script_hash}')
    s = """{
val minErgsToJoin = %s * 1000000000L

val memberBoxScriptHash = fromBase58("%s")

val letsTokenId = SELF.tokens(0)._1

val tokenBox = OUTPUTS(0) // the first output must also be a tokenBox
// first output contains remaining LETS tokens

def isLets(b:Box) = { // returns true if b is a LETS box
   // A LETS box must have exactly 1 membership token in tokens(0)
   b.tokens(0)._1 == letsTokenId && b.tokens(0)._2 == 1 &&
   blake2b256(b.propositionBytes) == memberBoxScriptHash &&
   SELF.R4[Long].get == 0 && // start the box with zero LETS balance
   b.value >= minErgsToJoin && // the box must contain some minimum ergs
   b.R6[Long].get <= HEIGHT // store the creation height in R6
}

// how many lets boxes created in the tx
val numLetsBoxes = OUTPUTS.filter({(b:Box) => isLets(b)}).size

// In the transaction following is preserved for the token box ...
tokenBox.tokens(0)._1 == SELF.tokens(0)._1 &&                //  token id
tokenBox.tokens(0)._2 == SELF.tokens(0)._2 - numLetsBoxes && //  quantity
tokenBox.propositionBytes == SELF.propositionBytes
}""" % (opts.mintojoin, member_script_hash.decode("utf-8"))
    logging.debug(f'json: {s}')
    logging.debug('send to /script/p2sAddress')

    code, p2s_address = api.request('/script/p2sAddress', data={'source': s})
    logging.debug(f'result: [{code}] {p2s_address}')
    if code != 200:
        logging.error(p2s_address)
        exit(1)

    json_data = {
        "requests": [
            {
                "address": p2s_address.get('address', ''),
                "amount": 1000000,
                "name": "LETS",
                "description": "test desc",
                "decimals": 0
            }
        ],
        "fee": 1000000,
        "inputsRaw": []
    }
    logging.debug('received string using as address for request to /wallet/transaction/generate')
    code, tx_json = api.request('/wallet/transaction/generate', data=json_data)
    logging.debug(f'result: [{code}] {tx_json}')
    if code != 200:
        logging.error(tx_json)
        exit(1)

    # If no errors POST to /transactions
    url_ = '/transactions'
    logging.debug('Send transaction to %s' % url_)
    code, txid = api.request(url_, data=tx_json)
    if code != 200:
        logging.error(txid)
        exit(1)

    logging.debug(f'txId: {txid}')

    tx_data = {}
    for box in tx_json.get('outputs', [])[:1]:
        tx_data.update(boxId=box['boxId'], transactionId=txid, updated=int(time()))
        for asset in box.get('assets', [])[:1]:
            tx_data.update(tokenId=asset.get('tokenId'))

    logging.debug(f'w -> system.json: {tx_data}')
    if not tx_data:
        logging.error('Not found needed box')
        exit(1)

    out_filename = 'system.json'
    try:
        with open(out_filename, 'w+') as fw:
            logging.debug(f'Write to file {out_filename}')
            fw.write(json.dumps(tx_data))
    except IOError as er:
        logging.debug(f'Write file error: {er}')
        exit(1)

    logging.debug('OK')


if __name__ == '__main__':
    main()
