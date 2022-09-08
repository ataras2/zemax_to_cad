# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 16:33:23 2022

@author: Adam
"""

from Surface import Surface


class Prescription_Writer:
    """
        class that writes Surface objects to .txt
    """
    PRECISION = 6
    def __init__(self, outfile):
        self.outfile = outfile
        
    def write_sw_txt(self, surfs : list[Surface], key_subset = "all", single_config_surfs = []):
        """ 
            write to a .txt in the form
            
            "<surf_idx>_<name>_<[x,y,z,tilt_x,tilt_y,tilt_z]>" = <value>
        """
        
        if isinstance(key_subset, str):
            key_subset = Prescription_Writer.get_key_subset(key_subset)
        
        with open(self.outfile, 'w') as f:
            for surf in surfs:
                if surf.name in single_config_surfs:
                    if surf.config == 1:
                        for key in key_subset:
                            f.write(Prescription_Writer.get_sw_line(surf, key, use_config=False) + '\n')
                else:
                    for key in key_subset:
                        f.write(Prescription_Writer.get_sw_line(surf, key) + '\n')

    def get_sw_line(s : Surface, key : str, use_surf_idx : bool = False, use_config = True) -> str:
        """
            return the string corresponding to a single line of the solidworks text file,
            of the form

            "global_variable_name" = value

            inputs
                s : surface object to be written
                key : key of the surface object to use e.g. 'x' or 'tilt_x'
                use_surf_idx : if the string should use the surface index of the object
                use_config : if the string should use the config number
        """
        surf = s.to_dict()
        
        assert (s.name is not None) or use_surf_idx
        
        line = '"'
        
        if use_surf_idx:
            line += f'{surf["surf_idx"]}_'
            
        if s.name is not None:
            line += f'{surf["name"]}_{key}'
        else:
            line += f'{key}'
            
        if s.config is not None and use_config:
            line += f'_{surf["config"]}'
            
        line += f'" = {surf[key]:.{Prescription_Writer.PRECISION}f}'
        
        return line


    def get_key_subset(subset_name):
        subset_name = subset_name.lower()
        if subset_name == "all":
            l = ["x","y","z","tilt_x","tilt_y","tilt_z"]
        elif subset_name == "pos" or subset_name == "position":
            l = ["x","y","z"]
        elif subset_name == "ang" or subset_name == "angles":
            l = ["tilt_x","tilt_y","tilt_z"]
        elif subset_name == "xzang" or subset_name == "xzangle":
            l = ["x","z","tilt_y"]
        else:
            raise ValueError(f"{subset_name} is not a valid key subset")
        
        return l
            


if __name__ == "__main__":
    import numpy as np
    
    
    def test_write_sw_txt():
        fname = 'outputs/test_write_sw.txt'
        
        pw = Prescription_Writer(fname)
        
        surfs = [
              Surface(0, np.array([0.1,0.,-0.4]), np.array([0.,45.,0.]), name='text', config=1),
              Surface(0, np.array([1.1,0.,-0.4]), np.array([0.,45.,0.]), name='text', config=2),
              Surface(0, np.array([0.1,0.,5.]), np.array([0.,45.,0.]), name='test2', config=1),
              Surface(0, np.array([1.1,0.,5.]), np.array([0.,45.,0.]), name='test2', config=2)
            ]
        pw.write_sw_txt(surfs)
        
        
        fname = 'outputs/test_write_sw_pos_only.txt'
        pw = Prescription_Writer(fname)
        pw.write_sw_txt(surfs, key_subset="pos")
        
        fname = 'outputs/test_write_sw_xzAng_only.txt'
        pw = Prescription_Writer(fname)
        pw.write_sw_txt(surfs, key_subset="xzAng",single_config_surfs=['text'])
        
        
    test_write_sw_txt()
    
    
    
    
    
    