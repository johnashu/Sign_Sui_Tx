# Expose TX Signing Tool For SUI 

Asynchronous Base Service to Enable remote TX Signing

Serves results via API POST request.
# Run with Docker

On an OS with Docker installed.

`docker-compose build`

`docker-compose up`

# Run locally

`python3 main.py`

# Build Request

Example with Python

```python
import requests

# define URL
url = "http://127.0.0.1:5000"

# # test request
token = "45yhrdue586rfhe5r87w4srj568ew45sjh568e4uj5e6rtjhyt4535jrtdsedgv"
headers = {"token": token}
params = {
        "signed_txns": [
            {"owner_address": address, "tx_bytes": tx},
            {"owner_address": address, "tx_bytes": tx},
        ]
    }

# send request
response = requests.post(url, params=params)
print(f"{response.json()}\n")

```

# Curl Example

Curl requests can be displayed by running `python3 test_api.py`

To add specific headers update `headers = None` in `test_api.py` to a dictionary of headers.

Look for the following in the logs output or check the `api_tests.log`

```
[INFO]: cURL Request:

To convert CURL requests to example code for languages other than python - use https://curlconverter.com/

```curl

```

# Test Program

Start the service locally or remotely

`python3 main.py`

Set the url in `tests/test_api.py` 

i.e. `url = "http://127.0.0.1:5000"`

Run the tests

`pytest`

``` bash

>>> pytest

```

# Example responses:

> Happy Flow

```json
[
  {
    "item": 0,
    "status": "success",
    "message": "success",
    "new_tx_bytes": "new_tx_bytes",
    "signed_txn": "signed_txn",
    "pub_key": "pub_key",
    "owner_address": "0x2c53ba8163f740bb278194ac799f79275fe8dc6a",
    "tx_bytes_sent": "YunLZjSe5u3S9C2/6m1JsUjd0zaXZvx MyNieP61lQ0="
  },
  {
    "item": 1,
    "status": "success",
    "message": "success",
    "new_tx_bytes": "new_tx_bytes",
    "signed_txn": "signed_txn",
    "pub_key": "pub_key",
    "owner_address": "0x2c53ba8163f740bb278194ac799f79275fe8dc6a",
    "tx_bytes_sent": "YunLZjSe5u3S9C2/6m1JsUjd0zaXZvx MyNieP61lQ0="
  }
]


```

> Errors

``` json

 

```



