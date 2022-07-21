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
url = "http://127.0.0.1:9000"

#
# build params using "addresses" key
params = {
    
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


```

> Errors

``` json

 

```



