# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 16:35:26 2022

@author: Adam
"""

from Prescription_Reader import Prescription_Reader
from Prescription_Writer import Prescription_Writer

class AT_ZOS:
    """ 
        'Fine, I'll do it myself'
        
        A python interface to run the workflow 
        
        Zemax (prescription data) -> txt -> AT_ZOS -> txt -> Solidworks
    """
    
    def __init__(self, in_fnames, out_fname):        
        self.readers = []
        for fname in in_fnames:
            self.readers.append(Prescription_Reader(fname)) 
        
        self.writer = Prescription_Writer(out_fname)


if __name__ == "__main__":
    
    in_fnames = [
            "coords_small_c1.txt",
            "coords_small_c2.txt"
        ]
    
    zos = AT_ZOS
    