import json
import logging
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, "..", "pins.json"), "r") as f:
    pins = json.loads(f.read())

with open(os.path.join(BASE_DIR, "..", "config.json"), "r") as f:
    config = json.loads(f.read())

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
