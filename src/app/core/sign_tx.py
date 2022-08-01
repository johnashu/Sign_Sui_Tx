from asyncio.subprocess import PIPE
import subprocess
import logging


async def parse_response(res: str) -> tuple:

    pub_key = signed_txn = flag = None
    for x in res.strip().split("\n"):
        logging.error(x)
        x = x.split("sui::keytool:")
        y = x[1].strip().split(":")
        if "Public" in y[0]:
            pub_key = y[1].strip()
        if "Signature" in y[0]:
            signed_txn = y[1].strip()
        if "Flag" in y[0]:
            flag = y[1].strip()

    return signed_txn, pub_key, flag


async def sign_tx(owner_address: str, tx_bytes: str):
    cmd = ["sui", "keytool", "sign", "--address", owner_address, "--data", tx_bytes]
    logging.error(" ".join(cmd))
    proc = subprocess.run(
        cmd,
        encoding="utf8",
        universal_newlines=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    raw_proc = proc.stderr
    signed_txn, pub_key, flag = await parse_response(raw_proc)
    return signed_txn, pub_key, flag, raw_proc
