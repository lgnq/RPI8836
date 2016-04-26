#!/usr/bin/env python
#-*- coding: utf-8 -*-

import define
import tw8836
import spi
import fontosd
import bmposd
import sx1505

import time

img = [
0x000000,
0x0015C0,
0x0044A0,
0x007390,
0x00A2A0,
0x00D1B0,
0x0100B0,
0x013020,
0x015F60,
0x018EE0,
0x01BEA0,
0x01EED0,
0x021EC0,
0x024F00,
0x027F60,
0x02AFB0,
0x02E080,
0x031160,
0x034250,
0x037350,
0x03A410,
0x03D4C0,
0x0405B0,
0x043680,
0x046710,
0x0497D0,
0x04C8C0,
0x04F970,
0x0529F0,
0x055A80,
0x058B60,
0x05BBE0,
0x05ECA0,
0x061D00,
0x064D70,
0x067DA0,
0x06AE10,
0x06DE50,
0x070EA0,
0x073F40,
0x076FC0,
0x079FD0,
0x07D020,
0x080020,
0x083020,
0x085FE0,
0x088FD0,
0x08BF90,
0x08EF40,
0x091E80,
0x094DE0,
0x097D10,
0x09ABD0,
0x09DAD0,
0x0A0970,
0x0A37F0,
0x0A7050,
0x0AA840,
0x0AE030,
0x0B1820,
0x0B5000,
0x0B87E0,
0x0BBEE0,
0x0BF5C0,
0x0C2CD0,
0x0C6360,
0x0C9AC0,
0x0CD1E0,
0x0D0910,
0x0D3FF0,
0x0D76B0,
0x0DAD70,
0x0DE490,
0x0E1B90,
0x0E5240,
0x0E88F0,
0x0EBFD0,
0x0EF700,
0x0F2E60,
0x0F6550,
0x0F9BD0,
0x0FD3C0,
0x100B60,
0x104370,
0x107B50,
0x10B300,
0x10EAC0,
0x111930,
0x1147A0,
0x117630,
0x11A4B0,
0x11D380,
0x1202E0,
0x123230,
0x126150,
0x1290B0,
0x12C070,
0x12F000,
0x131FD0,
0x134FB0,
0x137FD0,
0x13B000,
0x13DFD0,
0x141010,
0x144050,
0x1470A0,
0x14A0D0,
0x14D150,
0x1501D0,
0x153250,
0x1562D0,
0x159380,
0x15C410,
0x15F480,
0x162500,
0x1655A0,
0x168650,
0x16B6D0,
0x16E6F0,
0x171700,
0x174730,
0x177780,
0x17A770,
0x17D7C0,
0x1807A0,
0x183780,
0x186780,
0x189700,
0x18C680,
0x18F5E0,
0x192570,
0x1954A0,
0x1983C0,
0x19B2F0,
0x19E1D0,
0x1A10E0,
0x1A3FD0,
0x1A6EF0,
0x1A9DC0,
0x1ACCA0,
0x1AFB50,
]

print 'this is tw8836 demo using raspberrypi 2'

tw8836.detect()

spi.init()

#spi.sector_erase(0)
#spi.program_test()

try:
    print 'Enable LVDS RX'
    sx1505.lvds_rx_onoff(define.ON)
    
    print 'FPPWC ON'
    sx1505.fppwc_onoff(define.ON)
    
    #print 'FPBIAS ON'
    #sx1505.fpbias_onoff(define.ON)
except IOError:
    print '\033[1;40;31mNot\033[0m find SX1505 at address 0x20'

tw8836.init()

tw8836.sspll1_set_freq(72000000)
tw8836.sspll2_set_freq(108000000)

print 'SSPLL1 frequency is:', tw8836.sspll1_get_freq()
print 'SSPLL2 frequency is:', tw8836.sspll2_get_freq()

print 'SPI CLK is:', tw8836.spi_clk_get()

tw8836.rb_swap(define.ON)
    
fontosd.onoff_control(define.ON)
bmposd.onoff_control(define.ON)

#bmposd.devalue_set()

#bmposd.lut_load(bmposd.WINNO1, 0x800000, 0)
#bmposd.image_display(bmposd.WINNO1, 0x800000, 200, 0, bmposd.PIXEL_ALPHA_MODE, 0x61, 0)

bmposd.lut_load(bmposd.WINNO1, 0x800000, 0)
bmposd.image_display(bmposd.WINNO1, 0x800000, 200, 0, bmposd.PIXEL_ALPHA_MODE, 0x61, 0)

#bmposd.win_start_addr_set(bmposd.WINNO1, 0x800000+0x0015C0+16+256*4)
#bmposd.rlc_set(bmposd.WINNO1, 8, 8)

#bmposd.win_start_addr_set(bmposd.WINNO1, 0x800000+16+256*4)

for d in img:
    tw8836.wait_vblank(1)
    bmposd.win_start_addr_set(bmposd.WINNO1, 0x800000+d+16+256*4)
    bmposd.rlc_set(bmposd.WINNO1, 8, 8)
    time.sleep(0.3)
    #bmposd.image_display(bmposd.WINNO1, 0x800000+d, 200, 0, bmposd.PIXEL_ALPHA_MODE, 0x61, 0)

#bmposd.lut_load(bmposd.WINNO3, 0x10E080, 0)
#bmposd.image_display(bmposd.WINNO3, 0x10E080, 0, 0, bmposd.NO_ALPHA_MODE, 50, 0)

bmposd.color_fill_onoff(8, define.ON)
bmposd.color_fill_set(8, 200, 200, 200, 200, 6)
    
bmposd.alpha_blending_onoff(8, define.ON)
bmposd.alpha_blending_mode_set(8, bmposd.GLOBAL_ALPHA_MODE)
bmposd.global_alpha_value_set(8, 50)
    
bmposd.win_onoff(8, define.ON)
    
"""
for i in range(0, 10):
    bmposd.color_fill_onoff(i, define.ON)
    bmposd.color_fill_set(i, 20*i+50, 20*i+50, 100, 100, i)
    
    bmposd.alpha_blending_onoff(i, define.ON)
    bmposd.alpha_blending_mode_set(i, bmposd.GLOBAL_MODE)
    bmposd.global_alpha_value_set(i, 50)
    
    bmposd.window_onoff(i, define.ON)
"""

#tw8836.wait_vblank(1)

