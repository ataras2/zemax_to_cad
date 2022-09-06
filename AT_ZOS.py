# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 16:35:26 2022

@author: Adam
"""

from Prescription_Reader import Prescription_Reader
from Prescription_Writer import Prescription_Writer

import numpy as np

class AT_ZOS:
    """ 
        'Fine, I'll do it myself'
        
        A python interface to run the workflow 
        
        Zemax (prescription data) -> txt -> AT_ZOS -> txt -> Solidworks
    """
    
    def __init__(self, in_fnames, out_fname):        
        self.readers = []
        for i in range(len(in_fnames)):
            self.readers.append(Prescription_Reader(in_fnames[i], config=i+1)) 
        
        self.writer = Prescription_Writer(out_fname)

        all_surfs = []
        for reader in self.readers:
            for surf in reader.objs:
                all_surfs.append(surf)

        # sort by surface index
        all_surfs.sort(key = lambda x: x.surf_idx)
        self.all_surfs = all_surfs

    def transform_surfs(self, R=np.eye(3), T=np.zeros(3)):
        for surf in self.all_surfs:
            surf.apply_transform(R,T)

    def write_out(self, surfs = None, subset="all"):
        
        self.writer.write_sw_txt(self.all_surfs, key_subset=subset)

if __name__ == "__main__":
    
    in_fnames = [
            "data/coords_small_c1.txt",
            "data/coords_small_c2.txt"
        ]
    
    out_fname = "outputs/coords_small_sw.txt"
    
    zos = AT_ZOS(in_fnames, out_fname)
    
    T = np.array([0,0,0])
    zos.transform_surfs(T=T)
    zos.write_out("xzAng")
    