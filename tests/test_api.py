import requests
import curlify
import logging, json

logging.basicConfig(level=logging.INFO, format="[%(levelname)s]: %(message)s")


def create_mismatch_address(l: list) -> list:
    """Replace Last Letter of the addresses to create a mismatch

    Args:
        l (list): list of addresses to change

    Returns:
        list: list of changed addresses
    """
    rtn = []
    for x in l:
        x = x[:-1] + "a"
        rtn.append(x)
    return rtn


# Simple test script - execute when the app is running
url = "http://127.0.0.1:5000"

# Addresses should be correct to check that it converted correctly.
address = "0x2c53ba8163f740bb278194ac799f79275fe8dc6a"
token = "45yhrdue586rfhe5r87w4srj568ew45sjh568e4uj5e6rtjhyt4535jrtdsedgv"
tx = "YunLZjSe5u3S9C2/6m1JsUjd0zaXZvx+MyNieP61lQ0="

happy_flow = {"signed_txns": {"owner_address": address, "tx_bytes": tx}}
wrong_address = {"signed_txns": {"owner_address": "wrong_address", "tx_bytes": tx}}
wrong_token = {
    "token": "wrong_token",
    "signed_txns": {"owner_address": address, "tx_bytes": tx},
}
wrong_key = {"some_wrong_key": {"owner_address": address, "tx_bytes": tx}}
empty_request = {"signed_txns": {}}

headers = {"token": token}

mm = create_mismatch_address([address])
mismatch_one = {"some_wrong_key": {"owner_address": mm, "tx_bytes": tx}}


def make_request(params: dict, url: str = url, headers: list = None) -> list:
    res = requests.post(url, params=params, headers=headers)
    # logging.info Response
    logging.info(f"{res}  ::  {res.json()}\n\n")
    # logging.info cURL request..
    logging.info(f"cURL Request:\n{curlify.to_curl(res.request)}\n")
    return res.json()


def base(
    params: tuple, expected: str, status: str = None, mismatch: bool = False, **kw
) -> None:
    for p in params:
        r = make_request(p, **kw)
        exp_res = r[0].get(expected)
        assert exp_res, f"Expected: {exp_res} | Got: {status}"
        if status:
            assert exp_res == status, f"Expected: {exp_res} | Got: {status}"
        for idx, x in enumerate(r):
            if x.get("status") == "success":
                assert (
                    address == x["owner_address"]
                ), f"Expected: {address} | Got: {x['address']}"

            elif mismatch:
                assert address != x["owner_address"]


def test_happy_flow(**kw) -> None:
    base((happy_flow,), "status", status="success", **kw)


def test_address_mismatch(**kw) -> None:
    base((mismatch_one,), "status", status="error", mismatch=True, **kw)


def test_wrong_address(**kw) -> None:
    base((wrong_address,), "status", **kw)


def test_error_responses(**kw) -> None:
    base((wrong_key, empty_request), "error", **kw)


if __name__ == "__main__":
    kw = dict(url=url, headers=headers)

    # # test request
    params = {
        "signed_txns": [
            {"owner_address": address, "tx_bytes": tx},
            {"owner_address": address, "tx_bytes": tx},
        ]
    }
    make_request(json.dumps(params), **kw)

    # # manual check tests. - uncomment to run.
    # test_happy_flow(**kw)
    # test_address_mismatch(**kw)
    # test_error_responses(**kw)
    # test_wrong_address(**kw)
