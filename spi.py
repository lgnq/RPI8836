#!/usr/bin/env python

import tw8836

ON = 1
OFF = 0

DEBUG = OFF

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

SPI_CMD_OPT_NONE		 = 0x00
SPI_CMD_OPT_BUSY		 = 0x04
SPI_CMD_OPT_WRITE		 = 0x02
SPI_CMD_OPT_WRITE_BUSY	 = 0x06
SPI_CMD_OPT_WRITE_BUSY_AUTO	 = 0x16

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

def read_id():
    tw8836.write_page(0x04)
    
    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)

    #read id command
    tw8836.write(0xFA, SPICMD_RDID)

    tw8836.write(0xF6, 0x04)
    tw8836.write(0xF7, 0xD0)

    #read data length
    tw8836.write(0xF5, 0x00)
    tw8836.write(0xF8, 0x00)
    tw8836.write(0xF9, 0x03)

    #start DMA write (no BUSY check)
    tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)

    manufacture_id = tw8836.read(0xD0)
    device_id_1 = tw8836.read(0xD1)
    device_id_2 = tw8836.read(0xD2)

    print 'manufacture id is', hex(manufacture_id)
    print 'device id 1 is', hex(device_id_1)
    print 'device id 2 is', hex(device_id_2)

    if (manufacture_id == 0x1C):
        print 'xxx SPI flash detected'
    elif (manufacture_id == 0xC2):
        print 'MXIC SPI flash detected'
    elif (manufacture_id == 0xC8):
        if (device_id_1 == 0x40):
            if (device_id_2 == 0x20):
                print 'GD SPI flash [GD25Q512MC] detected'
            elif (device_id_2 == 0x19):
                print 'GD SPI flash [GD25Q256C] detected'
            elif (device_id_2 == 0x18):
                print 'GD SPI flash [GD25Q128C] detected'
            elif (device_id_2 == 0x17):
                print 'GD SPI flash [GD25Q64C] detected'
            else:
                print 'wrong GD SPI flash detected'
    else:
        print 'wrong SPI flash ID detected'               

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

    if (DEBUG == ON):
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

    if (DEBUG == ON):
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

    if (DEBUG == ON):
        print 'status 3 is', hex(status)

    return status

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

    while (tw8836.read(0xF4) & 0x01):
        if (DEBUG == ON):
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
        if (DEBUG == ON):
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
        if (DEBUG == ON):
            print 'wait...'

def write_enable():
	tw8836.write_page(0x04)
	
	tmp = tw8836.read(0xF4)
	print 'REG0x4F4 is', hex(tmp)
	if (tmp & 0x01):
		print 'oops... you need lv_reset!'
	
	tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)
	tw8836.write(0xF5, 0)
	tw8836.write(0xF8, 0)	
	tw8836.write(0xF9, 0)
	
	tw8836.write(0xFA, SPICMD_WREN)
	tw8836.write(0xF4, 0x01 | SPI_CMD_OPT_NONE)

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

def enter_4b_mode():
    tw8836.write_page(0x04)
    
    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) + DMA_CMD_COUNT_1)	
    
    tw8836.write(0xF5, 0)	#length high
    tw8836.write(0xF8, 0)	#length middle
    tw8836.write(0xF9, 0)	#length low
    
    tw8836.write(0xFA, SPICMD_EN4B)
    tw8836.write(0xF4, 0x01 | SPI_CMD_OPT_NONE)

def exit_4b_mode():
    tw8836.write_page(0x04)
    
    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) + DMA_CMD_COUNT_1)
    
    tw8836.write(0xF5, 0)	#length high
    tw8836.write(0xF8, 0)	#length middle
    tw8836.write(0xF9, 0)	#length low
    
    tw8836.write(0xFA, SPICMD_EX4B)
    tw8836.write(0xF4, 0x01 | SPI_CMD_OPT_NONE)
	
def quad_enable():
    id = read_id()

    if (id[0] == 0x1C):     #EON
        print 'EON'
    elif (id[0] == 0xC2):   #MXIC
        status = status1_read()
        if (status & 0x40):
            print 'SPI flash is already in QUAD mode'
        else:
            write_enable()
            status1_write(status | 0x40)
            write_disable()
            print 'SPI flash is in QUAD mode'
            
        if (id[1] == 0x20):
            if (id[2] == 0x19):
                enter_4b_mode()
                
                status = status2_read()
                if (status & 0x20):
                    print 'SPI flash is in 4 Byte mode'
                else:
                    print 'SPI flash is not in 4 Byte mode'
    elif (id[0] == 0xC8):   #GD
        if (id[1] == 0x40):
            if (id[2] == 0x20):     #GD25Q512MC
                status = status1_read()

                if (status & 0x40):
                    print 'SPI flash is already in QUAD mode'
                else:
                    write_enable()
                    status1_write(status | 0x40)
                    write_disable()
                    print 'SPI flash is in QUAD mode'
                    
                enter_4b_mode()
                
                status = status2_read()
                if (status & 0x20):
                	print 'SPI flash is in 4 Byte mode'
                else:
                    print 'SPI flash is not in 4 Byte mode'
            elif (id[2] == 0x19):   #GD25Q256C            
                status = status1_read()

                if (status & 0x40):
                    print 'SPI flash is already in QUAD mode'
                    return
                else:
                    write_enable()
                    status1_write(status | 0x40)
                    write_disable()
                    print 'SPI flash is in QUAD mode'
            elif (id[2] == 0x18):
                print 'todo'
            elif (id[2] == 0x17):
                print 'todo'        
            elif (id[2] == 0x16):
                print 'todo'
            else:
                print 'todo'
    else:
        print 'todo'            

def dma_spi_to_xram(spi_addr, xram_addr, size):
    status = status2_read()

    if (status & 0x20):		#in 4B mode
        tw8836.write_page(0x04)
    
        tw8836.write(0xF3, (DMA_DEST_MCU_XMEM << 6) | (DMA_ACCESS_MODE_INC << 4) | DMA_CMD_COUNT_5)

        tw8836.write(0xFA, SPICMD_READ_SLOW)

        tw8836.write(0xFB, (spi_addr >> 24))
        tw8836.write(0xFC, (spi_addr >> 16))
        tw8836.write(0xFD, (spi_addr >> 8))
        tw8836.write(0xFE, (spi_addr))
    
        tw8836.write(0xF6, (xram_addr >> 8))        # xram address high
        tw8836.write(0xF7, (xram_addr))             # xram address low

        tw8836.write(0xF5, (size >> 16))            # data Buff count high
        tw8836.write(0xF8, (size >> 8))             # data Buff count middle
        tw8836.write(0xF9, (size))                  # data Buff count Low

        #start DMA read (no BUSY check)
        tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)
    else:
        tw8836.write_page(0x04)
    
        tw8836.write(0xF3, (DMA_DEST_MCU_XMEM << 6) | (DMA_ACCESS_MODE_INC << 4) | DMA_CMD_COUNT_4)

        tw8836.write(0xFA, SPICMD_READ_SLOW)

        tw8836.write(0xFB, (spi_addr >> 16))
        tw8836.write(0xFC, (spi_addr >> 8))
        tw8836.write(0xFD, (spi_addr))
    
        tw8836.write(0xF6, (xram_addr >> 8))        # xram address high
        tw8836.write(0xF7, (xram_addr))             # xram address low

        tw8836.write(0xF5, (size >> 16))            # data Buff count high
        tw8836.write(0xF8, (size >> 8))             # data Buff count middle
        tw8836.write(0xF9, (size))                  # data Buff count Low

        #start DMA read (no BUSY check)
        tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_READ<<1) | DMA_START)

def dma_xram_to_spi(xram_addr, spi_addr, size):
    status = status2_read()

    if (status & 0x20):     #in 4B mode
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
            if (DEBUG == ON):
                print 'wait...'

        #  printf("\r\n0xF4 = 0x%x after DMA", tw8836.read(0xF4))

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (DEBUG == ON):
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
            if (DEBUG == ON):
                print 'wait...'

        #  printf("\r\n0xF4 = 0x%x after DMA", tw8836.read(0xF4))

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (DEBUG == ON):
                print 'wait...'

        #printf("\r\nSPI wirte to addr[0x%x] size[0x%x] finished!", spi_addr, size)

def xram_write(addr, data, size):
    tw8836.write(0xFF, 0x04)

    #XMEM access by I2C enable
    tw8836.write(0xC2, tw8836.read(0xC2) | 0x01)
    while ((tw8836.read(0xC2) & 0x2) == 0):
        if (DEBUG == ON):
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
    status = status2_read()

    if (status & 0x20):     #in 4B mode    
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
            if (DEBUG == ON):
                print 'wait...'

        #printf("\r\n0xF4 = 0x%x after DMA", tw8836.read(0xF4))

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (DEBUG == ON):
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
            if (DEBUG == ON):
                print 'wait...'

        #printf("\r\n0xF4 = 0x%x after DMA", tw8836.read(0xF4))

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (DEBUG == ON):
                print 'wait...' 

        #printf("\r\nsector addr[0x%x] erase finished!", sector_addr)

def block_erase(block_addr):
    status = status2_read()

    if (status & 0x20):     #in 4B mode      
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
            if (DEBUG == ON):
                print 'wait...'  

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (DEBUG == ON):
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
            if (DEBUG == ON):
                print 'wait...'  

        #check write enable bit is cleared
        while (status1_read() & 0x02):
            if (DEBUG == ON):
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
        if (DEBUG == ON):
            print 'wait...'
    
    #check write enable bit is cleared
    while (status1_read() & 0x02):
        if (DEBUG == ON):
            print 'wait...'

    print 'chip erase success!'

#size is limited to 2048?
def write(addr, data, size):
    tw8836.mcu_halt()

    xram_write(0x0, data, size)

    dma_xram_to_spi(0x0, addr, size)

#size is limited to 2048?
def read(addr, data, size):
    dma_spi_to_xram(addr, 0x0, size)

    tw8836.mcu_halt()

    tw8836.write_page(0x04)

    #XMEM access by I2C enable
    tw8836.write(0xC2, tw8836.read(0xC2) | 0x01)
    while ((tw8836.read(0xC2) & 0x2) == 0):
        if (DEBUG == ON):
            print 'wait...'

    #write XMEM start address
    tw8836.write(0xDB, 0x0)    #xram addr high byte
    tw8836.write(0xDC, 0x0)    #xram addr low byte

    #read XMEM data register 0xDD  
    for d in data:
        d = tw8836.read(0xDD)
    
    #XMEM access by TW8836
    tw8836.write(0xC2, tw8836.read(0xC2) & ~0x01)

#  tw8836_mcu_return()    #eamon 20150522

def program_test():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    #chip_erase()
    #sector_erase(0x0)
    block_erase(0x0)

    read(0x0, data, 10)

    for d in data:
        print hex(d)

    for i in range(0, 10):
        data[i] = i+2
        
    write(0x0, data, 10)

    read(0x0, data, 10)

    print 'read back from SPI and verify :'
    for i in range(0, 10):
        print hex(data[i])

        if (data[i] != i+2):
            print 'verify error!'
            
            return

    #spi_crc_check(0x0, 20) 

    print 'spi program ok!'
