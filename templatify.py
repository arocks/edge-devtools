#!/usr/bin/env python
"""templatify - escapes a Django template for startproject templates
"""
import os, sys, re, argparse

replacements = {
    "{% ": "{% templatetag openblock %} ",
    " %}": " {% templatetag closeblock %}",
    "{{ ": "{% templatetag openvariable %} ",
    " }}": " {% templatetag closevariable %}",
}


def multiple_replace(subdict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, subdict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: subdict[mo.string[mo.start() : mo.end()]], text)


def transform(infileobj, outfileobj):
    global replacements
    contents = infileobj.read()
    contents = multiple_replace(replacements, contents)
    outfileobj.write(contents)


def copy_dirs(src, dest, ignore=None, verbosity=False):
    if os.path.isdir(src):
        if (dest is not None) and (not os.path.isdir(dest)):
            os.makedirs(dest)
            if verbosity:
                print(f"Created {dest} directory")
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                copy_dirs(
                    os.path.join(src, f),
                    os.path.join(dest, f) if dest is not None else None,
                    ignore,
                    verbosity,
                )
    else:
        # shutil.copyfile(src, dest)
        if verbosity:
            print(f"Writing: {src}=>{dest}")
            with open(src, "r") as infileobj:
                if dest is not None:
                    with open(dest, "w") as outfileobj:
                        transform(infileobj, outfileobj)
                else:
                    transform(infileobj, sys.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("template", help="the template file/directory to templatify")
    parser.add_argument("-o", "--output", dest="outfile", help="Output file/directory")
    parser.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        help="Perform destructive in-place replacement on same file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show verbose output",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.template):
        # Single file passed
        infile = args.template
        outfile = None
        if args.outfile:
            outfile = args.outfile
        elif args.inplace:
            outfile = infile
        if args.verbose:
            print(f"Writing: {infile}=>{outfile}")
        with open(infile, "r") as infileobj:
            if outfile is not None:
                with open(outfile, "w") as outfileobj:
                    transform(infileobj, outfileobj)
            else:
                transform(infileobj, sys.stdout)
    else:
        # Directory passed
        indir = args.template
        outdir = None
        if args.outfile:
            outdir = args.outfile
        copy_dirs(indir, outdir, verbosity=args.verbose)


if __name__ == "__main__":
    main()
