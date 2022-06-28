from client import Client

import argparse


parser = argparse.ArgumentParser()

parser.add_argument('command')
parser.add_argument('--player-name', type=str)
parser.add_argument('--profession', type=str)
parser.add_argument('--enemy-name', type=str)

args = parser.parse_args()

command = args.command

client = Client(player_name=args.player_name,
                enemy_name=args.enemy_name, profession=args.profession)

if command == 'get_players':
    print(client.get_players())
elif command == 'get_player':
    print(client.get_player())
elif command == 'create_player':
    print(client.create_player())
elif command == 'get_token':
    print(client.get_token())
elif command == 'login':
    print(client.login())
elif command == 'logout':
    print(client.logout())
elif command == 'attack':
    print(client.attack())
