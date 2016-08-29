#!/usr/bin/env python
#-*- coding: utf-8 -*-

import define
import tw8836
import spi

def quad_check():
    status = spi.status1_read()
    
    if (status & 0x40):
        print 'SPI flash is already in QUAD mode'
        return define.TRUE
    else:
        print 'SPI flash is not in QUAD mode yet'
        return define.FALSE
        
def quad_enable():
    status = spi.status1_read()
    
    spi.write_enable()
    spi.status1_write(status | 0x40)
    spi.write_disable()
    
def quad_disable():
    status = spi.status1_read()

    spi.write_enable()
    spi.status1_write(status & ~0x40)
    spi.write_disable()
    
def four_byte_check():
    status = spi.status2_read()
    
    if (status & 0x20):
        if define.DEBUG == define.ON:
            print 'SPI flash is in 4 Byte mode'
        spi.bank_address_register_write(0x80)
        
        return define.TRUE
    else:
        if define.DEBUG == define.ON:
            print 'SPI flash is not in 4 Byte mode'
        spi.bank_address_register_write(0x0)
        
        return define.FALSE

def four_byte_enter():
    tw8836.write_page(0x04)
    
    tw8836.write(0xF3, (spi.DMA_DEST_CHIPREG << 6) + spi.DMA_CMD_COUNT_1)    
    
    tw8836.write(0xF5, 0)    #length high
    tw8836.write(0xF8, 0)    #length middle
    tw8836.write(0xF9, 0)    #length low
    
    tw8836.write(0xFA, spi.SPICMD_EN4B)
    tw8836.write(0xF4, spi.SPI_CMD_OPT_NONE | spi.DMA_START)

def four_byte_exit():
    tw8836.write_page(0x04)
    
    tw8836.write(0xF3, (spi.DMA_DEST_CHIPREG << 6) + spi.DMA_CMD_COUNT_1)
    
    tw8836.write(0xF5, 0)    #length high
    tw8836.write(0xF8, 0)    #length middle
    tw8836.write(0xF9, 0)    #length low
    
    tw8836.write(0xFA, spi.SPICMD_EX4B)
    tw8836.write(0xF4, spi.SPI_CMD_OPT_NONE | spi.DMA_START)
    
def dummy_cycles_config(mode, cycles):
    print 'dummy_cycles_config in issi.py'
    
    status2_register = spi.status2_read()
    print hex(status2_register)        
    
