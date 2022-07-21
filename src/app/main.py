import uvicorn
import urllib.parse, json
import logging

from core.sign_tx import *
from includes.messages import *
from includes.tokens import *


async def process_sign(send, signed_txns: list) -> list:
    body = []

    err = {
        "error": "Signing failed owner_address or bytes empty.",
        "owner_address": owner_address,
        "tx_bytes_sent": tx_bytes,
    }

    for i, x in enumerate(signed_txns):
        owner_address = x.get("owner_address")
        tx_bytes = x.get("tx_bytes")

        if not owner_address or not tx_bytes:
            body.append(err)
            return False, await send_response(send, body, status=400)
        else:
            signed_txn, pub_key = await sign_tx(owner_address, tx_bytes)
            if not signed_txn or not pub_key:
                body.append(err)
                return False, await send_response(send, body, status=404)

            body.append(
                {
                    "item": i,
                    "status": "success",
                    "signed_txn": signed_txn,
                    "pub_key": pub_key,
                    "owner_address": owner_address,
                    "tx_bytes_sent": tx_bytes,
                }
            )

    return True, body


async def send_response(send, body: list, status: int = 200):
    await send(dict(http_response_start, **{"status": status}))
    body = json.dumps(body).encode("utf-8")
    await send(dict(http_response_body, **{"body": body}))


async def app(scope, receive, send):
    assert scope["type"] == "http"
    q = scope["query_string"]
    h = scope["headers"]
    token = dict((x, y) for x, y in h).get(b"token")
    token = token.decode()

    if token not in accepted_tokens:
        body = [{"error": token_refused}]
        await send_response(send, body, status=401)
    if not q:
        body = [{"error": empty_msg}]
        await send_response(send, body, status=400)
    else:
        dec = urllib.parse.unquote_plus(q.decode())
        params = json.loads(dec)
        signed_txns = params.get("signed_txns")
        if not signed_txns:
            body = [{"error": bad_request_msg}]
            await send_response(send, body, status=400)
        else:
            res, body = await process_sign(send, signed_txns)
            if res:
                await send_response(send, body)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
