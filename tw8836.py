#!/usr/bin/env python
#-*- coding: utf-8 -*-

import define
import smbus

ADDR = 0x45
bus = smbus.SMBus(1)

regs = [
0xFF, 0x00,  # Page 0
0x00, 0x36,
0x02, 0xC8,
0x03, 0xE8,
0x04, 0x00,
0x06, 0x06,
0x07, 0x08,
0x08, 0x86,
0x0F, 0x00,
0x1F, 0x00,
0x40, 0x3B,
0x41, 0x11,
0x42, 0x47,
0x43, 0x28,
0x44, 0x3A,
0x45, 0xBC,
0x46, 0x85,
0x47, 0x00,
0x48, 0x00,
0x4B, 0x00,
0x50, 0xA0,
0x51, 0x09,
0x52, 0x02,
0x53, 0x05,
0x54, 0x11,
0x56, 0x04,
0x57, 0x00,
0x5F, 0x00,
0x60, 0x00,
0x66, 0x30,
0x67, 0x00,
0x68, 0x00,
0x69, 0x02,
0x6A, 0x20,
0x6B, 0xF0,
0x6C, 0x20,
0x6D, 0xD0,
0x6E, 0x10,
0x6F, 0x10,
0x80, 0x00,
0x81, 0x00,
0x82, 0x00,
0x83, 0x00,
0x84, 0x01,
0x85, 0x00,
0x86, 0x00,
0x88, 0x00,
0x89, 0x00,
0x8A, 0x00,
0x8B, 0x00,
0x8C, 0x00,
0x8D, 0x00,
0x8E, 0x00,
0x90, 0x00,
0x91, 0x00,
0x92, 0x00,
0x93, 0x00,
0x94, 0x00,
0x95, 0x00,
0x96, 0x00,
0x98, 0x00,
0x99, 0x00,
0x9A, 0x00,
0x9B, 0x00,
0x9C, 0x31,
0x9D, 0x00,
0x9E, 0x80,
0xA0, 0x00,
0xA1, 0x00,
0xA2, 0x20,
0xA3, 0x00,
0xA4, 0xC0,
0xB0, 0x0F,
0xB1, 0xF8,
0xB2, 0x00,
0xB3, 0x00,
0xB4, 0x0A,
0xD4, 0x00,
0xD6, 0x00,
0xD7, 0x00,
0xD8, 0x80,
0xD9, 0x00,
0xDA, 0x80,
0xDB, 0x55,
0xDC, 0x00,
0xDD, 0x80,
0xDE, 0x00,
0xDF, 0x80,
0xE6, 0x00,
0xE7, 0x16,
0xE8, 0x01,
0xE9, 0x55,
0xEA, 0x55,
0xEB, 0x40,
0xEC, 0x30,
0xED, 0x23,
0xEE, 0x00,
0xEF, 0x00,
0xF6, 0x00,
0xF7, 0x16,
0xF8, 0x01,
0xF9, 0x4B,
0xFA, 0xDB,
0xFB, 0x40,
0xFC, 0x30,
0xFD, 0x23,

0xFF, 0x01,  # Page 1
0x01, 0x93,
0x02, 0x40,
0x04, 0x00,
0x05, 0x01,
0x06, 0x03,
0x07, 0x02,
0x08, 0x12,
0x09, 0xF0,
0x0A, 0x0B,
0x0B, 0xD0,
0x0C, 0xCC,
0x0D, 0x00,
0x10, 0x00,
0x11, 0x5C,
0x12, 0x11,
0x13, 0x80,
0x14, 0x80,
0x15, 0x00,
0x17, 0x30,
0x18, 0x44,
0x1A, 0x10,
0x1B, 0x00,
0x1C, 0x27,
0x1D, 0x7F,
0x1E, 0x00,
0x1F, 0x00,
0x20, 0x50,
0x21, 0x22,
0x22, 0xF0,
0x23, 0xD8,
0x24, 0xBC,
0x25, 0xB8,
0x26, 0x44,
0x27, 0x38,
0x28, 0x00,
0x29, 0x00,
0x2A, 0x78,
0x2B, 0x44,
0x2C, 0x30,
0x2D, 0x14,
0x2E, 0xA5,
0x2F, 0xE0,
0x30, 0xD0,
0x31, 0x00,
0x32, 0x00,
0x33, 0x05,
0x34, 0x1A,
0x35, 0x00,
0x36, 0xE3,
0x37, 0x28,
0x38, 0xAF,
0x40, 0x00,
0x41, 0x80,
0x42, 0x00,
0xC0, 0x01,
0xC1, 0xC7,
0xC2, 0xD2,
0xC3, 0x03,
0xC4, 0x5A,
0xC5, 0x00,
0xC6, 0x20,
0xC7, 0x04,
0xC8, 0x00,
0xC9, 0x06,
0xCA, 0x06,
0xCB, 0x16,
0xCC, 0x00,
0xCD, 0x54,
0xD0, 0x00,
0xD1, 0xF0,
0xD2, 0xF0,
0xD3, 0xF0,
0xD4, 0x20,
0xD5, 0x00,
0xD6, 0x10,
0xD7, 0x00,
0xD8, 0x00,
0xD9, 0x02,
0xDA, 0x80,
0xDB, 0x80,
0xDC, 0x10,
0xE0, 0x00,
0xE1, 0x05,
0xE2, 0xD9,
0xE3, 0x37,
0xE4, 0x55,
0xE5, 0x55,
0xE6, 0x20,
0xE7, 0x2A,
0xE8, 0x20,
0xE9, 0x00,
0xEA, 0x03,

0xFF, 0x02,  # Page 2
0x01, 0x00,
0x02, 0x20,
0x03, 0x00,
0x04, 0x20,
0x05, 0x13,
0x06, 0x48,
0x07, 0x40,
0x08, 0x20,
0x09, 0x99,
0x0A, 0x09,
0x0B, 0x10,
0x0C, 0x21,
0x0D, 0x41,
0x0E, 0x30,
0x0F, 0x02,
0x10, 0x30,
0x11, 0x20,
0x12, 0x03,
0x13, 0x00,
0x14, 0x0A,
0x15, 0x12,
0x16, 0xE0,
0x17, 0x01,
0x18, 0x00,
0x19, 0xF3,
0x1A, 0x00,
0x1B, 0x00,
0x1C, 0x42,
0x1D, 0xB2,
0x1E, 0x02,
0x20, 0x00,
0x21, 0x00,
0x40, 0x10,
0x41, 0x00,
0x42, 0x05,
0x43, 0x01,
0x44, 0x64,
0x45, 0xF4,
0x46, 0x00,
0x47, 0x0A,
0x48, 0x36,
0x49, 0x10,
0x4A, 0x00,
0x4B, 0x00,
0x4C, 0x00,
0x4D, 0x44,
0x4E, 0x04,
0x80, 0x20,
0x81, 0x80,
0x82, 0x80,
0x83, 0x80,
0x84, 0x80,
0x85, 0x80,
0x86, 0x80,
0x87, 0x80,
0x88, 0x80,
0x89, 0x80,
0x8A, 0x80,
0x8B, 0x40,
0x8C, 0x00,
0xB0, 0x10,
0xB1, 0x40,
0xB2, 0x40,
0xB6, 0x67,
0xB7, 0x94,
0xBF, 0x00,
0xE0, 0x00,
0xE1, 0x00,
0xE2, 0x00,
0xE3, 0x00,
0xE4, 0x21,
0xF0, 0x00,
0xF1, 0x00,
0xF2, 0x00,
0xF3, 0x00,
0xF4, 0x00,
0xF5, 0x00,
0xF8, 0x00,
0xF9, 0x80,

0xFF, 0x03,  # Page 3
0x00, 0x10,
0x01, 0x06,
0x02, 0x06,
0x03, 0x0D,
0x04, 0x0C,
0x05, 0x00,
0x06, 0x00,
0x07, 0x00,
0x08, 0x1A,
0x09, 0x00,
0x0A, 0x00,
0x0B, 0x80,
0x0C, 0x2F,
0x0D, 0x21,
0x0E, 0x24,
0x10, 0x40,
0x11, 0x0F,
0x12, 0x00,
0x13, 0x00,
0x14, 0x00,
0x15, 0x01,
0x16, 0x04,
0x17, 0x00,
0x18, 0x00,
0x19, 0x00,
0x1A, 0x00,
0x1B, 0x00,
0x1C, 0x00,
0x1D, 0x00,
0x1E, 0x00,
0x1F, 0x00,
0x20, 0x40,
0x21, 0x0F,
0x22, 0x00,
0x23, 0x00,
0x24, 0x1E,
0x25, 0x01,
0x26, 0x28,
0x27, 0x00,
0x28, 0x00,
0x29, 0x00,
0x2A, 0x00,
0x2B, 0x00,
0x2C, 0x00,
0x2D, 0x00,
0x2E, 0x00,
0x2F, 0x28,
0x30, 0x40,
0x31, 0x0F,
0x32, 0x00,
0x33, 0x00,
0x34, 0x3C,
0x35, 0x01,
0x36, 0x28,
0x37, 0x00,
0x38, 0x00,
0x39, 0x00,
0x3A, 0x00,
0x3B, 0x00,
0x3C, 0x00,
0x3D, 0x00,
0x3E, 0x00,
0x3F, 0x50,
0x40, 0x40,
0x41, 0x0F,
0x42, 0x00,
0x43, 0x00,
0x44, 0x5A,
0x45, 0x01,
0x46, 0x28,
0x47, 0x00,
0x48, 0x00,
0x49, 0x00,
0x4A, 0x00,
0x4B, 0x00,
0x4C, 0x00,
0x4D, 0x00,
0x4E, 0x00,
0x4F, 0x78,
0x50, 0x40,
0x51, 0x0F,
0x52, 0x00,
0x53, 0x00,
0x54, 0x78,
0x55, 0x01,
0x56, 0x28,
0x57, 0x00,
0x58, 0x00,
0x59, 0x00,
0x5A, 0x00,
0x5B, 0x00,
0x5C, 0x00,
0x5D, 0x00,
0x5E, 0x00,
0x5F, 0xA0,
0x60, 0x40,
0x61, 0x0F,
0x62, 0x00,
0x63, 0x00,
0x64, 0x96,
0x65, 0x01,
0x66, 0x28,
0x67, 0x00,
0x68, 0x00,
0x69, 0x00,
0x6A, 0x00,
0x6B, 0x00,
0x6C, 0x00,
0x6D, 0x00,
0x6E, 0x00,
0x6F, 0xC8,
0x70, 0x40,
0x71, 0x0F,
0x72, 0x00,
0x73, 0x00,
0x74, 0xB4,
0x75, 0x01,
0x76, 0x28,
0x77, 0x00,
0x78, 0x00,
0x79, 0x00,
0x7A, 0x00,
0x7B, 0x00,
0x7C, 0x00,
0x7D, 0x00,
0x7E, 0x00,
0x7F, 0xF0,
0x80, 0x40,
0x81, 0x0F,
0x82, 0x00,
0x83, 0x00,
0x84, 0xD2,
0x85, 0x01,
0x86, 0x28,
0x87, 0x10,
0x88, 0x00,
0x89, 0x00,
0x8A, 0x00,
0x8B, 0x00,
0x8C, 0x00,
0x8D, 0x00,
0x8E, 0x00,
0x8F, 0x18,
0x90, 0x0D,
0x91, 0x34,
0x92, 0x01,
0x93, 0x80,
0x94, 0x9E,

0xFF, 0x04,  # Page 4
0x00, 0x00,
0x04, 0x00,
0x05, 0x00,
0x06, 0x00,
0x07, 0x00,
0x0E, 0x00,
0x0F, 0x1E,
0x10, 0x00,
0x11, 0x00,
0x12, 0x00,
0x20, 0x00,
0x21, 0x00,
0x22, 0x00,
0x23, 0x00,
0x24, 0x00,
0x25, 0x00,
0x26, 0x00,
0x27, 0x00,
0x28, 0x00,
0x29, 0x00,
0x2A, 0x00,
0x2B, 0x00,
0x2C, 0x00,
0x2D, 0x00,
0x2E, 0x00,
0x2F, 0x00,
0x30, 0x00,
0x31, 0x00,
0x32, 0x00,
0x33, 0x00,
0x34, 0x00,
0x35, 0x00,
0x36, 0x00,
0x40, 0x00,
0x41, 0x00,
0x42, 0x00,
0x43, 0x00,
0x44, 0x00,
0x45, 0x00,
0x46, 0x00,
0x47, 0x00,
0x48, 0x00,
0x49, 0x00,
0x4A, 0x00,
0x4B, 0x00,
0x4C, 0x00,
0x4D, 0x00,
0x4E, 0x00,
0x50, 0x00,
0x51, 0x00,
0x52, 0x00,
0x53, 0x00,
0x54, 0x00,
0x55, 0x00,
0x56, 0x00,
0x57, 0x00,
0x58, 0x00,
0x59, 0x00,
0x5A, 0x00,
0x5B, 0x00,
0x5C, 0x00,
0x5D, 0x00,
0x5E, 0x00,
0x60, 0x00,
0x61, 0x00,
0x62, 0x00,
0x63, 0x00,
0x64, 0x00,
0x65, 0x00,
0x66, 0x00,
0x67, 0x00,
0x68, 0x00,
0x69, 0x00,
0x6A, 0x00,
0x6B, 0x00,
0x6C, 0x00,
0x6D, 0x00,
0x6E, 0x00,
0x70, 0x00,
0x71, 0x00,
0x72, 0x00,
0x73, 0x00,
0x74, 0x00,
0x75, 0x00,
0x76, 0x00,
0x77, 0x00,
0x78, 0x00,
0x79, 0xF0,
0x7A, 0x00,
0x7B, 0x00,
0x7C, 0x00,
0x7D, 0x00,
0x7E, 0x00,
0x80, 0x00,
0x81, 0x00,
0x82, 0x00,
0x83, 0x00,
0x84, 0x00,
0x85, 0x00,
0x86, 0x00,
0x87, 0x00,
0x88, 0x00,
0x89, 0x00,
0x8A, 0x00,
0x8B, 0x00,
0x8C, 0x00,
0x8D, 0x00,
0x8E, 0x00,
0x90, 0x00,
0x91, 0x00,
0x92, 0x00,
0x93, 0x00,
0x94, 0x00,
0x95, 0x00,
0x96, 0x00,
0x97, 0x00,
0x98, 0x00,
0x99, 0x00,
0x9A, 0x00,
0x9B, 0x00,
0x9C, 0x00,
0x9D, 0x00,
0x9E, 0x00,
0xA0, 0x00,
0xA1, 0x00,
0xA2, 0x00,
0xA3, 0x00,
0xA4, 0x00,
0xA5, 0x00,
0xA6, 0x00,
0xA7, 0x00,
0xA8, 0x00,
0xA9, 0x00,
0xAA, 0x00,
0xAB, 0x00,
0xAC, 0x00,
0xAD, 0x00,
0xAE, 0x00,
0xB0, 0x00,
0xB1, 0x00,
0xB2, 0x00,
0xB3, 0x00,
0xB4, 0x00,
0xB5, 0x00,
0xB6, 0x00,
0xB7, 0x00,
0xB8, 0x00,
0xB9, 0x00,
0xBA, 0x00,
0xBB, 0x00,
0xBC, 0x00,
0xBD, 0x00,
0xBE, 0x00,
0xC0, 0x05,
0xC1, 0x60,
0xC2, 0x00,
0xC3, 0xC8,
0xC4, 0x80,
0xC5, 0x80,
0xC6, 0x00,
0xC7, 0x00,
0xC8, 0x00,
0xC9, 0x80,
0xCA, 0xEB,
0xCB, 0x00,
0xCC, 0x04,
0xCD, 0x80,
0xCE, 0x04,
0xCF, 0x1F,
0xD0, 0x40,
0xD1, 0x20,
0xD2, 0x19,
0xD3, 0x00,
0xD4, 0x00,
0xD5, 0x00,
0xD6, 0x00,
0xD7, 0x00,
0xD8, 0x05,
0xD9, 0x08,
0xDA, 0x00,
0xDB, 0x00,
0xDC, 0x00,
0xDD, 0x1C,
0xDE, 0x00,
0xDF, 0x00,
0xE0, 0x00,
0xE1, 0x20,
0xE2, 0x69,
0xE3, 0x78,
0xE4, 0x01,
0xE5, 0x0E,
0xE6, 0x00,
0xE7, 0x1B,
0xE8, 0x00,
0xE9, 0x0C,
0xEA, 0x00,
0xEB, 0x0C,
0xF0, 0x00,
0xF1, 0x00,
0xF2, 0x00,
0xF3, 0x40,
0xF4, 0x80,
0xF5, 0x00,
0xF6, 0x04,
0xF7, 0x90,
0xF8, 0x00,
0xF9, 0x00,
0xFA, 0x00,
0xFB, 0x00,
0xFC, 0x00,
0xFD, 0x00,
0xFE, 0x00,

0xFF, 0x05,  # Page 5
0x00, 0x00,
0x01, 0x02,
0x02, 0x0F,
0x03, 0xFF,
0x04, 0x00,
0x05, 0x00,
0x06, 0x0F,
0x07, 0xFF,
0x08, 0x08,
0x09, 0x09,
0x0A, 0x01,
0x0B, 0x40,
0x10, 0x00,
0x11, 0x08,
0x12, 0x67,
0x13, 0x90,
0x14, 0x00,
0x15, 0x08,
0x16, 0x67,
0x17, 0x90,
0x18, 0x00,
0x19, 0x08,
0x1A, 0x67,
0x1B, 0x90,
0x1C, 0x00,
0x1D, 0x00,
0x1E, 0x00,
0x1F, 0xFF,
0x20, 0xFF,
0x21, 0xFF,
0x22, 0x04,
0x23, 0x65,
0x24, 0x04,
0x25, 0x2B,
0x26, 0x00,
0x27, 0x2C,
0x28, 0x08,
0x29, 0x40,
0x2A, 0x00,
0x2B, 0x05,
0x2C, 0x08,
0x2D, 0x98,
0x2E, 0x00,
0x2F, 0xBC,
0x30, 0x00,
0x31, 0xBC,
0x32, 0x08,
0x33, 0x3B,
0x34, 0x08,
0x35, 0x3D,
0x36, 0x00,
0x37, 0x2A,
0x38, 0x00,
0x39, 0x2A,
0x3A, 0x04,
0x3B, 0x61,
0x3C, 0x04,
0x3D, 0x61,
0x40, 0xFF,
0x41, 0x00,
0x42, 0xFF,
0x43, 0x06,
0x44, 0xDD,
0x45, 0xCF,

0xFF, 0x06,  # Page 6
0x40, 0x00,
0x41, 0x00,
0x42, 0x00,
0x43, 0x00,
0x44, 0x00,
0x45, 0x00,
0x46, 0x01,
0x47, 0x00,
0x48, 0x07,
0x49, 0x01,
0x4A, 0x00,
0x4B, 0x34,
0x4C, 0x40,
0x4D, 0x17,
0x4E, 0x00,
  
  0xFF, 0xFF,
]

def write_page(page):
    bus.write_byte_data(ADDR, 0xFF, page)

def write(idx, val):
    bus.write_byte_data(ADDR, idx, val)

def read(idx):
    return bus.read_byte_data(ADDR, idx)
	
def read_id():
	write_page(0x00)
	
	id = read(0x00)
	rev = read(0x01)
	
	return id, rev

def mcu_halt():
	write_page(0x04);

	write(0xED, 0x55)
	write(0xED, 0xAA)
	write(0xEC, 0x00)

def mcu_return():
	write_page(0x04);

	write(0xED, 0x55)
	write(0xED, 0xAA)
	write(0xEC, 0x01)	 

def rb_swap(onoff):
    write_page(0x00);
    
    dat = read(0x07)

    if (onoff):
        dat |= 0x80
    else:
        dat &= ~(0x08)
        
    write(0x07, dat)    
    
def init_regs(regs):
	i = 0

	while (1):
		if ((regs[i] == 0xFF) and (regs[i+1] == 0xFF)):
			break;

		if (define.DEBUG == define.ON):
			print hex(regs[i])

		write(regs[i], regs[i+1])	

		i = i + 2

def detect():
	id = read_id()
	print 'TW88xx id is', hex(id[0])
	print 'TW88xx rev is', hex(id[1])

	if (id[0] == 0x36):
		if (id[1] == 0x11):
			print 'find \033[1;40;32mTW8836B2\033[0m!'
			#init_regs(regs)
	else:
		print 'wrong TW88xx ID detected!'

def init():
    init_regs(regs)

def sspll1_get_freq_reg():
    write_page(0x00)
    
    fpll = read(0xF8) & 0x0F
    fpll <<= 8
    fpll |= read(0xF9)
    fpll <<= 8
    fpll |= read(0xFA)
    
    return fpll

def sspll2_get_freq_reg():
    write_page(0x00)
    
    fpll = read(0xE8) & 0x0F
    fpll <<= 8
    fpll |= read(0xE9)
    fpll <<= 8
    fpll |= read(0xEA)
    
    return fpll

def sspll1_get_post():
    write_page(0x00)
    
    post = read(0xFD)
    post = (post>>6)&0x03
    
    return post

def sspll2_get_post():
    write_page(0x00)
    
    post = read(0xED)
    post = (post>>6)&0x03
    
    return post
    
def sspll_fpll2freq(fpll, post):
    freq = fpll >> 6
    freq *= 421875
    freq >>= 3
    freq >>= post
    
    return freq
    
"""
    get SSPLL 1 Frequency.


	FPLL = REG(0x0f8[3:0], 0x0f9[7:0], 0x0fa[7:0])
	POST = REG(0x0fd[7:6])
	PLL Osc Freq = 108MHz * FPLL / 2^17 / 2^POST
"""
def sspll1_get_freq():
    fpll = sspll1_get_freq_reg()
    post = sspll1_get_post()
    
    freq = sspll_fpll2freq(fpll, post)
    
    #print 'SSPLL 1 Frequency is', freq, 'POST is', post
    
    return freq

"""
    get SSPLL 2 Frequency.


	FPLL = REG(0x0f8[3:0], 0x0f9[7:0], 0x0fa[7:0])
	POST = REG(0x0fd[7:6])
	PLL Osc Freq = 108MHz * FPLL / 2^17 / 2^POST
"""
def sspll2_get_freq():
    fpll = sspll2_get_freq_reg()
    post = sspll2_get_post()
    
    freq = sspll_fpll2freq(fpll, post)
    
    #print 'SSPLL 2 Frequency is', freq, 'POST is', post

    return freq

def sspll_freq2fpll(freq, post):
    fpll = freq/1000
    fpll <<= post
    fpll <<= 12
    fpll = fpll / 3375
    
    return fpll

def sspll1_set_freq_reg(fpll):
    write_page(0x00)
    
    write(0xFA, fpll & 0xFF)
    write(0xF9, (fpll>>8) & 0xFF)
    write(0xF8, (fpll>>16) & 0xFF)

def sspll2_set_freq_reg(fpll):
    write_page(0x00)
    
    write(0xEA, fpll & 0xFF)
    write(0xE9, (fpll>>8) & 0xFF)
    write(0xE8, (fpll>>16) & 0xFF)
    
def sspll1_set_analog_control(value):
    write_page(0x00)
    
    write(0xFD, value)

def sspll2_set_analog_control(value):
    write_page(0x00)
    
    write(0xED, value)
    
def sspll1_set_freq(freq):
    if (freq > 150000000):
        print 'ERROR! Max SSPLL frequency is 150MHz'
        return
        
    if (freq < 27000000):
        vco = 2
        curr = 0
        post = 2
    elif (freq < 54000000):
        vco = 2
        curr = 1
        post = 1
    elif (freq < 108000000):
        vco = 2
        curr = 2
        post = 0
    else:
        vco = 3
        curr = 3
        post = 0
        
    curr = vco + 1

    fpll = sspll_freq2fpll(freq, post)
    sspll1_set_freq_reg(fpll)
    sspll1_set_analog_control((vco << 4) | (post << 6) | curr)

def sspll2_set_freq(freq):
    if (freq > 150000000):
        print 'ERROR! Max SSPLL frequency is 150MHz'
        return
        
    if (freq < 27000000):
        vco = 2
        curr = 0
        post = 2
    elif (freq < 54000000):
        vco = 2
        curr = 1
        post = 1
    elif (freq < 108000000):
        vco = 2
        curr = 2
        post = 0
    else:
        vco = 3
        curr = 3
        post = 0
        
    curr = vco + 1

    fpll = sspll_freq2fpll(freq, post)
    sspll2_set_freq_reg(fpll)
    sspll2_set_analog_control((vco << 4) | (post << 6) | curr)
    
def spi_clk_get():
    write_page(0x04)

    SPI_CK_SEL = (read(0xE1) >> 4) & 0x3
    if (SPI_CK_SEL == 0x00):
        return 27000000
    elif (SPI_CK_SEL == 0x01):
        return 32000
    elif (SPI_CK_SEL == 0x02):
        SPI_CK_DIV = read(0xE1) & 0xF
        
        if (SPI_CK_DIV == 0x0):
            div = 1
        elif (SPI_CK_DIV == 0x1):
            div = 1.5
        elif (SPI_CK_DIV == 0x2):
            div = 2
        elif (SPI_CK_DIV == 0x3):
            div = 2.5
        elif (SPI_CK_DIV == 0x4):
            div = 3
        elif (SPI_CK_DIV == 0x5):
            div = 3.5
        elif (SPI_CK_DIV == 0x6):
            div = 4
        elif (SPI_CK_DIV == 0x7):
            div = 5
        elif (SPI_CK_DIV == 0x8):
            div = 8
        elif (SPI_CK_DIV == 0x9):
            div = 16
        elif (SPI_CK_DIV == 0xA):
            div = 32
            
        PLL_SEL = read(0xE0) & 0x1
        
        if (PLL_SEL == 0x0):
            write_page(0x0)
        
            SPI_PLL_SEL = (read(0x4B) >> 5) & 0x1
            
            if (SPI_PLL_SEL == 0x0):
                return sspll1_get_freq() / div
            elif (SPI_PLL_SEL == 0x1):
                return sspll2_get_freq() / div
        elif (PLL_SEL == 0x1):
            return 108000000 / div

"""
def spi_clk_set():
"""
    
def wait_vblank(n):
    write_page(0x00)
    
    for i in range(n):
        write(0x02, 0xFF)
        while ((read(0x02) & 0x40) == 0x00):
            print 'wait vblank'
            