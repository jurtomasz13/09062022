"""Module that connects commands to their coresponding methods from client.py"""

import argparse
import json

from client import Client

parser = argparse.ArgumentParser()

parser.add_argument("command")
parser.add_argument("--player-name", type=str)
parser.add_argument("--profession", type=str)
parser.add_argument("--enemy-name", type=str)

args = parser.parse_args()

command = args.command

client = Client(
    player_name=args.player_name, enemy_name=args.enemy_name, profession=args.profession
)


def pretty_json(json_data):
    """Returns prettiefied JSON representation of the given data"""
    return json.dumps(json_data, indent=2, sort_keys=True)


methods = [
    method
    for method in dir(client)
    if callable(getattr(client, method)) and not method.startswith("__")
]

options = {method: getattr(client, method) for method in methods}

if command in options.keys():
    result = options[command]()
    print(pretty_json(result))
else:
    print("Wrong command")
