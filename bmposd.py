#!/usr/bin/env python
#-*- coding: utf-8 -*-

import define
import tw8836
import spi

#RLE2/MRLE headerv 16 Byte
ID0_IDX         = 0
ID1_IDX         = 1
OP_BMPBITS_IDX  = 2
RLEDATA_CNT_IDX = 3
WIDTH_L_IDX     = 4
WIDTH_H_IDX     = 5
HEIGHT_L_IDX    = 6
HEIGHT_H_IDX    = 7
SIZE0_IDX       = 8
SIZE1_IDX       = 9
SIZE2_IDX       = 10
SIZE3_IDX       = 11
LUT_FORMAT_IDX  = 12 
LUT_COLORS_IDX  = 13
DUMMY0_IDX      = 14
DUMMY1_IDX      = 15

MRLE_HEADER_SIZE     = 16

WINNO0 = 0
WINNO1 = 1
WINNO2 = 2
WINNO3 = 3
WINNO4 = 4
WINNO5 = 5
WINNO6 = 6
WINNO7 = 7
WINNO8 = 8

GLOBAL_MODE = 0
PIXEL_MODE  = 1

NO_INC      = 0x0
BYTE_INC    = 0x1
ADDR_INC    = 0x2

def devalue_set():
    tw8836.write_page(0x02)
    
    hde = tw8836.read(10)
    pclko = tw8836.read(0x0D) & 0x03
    pclko = 0
    
    temp = hde + pclko - 18

    tw8836.write_page(0x04)
    
    tw8836.write(0x0E, temp>>8)
    tw8836.write(0x0F, temp&0xFF)
    
def onoff_control(onoff):
    tw8836.write_page(0x04)
    
    val = tw8836.read(0x00)
    
    if (onoff == define.ON):
        tw8836.write(0x00, val | 0x04)
    else:
        tw8836.write(0x00, val & ~0x04)

def window_onoff(winno, onoff):
    tw8836.write_page(0x04)
    
    if (winno == WINNO0):
        temp = tw8836.read(0x20)
        if (onoff):
            tw8836.write(0x20, temp | 0x01)
        else:
            tw8836.write(0x20, temp & ~0x01)
    else:
        temp = tw8836.read(0x40 + (winno-1)*0x10)
        if (onoff):
            tw8836.write(0x40 + (winno-1)*0x10, temp | 0x01)
        else:
            tw8836.write(0x40 + (winno-1)*0x10, temp & ~0x01)

def header_parse(mrle_spi_addr):
    header = []
    spi.read(mrle_spi_addr, header, MRLE_HEADER_SIZE)
    
    if (define.DEBUG == define.ON):
        print header
    
    if ((header[ID0_IDX] != ord('I')) or (header[ID1_IDX] != ord('T'))):
        print 'ERROR! wrong osd header'
    
    for i in range(0, MRLE_HEADER_SIZE):
        print hex(header[i])
    
    width  = header[WIDTH_L_IDX] + (header[WIDTH_H_IDX] << 8)
    height = header[HEIGHT_L_IDX] + (header[HEIGHT_H_IDX] << 8)
    size   = (header[SIZE3_IDX]<<24) + (header[SIZE2_IDX]<<16) + (header[SIZE1_IDX]<<8) + header[SIZE0_IDX]
    colors = header[LUT_COLORS_IDX] + 1
    rle    = header[RLEDATA_CNT_IDX] & 0xF
    
    if (colors == 256):
        bpp = 8
    elif (colors == 128):
        bpp = 7
    elif (colors == 64):
        bpp = 6    
    elif (colors == 32):
        bpp = 5
    elif (colors == 16):
        bpp = 4
    elif (colors == 8):
        bpp = 3
    elif (colors == 4):
        bpp = 2
        
    lut_size = colors * 4

    lut_spi_addr   = mrle_spi_addr + MRLE_HEADER_SIZE
    image_spi_addr = mrle_spi_addr + MRLE_HEADER_SIZE + lut_size
    
    print width, height, size, colors, bpp, rle, lut_size, hex(lut_spi_addr), hex(image_spi_addr)
    return width, height, bpp, rle, lut_size, lut_spi_addr, image_spi_addr

def image_starting_addr_reg_set(winno, image_loc):
    tw8836.write_page(0x04)

    if (winno == WINNO0):
        tw8836.write(0x27, image_loc>>20)
        tw8836.write(0x28, image_loc>>12)
        tw8836.write(0x29, image_loc>>4)
        tw8836.write(0x37, image_loc&0x0F)
    else:
        tw8836.write(0x47 + (winno-1)*0x10, image_loc>>20)
        tw8836.write(0x48 + (winno-1)*0x10, image_loc>>12)
        tw8836.write(0x49 + (winno-1)*0x10, image_loc>>4)
        tw8836.write(0x4F + (winno-1)*0x10, image_loc&0x0F)

def image_width_height_reg_set(winno, width, height):
    tw8836.write_page(0x04)

    if (winno == WINNO0):
        temp = height>>8
        temp <<= 4
        temp |= width>>8
        
        tw8836.write(0x2A, temp)
        tw8836.write(0x2B, width&0xFF)
        tw8836.write(0x2C, height&0xFF)
    else:
        temp = tw8836.read(0x4A + (winno-1)*0x10)
        temp = (temp & 0xC0) | ((width>>8) & 0x0F)
        tw8836.write(0x4A + (winno-1)*0x10, temp)
        tw8836.write(0x4B + (winno-1)*0x10, width & 0xFF)

def window_reg_set(winno, x, y, w, h):
    tw8836.write_page(0x04)
    
    if (winno == WINNO0):
        temp = (((y>>8)&0x7)<<4) | ((x>>8)&0x7)
        tw8836.write(0x21, temp)
        tw8836.write(0x22, x&0xFF)
        tw8836.write(0x23, y&0xFF)
        
        temp = (((h>>8)&0xF)<<4) | ((w>>8)&0xF)
        tw8836.write(0x24, temp)
        tw8836.write(0x25, w&0xFF)
        tw8836.write(0x26, h&0xFF)
    else:
        temp = (((y>>8)&0x7)<<4) | ((x>>8)&0x7)
        tw8836.write(0x41 + (winno-1)*0x10, temp)
        tw8836.write(0x42 + (winno-1)*0x10, x&0xFF)
        tw8836.write(0x43 + (winno-1)*0x10, y&0xFF)
        
        temp = (((h>>8)&0xF)<<4) | ((w>>8)&0xF)
        tw8836.write(0x44 + (winno-1)*0x10, temp)
        tw8836.write(0x45 + (winno-1)*0x10, w&0xFF)
        tw8836.write(0x46 + (winno-1)*0x10, h&0xFF)

def alpha_blending_onoff(winno, onoff):
    tw8836.write_page(0x04)
    
    if (winno == WINNO0):
        temp = tw8836.read(0x20)
        if (onoff):
            tw8836.write(0x20, temp | (1<<4))
        else:
            tw8836.write(0x20, temp & ~(1<<4))
    else:
        temp = tw8836.read(0x40 + (winno-1)*0x10)
        if (onoff):
            tw8836.write(0x40 + (winno-1)*0x10, temp | (1<<4))
        else:
            tw8836.write(0x40 + (winno-1)*0x10, temp & ~(1<<4))

def alpha_blending_mode_set(winno, mode):
    tw8836.write_page(0x04)
    
    if (winno == WINNO0):
        temp = tw8836.read(0x20)    
        if (mode == PIXEL_MODE):
            tw8836.write(0x20, temp | (1<<5))            
        elif (mode == GLOBAL_MODE):
            tw8836.write(0x20, temp & ~(1<<5))        
    else:
        temp = tw8836.read(0x40 + (winno-1)*0x10)    
        if (mode == PIXEL_MODE):
            tw8836.write(0x40 + (winno-1)*0x10, temp | (1<<5))            
        elif (mode == GLOBAL_MODE):
            tw8836.write(0x40 + (winno-1)*0x10, temp & ~(1<<5)) 

"""
alpha = 0x00 - MIN alpha blending
alpha = 0x7F - MAX alpha blending
"""
def global_alpha_value_set(winno, alpha):
    tw8836.write_page(0x04)
    
    if (winno == WINNO0):
        tw8836.write(0x30, alpha)
    else:
        tw8836.write(0x4C + (winno-1)*0x10, alpha)

def win_pixel_width_set(winno, bpp):
    tw8836.write_page(0x04)

    if (winno == WINNO0):
        temp = tw8836.read(0x20)
        if (bpp == 4):
            tw8836.write(0x20, (temp&0x3F) | (0<<6))
        elif (bpp == 6):
            tw8836.write(0x20, (temp&0x3F) | (1<<6))
        else:
            tw8836.write(0x20, (temp&0x3F) | (2<<6))            
    else:
        temp = tw8836.read(0x40 + (winno-1)*0x10)
        if (bpp == 4):
            tw8836.write(0x40 + (winno-1)*0x10, (temp&0x3F) | (0<<6))
        elif (bpp == 6):
            tw8836.write(0x40 + (winno-1)*0x10, (temp&0x3F) | (1<<6))
        else:
            tw8836.write(0x40 + (winno-1)*0x10, (temp&0x3F) | (2<<6))

def lut_offset_set(winno, offset):
    tw8836.write_page(0x04)

    if (winno == WINNO0):
        tw8836.write(0x31, (offset>>4) & 0x1F)
    else:
        tw8836.write(0x4D + (winno-1)*0x10, (offset>>4) & 0x1F)

def rlc_reset(winno):
    tw8836.write_page(0x04)
    
    if (winno == WINNO0):
        return
    elif ((winno == WINNO1) or (winno == WINNO2)):
        tw8836.write(0x06, 1<<1)
    else:
        tw8836.write(0x04, 1<<1)
        
def rlc_set(winno, bpp, rle):
    tw8836.write_page(0x04)

    if (rle):
        if (winno == WINNO0):
            print 'ERROR! WIN 0 can not display RLE image'
            return
        elif ((winno == WINNO1) or (winno == WINNO2)):
            tw8836.write(0x06, winno<<4)
            tw8836.write(0x07, (bpp<<4) | (rle))
        else:
            tw8836.write(0x04, winno<<4)
            tw8836.write(0x05, (bpp<<4) | (rle))
    else:
        rlc_reset(winno)

def lut_write_enable():
    tw8836.write_page(0x04)
    
    temp = tw8836.read(0x10)
    tw8836.write(0x10, temp | 0x80)

def lut_inc_select(mode):
    tw8836.write_page(0x04)
    
    temp = tw8836.read(0x10)
    temp = temp & 0x9F
    tw8836.write(0x10, temp | (mode<<5))

def lut_select(winno):
    tw8836.write_page(0x04)
    
    temp = tw8836.read(0x10)
    temp = temp & 0xFD
    if ((winno == WINNO1) or (winno == WINNO2)):
        tw8836.write(0x10, temp | (1<<2))
    else:
        tw8836.write(0x10, temp & ~(1<<2))

def lut_addr_set(addr):
    tw8836.write_page(0x04)

    temp = tw8836.read(0x10)
    temp = temp & 0xF7

    tw8836.write(0x10, temp | ((addr>>8)<<3))
    tw8836.write(0x11, addr&0xFF)

def lut_load(winno, lut_spi_addr, lut_size, lut_offset):
    lut_write_enable()
    lut_inc_select(BYTE_INC)
    lut_select(winno)
    lut_addr_set(lut_offset)
    
    spi.spi2lut(lut_spi_addr, lut_offset, lut_size)
    
def image_display(winno, mrle_spi_addr, x, y, w, h):
    header = header_parse(mrle_spi_addr)
    
    width           = header[0]
    height          = header[1] 
    bpp             = header[2]
    rle             = header[3]
    lut_size        = header[4]
    lut_spi_addr    = header[5]
    image_spi_addr  = header[6]
    
    image_starting_addr_reg_set(winno, image_spi_addr)
    image_width_height_reg_set(winno, w, h)
    window_reg_set(winno, x, y, w, h)
    
    alpha_blending_mode_set(winno, GLOBAL_MODE)
    global_alpha_value_set(winno, 0x50)
    alpha_blending_onoff(winno, define.ON)
    
    win_pixel_width_set(winno, bpp)
    lut_offset_set(winno, 0)
    rlc_set(winno, bpp, rle)
    
    lut_load(winno, lut_spi_addr, lut_size, 0)
    
    window_onoff(winno, define.ON)

def color_fill_onoff(winno, onoff):
    tw8836.write_page(0x04)
    
    if (winno == WINNO0):
        temp = tw8836.read(0x20)
        if (onoff):
            tw8836.write(0x20, temp | (1<<2))
        else:
            tw8836.write(0x20, temp & ~(1<<2))
    else:
        temp = tw8836.read(0x40 + (winno-1)*0x10)
        if (onoff):
            tw8836.write(0x40 + (winno-1)*0x10, temp | (1<<2))
        else:
            tw8836.write(0x40 + (winno-1)*0x10, temp & ~(1<<2))
            
def color_fill_set(winno, x, y, w, h, color):
    window_reg_set(winno, x, y, w, h)
    
    tw8836.write_page(0x04)
    
    if (winno == WINNO0):
        tw8836.write(0x36, color)
    else:
        tw8836.write(0x4E + (winno-1)*0x10, color)
        