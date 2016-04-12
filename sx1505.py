#!/usr/bin/env python
#-*- coding: utf-8 -*-

import define
import smbus

SX1504_DATA_REG			= 0	#data register index
SX1504_DIR_REG			= 1	#direction register index

SX1504_DIR_IN			= 1	#input direction
SX1504_DIR_OUT			= 0	#output direction

SX1504_PIN1_FP_PWC		= 0
SX1504_PIN0_FP_BIAS		= 1
SX1504_PIN4_LVDSTX		= 4

ADDR = 0x20
bus = smbus.SMBus(1)

def write(idx, val):
    bus.write_byte_data(ADDR, idx, val)

def read(idx):
    return bus.read_byte_data(ADDR, idx)

def pin_setup(pin, dir, val):
	mask = 1
	mask <<= pin

	if (dir == SX1504_DIR_IN):
		#read..
		dir_reg  = read(SX1504_DIR_REG)
		dir_reg |= mask

		write(SX1504_DIR_REG, dir_reg)

		data_reg = read(SX1504_DATA_REG)

		if (data_reg & mask):
			return 1
		else:
			return 0
	else:
		#write..
		dir_reg  = read(SX1504_DIR_REG)
		dir_reg &= ~mask

		data_reg = read(SX1504_DATA_REG)
		if (val):
			data_reg |= mask
		else:
			data_reg &= ~mask

		write(SX1504_DIR_REG, dir_reg)		#write direction first,
		write(SX1504_DATA_REG, data_reg)	#and then write data.
		
		return 0




