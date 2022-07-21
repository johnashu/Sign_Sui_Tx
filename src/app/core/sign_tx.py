import subprocess


def parse_response(res: str) -> tuple:
    return "new_tx_bytes", "signed_txn", "pub_key"


async def sign_tx(owner_address: str, tx_bytes: str):
    cmd = f"sui keytool sign --address {owner_address} --data {tx_bytes}"
    res = True  # subprocess.run(cmd)
    status = "success"
    new_tx_bytes, signed_txn, pub_key = parse_response(res)

    return status, new_tx_bytes, signed_txn, pub_key
