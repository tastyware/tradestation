sync/async
==========

After creating a session (which is always initialized synchronously), the rest of the API endpoints implemented in the SDK have both sync and async implementations.

Let's see how this looks:

.. code-block:: python

    from tradestation import Account, Session
    session = Session('api_key', 'secret_key', 'refresh_token')
    accounts = Account.get_accounts(session)

The async implementation is similar:

.. code-block:: python

    session = Session('api_key', 'secret_key', 'refresh_token')
    # using async implementation
    accounts = await Account.a_get_accounts(session)

That's it! All sync methods have a parallel async method that starts with `a_`.
