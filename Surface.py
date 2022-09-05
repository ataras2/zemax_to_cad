# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 16:32:03 2022

@author: Adam
"""

import numpy as np
import scipy.spatial.transform

class Surface:
    def __init__(self, surf_idx, coords, tilts, name):
        self.surf_idx = surf_idx
        self.coords = coords
        self.tilts = tilts
        self.name = name
        
    def apply_transform(self, R=np.eye(3), T=np.zeros(3)):
        self.coords = R@self.coords + T
        
        # convert tilt to rotm and then back
        R_tilts = scipy.spatial.transform.Rotation.from_rotvec(
                        np.deg2rad(self.tilts)).as_matrix()
        overall_rotvec = scipy.spatial.transform.Rotation.from_matrix(
                        R@R_tilts).as_rotvec()
        self.tilts = np.rad2deg(overall_rotvec)
    
    def __str__(self):
        if self.name is not None:
            s = f'Surf {self.surf_idx} ({self.name}): coords {self.coords}, tilts: {self.tilts}'
        else:
            s = f'Surf {self.surf_idx}: coords {self.coords}, tilts: {self.tilts}'    
        return s
    

    def isRotationMatrix(M):
        tag = False
        I = np.identity(M.shape[0])
        if np.all((np.matmul(M, M.T)) == I) and (np.linalg.det(M)==1): tag = True
        return tag    