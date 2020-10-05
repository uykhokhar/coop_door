import json
import os
import urllib

from http import client


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, "..", "pins.json"), "r") as f:
    pins = json.loads(f.read())

with open(os.path.join(BASE_DIR, "..", "config.json"), "r") as f:
    config = json.loads(f.read())

with open(os.path.join(BASE_DIR, "..", "creds.json"), "r") as f:
    creds = json.loads(f.read())


def notification(message, priority=-1):
    """priority:
        -2 to generate no notification/alert,
        -1 to always send as a quiet notification,
         1 to display as high-priority and bypass the user's quiet hours,
         2 to also require confirmation from the user"""
    conn = client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": creds['token'],
                     "user": creds['user'],
                     "message": message,
                     "priority": priority
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    return conn.getresponse()
