# Based on https://community.tradestation.com/Discussions/Topic.aspx?Topic_ID=205209
# This file is designed to provide a simple way to obtain a refresh
# token and an initial access token using v3 of the Web API.

import re
from typing import Any
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

import httpx
from pydantic import BaseModel

from tradestation import OAUTH_SCOPES, OAUTH_URL

AUDIENCE = "https://api.tradestation.com"
PORT = 3001
REDIRECT_URI = f"http://localhost:{PORT}"
SCOPES = " ".join(OAUTH_SCOPES)


class Credentials(BaseModel):
    key: str = ""
    secret: str = ""
    scopes: str = SCOPES

    def clear(self) -> None:
        self.key = ""
        self.secret = ""
        self.scopes = SCOPES


credentials = Credentials()


def get_access_url(credentials: Credentials) -> str:
    query_string = "&".join(
        [
            "response_type=code",
            f"audience={AUDIENCE}",
            f"redirect_uri={REDIRECT_URI}",
            f"client_id={credentials.key}",
            f"scope={credentials.scopes}",
        ]
    )
    access_url = f"{OAUTH_URL}/authorize?{query_string}"
    return access_url


def convert_auth_code(credentials: Credentials, auth_code: str) -> dict[str, Any]:
    """
    Uses an api key, a secret key and authorization code to obtain a response
    containing an access token, refresh token, user id, and expriation time
    """
    post_data = {
        "grant_type": "authorization_code",
        "client_id": credentials.key,
        "client_secret": credentials.secret,
        "redirect_uri": REDIRECT_URI,
        "code": auth_code,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = httpx.post(f"{OAUTH_URL}/oauth/token", headers=headers, data=post_data)
    if response.status_code != 200:
        raise Exception(
            "Could not load access and refresh tokens from authorization code!"
        )

    return response.json()


root_page: bytes = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Web API</title>
    <style>
        :root {{
            font-family: sans-serif;
        }}

        #main-div {{
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
        }}

        #content-wrapper {{
            display: flex;
            height: 100%;
            flex-direction: column;
            align-items: center;
        }}

        #content {{
            padding-top: 4em;
            margin-bottom: 4rem;
            text-align: center;
        }}

        #title-text {{
            font-size: 7rem;
            font-family: Verdana;
            border-top: 1px solid black;
            border-bottom: 1px solid black;
        }}

        .api-form {{
            padding-top: 1em;
        }}

        .input-row {{
            display: flex;
            align-items: center;
            padding-bottom: 0.4rem;
            gap: 10px;
        }}

        .label-wrapper {{
            width: 150px;
            font-weight: bold;
            text-align: right;
        }}

        .input-wrapper {{
            width: 100%;
        }}

        input[type='text'] {{
            width: 100%;
            padding: 5px;
            box-sizing: border-box;
        }}

        .submit-wrapper {{
            text-align: right;
        }}

        #submit-button {{
            margin-top: 1em;
            color: white;
            background-color: #007bff;
            padding-top: 4px;
            paddig-bototm: 4px;
        }}

        #url-wrapper {{
            position: fixed;
            bottom: 0px;
            left: 0px;
        }}

        #url {{
            color: darkgray;
            text-align: left;
            word-wrap: break-word;
            word-break: break-all;
            white-space: pre-wrap;
            padding: 10px;
        }}

		.fade-in {{
			animation: fadein 2.5s;
		}}

		@keyframes fadein {{
			0% {{
				opacity: 0;
			}}
			100% {{
				opacity: 1;
			}}
		}}
    </style>
</head>
<body>
    <div id="main-div" class="fade-in">
        <div id="content-wrapper">
            <div id='content'>
                <div id="title-text">WEB API V3</div>
                <form class='api-form' action="/submit">
                    <div class='input-row'>
                        <div class='label-wrapper'>
                            <label class='input-label'>API Key:
                        </div>
                        <div class='input-wrapper'>
                            <input placeholder='API Key' type="text" name="apiKey">
                        </div>
                    </div>
                    <div class='input-row'>
                        <div class='label-wrapper'>
                            <label class='input-label'>Secret Key: 
                        </div>
                        <div class='input-wrapper'>
                            <input placeholder='Secret Key' type="text" name="apiSecret">
                        </div>
                    </div>
                    <div class='input-row'>
                        <div class='label-wrapper'>
                            <label class='input-label'>Scopes: 
                        </div>
                        <div class='input-wrapper'>
                            <input placeholder='Scopes' type="text" name="scopes" value="{SCOPES}">
                        </div>
                    </div>
                    <div class='submit-wrapper'>
                        <input type="submit" id='submit-button' value="Submit">
                    </div>
                </form>
                <div id='url-wrapper'>
                    <pre id='url'> </pre>
                <div>
            </div>
        </div>
    </div>
    <script>
        const form = document.querySelector('form');
        const url = document.getElementById('url');
        const buildUrl = () => {{
            const data = new FormData(form);
            const key = data.get('apiKey');
            const scopes = encodeURIComponent(data.get('scopes'));
            loginUrl = `{OAUTH_URL}/authorize?response_type=code&audience={AUDIENCE}&client_id=${{key}}&redirect_uri={REDIRECT_URI}&scope=${{scopes}}`;
            url.innerText = loginUrl;
        }}
        form.addEventListener('input', buildUrl);
    </script>
</body>
</html>
""".encode("utf-8")

bad_request_page: bytes = (
    "<!DOCTYPE html><html><body><pre>400 - Bad page request.</pre></html>".encode(
        "utf-8"
    )
)

unknown_page: bytes = (
    "<!DOCTYPE html><html><body><pre>404 - Page not found.</pre></html>".encode("utf-8")
)


def response_page(
    refresh_token: str, access_token: str, response: dict[str, Any]
) -> bytes:
    return f"""<!DOCTYPE html>
<html>
<head>
<style>
    :root {{
        font-family: sans-serif;
    }}
    body {{
        font-size: 1.1rem;
        padding: 2em;
    }}
    pre {{
        white-space: pre-wrap;
        border: 1px solid black;
        padding: 2em;
        word-wrap: break-word;
    }}
    #refresh-token-label {{
        font-weight: bold;
        margin-top: 1em;
    }}
</style>
</head>
<body>
<div id='refresh-token-label'>Refresh Token:</div>
<pre>{refresh_token}</pre>
<b>Access Token:</b> 
<pre>{access_token}</pre>
<b>Complete Response:</b> 
<pre id='complete-response'>{response}</pre>
</body>
<script>
    // Format complete response
    const completeResponseEl = document.getElementById('complete-response');
    const responseText = completeResponseEl.innerText;
    completeResponseEl.innerText = JSON.stringify(JSON.parse(responseText.trim().replace(/'/g,'"')), null, 4);
</script>
</html>""".encode("utf-8")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # pragma: no cover
        # Serve root page with sign in link
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(root_page)

            return

        if self.path.startswith("/submit"):
            # Parse query components from url
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&"))

            credentials.key = query_components["apiKey"]
            credentials.secret = query_components["apiSecret"]
            credentials.scopes = query_components["scopes"].replace("+", "%20")

            # Redirect to login page using API key submitted by user
            self.send_response(302)
            self.send_header("Location", get_access_url(credentials))
            self.end_headers()

            return

        if self.path.startswith("/?code"):
            # Check if query path contains case insensitive "code="
            code_match = re.search(r"code=(.+)", self.path, re.I)

            if code_match and credentials.key and credentials.secret:
                user_auth_code = code_match[1]
                token_access = convert_auth_code(credentials, user_auth_code)

                # Clear stored info
                credentials.clear()

                access_token = token_access["access_token"]
                refresh_token = token_access["refresh_token"]

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                token_page = response_page(refresh_token, access_token, token_access)
                self.wfile.write(token_page)
                return

            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(bad_request_page)

                return

        # Send 404 error if path is none of the above
        self.send_response(404)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(unknown_page)


def login() -> None:
    """
    Starts a local HTTP server and opens the browser to OAuth login.
    """
    httpd = HTTPServer(("", PORT), RequestHandler)
    print(f"Opening url: {REDIRECT_URI}")
    webbrowser.open(REDIRECT_URI)
    httpd.serve_forever()


if __name__ == "__main__":
    login()
