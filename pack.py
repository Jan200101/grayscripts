#!/usr/bin/env python3

import os
import base64
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--unpack', action='store_true') 
parser.add_argument('-p', '--pack', action='store_true') 
parser.add_argument('file', type=argparse.FileType("r"))

args = parser.parse_args()

if args.pack == args.unpack:
    print("Either -p or -u must be specified")
    exit(0)

def confirm(msg):
    while True:
        d = input(msg)
        m = {
            "y": True,
            "yes": True,
            "n": False,
            "no": False,
        }.get(d.lower())

        if m is not None:
            return m

if args.unpack:
    e = [x.split("!") for x in args.file.read().split("\n") if x]

    for z in e:
        p, d = z

        os.makedirs(os.path.dirname(p), exist_ok=True)
        if os.path.isfile(p) and not confirm(f"[!] {p} already exists, replace? [y/n]"):
            print(f"[!] Skipping {p}")
            continue

        with open(p, "wb") as fd:
            print(f"[*] Unpacking {p}")
            fd.write(base64.b64decode(d))
