# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 16:33:23 2022

@author: Adam
"""

from Surface import Surface


class Prescription_Writer:
    PRECISION = 6
    def __init__(self, outfile):
        self.outfile = outfile
        
    def write_sw_txt(self, list_of_surfs):
        """ 
            write to a .txt in the form
            
            "<surf_idx>_<name>_<[x,y,z]>" = 
        """
        
        pass

    def get_sw_line(surf : dict, key : str):
        return f'"{surf["surf_idx"]}_{key}" = {surf[key]:.{Prescription_Writer.PRECISION}f}'



if __name__ == "__main__":
    import numpy as np
    def test_get_sw_line():
        s = Surface(0, np.array([0.1,0.,0.]), np.array([0.,45.,0.]), name=None)
        
        assert Prescription_Writer.get_sw_line(s.to_dict(),"x") == '"0_x" = 0.100000'
        assert Prescription_Writer.get_sw_line(s.to_dict(),"y") == '"0_y" = 0.000000'
        assert Prescription_Writer.get_sw_line(s.to_dict(),"tilt_x") == '"0_tilt_x" = 0.000000'
    
    test_get_sw_line()
    
    
    
    
    
    