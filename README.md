# thingy-api-purple

## Setup

```bash
# Setup virtualenv
pip install -r requirements

python run_server.py
```
## Authorization

The JWT is issued from [auth0](https://www.auth0.com "auth0")
which allows login with a **Github** or **Google** account.

The endpoints are protected using [aiohttp-jwt](https://github.com/hzlmn/aiohttp-jwt/ "aiohttp-jwt") as
middleware.


### Start NodeRed
```
dokcer-compose up -d
```



 

