#!/usr/bin/env python3
"""Post a tweet to X via OAuth 1.0a User Context.

Usage:
    python post.py "<tweet text, <=280 chars>"
    echo "tweet text" | python post.py -

Reads credentials from environment or a .env file in this skill directory
or the current working directory.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

TWEET_ENDPOINT = "https://api.x.com/2/tweets"
MAX_LEN = 280
REQUIRED_ENV = ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET")


def load_env() -> None:
    for candidate in (Path(__file__).resolve().parent / ".env", Path.cwd() / ".env"):
        if candidate.is_file():
            load_dotenv(candidate, override=False)


def read_text(argv: list[str]) -> str:
    if len(argv) < 2:
        sys.exit("usage: post.py \"<text>\"  |  echo text | post.py -")
    raw = sys.stdin.read() if argv[1] == "-" else argv[1]
    text = raw.strip()
    if not text:
        sys.exit("error: empty tweet text")
    if len(text) > MAX_LEN:
        sys.exit(f"error: tweet exceeds {MAX_LEN} chars ({len(text)})")
    return text


def post(text: str) -> dict:
    missing = [k for k in REQUIRED_ENV if not os.environ.get(k)]
    if missing:
        sys.exit(f"error: missing env vars: {', '.join(missing)}")

    session = OAuth1Session(
        client_key=os.environ["X_API_KEY"],
        client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],
        resource_owner_secret=os.environ["X_ACCESS_SECRET"],
    )
    resp = session.post(TWEET_ENDPOINT, json={"text": text}, timeout=30)
    if resp.status_code != 201:
        sys.exit(f"error: HTTP {resp.status_code} {resp.text}")
    return resp.json()["data"]


def main() -> None:
    load_env()
    text = read_text(sys.argv)
    data = post(text)
    tweet_id = data["id"]
    print(f"id: {tweet_id}")
    print(f"url: https://x.com/i/web/status/{tweet_id}")
    print(f"text: {data['text']}")


if __name__ == "__main__":
    main()
