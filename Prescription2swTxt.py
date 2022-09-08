# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 16:35:26 2022

@author: Adam
"""

from Prescription_Reader import Prescription_Reader
from Prescription_Writer import Prescription_Writer

import numpy as np

class Prescription2swTxt:
    """ 
        'Fine, I'll do it myself'
        
        A python interface to run the workflow 
        
        Zemax (prescription data) -> txt -> AT_ZOS -> txt -> Solidworks
    """
    
    def __init__(self, in_fnames, out_fname, **kwargs):        
        self.readers = []
        for i in range(len(in_fnames)):
            self.readers.append(Prescription_Reader(in_fnames[i], config=i+1)) 
        
        self.writer = Prescription_Writer(out_fname)

        self.all_surfs = self.filter_surfs(**kwargs)

    def filter_surfs(self, filter_names = None):
        all_surfs = []
        for reader in self.readers:
            for surf in reader.objs:
                if filter_names is None:
                    all_surfs.append(surf)
                elif surf.name is not None:
                    if surf.name in filter_names:
                        all_surfs.append(surf)

        # sort by surface index
        all_surfs.sort(key = lambda x: x.surf_idx)
        return all_surfs

    def transform_surfs(self, R=np.eye(3), T=np.zeros(3)):
        for surf in self.all_surfs:
            surf.apply_transform(R,T)

    def write_out(self, **kwargs):
        self.writer.write_sw_txt(self.all_surfs, **kwargs)

if __name__ == "__main__":
    
    in_fnames = [
            "data/hdllr_c1.txt",
            "data/hdllr_c2.txt",
            "data/hdllr_c3.txt",
            "data/hdllr_c4.txt"
        ]
    
    out_fname = "outputs/coords_hdllr_sw.txt"
    
# =============================================================================
#     surfs_of_interest = ["OAP 1", 
#                          "DM", 
#                          "OAP 2", 
#                          "Dichroic to Hi-5", 
#                          "Focusing mirror", 
#                          "Tip-tilt mirror",
#                          "Knife-edge mirror",
#                          "Fold mirror",
#                          "LB5552-E"
#                          ]
# =============================================================================
    
    
    surfs_of_interest = ["OAP 1", 
                         "DM"
                         ]
    
    zos = Prescription2swTxt(in_fnames, out_fname, filter_names=surfs_of_interest)
    
    T = np.array([-510,200,150])
    
    R = np.array([[0, 0, 1],
                  [0, 1, 0],
                  [-1, 0, 0]])
    
    zos.transform_surfs(T=T, R=R)
    zos.write_out(subset="xzAng")
    