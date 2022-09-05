# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 16:32:03 2022

@author: Adam
"""

import numpy as np

class Surface:
    def __init__(self, surf_idx, coords, tilts, name):
        self.surf_idx = surf_idx
        self.coords = coords
        self.tilts = tilts
        self.name = name
        
    def apply_transform(self, R=np.eye(3), T=np.zeros(3)):
        self.coords = R@self.coords + T
        
        raise ValueError('not implemented fully (needs tilt correction too)')
    
    
    def __str__(self):
        if self.name is not None:
            s = f'Surf {self.surf_idx} ({self.name}): coords {self.coords}, tilts: {self.tilts}'
        else:
            s = f'Surf {self.surf_idx}: coords {self.coords}, tilts: {self.tilts}'    
        return s