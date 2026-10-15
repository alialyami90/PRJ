#!/usr/bin/env python3
"""Checks the App Store Connect API key before xcodebuild tries it, and says what is wrong in plain words.

xcodebuild only reports "Cannot verify client's JWT headers" for every kind of bad key. This asks the App Store
Connect API directly, first as a Team key (key id + issuer id), then as an Individual key (no issuer), and
looks the app up by its bundle id. Reads KEY_ID, ISSUER_ID, KEY_PATH and BUNDLE_ID from the environment and
never prints them. Needs PyJWT and cryptography.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

import jwt

KEY_ID = os.environ["KEY_ID"]
ISSUER_ID = os.environ["ISSUER_ID"]
BUNDLE_ID = os.environ["BUNDLE_ID"]
with open(os.environ["KEY_PATH"]) as f:
    PRIVATE_KEY = f.read()

API = "https://api.appstoreconnect.apple.com/v1"
URL = f"{API}/apps?filter[bundleId]={BUNDLE_ID}&fields[apps]=bundleId"


def token(team_key):
    now = int(time.time())
    claims = {"aud": "appstoreconnect-v1", "iat": now, "exp": now + 600}
    if team_key:
        claims["iss"] = ISSUER_ID
    else:
        claims["sub"] = "user"
    return jwt.encode(claims, PRIVATE_KEY, algorithm="ES256", headers={"kid": KEY_ID, "typ": "JWT"})


def get(team_key, url=URL):
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token(team_key)}"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, None


def fail(message):
    print(f"::error::{message}")
    sys.exit(1)


try:
    jwt.encode({"aud": "check"}, PRIVATE_KEY, algorithm="ES256")
except Exception:
    fail("APP_STORE_CONNECT_KEY is not a readable .p8 private key. Paste the whole file again.")

status, body = get(team_key=True)
if status == 200:
    if not body["data"]:
        _, registered = get(True, f"{API}/bundleIds?filter[identifier]={BUNDLE_ID}&fields[bundleIds]=identifier")
        _, apps = get(True, f"{API}/apps?fields[apps]=bundleId&limit=200")
        others = sorted(a["attributes"]["bundleId"] for a in (apps or {}).get("data", []))
        print(f"Bundle ID {BUNDLE_ID} registered on developer.apple.com: {'yes' if registered and registered['data'] else 'no'}")
        print(f"Apps this key can see in App Store Connect: {', '.join(others) or 'none'}")
        fail(f"The key works, but App Store Connect has no app with bundle ID {BUNDLE_ID}. "
             "Create the app record (Apps > + > New App) with that bundle ID.")
    print(f"App Store Connect accepted the Team key and found the app {BUNDLE_ID}.")
    sys.exit(0)
if status == 403:
    fail("App Store Connect accepted the key but it lacks permission. Give the Team key the Admin role, "
         "and accept any pending agreement under Business.")

individual_status, _ = get(team_key=False)
if individual_status in (200, 403):
    fail("This is an Individual key. xcodebuild needs a Team key: in App Store Connect go to Users and Access > "
         "Integrations > App Store Connect API > Team Keys, create one with Admin access, and update "
         "APP_STORE_CONNECT_KEY_ID and APP_STORE_CONNECT_KEY to the new key's ID and .p8 file.")
fail(f"App Store Connect rejected the key (HTTP {status}). The Key ID, the Issuer ID and the .p8 file must all "
     "belong to the same active Team key: check that APP_STORE_CONNECT_KEY_ID is the ID in the row of the key "
     "whose .p8 you pasted, that the key isn't revoked, and that APP_STORE_CONNECT_ISSUER_ID is the one shown above "
     "the Team Keys list.")
