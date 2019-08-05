#!/usr/bin/env python3

import requests
import json
import argparse
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument('--node', type=str, default='[::1]:55000')
parser.add_argument('--reps', type=str, help='File with list of representatives in JSON format', required=False)
args = parser.parse_args()

node_uri = f"http://{args.node}"

def node(data):
    return requests.post(node_uri, json=data).json()

def prettyjson(data, sorted=True):
    return json.dumps(data, indent=4, sort_keys=sorted)

if args.reps:
    with open(args.reps, 'r') as f:
        representatives_list = json.load(f)
    representatives = {r['address']: r['alias'] for r in representatives_list}
else:
    print("No --reps file given")

while representatives:
    try:
        os.system('clear')
        print("\n====CLI NODE MONITOR=====\n")

        # Print info about confirmation quorum
        peers = node({"action": "peers"})['peers']
        print(f"Peers: {len(peers)}\n")
        quorum = node({"action": "confirmation_quorum"})
        print(f"Quorum information:\n{prettyjson(quorum)}")

        # Print info about representatives online/offline and their weight
        print("\nRepresentatives:\n")
        online_weights = node({"action":"representatives_online", "weight":"true"})['representatives']
        if online_weights:
            offline = []
            print("Online:")
            for address, alias in representatives.items():
                rep = online_weights.get(address, '')
                if rep:
                    alias_padded = alias + " "*(20-len(alias))
                    print(f"\t{alias_padded} \t {int(int(rep['weight'])/1e30)} BNANO")
                else:
                    offline.append(alias)
            print("Offline:")
            for alias in offline:
                print(f"\t{alias}")
        else:
            print("Offline:")
            for address, alias in representatives.items():
                print(f"\t{alias}")

        time.sleep(5)
    except KeyboardInterrupt:
        break