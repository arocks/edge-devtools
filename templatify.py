#!/usr/bin/env python
"""templatify - escapes a Django template for startproject templates
"""
import argparse
import re


def multiple_replace(subdict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, subdict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: subdict[mo.string[mo.start():mo.end()]], text)

parser = argparse.ArgumentParser()
parser.add_argument("template", help="the template file to templatify")
parser.add_argument("-o", "--output", dest="outfile", help="Output file")
args = parser.parse_args()

replacements = {
    "{% ": "{% templatetag openblock %} ",
    " %}": " {% templatetag closeblock %}",
    "{{ ": "{% templatetag openvariable %} ",
    " }}": " {% templatetag closevariable %}",
}

with open(args.template, "r") as f:
    contents = f.read()
    contents = multiple_replace(replacements, contents)
    if args.outfile:
        with open(args.outfile, "w") as o:
            o.write(contents)
    else:
        print(contents)
