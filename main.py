#!/usr/bin/env python
#-*- coding: utf-8 -*-

import define
import tw8836
import spi
import fontosd
import bmposd
import sx1505

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

#bmposd.lut_load(bmposd.WINNO1, 0x100000, 0)
#bmposd.image_display(bmposd.WINNO1, 0x100000, 0, 0, bmposd.NO_ALPHA_MODE, 0, 0)

bmposd.lut_load(bmposd.WINNO3, 0x10E080, 0)
bmposd.image_display(bmposd.WINNO3, 0x10E080, 0, 0, bmposd.NO_ALPHA_MODE, 50, 0)

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

