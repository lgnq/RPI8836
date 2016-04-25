#!/usr/bin/env python
#-*- coding: utf-8 -*-

import define
import tw8836
import spi

def onoff_control(onoff):
    tw8836.write_page(0x04)
    
    val = tw8836.read(0x00)
    
    if (onoff == define.ON):
        tw8836.write(0x00, val | 0x04)
    else:
        tw8836.write(0x00, val & ~0x04)

def header_parse(header):
    print header
    
    if ((header[0] != ord('I')) and (header[1] != ord('T'))):
        print 'ERROR! wrong osd header'

def image_display(winno, image_addr):
    header = []
    spi.read(image_addr, header, 0x10)
    header_parse(header)

