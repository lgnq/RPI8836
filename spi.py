#!/usr/bin/env python

import tw8836

DMA_NO_BUSY_CHECK = 0
DMA_BUSY_CHECK = 1

DMA_START = 1

DMA_READ = 0
DMA_WRITE = 1

DMA_DEST_CHIPREG = 1
DMA_CMD_COUNT_1 = 1

SPICMD_WREN = 0x06
SPICMD_RDID = 0x9F

SPI_CMD_OPT_NONE		 = 0x00
SPI_CMD_OPT_BUSY		 = 0x04
SPI_CMD_OPT_WRITE		 = 0x02
SPI_CMD_OPT_WRITE_BUSY	 = 0x06
SPI_CMD_OPT_WRITE_BUSY_AUTO	 = 0x16


def read_id():
    tw8836.write_page(0x04)
    
    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)

    #read id command
    tw8836.write(0xFA, SPICMD_RDID)

    tw8836.write(0xF6, 0x04)
    tw8836.write(0xF7, 0xD0)

    #read data length
    tw8836.write(0xF5, 0x00)
    tw8836.write(0xF8, 0x00)
    tw8836.write(0xF9, 0x03)

    #start DMA write (no BUSY check)
    tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)

    manufacture_id = tw8836.read(0xD0)
    device_id_1 = tw8836.read(0xD1)
    device_id_2 = tw8836.read(0xD2)

    print 'manufacture id is', hex(manufacture_id)
    print 'device id 1 is', hex(device_id_1)
    print 'device id 2 is', hex(device_id_2)

    return manufacture_id, device_id_1, device_id_2

def read_status():
    tw8836.write_page(0x04)

def quad_init():
    id = read_id()

    if (id[0] == 0x1C):
        print 'EON'
    elif (id[0] == 0xC2):
        print 'MXIC'
    elif (id[0] == 0xC8):
        print 'GD'

def write_enable():
	tw8836.write_page(0x04)
	
	tmp = tw8836.read(0xF4)
	print 'REG0x4F4 is', hex(tmp)
	if (tmp & 0x01):
		print 'oops... you need lv_reset!'
	
	tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | 0x01)
	tw8836.write(0xF5, 0)
	tw8836.write(0xF8, 0)	
	tw8836.write(0xF9, 0)
	
	tw8836.write(0xFA, SPICMD_WREN)
	tw8836.write(0xF4, 0x01 | SPI_CMD_OPT_NONE);

def sector_erase():
	write_enable()	

def block_erase():
	write_enable()

def chip_erase():		
	write_enable()
