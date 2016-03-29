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

DMA_DEST_CHIPREG = 1

DMA_CMD_COUNT_1 = 1
DMA_CMD_COUNT_2 = 2
DMA_CMD_COUNT_3 = 3

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

def status_read():
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
        print 'status is', hex(status)

    return status            

def status_write(status):
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
	tw8836.write(0xF4, 0x01 | SPI_CMD_OPT_NONE);

def write_disable():
    tw8836.write_page(0x04)
    
    tw8836.write(0xF3, (DMA_DEST_CHIPREG << 6) | DMA_CMD_COUNT_1)

    #write disable command
    tw8836.write(0xFA, SPICMD_WRDI);

    #write data length
    tw8836.write(0xF5, 0)
    tw8836.write(0xF8, 0)   
    tw8836.write(0xF9, 0)
    
    #start DMA write (no BUSY check)
    tw8836.write(0xF4, (DMA_NO_BUSY_CHECK<<2) | (DMA_WRITE<<1) | DMA_START);

def quad_enable():
    id = read_id()

    if (id[0] == 0x1C):     #EON
        print 'EON'
    elif (id[0] == 0xC2):   #MXIC
        status = status_read()
        if (status & 0x40):
            print 'SPI flash is already in QUAD mode'
            return
        else:
            write_enable()
            status_write(status | 0x40)
            write_disable()
            print 'SPI flash is in QUAD mode'
    elif (id[0] == 0xC8):   #GD
        if (id[1] == 0x40):
            if (id[2] == 0x20):     #GD25Q512MC
                status = status_read()

                if (status & 0x40):
                    print 'SPI flash is already in QUAD mode'
                    return
                else:
                    write_enable()
                    status_write(status | 0x40)
                    write_disable()
                    print 'SPI flash is in QUAD mode'
            elif (id[2] == 0x19):   #GD25Q256C            
                status = status_read()

                if (status & 0x40):
                    print 'SPI flash is already in QUAD mode'
                    return
                else:
                    write_enable()
                    status_write(status | 0x40)
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

def sector_erase():
	write_enable()	

def block_erase():
	write_enable()

def chip_erase():		
	write_enable()
