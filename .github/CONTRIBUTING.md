# Contributions

In order to run the test suite locally, you'll need to follow these steps to be able to authenticate to Tradestation.

## Steps to follow to contribute

1. Fork the repository to your personal Github account and make your proposed changes.
2. Export your API key, secret key, refresh token, and account number to the following Github Actions repository secrets: `TS_API_KEY`, `TS_SECRET_KEY`, `TS_REFRESH`, and `TS_ACCOUNT`. The account should be a simulation account.
3. Run `make install` to create the virtual environment, `make lint` to format your code, and `make test` to run the tests locally.
