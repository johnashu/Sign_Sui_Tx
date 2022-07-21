from asyncio.subprocess import PIPE
import subprocess
import logging


async def parse_response(res: str) -> tuple:

    pub_key = ""
    signed_txn = ""
    for x in res.strip().split("\n"):
        logging.error(x)
        x = x.split("sui::keytool:")
        y = x[1].strip().split(":")
        if "Public" in y[0]:
            pub_key = y[1].strip()
        if "Signature" in y[0]:
            signed_txn = y[1].strip()

    return signed_txn, pub_key


async def sign_tx(owner_address: str, tx_bytes: str):
    cmd = ["sui", "keytool", "sign", "--address", owner_address, "--data", tx_bytes]
    # res = subprocess.run(cmd, capture_output=True)
    proc = subprocess.Popen(
        cmd, universal_newlines=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    try:
        outs, errs = proc.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    logging.error(outs)
    logging.error(errs)
    logging.error(proc)
    status = "success"
    signed_txn, pub_key = await parse_response(errs)
    return status, signed_txn, pub_key


# address = "0x23beb41b7c55e126750f2077c02b32cdfa62631d"
# tx = "VHJhbnNhY3Rpb25EYXRhOjoAAA5DDnUxesba/mkUle3mKD19oMuNBOlVM5Q2T84wXCMpPv80EKJ0lG4CAAAAAAAAACDB6V7wwJvpauO/5C8WV0U347WvnIWAUcuQQ5y9crBuSiO+tBt8VeEmdQ8gd8ArMs36YmMdBOlVM5Q2T84wXCMpPv80EKJ0lG4CAAAAAAAAACDB6V7wwJvpauO/5C8WV0U347WvnIWAUcuQQ5y9crBuSgEAAAAAAAAA6AMAAAAAAAA="
# sign_tx(address, tx)


# {'signed_txns': [{'owner_address': '0x23beb41b7c55e126750f2077c02b32cdfa62631d', 'tx_bytes': 'VHJhbnNhY3Rpb25EYXRhOjoAAA5DDnUxesba/mkUle3mKD19oMuNBOlVM5Q2T84wXCMpPv80EKJ0lG4CAAAAAAAAACDB6V7wwJvpauO/5C8WV0U347WvnIWAUcuQQ5y9crBuSiO+tBt8VeEmdQ8gd8ArMs36YmMdMSLyDVC/GFMeFb0zY3KOGJnN1DYCAAAAAAAAACAxCFCOmlbmlOWDzjdSDz9pxrju+AD0G/lDHq8tGFRIqQEAAAAAAAAA6AMAAAAAAAA='}, {'owner_address': '0x23beb41b7c55e126750f2077c02b32cdfa62631d', 'tx_bytes': 'VHJhbnNhY3Rpb25EYXRhOjoAAA5DDnUxesba/mkUle3mKD19oMuNBOlVM5Q2T84wXCMpPv80EKJ0lG4CAAAAAAAAACDB6V7wwJvpauO/5C8WV0U347WvnIWAUcuQQ5y9crBuSiO+tBt8VeEmdQ8gd8ArMs36YmMdMSLyDVC/GFMeFb0zY3KOGJnN1DYCAAAAAAAAACAxCFCOmlbmlOWDzjdSDz9pxrju+AD0G/lDHq8tGFRIqQEAAAAAAAAA6AMAAAAAAAA='}]}
