#!/usr/bin/env python
import subprocess
from pathlib import Path
from os import chdir
from sys import exit

PARENT_DIR = Path(__file__).resolve().parent.parent
EDGE_DIR = PARENT_DIR / 'edge'
REQ_DIR = EDGE_DIR / 'requirements'

# COMMANDS:
# pipenv lock --requirements > requirements/base.txt
# echo "-r base.txt" > requirements/development.txt
# pipenv lock --requirements --dev >> requirements/development.txt

base_reqs = REQ_DIR / "base.txt"
dev_reqs = REQ_DIR / "development.txt"

chdir(EDGE_DIR)

if not base_reqs.exists():
    print(f"base.txt not found!")
    exit(-1)
if not dev_reqs.exists():
    print(f"development.txt not found!")
    exit(-1)

# Updating base requirements
proc = subprocess.run(["pipenv", "lock", "--requirements"],
                      stdout=subprocess.PIPE)
base_contents = proc.stdout.decode("utf-8")
with open(base_reqs, "w") as f:
    f.write(base_contents)
    print("base.txt is updated!")

# Updating dev requirements
proc = subprocess.run(["pipenv", "lock", "--requirements", "--dev"],
                      stdout=subprocess.PIPE)
dev_contents = proc.stdout.decode("utf-8")
with open(dev_reqs, "w") as f:
    f.write("-r base.txt\n")
    f.write(dev_contents)
    print("development.txt is updated!")
