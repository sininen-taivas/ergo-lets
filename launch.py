#!/usr/bin/env python3
import json
import logging
from argparse import ArgumentParser, FileType, ArgumentTypeError

from utils.util import TARGET_SERVER, ErgoClient, setup_logger, pwgen
from base58 import b58encode

def parse_cli():
    parser = ArgumentParser()
    parser.add_argument(
        '--minToJoin',
        help=''
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


def main():
    opts = parse_cli()
    setup_logger(not opts.quiet)

    target_ = 'mainnet'
    if opts.testnet:
        target_ = 'testnet'

    server_ = opts.server or TARGET_SERVER[target_]
    api = ErgoClient(server_, opts.api_key)

    # generate random 32-bytes string
    random_string = pwgen(32)
    logging.debug(f'Generate random string {random_string}')
    member_script_hash = b58encode(random_string)
    logging.debug(f'Base58 hash {member_script_hash}')

    print('> TODO')
    print('- format JSON')
    print('- send to /script/p2sAddress')
    print('- received string using as address for request to /wallet/transaction/generate')
    print('- received transaction sending to /transactions')
    print('- write to system.json: {"boxId":$boxId, "transactionId":$txId, "asset": $tokenId, "updated": $timestamp}')
    # generate JSON for API
    # data = {

    # }



if __name__ == '__main__':
    main()
