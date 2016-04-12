#!/usr/bin/env python
#-*- coding: utf-8 -*-

import define
import tw8836
import spi
import fontosd
import bmposd
import sx1505

"""
tw8836.write_page(0x00)

id = tw8836.read(0x00)
print 'id is', hex(id)

revision = tw8836.read(0x01)
print 'revision is', hex(revision)
"""

print 'this is tw8836 demo using raspberrypi 2'

tw8836.init()

try:
	print 'sx1505', hex(sx1505.read(0x00))
	print 'sx1505', hex(sx1505.read(0x01))
except IOError:
	print 'not find SX1505 at address 0x20'


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

#spi.sector_erase(0)
spi.program_test()

fontosd.onoff_control(define.ON)
bmposd.onoff_control(define.ON)

tw8836.wait_vblank(1)

