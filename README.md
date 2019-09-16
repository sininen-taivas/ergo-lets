# Trustless LETS
## Installation
Just install python of 3rd version.

## Launch Script
### Usage

```bash
python3 launch.py --api-key API_KEY
```

### Command Line Options
- `-h`, `--help`            show this help message and exit
- `--mintojoin MINTOJOIN` Minimum number of ergs to be locked in the newly created member’s box
- `-s SERVER, --server SERVER` Address of RPC server in format SERVER:PORT
- `-q`, `--quiet`         Do not show debug output
- `--api-key API_KEY`     API key to pass RPC node authentication
- `--mainnet`             Using main net, default server localhost:9053
- `--testnet`             Using test net, default server localhost:9052

### How it works
- receives `api-key` as required param
- script allows run system with input params like `--mintojoin` default is `10`
- script generates random 32 bytes and save it as base58-string in `memberScriptHash` variable.

```scala
{
val minErgsToJoin = $minToJoin * 1000000000L

val memberBoxScriptHash = fromBase58("$memberScriptHash")

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
}
```

- sending json document to `/script/p2sAddress`
- received string using as address for request to `/wallet/transaction/generate`
- send transaction to `/transactions`
- write to system.json follow object `{"boxId":$boxId, "transactionId":$txId, "asset": $tokenId, "updated": $timestamp}` [^note1]

[^note1]: `tokenId` is first identifer from `assets` list from first `outputs`

### Development

```bash
git clone https://github.com/sininen-taivas/LETS
git submodule init
git submodule update
# setup virtualenv
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```