#!/usr/bin/env python3

import os
import base64
import argparse
import pathlib
import sys

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-u', '--unpack', action='store_true',)
group.add_argument('-p', '--pack', action='store_true')
parser.add_argument('-f', '--force', action='store_true')
parser.add_argument('path', type=pathlib.Path)

args = parser.parse_args()

def confirm(msg):
    if args.force:
        return True

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

def unpack(path):
    with open(path, "r") as file:
        e = [x.split("!") for x in file.read().split("\n") if x]

        for z in e:
            p, d = z

            os.makedirs(os.path.dirname(p), exist_ok=True)
            if os.path.isfile(p) and not confirm(f"[!] {p} already exists, replace? [y/n]"):
                print(f"[!] Skipping {p}")
                continue

            with open(p, "wb") as fd:
                print(f"[*] Unpacking {p}")
                fd.write(base64.b64decode(d))

def pack_content(path):
    if path.is_dir():
        s = ""
        for x in path.iterdir():
            s += pack_content(x)
        return s
    elif not path.is_file:
        print(f"[!] Unable to process {path}")

    posix_path = path.as_posix()
    print(f"[*] Processing {posix_path}")
    with path.open("rb") as fd:
        data = base64.b64encode(fd.read()).decode()
        return f"{posix_path}!{data}\n"

def pack(path):
    print("[*] Packing...")
    s = pack_content(path)

    outfile = f"{path.name}.pack"
    with open(outfile, "w") as fd:
        fd.write(s)
    print(f"[*] Created pack file {outfile}")

if args.pack:
    pack(args.path)
elif args.unpack:
    unpack(args.path)
