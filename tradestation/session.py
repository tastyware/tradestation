import asyncio
import json
from random import randrange
from typing import Any

import httpx
import jwt
from httpx import AsyncClient, Client
from typing_extensions import Self

from tradestation import API_URL_SIM, API_URL_V2, API_URL_V3, OAUTH_URL, logger
from tradestation.utils import TradestationError, validate_and_parse, validate_response


class Session:
    """
    Contains a local user login which can then be used to interact with the
    remote API.

    :param api_key: Tradestation API key (client ID)
    :param secret_key: Tradestation secret key (client secret)
    :param refresh_token:
        Tradestation refresh token used to obtain new access tokens; can be
        acquired initially by calling :func:`tradestation.oauth.login`
    :param access_token:
        previously generated access token; if absent, refresh token will be
        used to generate a new one automatically
    :param id_token:
        previously generated ID token; if absent, you won't be able to access
        the `user_info` property until refreshing
    :param is_test: whether to use the simulated API endpoints, default False
    :param use_v2: whether to use the older v2 endpoints instead of the v3 ones
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        refresh_token: str,
        access_token: str | None = None,
        id_token: str | None = None,
        token_lifetime: int = 1200,
        is_test: bool = False,
        use_v2: bool = False,
    ):
        if is_test and use_v2:
            raise TradestationError(
                "The simulation environment doesn't support v2 URLs!"
            )
        if is_test:
            self.base_url = API_URL_SIM
        elif use_v2:
            self.base_url = API_URL_V2
        else:
            self.base_url = API_URL_V3

        #: Tradestation client ID
        self.api_key = api_key
        #: Tradestation client secret
        self.secret_key = secret_key
        #: Access token for authenticating requests. By default, is valid for
        #: 20 minutes, and then needs to be replaced.
        self.access_token = access_token
        #: Refresh token for generating new access tokens
        self.refresh_token = refresh_token
        #: ID token containing personal info like name, email
        self.id_token = id_token
        #: Lifetime, in seconds, of access tokens before they expire
        #: Defaults to 20 minutes
        self.token_lifetime = token_lifetime

        #: Whether this is a simulated or real session
        self.is_test = is_test
        # The headers to use for API requests
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        #: httpx client for sync requests
        self.sync_client = Client(base_url=self.base_url, headers=headers)
        #: httpx client for async requests
        self.async_client = AsyncClient(base_url=self.base_url, headers=headers)

        if not access_token:
            self.refresh()

    async def _a_get(self, url, **kwargs) -> Any:
        response = await self.async_client.get(url, **kwargs)
        return validate_and_parse(response)

    def _get(self, url, **kwargs) -> Any:
        response = self.sync_client.get(url, **kwargs)
        return validate_and_parse(response)

    async def a_refresh(self) -> None:
        """
        Refreshes the acccess token using the stored refresh token.
        """
        async with AsyncClient() as client:
            response = await client.post(
                f"{OAUTH_URL}/oauth/token",
                data={
                    "grant_type": "refresh_token",
                    "client_id": self.api_key,
                    "client_secret": self.secret_key,
                    "refresh_token": self.refresh_token,
                },
            )
            data: dict[str, str] = validate_and_parse(response)
            # update the relevant tokens
            self.access_token = data["access_token"]
            self.id_token = data["id_token"]
            self.token_lifetime = int(data.get("expires_in", 1200))
            logger.debug(f"Refreshed token, expires in {self.token_lifetime} seconds.")
            auth_headers = {"Authorization": f"Bearer {self.access_token}"}
            # update the httpx clients with the new token
            self.sync_client.headers.update(auth_headers)
            self.async_client.headers.update(auth_headers)

    def refresh(self) -> None:
        """
        Refreshes the acccess token using the stored refresh token.
        """
        response = httpx.post(
            f"{OAUTH_URL}/oauth/token",
            data={
                "grant_type": "refresh_token",
                "client_id": self.api_key,
                "client_secret": self.secret_key,
                "refresh_token": self.refresh_token,
            },
        )
        data: dict[str, str] = validate_and_parse(response)
        # update the relevant tokens
        self.access_token = data["access_token"]
        self.id_token = data["id_token"]
        self.token_lifetime = int(data.get("expires_in", 1200))
        logger.debug(f"Refreshed token, expires in {self.token_lifetime} seconds.")
        auth_headers = {"Authorization": f"Bearer {self.access_token}"}
        # update the httpx clients with the new token
        self.sync_client.headers.update(auth_headers)
        self.async_client.headers.update(auth_headers)

    async def a_revoke(self) -> None:  # pragma: no cover
        """
        Revokes all valid refresh tokens.
        """
        async with AsyncClient() as client:
            response = await client.post(
                f"{OAUTH_URL}/oauth/revoke",
                data={
                    "client_id": self.api_key,
                    "client_secret": self.secret_key,
                    "token": self.refresh_token,
                },
            )
            validate_response(response)
            logger.debug("Successfully revoked refresh tokens!")

    def revoke(self) -> None:  # pragma: no cover
        """
        Revokes all valid refresh tokens.
        """
        response = httpx.post(
            f"{OAUTH_URL}/oauth/revoke",
            data={
                "client_id": self.api_key,
                "client_secret": self.secret_key,
                "token": self.refresh_token,
            },
        )
        validate_response(response)
        logger.debug("Successfully revoked refresh tokens!")

    def serialize(self) -> str:
        """
        Serializes the session to a string, useful for storing
        a session for later use.
        Could be used with pickle, Redis, etc.
        """
        attrs = self.__dict__.copy()
        del attrs["async_client"]
        del attrs["sync_client"]
        return json.dumps(attrs)

    @classmethod
    def deserialize(cls, serialized: str) -> Self:
        """
        Create a new Session object from a serialized string.
        """
        deserialized = json.loads(serialized)
        self = cls.__new__(cls)
        self.__dict__ = deserialized
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        self.sync_client = Client(base_url=self.base_url, headers=headers)
        self.async_client = AsyncClient(base_url=self.base_url, headers=headers)
        return self

    @property
    def user_info(self) -> dict[str, str]:
        """
        Contains user info depending on the OAuth scopes provided (eg email, name)
        If you call this on a session where you didn't provide an `id_token` and you
        haven't refreshed yet, this will return an empty dict.
        """
        if self.id_token is None:
            return {}
        return jwt.decode(self.id_token, options={"verify_signature": False})


class AutoRefreshSession(Session):
    """
    A special session that automatically refreshes the access token before
    expiration. It should always be initialized as an async context manager,
    or by awaiting it, since the object cannot be fully instantiated without
    async.

    Example usage::

        from tradestation import AutoRefreshSession

        async with AutoRefreshSession(api_key, secret_key, refresh_token) as session:
            # ...

    Or::

        session = await AutoRefreshSession(api_key, secret_key, refresh_token)
        # ...
        await session.close()

    """

    async def __aenter__(self):
        self._auto_refresh_task = asyncio.create_task(self._auto_refresh())
        return self

    def __await__(self):
        return self.__aenter__().__await__()

    async def __aexit__(self, *exc):
        await self.close()

    async def close(self) -> None:
        """
        Closes the auto-refresh task.
        """
        self._auto_refresh_task.cancel()
        await self._auto_refresh_task

    async def _auto_refresh(self) -> None:
        # infinite loop
        while True:
            try:
                # renewal happens between 30 and 60 seconds before token expiration;
                # this helps reduce the likelihood of many refreshes simultaneously
                delay = max(1, self.token_lifetime - randrange(30, 60))
                await asyncio.sleep(delay)
                await self.a_refresh()
            except asyncio.CancelledError:
                logger.debug("Auto-refresh task cancelled, exiting gracefully.")
                return
