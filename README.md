[![Docs](https://readthedocs.org/projects/tradestation/badge/?version=latest)](https://tradestation.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/tradestation)](https://pypi.org/project/tradestation)
[![Downloads](https://static.pepy.tech/badge/tradestation)](https://pepy.tech/project/tradestation)
[![Release)](https://img.shields.io/github/v/release/tastyware/tradestation?label=release%20notes)](https://github.com/tastyware/tradestation/releases)

# tradestation
A simple, unofficial, sync/async SDK for Tradestation built on their public API. This will allow you to create trading algorithms for whatever strategies you may have quickly and painlessly in Python.

## Features

- Up to 10x less code than using the API directly
- Sync/async functions for all endpoints
- Powerful websocket implementation for account alerts and data streaming, with support for auto-reconnection and reconnection callbacks
- 100% typed, with Pydantic models for all JSON responses from the API
- 95%+ unit test coverage
- Comprehensive documentation
- Utility functions for timezone calculations, futures monthly expiration dates, and more

## Installation

```console
$ pip install tradestation
```

## Initial setup

Tradestation uses OAuth for secure authentication to the API. In order to obtain access tokens, you need to authenticate with OAuth 2's authorization code flow, which requires a local HTTP server running to handle the callback. Fortunately, the SDK makes doing this easy:

```python
from tradestation.oauth import login
login()
```

This will let you authenticate in your local browser. Fortunately, this only needs to be done once, as afterwards you can use the refresh token to obtain new access tokens indefinitely.

## Creating a session

A session object is required to authenticate your requests to the Tradestation API.
You can create a simulation session by passing `is_test=True`.

```python
from tradestation import Session
session = Session('api_key', 'secret_key', 'refresh_token')
```
