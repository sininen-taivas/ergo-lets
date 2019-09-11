# Trustless LETS

## Launch Script
Script launch.py allow run system with input params like `--minToJoin`.

Script generate random 32 bytes and save it as base58-string in `memberScriptHash` variable.


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