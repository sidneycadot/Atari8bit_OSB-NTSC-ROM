#! /usr/bin/env python

# Read CC65Version.dump

f = open("CC65Version.dump")

memoryMap = {}

for line in f:

    (address, content) = [int(s, 16) for s in line.split()]

    if 0xc000 <= address <= 0xffff:
        assert address not in memoryMap
        memoryMap[address] = content

f.close()

# Read atariosb-ntsc.rom

f   = open("atariosb-ntsc.rom")
rom = map(ord, f.read())
f.close()

# Print areas of consecutive bytes that are not defined in the dump file.

if True:
    print "Number of bytes in dump file: %d." % len(memoryMap)
    current = None # indicates we are not tracking an undefined stretch.
    for i in xrange(0xe400, 0x10000 + 1):
        if (i in memoryMap) or (i == 0x10000):
            if current is not None:
                # We were tracking an undefined area, but we now encounter a defined byte!
                contents = ",".join(["%02x" % rom[address - 0xd800] for address in xrange(current, i)])
                print "NOTE: memory area not defined in dump file: %04x to %04x (%2d bytes); ROM is %s" % (current, i - 1, i - current, contents)
                current = None # stop tracking undefined area.
        else:
            if current is None:
                current = i

# Make sure that all bytes found in CC65Version.dump correspond to the bytes seen in the ROM file.

for (address, content) in memoryMap.iteritems():
    found = rom[address - 0xd800]
    assert content == found

print "ok!"
