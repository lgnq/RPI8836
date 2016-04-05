#!/usr/bin/env python
#-*- coding: utf-8 -*-

import define
import tw8836

def onoff_control(onoff):
    tw8836.write_page(0x04)
    
    val = tw8836.read(0x00)
    
    if (onoff == define.ON):
        tw8836.write(0x00, val | 0x04)
    else:
        tw8836.write(0x00, val & ~0x04)

    
    
