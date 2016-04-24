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

tw8836.sspll1_set_freq(108000000)
tw8836.sspll2_set_freq(108000000)

print 'SSPLL1 frequency is:', tw8836.sspll1_get_freq()
print 'SSPLL2 frequency is:', tw8836.sspll2_get_freq()

print 'SPI CLK is:', tw8836.spi_clk_get()

tw8836.rb_swap(define.ON)
    
fontosd.onoff_control(define.ON)
bmposd.onoff_control(define.ON)

#tw8836.wait_vblank(1)

