#! /usr/bin/env python

import sys, re

def CC65VersionListToDump():

    re_hex2 = re.compile("^[0123456789ABCDEF]{2}$")
    re_hex6 = re.compile("^[0123456789ABCDEF]{6}$")

    for line in sys.stdin:

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
                print "%04x %02x" % (addr + i, byte_value)

def OriginalVersionListToDump():

    re_empty   = re.compile("^$")
    re_asmerr  = re.compile("^  assembly errors =   0$")
    re_newfile = re.compile("^\\\\newfile .*$")
    re_newpage = re.compile("^\\\\newpage$")
    re_header  = re.compile("^err line  addr  b1 b2 b3 b4 .{64} page [ 0-9]{4}$")

    re_hex2    = re.compile("^[0123456789ABCDEF]{2}$")
    re_hex4    = re.compile("^[0123456789ABCDEF]{4}$")

    for line in sys.stdin:

        assert line[-1] == "\n"
        line = line[:-1]

        if re_empty.match(line) or re_asmerr.match(line) or re_newpage.match(line) or re_header.match(line) or re_newfile.match(line):
            # Ignore these lines.
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
                    print "%04x %02x" % (addr + i, byte_value)

def main():

    assert len(sys.argv) == 2

    assert sys.argv[1].startswith("--version=")

    version = sys.argv[1][10:]

    assert version in ["cc65", "original"]

    if version == "cc65":
        CC65VersionListToDump()
    elif version == "original":
        OriginalVersionListToDump()

if __name__ == "__main__":
    main()
