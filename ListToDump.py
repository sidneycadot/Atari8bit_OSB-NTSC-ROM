#! /usr/bin/env python

import sys
import re

def CC65VersionListToDump(CC65VersionFilename, CC65VersionDumpFilename):

    re_hex2 = re.compile("^[0123456789ABCDEF]{2}$")
    re_hex6 = re.compile("^[0123456789ABCDEF]{6}$")

    fi = open(CC65VersionFilename)
    fo = open(CC65VersionDumpFilename, "w")

    for line in fi:

        assert line[-1] == "\n"
        line = line[:-1]

        addr_string = line[0:6]
        if re_hex6.match(addr_string):
            addr = int(addr_string, 16)
            for i in xrange(4):
                byte_string = line[11 + 3 * i: 13 + 3 * i]
                if not re_hex2.match(byte_string):
                    break
                byte_value = int(byte_string, 16)
                print >> fo, "%04x %02x" % (addr + i, byte_value)

    fo.close()
    fi.close()

def OriginalVersionListToDump(OriginalVersionFilename, OriginalVersionDumpFilename):

    re_empty   = re.compile("^$")
    re_asmerr  = re.compile("^  assembly errors =   0$")
    re_newfile = re.compile("^\\\\newfile .*$")
    re_newpage = re.compile("^\\\\newpage$")
    re_header  = re.compile("^err line  addr  b1 b2 b3 b4 .{64} page [ 0-9]{4}$")

    re_hex2    = re.compile("^[0123456789ABCDEF]{2}$")
    re_hex4    = re.compile("^[0123456789ABCDEF]{4}$")

    fi = open(OriginalVersionFilename)
    fo = open(OriginalVersionDumpFilename, "w")

    for line in fi:

        assert line[-1] == "\n"
        line = line[:-1]

        if re_empty.match(line):
            pass
        elif re_asmerr.match(line):
            pass
        elif re_newpage.match(line):
            pass
        elif re_header.match(line):
            pass
        elif re_newfile.match(line):
            pass
        else:
            addr_string = line[10:14]
            if re_hex4.match(addr_string):
                addr = int(addr_string, 16)
                for i in xrange(4):
                    byte_string = line[16 + 3 * i:18 + 3 * i]
                    if not re_hex2.match(byte_string):
                        break
                    byte_value = int(byte_string, 16)
                    print >> fo, "%04x %02x" % (addr + i, byte_value)

    fo.close()
    fi.close()

def main():
    assert len(sys.argv) == 2
    if sys.argv[1] == "--version=cc65":
        CC65VersionListToDump("CC65Version.lst", "CC65Version.dump")
    elif sys.argv[1] == "--version=original":
        OriginalVersionListToDump("OriginalVersion.lst", "OriginalVersion.dump")

if __name__ == "__main__":
    main()
