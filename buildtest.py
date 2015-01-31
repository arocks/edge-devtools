#!/usr/bin/env python
import argparse


parser = argparse.ArgumentParser()
# parser.add_argument("template", help="the template file to templatify")
# parser.add_argument("-o", "--output", dest="outfile", help="Output file")
args = parser.parse_args()

import os
import shutil
from subprocess import call

PROJNAME = "my_proj"
SUPERUSER = "a"
SUPERUSER_PASSWORD = "a"
SUPERUSER_EMAIL = "a@a.com"

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if os.path.isdir(PROJNAME):
    print("Removing existing directory...")
    shutil.rmtree(PROJNAME)

call(["django-admin.py",
      "startproject",
      "--template=../edge",
      "--extension=py,md,html,env",
      PROJNAME])
print("Project build complete...")


import sys
src_dir = os.path.join(BASE_DIR, PROJNAME, 'src')
sys.path.insert(0, src_dir)
os.chdir(src_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "{0}.settings".format(PROJNAME))

import django
django.setup()
print("Django configured...")

from django.core import management
management.call_command('check')
management.call_command('migrate', interactive=False, verbosity=0)

# Create superuser
from django.contrib.auth.models import User
User.objects.create_superuser(SUPERUSER,
                              SUPERUSER_EMAIL,
                              SUPERUSER_PASSWORD)

# Run tests
management.call_command('test', 'profiles', verbosity=0)

# TO REMOVE: Since test cases are already checking this
# Testing web requests
# from django.test.client import Client
# client = Client()
# response = client.get('/')
# if response.status_code == 200:
#     print("Opening home page... ok")
# else:
#     print("Opening home page... FAILED! {0}".format(
#             response.status_code))
