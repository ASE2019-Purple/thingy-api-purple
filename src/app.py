import logging
import aiohttp
import aiohttp_cors
from aiohttp_swagger import setup_swagger

from aiohttp_jwt import JWTMiddleware, check_permissions, match_any, login_required

from aiohttp.web import json_response, Application

import os

env = os.getenv("ENVIRONMENT", "DEBUG")
IP = os.getenv("IP", "0.0.0.0")
# IP = getenv("IP", "localhost")
PORT = os.getenv("PORT", "8000")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if env == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)


# Auth0 Configuration
secret = "JjQVkqJJXmxpH1UvmvElStfLi1NJv55h"
audience = "thingy_api_purple"
issuer = "https://thingy-api-purple.eu.auth0.com/"
algorithms = "RS256"


# Use the following to retrieve from auth0 certificate
# openssl x509 -pubkey -noout -in cert.pem  > pubkey.pem

# The key should not be used like that,
# instead use the certificate at
# https://thingy-api-purple.eu.auth0.com/.well-known/jwks.json
# but extracting the secret did not work so far.
publickey = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsfXjR+4G02CFbGfGN6GA
4NCNMVETZo+JJkvac1pueXA4cx5CooCGZ2KkX8VC66yVHbc/EpMns71vf6InPxV6
qYhgsvtGlW71mnhdR0w3ZPD4Ki56MS1ENptZbGdbDw/XZITfOctlHH8thgJsUDcV
sgeYYkhhgqzTdzv40ZJCKG062446bRqxlturar47PyCDyq483avQI+xS6SHyuBBE
0pXPinxHlVo0yxaHynNRXckw7lqvvIonIGeen4iomtJBcji5ZCTDy4QDIC5d8PcM
Y3Dwv/Lyw6zsU/DGCBVBITHyOlRNNyroQ9YN7EgIrQeuQTG6fFJ9HCC2/s30I5Hh
zQIDAQAB
-----END PUBLIC KEY-----
"""


async def init(loop):
    """Cheap and dirty protected API example"""

    app = Application(
        middlewares=[
            JWTMiddleware(
                secret_or_pub_key=publickey,
                algorithms=algorithms,
                auth_scheme="Bearer",
                request_property="user",
                credentials_required=False,
                whitelist=[r"/(public|bar)"],
                audience=audience,
                issuer=issuer,
            )
        ]
    )

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            ),
            "http://localhost": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            ),
            "http://127.0.0.0": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            ),
        },
    )

    ############
    # API Views
    ############
    # TODO move to views

    async def public_handler(request):
        return json_response({"Access": "Public"})

    @login_required
    async def protected_handler(request):
        return json_response({"Access": "Protected"})

    @check_permissions(["openid"], comparison=match_any, permissions_property="scope")
    async def profile_handler(request):
        """
        This handler retrieves the user data from the 
        auth0 userinfo endpoint.

        The scope openid is required for this.

        See: https://auth0.com/docs/api/authentication#get-user-info
        """

        # pdb.set_trace()
        payload = request.get("user", {})
        session = aiohttp.ClientSession()

        userinfo = {}
        async with session.get(
            issuer + "userinfo",
            headers={"Authorization": request.headers["Authorization"]},
        ) as r:
            userinfo = await r.json()

        return json_response(
            {"name": userinfo.get("name"), "email": userinfo.get("email")}
        )

    cors.add(app.router.add_get("/", public_handler))
    cors.add(app.router.add_get("/public", public_handler))
    cors.add(app.router.add_get("/protected", protected_handler))
    cors.add(app.router.add_get("/profile", profile_handler))

    # Config
    setup_swagger(app, swagger_url="/api/v1/doc", swagger_from_file="swagger.yaml")
    logger.info("Starting server at %s:%s", IP, PORT)

    srv = await loop.create_server(app.make_handler(), IP, PORT)
    return srv
