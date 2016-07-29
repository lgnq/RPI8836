#!/usr/bin/env python
#-*- coding: utf-8 -*-

import define
import tw8836
import spi
import fontosd
import bmposd
import sx1505

import time
import sys

img = [
#0x000000,
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

img_norle = [
0x000000,
0x03F890,
0x07F120,
0x0BE9B0,
0x0FE240,
0x13DAD0,
0x17D360,
0x1BCBF0,
0x1FC480,
0x23BD10,
0x27B5A0,
0x2BAE30,
0x2FA6C0,
0x339F50,
0x3797E0,
0x3B9070,
0x3F8900,
0x438190,
0x477A20,
0x4B72B0,
0x4F6B40,
0x5363D0,
0x575C60,
0x5B54F0,
0x5F4D80,
0x634610,
0x673EA0,
0x6B3730,
0x6F2FC0,
0x732850,
]

if __name__ == '__main__':
    length = len(sys.argv)	
    
    if (length == 1 or sys.argv[1] == 'help' or sys.argv[1] == 'h' or sys.argv[1] == '?'):
        print 'this is tw8836 demo using raspberrypi 2'
        print '================= help ================='
        print 'help, h, ?   - print this help message'
        print 'init, i      - init TW8836'
        print 'show, s      - show image at address 0xXXXXXX'
        print '             - s winno address sx sy alpha level offset'
        print 'detect, d    - input source detect'
        print '================= note ================='
        print 'please set the I2C speed > 400Kbps'
        print 'sudo modprobe -r i2c_bcm2708'
        print 'sudo modprobe i2c-bcm2708 baudrate=1000000'
        print '========================================'
        print 'sudo cat /sys/module/i2c_bcm2708/parameters/baudrate'
        print 'lsmod'
                
        exit
    elif (sys.argv[1] == 'init' or sys.argv[1] == 'i'):
        tw8836.detect()
        
        while tw8836.SPI_READ_SLOW != tw8836.spi_read_mode_check():
            tw8836.spi_read_mode(tw8836.SPI_READ_SLOW)

        spi.init()
        
        while tw8836.SPI_READ_QUAD_IO != tw8836.spi_read_mode_check():
            tw8836.spi_read_mode(tw8836.SPI_READ_QUAD_IO)
        
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
            
        bmposd.onoff_control(define.ON)        
    elif sys.argv[1] == 'animation' or sys.argv[1] == 'a':
        img_spi_addr = 0x600000
        img_list = img
        
        bmposd.lut_load(bmposd.WINNO1, img_spi_addr + img_list[3], 0)
            
        for i in range(0, 50):
            tw8836.wait_vblank(1)
            #bmposd.all_win_off()
            bmposd.win_onoff(1, define.OFF)
            bmposd.image_display(bmposd.WINNO1, img_spi_addr + img_list[i], 0, 0, bmposd.PIXEL_ALPHA_MODE, 0x08, 0)        
            
            tw8836.wait_vblank(2)
    elif sys.argv[1] == 'show' or sys.argv[1] == 's':
        winno = bmposd.WINNO1
        img_spi_addr = 0x100000
        sx = 0
        sy = 0
        alpha = bmposd.NO_ALPHA_MODE
        level = 0x000000
        offset = 0
        
        spi.spi_flash_detect()
        
        if length > 2:
            winno = int(sys.argv[2], 16)
            
        if length > 3:
            img_spi_addr = int(sys.argv[3], 16)
            print 'show a picture at address', hex(img_spi_addr)
        
        bmposd.win_onoff(winno, define.OFF)
        
        bmposd.lut_load(winno, img_spi_addr, offset)
        
        if length > 4:
            sx = int(sys.argv[4], 16)

        if length > 5:
            sy = int(sys.argv[5], 16)
        
        if length > 6:
            if sys.argv[6] == 'pixel' or sys.argv[6] == 'p':
                print 'set pixel alpha blending'
                alpha = bmposd.PIXEL_ALPHA_MODE
            elif sys.argv[6] == 'golable' or sys.argv[6] == 'g':
                print 'set golable alpha blending'
                alpha = bmposd.GLOBAL_ALPHA_MODE
        
        if length > 7:
            level = int(sys.argv[7], 16)            

        if length > 8:
            offset = int(sys.argv[8], 16)            
        
        tw8836.wait_vblank(1)		
        bmposd.image_display(winno, img_spi_addr, sx, sy, alpha, level, offset)
    elif sys.argv[1] == 'detect' or sys.argv[1] == 'd':
        print 'detect the input status'
        print '======================='
        tw8836.detect_inputs()
    else:    
        #bmposd.devalue_set()
        
        #bmposd.lut_load(bmposd.WINNO8, 0x100000, 0)
        #bmposd.image_display(bmposd.WINNO8, 0x100000, 0, 0, bmposd.GLOBAL_ALPHA_MODE, 0x61, 0)
        
        img_spi_addr = 0x600000
        img_list = img
        
        bmposd.lut_load(bmposd.WINNO1, img_spi_addr+img_list[0], 0)
        bmposd.pixel_alpha_set(bmposd.WINNO1, 0, 0, 0x30)
        bmposd.pixel_alpha_set(bmposd.WINNO1, 0, 1, 0x40)
        bmposd.pixel_alpha_set(bmposd.WINNO1, 0, 2, 0x50)
        bmposd.pixel_alpha_set(bmposd.WINNO1, 0, 3, 0x60)
        bmposd.pixel_alpha_set(bmposd.WINNO1, 0, 4, 0x7F)
        bmposd.pixel_alpha_set(bmposd.WINNO1, 0, 5, 0x7F)
        bmposd.pixel_alpha_set(bmposd.WINNO1, 0, 6, 0x7F)
        bmposd.pixel_alpha_set(bmposd.WINNO1, 0, 7, 0x7F)
        bmposd.pixel_alpha_set(bmposd.WINNO1, 0, 8, 0x7F)
        bmposd.pixel_alpha_set(bmposd.WINNO1, 0, 9, 0x7F)
        bmposd.pixel_alpha_set(bmposd.WINNO1, 0, 10, 0x7F)
        
        bmposd.image_display(bmposd.WINNO1, img_spi_addr+img_list[0], 200, 0, bmposd.PIXEL_ALPHA_MODE, 0x8, 0)
        
        #bmposd.win_start_addr_set(bmposd.WINNO1, img_spi_addr+0x0015C0+16+256*4)
        #bmposd.rlc_set(bmposd.WINNO1, 8, 8)
        
        #bmposd.win_start_addr_set(bmposd.WINNO1, img_spi_addr+16+256*4)
        
        bmposd.color_fill_onoff(2, define.ON)
        bmposd.win_onoff(2, define.ON)
        
        while (1):
            for i in range(0, len(img_list)):
                tw8836.wait_vblank(1)
            
                bmposd.rlc_set(bmposd.WINNO1, 8, 8)
                bmposd.win_start_addr_set(bmposd.WINNO1, img_spi_addr+img_list[i]+16+256*4)
                bmposd.color_fill_set(bmposd.WINNO2, 200, 200, i, 20, 0)
        
                #bmposd.image_display(bmposd.WINNO1, img_spi_addr+d, 200, 0, bmposd.PIXEL_ALPHA_MODE, 0x8, 0)
        
                #time.sleep(0.01)
            
            for i in range(0, len(img_list)):
                tw8836.wait_vblank(1)
                
                n = len(img_list)-1-i
                bmposd.win_start_addr_set(bmposd.WINNO1, img_spi_addr+img_list[n]+16+256*4)
                bmposd.color_fill_set(bmposd.WINNO2, 200, 200, n, 20, 0)
        
        #bmposd.lut_load(bmposd.WINNO3, 0x10E080, 0)
        #bmposd.image_display(bmposd.WINNO3, 0x10E080, 0, 0, bmposd.NO_ALPHA_MODE, 50, 0)
        
        """
        bmposd.color_fill_onoff(8, define.ON)
        bmposd.color_fill_set(8, 200, 200, 200, 200, 6)
            
        bmposd.alpha_blending_onoff(8, define.ON)
        bmposd.alpha_blending_mode_set(8, bmposd.GLOBAL_ALPHA_MODE)
        bmposd.global_alpha_value_set(8, 50)
            
        bmposd.win_onoff(8, define.ON)
        """
        
        """
        tw8836.wait_vblank(1)
            
        bmposd.lut_load(bmposd.WINNO8, img_spi_addr+img_list[0], 0)
        bmposd.win_onoff(8, define.ON)
        bmposd.color_fill_onoff(8, define.ON)
        for i in range(0, 100):
            bmposd.color_fill_set(8, 200, 200, i, 20, 0)
            time.sleep(0.01)
        """
            
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

