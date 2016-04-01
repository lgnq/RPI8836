#!/usr/bin/env python

import define
import tw8836

def fontosd_onoff(onoff):
    tw8836.write_page(0x03)
    
    val = tw8836.read(0x0C)
    
    if (onoff == define.ON):
        if (val & 0x40):
            tw8836.write(0x0C, val & ~0x40)
            return 1
    else:
        if ((val & 0x40) == 0):
            tw8836.write(0x0C, val | 0x40)
            return 1
            
    return 0
    
    
