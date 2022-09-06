# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 15:35:05 2022

@author: Adam
"""


import numpy as np
from enum import Enum

from Surface import Surface

class Prescription_Reader:
    """
        A class that reads from a .txt that has been copy pasted from Zemax
        prescription data and converts it to a txt that is readable by solidworks
        
        Optional functionality includes doing coordinate changes (rotations, translations)
        on the data before writing
    """
    def __init__(self, fname, config=None):
        self.fname = fname
        self.config = config
        self.read_file()
        

    def read_file(self):
        with open(self.fname) as f:
            f_contents = f.readlines()
            
        # trim off top
        N_HEADER_ROWS = 8
        array_contents = f_contents[N_HEADER_ROWS:]

        self.objs = []
        row = 0
        while row < len(array_contents):
            self.objs.append(self._generate_object(array_contents[row:row+3]))
            row +=  4 # each object is four rows, 3 of data and one blank

    def _generate_object(self, rows):
        """ from three rows make an object """
        first_row = rows[0].split()
        
        coords = np.zeros(3,)
        tilts = np.zeros(3,)
        
        surf_idx = first_row[self.col.SURF.value]
        coords[0] = first_row[self.col.POS.value]
        tilts[0] = first_row[self.col.TILT.value]
        
        
        if len(first_row) == self.col.NAME.value:
            name = None
        elif len(first_row) > self.col.NAME.value:
            name = " ".join(first_row[self.col.NAME.value:])
        else:
            raise ValueError(f'{first_row}')
            
        # now read other rows
        for i in range(1,3):
            row_split = rows[i].split()
            row_split.insert(0, "") # sneak in extra to account for lack of surf_idx
            
            coords[i] = row_split[self.col.POS.value]
            tilts[i] = row_split[self.col.TILT.value]
        
        return Surface(surf_idx, coords, tilts, config=self.config, name=name)
    
    class col(Enum):
        SURF = 0
        Rx1 = 1
        Rx2 = 2
        Rx3 = 3
        POS = 4
        TILT = 5
        NAME = 6




    


if __name__ == "__main__":
# =============================================================================
#     pr = Prescription_Reader("coords_small.txt")
# =============================================================================
    pr = Prescription_Reader("data/coords.txt")
    
    
# =============================================================================
#     R = np.array([[1, 0, 0],
#                   [0, 1, 0],
#                   [0, 0, 1]])
# =============================================================================
    
    R = np.array([[0, 0, 1],
                  [0, 1, 0],
                  [-1, 0, 0]])
    
    for item in pr.objs:
        print(item)
        item.apply_transform(R=R)
        print(item)
    
    