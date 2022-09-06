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

    def get_sw_line(s : Surface, key : str, use_idx : bool = True):
        surf = s.to_dict()
        
        assert (s.name is not None) or use_idx
        
        line = '"'
        
        if use_idx:
            line += f'{surf["surf_idx"]}_'
        
        if s.name is not None:
            line += f'{surf["name"]}_{key}" = {surf[key]:.{Prescription_Writer.PRECISION}f}'
        else:
            line += f'{key}" = {surf[key]:.{Prescription_Writer.PRECISION}f}'
        return line



if __name__ == "__main__":
    import numpy as np
    def test_get_sw_line():
        # test default behaviour
        s = Surface(0, np.array([0.1,0.,-0.4]), np.array([0.,45.,0.]), name=None)
        
        assert Prescription_Writer.get_sw_line(s,"x") == '"0_x" = 0.100000'
        assert Prescription_Writer.get_sw_line(s,"y") == '"0_y" = 0.000000'
        assert Prescription_Writer.get_sw_line(s,"z") == '"0_z" = -0.400000'
        assert Prescription_Writer.get_sw_line(s,"tilt_x") == '"0_tilt_x" = 0.000000'
        assert Prescription_Writer.get_sw_line(s,"tilt_y") == '"0_tilt_y" = 45.000000'
        assert Prescription_Writer.get_sw_line(s,"tilt_z") == '"0_tilt_z" = 0.000000'
        
        # test with a name
        s = Surface(0, np.array([0.1,0.,-0.4]), np.array([0.,45.,0.]), name='text')
        
        assert Prescription_Writer.get_sw_line(s,"x") == '"0_text_x" = 0.100000'
        assert Prescription_Writer.get_sw_line(s,"y") == '"0_text_y" = 0.000000'
        assert Prescription_Writer.get_sw_line(s,"z") == '"0_text_z" = -0.400000'
        assert Prescription_Writer.get_sw_line(s,"tilt_x") == '"0_text_tilt_x" = 0.000000'
        assert Prescription_Writer.get_sw_line(s,"tilt_y") == '"0_text_tilt_y" = 45.000000'
        assert Prescription_Writer.get_sw_line(s,"tilt_z") == '"0_text_tilt_z" = 0.000000'
        
        # test without using the surf indx
        s = Surface(0, np.array([0.1,0.,-0.4]), np.array([0.,45.,0.]), name='text')
        
        assert Prescription_Writer.get_sw_line(s,"x", False) == '"text_x" = 0.100000'
        assert Prescription_Writer.get_sw_line(s,"y", False) == '"text_y" = 0.000000'
        assert Prescription_Writer.get_sw_line(s,"z", False) == '"text_z" = -0.400000'
        assert Prescription_Writer.get_sw_line(s,"tilt_x", False) == '"text_tilt_x" = 0.000000'
        assert Prescription_Writer.get_sw_line(s,"tilt_y", False) == '"text_tilt_y" = 45.000000'
        assert Prescription_Writer.get_sw_line(s,"tilt_z", False) == '"text_tilt_z" = 0.000000'
    
    test_get_sw_line()
    
    
    
    
    
    