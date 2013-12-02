#! /usr/bin/env python

# "RootVersion.s" contains the version that is very close to the version found in the
# "Atari Home Computer System Operating System Source Listing", with the following differences:
#
#    * Addition of a "\newfile" pseudo directive;
#    * Addition of a "\newpage" pseudo directive;
#    * Everything is converted to lower case.

import sys, re

re_empty   = re.compile("^$")
re_asmerr  = re.compile("^  assembly errors =   0$")
re_newfile = re.compile("^\\\\newfile$")
re_newpage = re.compile("^\\\\newpage$")
re_header  = re.compile("^err line  addr  b1 b2 b3 b4 .{64} page [ 0-9]{4}$")

def RootVersion_to_OriginalVersion(RootVersionFilename, OriginalVersionFilename):
    fi = open(RootVersionFilename)
    fo = open(OriginalVersionFilename, "w")

    for line in fi:

        assert len(line) > 0
        assert line[-1] == "\n"
        line = line[:-1]

        if re_newfile.match(line):
            print >> fo, "\f"
            continue
        if re_newpage.match(line):
            print >> fo, "\f"
            continue

        print >> fo, line.upper()

    fo.close()
    fi.close()

def RootVersion_to_AlmostCC65Version(RootVersionFilename, AlmostCC65VersionFilename):
    fi = open(RootVersionFilename)
    fo = open(AlmostCC65VersionFilename, "w")

    for line in fi:

        assert len(line) > 0
        assert line[-1] == "\n"
        line = line[:-1]

        if re_empty.match  (line): continue
        if re_asmerr.match (line): continue
        if re_newfile.match(line): continue
        if re_newpage.match(line): continue
        if re_header.match (line): continue

        line = line[33:]

        line = line.replace( "        .page"  , ";       .page"  )
        line = line.replace( "        .title" , ";       .title" )

        line = line.replace( "*="             , ".org    "       )

        print >> fo, line

    fo.close()
    fi.close()

def main():
    assert len(sys.argv) == 2
    version = sys.argv[1]
    if version == "--version=cc65":
        RootVersion_to_AlmostCC65Version("RootVersion.lst", "AlmostCC65Version.s")
    elif version == "--version=original":
        RootVersion_to_OriginalVersion("RootVersion.lst", "OriginalVersion.lst")

if __name__ == "__main__":
    main()
