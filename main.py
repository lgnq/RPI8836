#!/usr/bin/env python

import tw8836
import spi

"""
tw8836.write_page(0x00)

id = tw8836.read(0x00)
print 'id is', hex(id)

revision = tw8836.read(0x01)
print 'revision is', hex(revision)
"""

print 'this is tw8836 demo using raspberrypi2'

tw8836.init()

"""
tw88xx_id = tw8836.read_id()
print 'id is', hex(tw88xx_id[0])
print 'rev is', hex(tw88xx_id[1])

if (tw88xx_id[0] == 0x36):
	if (tw88xx_id[1] == 0x11):
		print 'TW8836B2 is founded!'
		tw8836.init()
	else:
		print 'TW8836A is founded!'
else:
	print 'unknown device!'		
"""

"""
spi_id = spi.read_id()
print spi_id
"""

spi.quad_enable()

spi.sector_erase()
