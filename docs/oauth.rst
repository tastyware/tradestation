oauth
=====

Unless you're creating a web app with an option for a TradeStation login, you can probably skip this section!

As mentioned previously, the utility function :func:`tradestation.oauth.login` handles creating a local HTTP server to handle the OAuth login callback. But what if you want to do this yourself?

Here's a simple example of how you could do this on your own server, using `FastAPI` and `authlib`:

.. code-block:: python

    from authlib.integrations.starlette_client import OAuth
    from fastapi import FastAPI, Request
    from starlette.middleware.sessions import SessionMiddleware
    from tradestation.oauth import AUDIENCE, REDIRECT_URI, SCOPES

    SESSION_ENCRYPTION_KEY = "some-random-string"

    oauth = OAuth()
    oauth.register(
        name="tradestation",
        server_metadata_url="https://signin.tradestation.com/.well-known/openid-configuration",
        client_id="api_key",
        client_secret="secret_key",
        access_token_params={"grant_type": "authorization_code"},
        authorize_params={"audience": AUDIENCE},
        authorize_state=SESSION_ENCRYPTION_KEY,
        client_kwargs={
            "response_type": "code",
            "scope": SCOPES,
        },
    )


    app = FastAPI(name="TradeStation SDK Login")
    app.add_middleware(SessionMiddleware, secret_key=SESSION_ENCRYPTION_KEY)


    @app.get("/login")
    async def login_tradestation(request: Request):
        # in production, you'd use `request.url_for("auth_tradestation")`
        return await oauth.tradestation.authorize_redirect(request, REDIRECT_URI)


    @app.get("/")
    async def auth_tradestation(request: Request):
        return await oauth.tradestation.authorize_access_token(request)


    if __name__ == "__main__":
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=3001)

.. note:
   If you run into a CSRF error, it probably has to do with your session state! Try clearing your browser cookies or testing in an incognito window.

That should be enough to get you started!
