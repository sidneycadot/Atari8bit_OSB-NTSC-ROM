#! /usr/bin/env python

import sys, re

# Compile regular expressions for the different line types

re_empty   = re.compile("^$")
re_asmerr  = re.compile("^  assembly errors =   0$")
re_newfile = re.compile("^\\\\newfile$")
re_newpage = re.compile("^\\\\newpage$")
re_header  = re.compile("^err line  addr  b1 b2 b3 b4 .{64} page [ 0-9]{4}$")

def Convert_RootVersion_to_OriginalVersion():

    # "RootVersion.s" contains the version that is very close to the version found in the
    # "Atari Home Computer System Operating System Source Listing", with the following differences:
    #
    #    * Addition of a "\newfile" pseudo directive;
    #    * Addition of a "\newpage" pseudo directive;
    #    * Everything is converted to lower case.

    for line in sys.stdin:

        assert len(line) > 0
        assert line[-1] == "\n"
        line = line[:-1]

        if re_newfile.match(line) or re_newpage.match(line):
            print "\f"
            continue

        print line.upper()

def Convert_RootVersion_to_AlmostCC65Version():

    for line in sys.stdin:

        assert len(line) > 0
        assert line[-1] == "\n"
        line = line[:-1]

        if re_empty.match(line) or re_asmerr.match(line) or re_newfile.match(line) or re_newpage.match(line) or re_header.match (line):
            # Discard these lines
            continue

        # discard first 33 characters in the lines
        line = line[33:]

        # comment out ".page" and ".title" directives
        line = line.replace("        .page"  , ";       .page"  )
        line = line.replace("        .title" , ";       .title" )

        # replace *= by equivalent ".org" directive
        line = line.replace("*="             , ".org    "       )

        print line

def main():

    assert len(sys.argv) == 2

    assert sys.argv[1].startswith("--version=")

    version = sys.argv[1][10:]

    assert version in ["cc65", "original"]

    if version == "cc65":
        Convert_RootVersion_to_AlmostCC65Version()
    elif version == "original":
        Convert_RootVersion_to_OriginalVersion()

if __name__ == "__main__":
    main()
