#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time

import define
import tw8836

import issi
import macronix
import gigadevice

DMA_NO_BUSY_CHECK = 0
DMA_BUSY_CHECK = 1

DMA_START = 1

DMA_READ = 0
DMA_WRITE = 1

DMA_DEST_FONTRAM    = 0
DMA_DEST_CHIPREG    = 1
DMA_DEST_SOSD_LUT   = 2
DMA_DEST_MCU_XMEM   = 3

DMA_ACCESS_MODE_INC = 0
DMA_ACCESS_MODE_DEC = 1
DMA_ACCESS_MODE_FIX = 2

DMA_CMD_COUNT_1 = 1
DMA_CMD_COUNT_2 = 2
DMA_CMD_COUNT_3 = 3
DMA_CMD_COUNT_4 = 4
DMA_CMD_COUNT_5 = 5

SPI_CMD_OPT_NONE         = 0x00
SPI_CMD_OPT_BUSY         = 0x04
SPI_CMD_OPT_WRITE         = 0x02
SPI_CMD_OPT_WRITE_BUSY     = 0x06
SPI_CMD_OPT_WRITE_BUSY_AUTO     = 0x16

"""
#-----------------------------------------------------------------------------
# SPI FLASH Command
#-----------------------------------------------------------------------------
"""
SPICMD_WRSR             = 0x01    #write status register
SPICMD_PP               = 0x02    #Page program
SPICMD_READ_SLOW        = 0x03    #Read data
SPICMD_WRDI             = 0x04    #write disable
SPICMD_RDSR             = 0x05    #read status register
SPICMD_WREN             = 0x06    #write enable
SPICMD_READ_FAST        = 0x0B    #fast read data
SPICMD_FASTDTRD         = 0x0D    #fast DT read
SPICMD_WRSR3            = 0x11    #write status register3(WB) 
SPICMD_RDCR             = 0x15    #read configuration register(Macronix)
SPICMD_RDSR3            = 0x15    #read status3 register(WB). dat[0]:4B
SPICMD_SE               = 0x20    #sector erase
SPICMD_RDINFO           = 0x2B    #read information register. S[2]=1:4byte mode 
SPICMD_RDSCUR           = 0x2B    #read security register
SPICMD_WRSCUR           = 0x2F    #write security register
SPICMD_CLSR             = 0x30    #clear SR fail flags
SPICMD_WRSR2            = 0x31    #write status register2(WB) 
SPICMD_RDSR2            = 0x35    #read status2 register(WB). dat[1]:QE
SPICMD_SBLK             = 0x36    #single block lock
SPICMD_4PP              = 0x38    #quad page program
SPICMD_SBULK            = 0x39    #single block unlock
SPICMD_READ_DUAL_O      = 0x3B    
SPICMD_RDBLOCK          = 0x3C    #block protect read
SPICMD_EXPLM            = 0x45    #exit parallel mode
SPICMD_CLRFREG          = 0x50    #clear flag status register(micron)
SPICMD_BE32K            = 0x52    #block erase 32KB
SPICMD_ENPLM            = 0x55    #enter parallel mode
SPICMD_CE               = 0x60    #chip erase. 0x60 or 0xC7
SPICMD_WDVEREG          = 0x61    #write volatile enhanced register(micron)
SPICMD_RDVEREG          = 0x65    #read volatile enhanced register(micron)
SPICMD_ENHBL            = 0x67    #enter high bank latch mode
SPICMD_WPSEL            = 0x68    #write protection selection
SPICMD_READ_QUAD_O      = 0x6B
SPICMD_RDFREG           = 0x70    #read flag status register(micron)
SPICMD_ESRY             = 0x70    #enable SO to output RY/BY#
SPICMD_GBLK             = 0x7E    #gang block lock
SPICMD_DSRY             = 0x80    #disable SO to output RY/BY#
SPICMD_WDVREG           = 0x81    #write volatile register(micron)
SPICMD_RDVREG           = 0x85    #read volatile register(micron)
SPICMD_REMS             = 0x90    #read electronic manufacturer & device ID
SPICMD_EXHBL            = 0x98    #exit high bank latch mode
SPICMD_GBULK            = 0x98    #gang block unlock
SPICMD_RDID             = 0x9F    #read identification.
SPICMD_HPM              = 0xA3    #high performance enable mode
SPICMD_RDP              = 0xAB    #Release from deep power down
SPICMD_RES              = 0xAB    #read electronic ID
SPICMD_CP               = 0xAD    #continusly program mode
SPICMD_QPIID            = 0xAF    #QPI ID read
SPICMD_WDNVREG          = 0xB1    #write non-volatile register(micron)
SPICMD_ENSO             = 0xB1    #enter secured OTP
SPICMD_RDNVREG          = 0xB5    #read non-volatile register(micron)
SPICMD_EN4B             = 0xB7    #enter 4Byte mode
SPICMD_DP               = 0xB9    #Deep power down
SPICMD_READ_DUAL_IO     = 0xBB    #2x I/O read command
SPICMD_2DTRD            = 0xBD    #dual I/O DT Read
SPICMD_EXSO             = 0xC1    #exit secured OTP
SPICMD_REMS4D           = 0xCF    #read ID for 4x I/O DT mode
SPICMD_BE               = 0xD8    #block erase 64KB
SPICMD_REMS4            = 0xDF    #read ID for 4x I/O mode
SPICMD_RDLOCK           = 0xE8    #read Lock register(micron)
SPICMD_EX4B             = 0xE9    #exit 4Byte mode
SPICMD_READ_QUAD_IO     = 0xEB    #4x I/O read command
SPICMD_4DTRD            = 0xED    #Quad I/O DT Read
SPICMD_REMS2            = 0xEF    #read ID for 2x I/O mode
    
def spi_flash_detect():
    global quad_check
    global quad_enable
    global quad_disable
    global four_byte_check
    global four_byte_enter
    global four_byte_exit
    global dummy_cycles_config
    
    size = 0
    
    tw8836.write_page(0x04)
    
    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)

    #read id command
    tw8836.write(0xFA, SPICMD_RDID)

    tw8836.write(0xF6, 0x04)    #I2C DMA buffer index page  0x4D0 
    tw8836.write(0xF7, 0xD0)    #I2C DMA buffer index

    #read data length
    tw8836.write(0xF5, 0x00)    #I2C DMA Read/Write data count high byte after command
    tw8836.write(0xF8, 0x00)    #I2C DMA Read/Write data count mid byte after command
    tw8836.write(0xF9, 0x03)    #I2C DMA Read/Write data count low byte after command

    #start DMA write (no BUSY check)
    tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)
    
    #wait while I2C DMA Start command execution bit is cleared
    while (tw8836.read(0xF4) & 0x01):
        if (define.DEBUG == define.ON):
            print 'DMA is busy'

    manufacture_id = tw8836.read(0xD0)
    device_id_1 = tw8836.read(0xD1)
    device_id_2 = tw8836.read(0xD2)

    print 'SPI flash manufacture id is', hex(manufacture_id)
    print 'SPI flash device id 1 is', hex(device_id_1)
    print 'SPI flash device id 2 is', hex(device_id_2)

    if (manufacture_id == 0x1C):
        print 'xxx SPI flash detected'
    elif (manufacture_id == 0xC2):
        quad_check      = macronix.quad_check
        quad_enable     = macronix.quad_enable
        quad_disable    = macronix.quad_disable
        
        four_byte_enter = macronix.four_byte_enter
        four_byte_exit  = macronix.four_byte_exit
        dummy_cycles_config = macronix.dummy_cycles_config
        
        if (device_id_1 == 0x20):
            if (device_id_2 == 0x16):
                size = 4
                print 'MXIC SPI flash [MX25L3233F] detected, size = 32Mbit[4MB]'   
            elif (device_id_2 == 0x17):
                size = 8
                print 'MXIC SPI flash [MX25L6435E] detected, size = 64Mbit[8MB]'                   
            elif (device_id_2 == 0x18):
                size = 16
                print 'MXIC SPI flash [MX25L12835E/F] detected, size = 128Mbit[16MB]'        
            elif (device_id_2 == 0x19):
                size = 32
                
                four_byte_exit()
                security_register1 = security_register_read()
                configuration_register1 = configuration_register_read()
                
                four_byte_enter()
                security_register2 = security_register_read()
                configuration_register2 = configuration_register_read()
                
                if ((security_register1 & 0x04) == 0) and ((security_register2 & 0x04) == 0x04) and (configuration_register1 == configuration_register2):
                    print 'MXIC SPI flash [MX25L25635E] detected, size = 256Mbit[32MB]'
                    four_byte_check = macronix.four_byte_check_35E
                    
                if ((configuration_register1 & 0x20) == 0) and ((configuration_register2 & 0x20) == 0x20) and (security_register1 == security_register2):
                    print 'MXIC SPI flash [MX25L25635F] detected, size = 256Mbit[32MB]'
                    four_byte_check = macronix.four_byte_check_35F                
            elif (device_id_2 == 0x1A):
                size = 64
                print 'MXIC SPI flash [MX66L51235F] detected, size = 512Mbit[64MB]'           
            else:
                print 'MXIC SPI flash detected, but not support yet.'
    elif (manufacture_id == 0xC8):
        quad_check      = gigadevice.quad_check
        quad_enable     = gigadevice.quad_enable
        quad_disable    = gigadevice.quad_disable
        
        four_byte_check = gigadevice.four_byte_check
        four_byte_enter = gigadevice.four_byte_enter
        four_byte_exit  = gigadevice.four_byte_exit
        
        dummy_cycles_config = gigadevice.dummy_cycles_config        
        
        if (device_id_1 == 0x40):
            if (device_id_2 == 0x20):
                size = 64
                print 'GD SPI flash [GD25Q512MC] detected'
            elif (device_id_2 == 0x19):
                size = 32
                print 'GD SPI flash [GD25Q256C] detected'
            elif (device_id_2 == 0x18):
                size = 16
                print 'GD SPI flash [GD25Q128C] detected'
            elif (device_id_2 == 0x17):
                size = 8
                print 'GD SPI flash [GD25Q64C] detected'
            else:
                print 'GD SPI flash detected, but not support yet.'
    elif (manufacture_id == 0xEF):
        if (device_id_1 == 0x40):
            if (device_id_2 == 0x17):
                size = 8
                print 'Winbond SPI flash [25Q64FV] detected'
            elif (device_id_2 == 0x18):
                size = 16
                print 'Winbond SPI flash [25Q128FV] detected'                
            elif (device_id_2 == 0x19):
                size = 32
                print 'Winbond SPI flash [25Q256FV] detected'
            else:
                print 'Winbond SPI flash detected, but not support yet.'
    elif (manufacture_id == 0x9D):
        quad_check      = issi.quad_check
        quad_enable     = issi.quad_enable
        quad_disable    = issi.quad_disable
        
        four_byte_check = issi.four_byte_check        
        four_byte_enter = issi.four_byte_enter
        four_byte_exit  = issi.four_byte_exit
        
        dummy_cycles_config = issi.dummy_cycles_config
        
        if device_id_1 == 0x60:
            if device_id_2 == 0x19:
                size = 32
                print 'ISSI SPI flash [IS25LP256D] detected'
            elif device_id_2 == 0x18:
                size = 16
                print 'ISSI SPI flash [IS25LP128D] detected'
            else:
                print 'GD SPI flash detected, but not support yet.'
        elif device_id_1 == 0x70:
            if device_id_2 == 0x19:
                size = 32
                print 'ISSI SPI flash [IS25WP256D] detected'                
            elif device_id_2 == 0x18:
                size = 16
                print 'ISSI SPI flash [IS25WP128D] detected'
            else:
                print 'ISSI SPI flash detected, but not support yet.'
    else:
        print 'wrong SPI flash ID detected'
    
    if (size > 16):
        print 'SPI flash size is', size
        print 'SPI flash size is bigger than 16MB, should be \033[1;40;32mEN4B\033[0m!'
        
        while (four_byte_check() == define.FALSE):
            four_byte_enter()        
        
    return manufacture_id, device_id_1, device_id_2

def status1_read():
    tw8836.write_page(0x04)

    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)

    #read status 1 command
    tw8836.write(0xFA, SPICMD_RDSR)

    tw8836.write(0xF6, 0x04)   #DMA register buffer1 0x4D0
    tw8836.write(0xF7, 0xD0)   #DMA register buffer1 0x4D0

    #read data length
    tw8836.write(0xF5, 0x0)
    tw8836.write(0xF8, 0x0)
    tw8836.write(0xF9, 0x1)

    #start DMA write (no BUSY check)
    tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)

    status = tw8836.read(0xD0)

    if (define.DEBUG == define.ON):
        print 'status 1 is', hex(status)

    return status

def status2_read():
    tw8836.write_page(0x04)

    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)

    #read status 1 command
    tw8836.write(0xFA, SPICMD_RDSR2)

    tw8836.write(0xF6, 0x04)   #DMA register buffer1 0x4D0
    tw8836.write(0xF7, 0xD0)   #DMA register buffer1 0x4D0

    #read data length
    tw8836.write(0xF5, 0x0)
    tw8836.write(0xF8, 0x0)
    tw8836.write(0xF9, 0x1)

    #start DMA write (no BUSY check)
    tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)

    status = tw8836.read(0xD0)

    if (define.DEBUG == define.ON):
        print 'status 2 is', hex(status)

    return status

def status3_read():
    tw8836.write_page(0x04)

    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)

    #read status 1 command
    tw8836.write(0xFA, SPICMD_RDSR3)

    tw8836.write(0xF6, 0x04)   #DMA register buffer1 0x4D0
    tw8836.write(0xF7, 0xD0)   #DMA register buffer1 0x4D0

    #read data length
    tw8836.write(0xF5, 0x0)
    tw8836.write(0xF8, 0x0)
    tw8836.write(0xF9, 0x1)

    #start DMA write (no BUSY check)
    tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)

    status = tw8836.read(0xD0)

    if (define.DEBUG == define.ON):
        print 'status 3 is', hex(status)

    return status

def security_register_read():
    tw8836.write_page(0x04)

    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)

    #read status 1 command
    tw8836.write(0xFA, SPICMD_RDSCUR)

    tw8836.write(0xF6, 0x04)   #DMA register buffer1 0x4D0
    tw8836.write(0xF7, 0xD0)   #DMA register buffer1 0x4D0

    #read data length
    tw8836.write(0xF5, 0x0)
    tw8836.write(0xF8, 0x0)
    tw8836.write(0xF9, 0x1)

    #start DMA write (no BUSY check)
    tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)

    security_register = tw8836.read(0xD0)

    if (define.DEBUG == define.ON):
        print 'security register is', hex(security_register)

    return security_register

def configuration_register_read():
    tw8836.write_page(0x04)

    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)

    #read status 1 command
    tw8836.write(0xFA, SPICMD_RDCR)

    tw8836.write(0xF6, 0x04)   #DMA register buffer1 0x4D0
    tw8836.write(0xF7, 0xD0)   #DMA register buffer1 0x4D0

    #read data length
    tw8836.write(0xF5, 0x0)
    tw8836.write(0xF8, 0x0)
    tw8836.write(0xF9, 0x1)

    #start DMA write (no BUSY check)
    tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)

    configuration_register = tw8836.read(0xD0)

    if (define.DEBUG == define.ON):
        print 'configuration register is', hex(configuration_register)

    return configuration_register

def configuration_write(configuration):
    status = status1_read()
    
    tw8836.write_page(0x04)

    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_3)

    #write status 1 command
    tw8836.write(0xFA, SPICMD_WRSR)
    tw8836.write(0xFB, status)
    tw8836.write(0xFC, configuration)

    tw8836.write(0xF6, 0x00)   #DMA register buffer1 0x4D0
    tw8836.write(0xF7, 0x00)   #DMA register buffer1 0x4D0

    #write data length
    tw8836.write(0xF5, 0x0)
    tw8836.write(0xF8, 0x0)
    tw8836.write(0xF9, 0x0)

    #start DMA write (BUSY check)
    tw8836.write(0xF4, (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

    while (tw8836.read(0xF4) & 0x01):
        if (define.DEBUG == define.ON):
            print 'wait...'
    
def status1_write(status):
    tw8836.write_page(0x04)

    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_2)

    #write status 1 command
    tw8836.write(0xFA, SPICMD_WRSR)
    tw8836.write(0xFB, status)

    tw8836.write(0xF6, 0x04)   #DMA register buffer1 0x4D0
    tw8836.write(0xF7, 0xD0)   #DMA register buffer1 0x4D0

    #write data length
    tw8836.write(0xF5, 0x0)
    tw8836.write(0xF8, 0x0)
    tw8836.write(0xF9, 0x1)

    #start DMA write (BUSY check)
    tw8836.write(0xF4, (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

    while tw8836.read(0xF4) & 0x01:
        if define.DEBUG == define.ON:
            print 'wait...'

def status2_write(status):
    tw8836.write_page(0x04)

    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_2)

    #write status 1 command
    tw8836.write(0xFA, SPICMD_WRSR2)
    tw8836.write(0xFB, status)

    tw8836.write(0xF6, 0x04)   #DMA register buffer1 0x4D0
    tw8836.write(0xF7, 0xD0)   #DMA register buffer1 0x4D0

    #write data length
    tw8836.write(0xF5, 0x0)
    tw8836.write(0xF8, 0x0)
    tw8836.write(0xF9, 0x1)

    #start DMA write (BUSY check)
    tw8836.write(0xF4, (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

    while (tw8836.read(0xF4) & 0x01):
        if (define.DEBUG == define.ON):
            print 'wait...'

def status3_write(status):
    tw8836.write_page(0x04)

    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_2)

    #write status 1 command
    tw8836.write(0xFA, SPICMD_WRSR3)
    tw8836.write(0xFB, status)

    tw8836.write(0xF6, 0x04)   #DMA register buffer1 0x4D0
    tw8836.write(0xF7, 0xD0)   #DMA register buffer1 0x4D0

    #write data length
    tw8836.write(0xF5, 0x0)
    tw8836.write(0xF8, 0x0)
    tw8836.write(0xF9, 0x1)

    #start DMA write (BUSY check)
    tw8836.write(0xF4, (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

    while (tw8836.read(0xF4) & 0x01):
        if (define.DEBUG == define.ON):
            print 'wait...'

def write_enable():
    tw8836.write_page(0x04)
    
    tmp = tw8836.read(0xF4)

    if tmp & 0x01:
        print 'oops... you need lv_reset!'

    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)
    
    #write enable command
    tw8836.write(0xFA, SPICMD_WREN)

    #write data length    
    tw8836.write(0xF5, 0)
    tw8836.write(0xF8, 0)    
    tw8836.write(0xF9, 0)
    
    tw8836.write(0xF4, SPI_CMD_OPT_NONE | DMA_START)

def write_disable():
    tw8836.write_page(0x04)
    
    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)

    #write disable command
    tw8836.write(0xFA, SPICMD_WRDI)

    #write data length
    tw8836.write(0xF5, 0)
    tw8836.write(0xF8, 0)
    tw8836.write(0xF9, 0)
    
    #start DMA write (no BUSY check)
    tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

def dma_spi_to_xram(spi_addr, xram_addr, size, read_mode):
    if read_mode == tw8836.SPI_READ_SLOW:
        dummy = 0
        spicmd = SPICMD_READ_SLOW
    elif read_mode == tw8836.SPI_READ_FAST:
        dummy = 1
        spicmd = SPICMD_READ_FAST
    elif read_mode == tw8836.SPI_READ_DUAL:
        dummy = 1
        spicmd = SPICMD_READ_DUAL_O
    elif read_mode == tw8836.SPI_READ_QUAD:
        dummy = 1   #TW8836 fixed 8 dummy cycles - 8/8 = 4    
        spicmd = SPICMD_READ_QUAD_O
    elif read_mode == tw8836.SPI_READ_DUAL_IO:
        dummy = 1        
        spicmd = SPICMD_READ_DUAL_IO
    elif read_mode == tw8836.SPI_READ_QUAD_IO:
        dummy = 3   #TW8836 fixed 6 dummy cycles - (6*4)/8 = 3
        spicmd = SPICMD_READ_QUAD_IO
    
    if four_byte_check() == define.TRUE:     #in 4B mode 
        tw8836.write_page(0x04)
    
        tw8836.write(0xC3, (DMA_DEST_MCU_XMEM << 6) | (DMA_ACCESS_MODE_INC << 4) | DMA_CMD_COUNT_5 + dummy)

        tw8836.write(0xCA, spicmd)

        tw8836.write(0xCB, (spi_addr >> 24))
        tw8836.write(0xCC, (spi_addr >> 16))
        tw8836.write(0xCD, (spi_addr >> 8))
        tw8836.write(0xCE, (spi_addr))
    
        tw8836.write(0xC6, (xram_addr >> 8))        # xram address high
        tw8836.write(0xC7, (xram_addr))             # xram address low

        tw8836.write(0xC5, (size >> 16))            # data Buff count high
        tw8836.write(0xC8, (size >> 8))             # data Buff count middle
        tw8836.write(0xC9, (size))                  # data Buff count Low

        #start DMA read (no BUSY check)
        tw8836.write(0xC4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)
        
        while (tw8836.read(0xC4) & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...' 
    else:
        tw8836.write_page(0x04)
    
        tw8836.write(0xC3, (DMA_DEST_MCU_XMEM << 6) | (DMA_ACCESS_MODE_INC << 4) | DMA_CMD_COUNT_4 + dummy)

        tw8836.write(0xCA, spicmd)

        tw8836.write(0xCB, (spi_addr >> 16))
        tw8836.write(0xCC, (spi_addr >> 8))
        tw8836.write(0xCD, (spi_addr))
    
        tw8836.write(0xC6, (xram_addr >> 8))        # xram address high
        tw8836.write(0xC7, (xram_addr))             # xram address low

        tw8836.write(0xC5, (size >> 16))            # data Buff count high
        tw8836.write(0xC8, (size >> 8))             # data Buff count middle
        tw8836.write(0xC9, (size))                  # data Buff count Low

        #start DMA read (no BUSY check)
        tw8836.write(0xC4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)
        
        while (tw8836.read(0xC4) & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'        

def dma_xram_to_spi(xram_addr, spi_addr, size):
    if four_byte_check() == define.TRUE:     #in 4B mode 
        write_enable()

        tw8836.write(0xFF, 0x04)

        tw8836.write(0xF3, (DMA_DEST_MCU_XMEM << 6) | (DMA_ACCESS_MODE_INC << 4) | DMA_CMD_COUNT_5)

        tw8836.write(0xFA, SPICMD_PP)

        tw8836.write(0xFB, (spi_addr >> 24))
        tw8836.write(0xFC, (spi_addr >> 16))
        tw8836.write(0xFD, (spi_addr >> 8))
        tw8836.write(0xFE, (spi_addr))
    
        tw8836.write(0xF6, (xram_addr>>8))          # xram address high
        tw8836.write(0xF7, (xram_addr))             # xram address low

        tw8836.write(0xF5, (size >> 16))            # data Buff count high
        tw8836.write(0xF8, (size >> 8))             # data Buff count middle
        tw8836.write(0xF9, (size))                  # data Buff count Low

        #start DMA write (BUSY check)
        tw8836.write(0xF4, (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

        #  printf("\r\n0xF4 = 0x%x before DMA 0x%x", tw8836.read(0xF4), (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)
        while (tw8836.read(0xF4) & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'

        #  printf("\r\n0xF4 = 0x%x after DMA", tw8836.read(0xF4))

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (define.DEBUG == define.ON):
                print 'wait...'

        #printf("\r\nSPI wirte to addr[0x%x] size[0x%x] finished!", spi_addr, size)
    else:
        write_enable()

        tw8836.write(0xFF, 0x04)

        tw8836.write(0xF3, (DMA_DEST_MCU_XMEM << 6) | (DMA_ACCESS_MODE_INC << 4) | DMA_CMD_COUNT_4)

        tw8836.write(0xFA, SPICMD_PP)

        tw8836.write(0xFB, (spi_addr >> 16))
        tw8836.write(0xFC, (spi_addr >> 8))
        tw8836.write(0xFD, (spi_addr))
    
        tw8836.write(0xF6, (xram_addr>>8))          # xram address high
        tw8836.write(0xF7, (xram_addr))             # xram address low

        tw8836.write(0xF5, (size >> 16))            # data Buff count high
        tw8836.write(0xF8, (size >> 8))             # data Buff count middle
        tw8836.write(0xF9, (size))                  # data Buff count Low

        #start DMA write (BUSY check)
        tw8836.write(0xF4, (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

        #  printf("\r\n0xF4 = 0x%x before DMA 0x%x", tw8836.read(0xF4), (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)
        while (tw8836.read(0xF4) & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'

        #  printf("\r\n0xF4 = 0x%x after DMA", tw8836.read(0xF4))

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (define.DEBUG == define.ON):
                print 'wait...'

        #printf("\r\nSPI wirte to addr[0x%x] size[0x%x] finished!", spi_addr, size)

def xram_write(addr, data, size):
    tw8836.write(0xFF, 0x04)

    #XMEM access by I2C enable
    tw8836.write(0xC2, tw8836.read(0xC2) | 0x01)
    while ((tw8836.read(0xC2) & 0x2) == 0):
        if (define.DEBUG == define.ON):
            print "wait"

    #write XMEM start address
    tw8836.write(0xDB, (addr>>8))
    tw8836.write(0xDC, addr)
    
    #write XMEM data register 0xDD 
    for d in data:
        tw8836.write(0xDD, d)

    #XMEM access by TW8836
    tw8836.write(0xC2, tw8836.read(0xC2) & ~0x01)

def sector_erase(sector_addr):
    if four_byte_check() == define.TRUE:     #in 4B mode 
        write_enable()

        tw8836.write_page(0x04)

        tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_5)

        #write sector erase command
        tw8836.write(0xFA, SPICMD_SE)

        #write block addr
        tw8836.write(0xFB, (sector_addr >> 24))
        tw8836.write(0xFC, (sector_addr >> 16))
        tw8836.write(0xFD, (sector_addr >> 8))
        tw8836.write(0xFE, (sector_addr))    

        #write data length
        tw8836.write(0xF5, 0x0)
        tw8836.write(0xF8, 0x0)
        tw8836.write(0xF9, 0x0)

        #start DMA write (BUSY check)
        tw8836.write(0xF4, (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

        #printf("\r\n0xF4 = 0x%x before DMA", tw8836.read(0xF4))
        while (tw8836.read(0xF4) & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'

        #printf("\r\n0xF4 = 0x%x after DMA", tw8836.read(0xF4))

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (define.DEBUG == define.ON):
                print 'wait...' 
                
        #check write in progress bit is cleared
        while (status1_read() & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'                 

        #printf("\r\nsector addr[0x%x] erase finished!", sector_addr)
    else:
        write_enable()

        tw8836.write_page(0x04)

        tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_4)

        #write sector erase command
        tw8836.write(0xFA, SPICMD_SE)

        #write block addr
        tw8836.write(0xFB, (sector_addr >> 16))
        tw8836.write(0xFC, (sector_addr >> 8))
        tw8836.write(0xFD, (sector_addr))   

        #write data length
        tw8836.write(0xF5, 0x0)
        tw8836.write(0xF8, 0x0)
        tw8836.write(0xF9, 0x0)

        #start DMA write (BUSY check)
        tw8836.write(0xF4, (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

        #printf("\r\n0xF4 = 0x%x before DMA", tw8836.read(0xF4))
        while (tw8836.read(0xF4) & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'

        #printf("\r\n0xF4 = 0x%x after DMA", tw8836.read(0xF4))

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (define.DEBUG == define.ON):
                print 'wait...' 
                
        #check write in progress bit is cleared
        while (status1_read() & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'                 

        #printf("\r\nsector addr[0x%x] erase finished!", sector_addr)

def block_erase(block_addr):
    if four_byte_check() == define.TRUE:     #in 4B mode 
        write_enable()

        tw8836.write_page(0x04)

        tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_5)

        #write block erase command
        tw8836.write(0xFA, SPICMD_BE)

        #write block addr
        tw8836.write(0xFB, (block_addr >> 24))
        tw8836.write(0xFC, (block_addr >> 16))
        tw8836.write(0xFD, (block_addr >> 8))
        tw8836.write(0xFE, (block_addr))    

        #write data length
        tw8836.write(0xF5, 0x0)
        tw8836.write(0xF8, 0x0)
        tw8836.write(0xF9, 0x0)

        #start DMA write (BUSY check)
        tw8836.write(0xF4, (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

        while (tw8836.read(0xF4) & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'  

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (define.DEBUG == define.ON):
                print 'wait...' 

        #check write in progress bit is cleared
        while (status1_read() & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...' 
                
        #printf("\r\nblock addr[0x%x] erase finished!\r\n", block_addr)
    else:
        write_enable()

        tw8836.write_page(0x04)

        tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_4)

        #write block erase command
        tw8836.write(0xFA, SPICMD_BE)

        #write block addr
        tw8836.write(0xFB, (block_addr >> 16))
        tw8836.write(0xFC, (block_addr >> 8))
        tw8836.write(0xFD, (block_addr))    

        #write data length
        tw8836.write(0xF5, 0x0)
        tw8836.write(0xF8, 0x0)
        tw8836.write(0xF9, 0x0)

        #start DMA write (BUSY check)
        tw8836.write(0xF4, (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

        while (tw8836.read(0xF4) & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'  

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (define.DEBUG == define.ON):
                print 'wait...' 
                
        #check write in progress bit is cleared
        while (status1_read() & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'                 
        
        #printf("\r\nblock addr[0x%x] erase finished!\r\n", block_addr)

def chip_erase():        
    write_enable()

    tw8836.write_page(0x04)
    
    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)

    #write chip erase command 0x60 or 0xC7
    tw8836.write(0xFA, SPICMD_CE)

    #write data length
    tw8836.write(0xF5, 0x0)
    tw8836.write(0xF8, 0x0)
    tw8836.write(0xF9, 0x0)

    #start DMA write (BUSY check)
    tw8836.write(0xF4, (DMA_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START)

    while (tw8836.read(0xF4) & 0x01):
        if (define.DEBUG == define.ON):
            print 'wait...'
    
    #check write enable bit is cleared
    while (status1_read() & 0x02):
        if (define.DEBUG == define.ON):
            print 'wait...'
            
    #check write in progress bit is cleared
    while (status1_read() & 0x01):
        if (define.DEBUG == define.ON):
            print 'wait...'             

    print 'chip erase success!'

#size is limited to 2048?
def write(addr, data, size):
    tw8836.mcu_halt()

    xram_write(0x0, data, size)

    dma_xram_to_spi(0x0, addr, size)

#size is limited to 2048?
def read(addr, size, mode):
    data = []
    
    tw8836.spi_read_mode_set(mode)
    dma_spi_to_xram(addr, 0x0, size, mode)

    tw8836.mcu_halt()

    tw8836.write_page(0x04)

    #XMEM access by I2C enable
    tw8836.write(0xC2, tw8836.read(0xC2) | 0x01)
    while ((tw8836.read(0xC2) & 0x2) == 0):
        if (define.DEBUG == define.ON):
            print 'wait...'

    #write XMEM start address
    tw8836.write(0xDB, 0x0)    #xram addr high byte
    tw8836.write(0xDC, 0x0)    #xram addr low byte

    #read XMEM data register 0xDD  
    for i in range(0, size):
        data.append(tw8836.read(0xDD))
        
    #XMEM access by TW8836
    tw8836.write(0xC2, tw8836.read(0xC2) & ~0x01)
    
    return data

#  tw8836_mcu_return()    #eamon 20150522

crc_table = [
    0x0000,  0x1021,  0x2042,  0x3063,  0x4084,  0x50A5,  0x60C6,  0x70E7,
    0x8108,  0x9129,  0xA14A,  0xB16B,  0xC18C,  0xD1AD,  0xE1CE,  0xF1EF,
    0x1231,  0x0210,  0x3273,  0x2252,  0x52B5,  0x4294,  0x72F7,  0x62D6,
    0x9339,  0x8318,  0xB37B,  0xA35A,  0xD3BD,  0xC39C,  0xF3FF,  0xE3DE,
    0x2462,  0x3443,  0x0420,  0x1401,  0x64E6,  0x74C7,  0x44A4,  0x5485,
    0xA56A,  0xB54B,  0x8528,  0x9509,  0xE5EE,  0xF5CF,  0xC5AC,  0xD58D,
    0x3653,  0x2672,  0x1611,  0x0630,  0x76D7,  0x66F6,  0x5695,  0x46B4,
    0xB75B,  0xA77A,  0x9719,  0x8738,  0xF7DF,  0xE7FE,  0xD79D,  0xC7BC,
    0x48C4,  0x58E5,  0x6886,  0x78A7,  0x0840,  0x1861,  0x2802,  0x3823,
    0xC9CC,  0xD9ED,  0xE98E,  0xF9AF,  0x8948,  0x9969,  0xA90A,  0xB92B,
    0x5AF5,  0x4AD4,  0x7AB7,  0x6A96,  0x1A71,  0x0A50,  0x3A33,  0x2A12,
    0xDBFD,  0xCBDC,  0xFBBF,  0xEB9E,  0x9B79,  0x8B58,  0xBB3B,  0xAB1A,
    0x6CA6,  0x7C87,  0x4CE4,  0x5CC5,  0x2C22,  0x3C03,  0x0C60,  0x1C41,
    0xEDAE,  0xFD8F,  0xCDEC,  0xDDCD,  0xAD2A,  0xBD0B,  0x8D68,  0x9D49,
    0x7E97,  0x6EB6,  0x5ED5,  0x4EF4,  0x3E13,  0x2E32,  0x1E51,  0x0E70,
    0xFF9F,  0xEFBE,  0xDFDD,  0xCFFC,  0xBF1B,  0xAF3A,  0x9F59,  0x8F78,
    0x9188,  0x81A9,  0xB1CA,  0xA1EB,  0xD10C,  0xC12D,  0xF14E,  0xE16F,
    0x1080,  0x00A1,  0x30C2,  0x20E3,  0x5004,  0x4025,  0x7046,  0x6067,
    0x83B9,  0x9398,  0xA3FB,  0xB3DA,  0xC33D,  0xD31C,  0xE37F,  0xF35E,
    0x02B1,  0x1290,  0x22F3,  0x32D2,  0x4235,  0x5214,  0x6277,  0x7256,
    0xB5EA,  0xA5CB,  0x95A8,  0x8589,  0xF56E,  0xE54F,  0xD52C,  0xC50D,
    0x34E2,  0x24C3,  0x14A0,  0x0481,  0x7466,  0x6447,  0x5424,  0x4405,
    0xA7DB,  0xB7FA,  0x8799,  0x97B8,  0xE75F,  0xF77E,  0xC71D,  0xD73C,
    0x26D3,  0x36F2,  0x0691,  0x16B0,  0x6657,  0x7676,  0x4615,  0x5634,
    0xD94C,  0xC96D,  0xF90E,  0xE92F,  0x99C8,  0x89E9,  0xB98A,  0xA9AB,
    0x5844,  0x4865,  0x7806,  0x6827,  0x18C0,  0x08E1,  0x3882,  0x28A3,
    0xCB7D,  0xDB5C,  0xEB3F,  0xFB1E,  0x8BF9,  0x9BD8,  0xABBB,  0xBB9A,
    0x4A75,  0x5A54,  0x6A37,  0x7A16,  0x0AF1,  0x1AD0,  0x2AB3,  0x3A92,
    0xFD2E,  0xED0F,  0xDD6C,  0xCD4D,  0xBDAA,  0xAD8B,  0x9DE8,  0x8DC9,
    0x7C26,  0x6C07,  0x5C64,  0x4C45,  0x3CA2,  0x2C83,  0x1CE0,  0x0CC1,
    0xEF1F,  0xFF3E,  0xCF5D,  0xDF7C,  0xAF9B,  0xBFBA,  0x8FD9,  0x9FF8,
    0x6E17,  0x7E36,  0x4E55,  0x5E74,  0x2E93,  0x3EB2,  0x0ED1,  0x1EF0
]

def crc_check(spiaddr, length):
    if four_byte_check() == define.TRUE:     #in 4B mode 
        tw8836.write_page(0x04)
        
        tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | (DMA_ACCESS_MODE_FIX << 4) | DMA_CMD_COUNT_5)
        
        tw8836.write(0xF6, 0x04)    #Reg Buffer
        tw8836.write(0xF7, 0xD0)
        
        tw8836.write(0xF5, (length>>16))
        tw8836.write(0xF8, (length>>8))
        tw8836.write(0xF9, length)
        
        tw8836.write(0xFA, SPICMD_READ_SLOW)
        
        tw8836.write(0xFB, (spiaddr>>24))
        tw8836.write(0xFC, (spiaddr>>16))
        tw8836.write(0xFD, (spiaddr>>8))
        tw8836.write(0xFE, spiaddr)

        tw8836.write(0xF4, SPI_CMD_OPT_NONE | DMA_START)

        crc = tw8836.read(0xEE)
        crc <<= 8;
        crc |= tw8836.read(0xEF)
        print hex(crc)
        """
        if (crc != crc):
            print 'CRC fail.', hex(crc)
            return 2;
        """
        return 0;    
    else:
        tw8836.write_page(0x04)
        
        tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | (DMA_ACCESS_MODE_FIX << 4) | DMA_CMD_COUNT_4)
        
        tw8836.write(0xF6, 0x04)    #Reg Buffer
        tw8836.write(0xF7, 0xD0)
        
        tw8836.write(0xF5, (length>>16))
        tw8836.write(0xF8, (length>>8))
        tw8836.write(0xF9, length)
        
        tw8836.write(0xFA, SPICMD_READ_SLOW)
        
        tw8836.write(0xFB, (spiaddr>>16))
        tw8836.write(0xFC, (spiaddr>>8))
        tw8836.write(0xFD, spiaddr)
        
        tw8836.write(0xF4, SPI_CMD_OPT_NONE | DMA_START)

        crc = tw8836.read(0xEE)
        crc <<= 8;
        crc |= tw8836.read(0xEF)
        print hex(crc)
        """
        if (crc != crc):
            print 'CRC fail.', hex(crc)
            return 2;
        """
        return 0;     
    
def spi_clk_recover_27mhz_source():
    tw8836.write_page(0x04)
    
    #Clock
    temp = tw8836.read(0xE1)
    print 'REG0x4E1 =', hex(temp)
    if (temp & 0x30):
        print' 27MHz'
        tw8836.write(0xE1, temp & ~0x30)

"""        
    #SPI Read Mode
    temp = tw8836.read(0xC0)
    print 'REG0x4C0 =', hex(temp)    
    if (temp & 0x07):
        print' Slow'
        tw8836.write(0xC0, temp & 0xF8)
"""

def init():
    spi_clk_recover_27mhz_source()
    
    spi_flash_detect()
    
    #quad_disable()
    while (quad_check() == define.FALSE):
        quad_enable()
        
    dummy_cycles_config(1, 1)    
    
def program_test():
    data = [1, 2, 3 , 4, 5]
    size = 200

    data = read(0x0, size, tw8836.SPI_READ_QUAD)

    print 'read the data from spi flash at 0x0 before test'
    for d in data:
        print hex(d)
        
    #chip_erase()
    #sector_erase(0x0)
    block_erase(0x0)
    
    time.sleep(1)

    data = read(0x0, size, tw8836.SPI_READ_QUAD)

    print 'read the data from spi flash at 0x0 after erase operation'
    for d in data:
        print hex(d)

    for i in range(0, size):
        data[i] = i+2
        
    write(0x0, data, size)

    data = read(0x0, size, tw8836.SPI_READ_QUAD)

    print 'read back from SPI and verify :'
    for i in range(0, size):
        print hex(data[i])

        if (data[i] != i+2):
            print 'verify error!'
            
            return

    crc_check(0x0, size) 

    print 'spi program ok!'

def spi2lut(spi_addr, lut_addr, lut_size):
    if four_byte_check() == define.TRUE:     #in 4B mode    
        write_enable()

        tw8836.write_page(0x04)

        tw8836.write(0xF3, (DMA_DEST_SOSD_LUT << 6) | (DMA_ACCESS_MODE_INC << 4) | DMA_CMD_COUNT_5)

        #write slow read command
        tw8836.write(0xFA, SPICMD_READ_SLOW)

        #write block addr
        tw8836.write(0xFB, (spi_addr >> 24))
        tw8836.write(0xFC, (spi_addr >> 16))
        tw8836.write(0xFD, (spi_addr >> 8))
        tw8836.write(0xFE, (spi_addr))    

        #write buffer start address
        tw8836.write(0xF6, lut_addr>>8)
        tw8836.write(0xF7, lut_addr&0xFF)
        
        #write data length
        tw8836.write(0xF5, lut_size>>16)
        tw8836.write(0xF8, lut_size>>8)
        tw8836.write(0xF9, lut_size&0xFF)

        #start DMA write (BUSY check)
        tw8836.write(0xF4, (SPI_CMD_OPT_NONE<<2) | (DMA_READ<<1) | DMA_START)
        
        #printf("\r\n0xF4 = 0x%x before DMA", tw8836.read(0xF4))
        while (tw8836.read(0xF4) & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'

        #printf("\r\n0xF4 = 0x%x after DMA", tw8836.read(0xF4))
        
        """
        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (define.DEBUG == define.ON):
                print 'wait...' 
        """
    else:
        write_enable()

        tw8836.write_page(0x04)

        tw8836.write(0xF3, (DMA_DEST_SOSD_LUT << 6) | (DMA_ACCESS_MODE_INC << 4) | DMA_CMD_COUNT_4)

        #write slow read command
        tw8836.write(0xFA, SPICMD_READ_SLOW)

        #write block addr
        tw8836.write(0xFB, (spi_addr >> 16))
        tw8836.write(0xFC, (spi_addr >> 8))
        tw8836.write(0xFD, (spi_addr))   

        #write data length
        tw8836.write(0xF5, 0x0)
        tw8836.write(0xF8, 0x0)
        tw8836.write(0xF9, 0x0)

        #start DMA write (BUSY check)
        tw8836.write(0xF4, (SPI_CMD_OPT_NONE<<2) | (DMA_READ<<1) | DMA_START)

        #printf("\r\n0xF4 = 0x%x before DMA", tw8836.read(0xF4))
        while (tw8836.read(0xF4) & 0x01):
            if (define.DEBUG == define.ON):
                print 'wait...'

        #printf("\r\n0xF4 = 0x%x after DMA", tw8836.read(0xF4))
        
        """
        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (define.DEBUG == define.ON):
                print 'wait...' 

        #printf("\r\nsector addr[0x%x] erase finished!", sector_addr)    
        """