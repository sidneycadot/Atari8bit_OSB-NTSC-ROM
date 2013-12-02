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

print "Number of bytes in dump file: %d." % len(memoryMap)

#for i in xrange(0xe400, 0xffff + 1):
#    if i not in memoryMap:
#        print "Address not found: %04x" % i

# Read atariosb-ntsc.rom
f   = open("atariosb-ntsc.rom")
rom = f.read()
f.close()

# Make sure that all bytes found in CC65Version.dump correspond to the bytes seen in the ROM file.
for (address, content) in memoryMap.iteritems():
    found = ord(rom[address - 0xd800])
    assert content == found

print "ok!"
