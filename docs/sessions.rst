Sessions
========

Initial setup
-------------

Tradestation uses OAuth for secure authentication to the API. In order to obtain access tokens, you need to authenticate with OAuth 2's authorization code flow, which requires a local HTTP server running to handle the callback. Fortunately, the SDK makes doing this easy:

.. code-block:: python

   from tradestation.oauth import login
   login()

This will let you authenticate in your local browser. Fortunately, this only needs to be done once, as afterwards you can use the refresh token to obtain new access tokens indefinitely.

Creating a session
------------------

A session object is required to authenticate your requests to the Tradestation API.
Create it by passing in the API key (client ID), secret key (client secret), and refresh token obtained in the initial setup.

.. code-block:: python

   from tradestation import Session
   session = Session('api_key', 'secret_key', 'refresh_token')

A simulated session can be used to test strategies or applications before using them in production:

.. code-block:: python

   from tradestation import Session
   session = Session('api_key', 'secret_key', 'refresh_token', is_test=True)

You can also use the legacy v2 API endpoints if desired:

.. code-block:: python

   from tradestation import Session
   session = Session('api_key', 'secret_key', 'refresh_token', use_v2=True)

Auto-refresh sessions
---------------------

Since TradeStation access tokens only last 20 minutes by default, it can be annoying to have to remember to refresh them constantly.
Fortunately, the SDK has a special class, `AutoRefreshSession`, that handles token refreshal (ok, ok, I know it's not a word!) for you!

.. code-block:: python

   from tradestation import AutoRefreshSession
   session = await AutoRefreshSession('api_key', 'secret_key', 'refresh_token', is_test=True)
   # ...
   await session.close()  # don't forget to cleanup the session when you're done!

You can also create auto-refresh sessions using async context managers:

.. code-block:: python

   async with AutoRefreshSession('api_key', 'secret_key', 'refresh_token') as session:
       # ...

In this case, the context manager will handle the cleanup for you.
Pretty easy, no? Other than initialization and cleanup, you can use auto-refresh sessions just like normal sessions.
