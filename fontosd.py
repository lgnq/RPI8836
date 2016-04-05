#!/usr/bin/env python
#-*- coding: utf-8 -*-

import define
import tw8836

"""
//----------------
// Font OSD
//----------------
"""
REG_FOSD_CHEIGHT		=	0x90
REG_FOSD_MUL_CON		=	0x91
REG_FOSD_ALPHA_SEL		=	0x92
REG_FOSD_MADD3			=	0x93
REG_FOSD_MADD4			=	0x94

def onoff_control(onoff):
    tw8836.write_page(0x03)
    
    val = tw8836.read(0x0C)
    
    if (onoff == define.ON):
        if (val & 0x40):
            tw8836.write(0x0C, val & ~0x40)
            return 1
    else:
        if ((val & 0x40) == 0):
            tw8836.write(0x0C, val | 0x40)
            return 1
            
    return 0
    
def devalue_set():
    tw8836.write_page(0x02)
    
    hde = tw8836.read(0x10)
    pclko = tw8836.read(0x0D) & 0x03
    
    pclko = 1

    tw8836.write_page(0x04)    
    mixing = tw8836.read(0x00) & 0x02
    if (mixing):
        mixing = 1
    else:
        mixing = 0
        
    if ((hde + pclko) < (mixing*2 + 36)):
        temp = (mixing*2+36) - hde - pclko + 1
    else:
        temp = hde + pclko - (mixing*2+36)
        
    tw8836.write_page(0x03)
    tw8836.write(0x03, temp)

"""
 set FONT Width & Height

	r300[4]		0: CharWidth 12. 1:CharWidth 16.
	r390[4:0]	(Font OSD Char Height ) >> 1
	r391[6:0]	Sub-Font Total Count. used bytes for one font. if 12x18, use 27.
"""    
def font_width_height_set(width, height):
    tw8836.write_page(0x03)
    
    val = tw8836.read(0x00)
    
    if (width == 16):
        val |= 0x10
    elif (width == 12):
        val &= ~0x10
    else:
        print 'font width is wrong, it must be 12 or 16'
        return
        
    tw8836.write(0x00, val)
    
    tw8836.write(REG_FOSD_CHEIGHT, height >> 1) 					#Font height(2~32)
    tw8836.write(REG_FOSD_MUL_CON, (width >> 2) * (height >> 1))	#sub-font total count.    

"""
 set FOSD blink attribute

 this will effect only when FW writes data on OsdRam.
 the background color will fill out when it blink.

	r304[7] Blink
"""
def blink_onoff(onoff):
    tw8836.write_page(0x03)
    
    val = tw8836.read(0x04)
    if (onoff):
        tw8836.write(0x04, val | 0x80)
    else:
        tw8836.write(0x04, val & ~0x80)
    
