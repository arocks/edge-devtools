#!/usr/bin/env python
import argparse
import os
import shutil
from subprocess import call

PROJNAME = "my_proj"
SUPERUSER = "a"
SUPERUSER_PASSWORD = "a"
SUPERUSER_EMAIL = "a@a.com"

parser = argparse.ArgumentParser()
args = parser.parse_args()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if os.path.isdir(PROJNAME):
    print("Removing existing directory...")
    shutil.rmtree(PROJNAME)

call(
    [
        "django-admin.py",
        "startproject",
        "--verbosity=3",
        "--template=../edge",
        "--extension=py,md,html,env",
        PROJNAME,
    ]
)
print("Project build complete...")

import sys

src_dir = os.path.join(BASE_DIR, PROJNAME, "src")
sys.path.insert(0, src_dir)
os.chdir(src_dir)

print("Copying local.env from sample...")
shutil.copyfile(
    "{0}/settings/local.sample.env".format(PROJNAME),
    "{0}/settings/local.env".format(PROJNAME),
)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "{0}.settings.development".format(PROJNAME)
)

import django

django.setup()
print("Django configured...")

from django.core import management

print("Checking apps...")
management.call_command("check")
print("Migrating...")
management.call_command("migrate", interactive=False, verbosity=2)

# Create superuser
print("Creating superuser...")
from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.create_superuser(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

# Run tests
# print("Running tests...")
# management.call_command('test', 'profiles', verbosity=0)

# Track changes
os.chdir("..")  # Up one level from `src` back to proj root
print("Setting a git repo...")
shutil.copyfile("../_gitignore_my_proj", ".gitignore")
call(["git", "init"])
call(["git", "add", "."])
call(["git", "commit", "-q", "-m", "'initial'"])
print("Git repo created!")

# change to project dir and run server
os.chdir("src")
try:
    call(["python", "-Wd", "manage.py", "runserver"])
except KeyboardInterrupt:
    print("\nBUILD TEST FINISHED")
