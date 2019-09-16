# Trustless LETS
## Installation
Just install python of 3rd version.

## Launch Script
Script launch.py allow run system with input params like `--minToJoin`.

Script generate random 32 bytes and save it as base58-string in `memberScriptHash` variable.

## Usage

```bash
python3 launch.py --api-key API_KEY
```

## Command Line Options
- `-h`, `--help`            show this help message and exit
- `--mintojoin MINTOJOIN`
-                         Minimum number of ergs to be locked in the newly
-                         created member’s box
- `-s SERVER, --server SERVER`
-                         Address of RPC server in format SERVER:PORT
- `-q`, `--quiet`         Do not show debug output
- `--api-key API_KEY`     API key to pass RPC node authentication
- `--mainnet`             Using main net, default server localhost:9053
- `--testnet`             Using test net, default server localhost:9052

## How it works
- receives `api-key` as required param
- generate random 32 bytes string
- sending json document in `/script/p2sAddress`
- received string using as address for request to `/wallet/transaction/generate`
- send transaction to `/transactions`
- wrint to system.json follow object `{"boxId":$boxId, "transactionId":$txId, "asset": $tokenId, "updated": $timestamp}`

## Development

```bash
git clone https://github.com/sininen-taivas/LETS
git submodule init
git submodule update
# setub virtualenv
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```