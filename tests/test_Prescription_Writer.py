import unittest

from Surface import Surface
from Prescription_Writer import Prescription_Writer
import numpy as np

class Test_get_sw_line(unittest.TestCase):
    def test_default(self):
        # test default behaviour
        s = Surface(0, np.array([0.1,0.,-0.4]), np.array([0.,45.,0.]), name=None)
        
        self.assertEqual(Prescription_Writer.get_sw_line(s,"x", True), '"0_x" = 0.100000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"y", True), '"0_y" = 0.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"z", True), '"0_z" = -0.400000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_x", True), '"0_tilt_x" = 0.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_y", True), '"0_tilt_y" = 45.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_z", True), '"0_tilt_z" = 0.000000')
        
    def test_with_name(self):
        # test with a name
        s = Surface(0, np.array([0.1,0.,-0.4]), np.array([0.,45.,0.]), name='text')
        
        self.assertEqual(Prescription_Writer.get_sw_line(s,"x", True), '"0_text_x" = 0.100000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"y", True), '"0_text_y" = 0.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"z", True), '"0_text_z" = -0.400000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_x", True), '"0_text_tilt_x" = 0.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_y", True), '"0_text_tilt_y" = 45.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_z", True), '"0_text_tilt_z" = 0.000000')
        
    def test_without_surf_idx(self):
        # test without using the surf indx
        s = Surface(0, np.array([0.1,0.,-0.4]), np.array([0.,45.,0.]), name='text')
        
        self.assertEqual(Prescription_Writer.get_sw_line(s,"x", False), '"text_x" = 0.100000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"y", False), '"text_y" = 0.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"z", False), '"text_z" = -0.400000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_x", False), '"text_tilt_x" = 0.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_y", False), '"text_tilt_y" = 45.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_z", False), '"text_tilt_z" = 0.000000')
        
        
    def test_with_config(self):
        # test using config number
        s = Surface(0, np.array([0.1,0.,-0.4]), np.array([0.,45.,0.]), config=2, name='text')
        
        self.assertEqual(Prescription_Writer.get_sw_line(s,"x", False), '"text_x_2" = 0.100000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"y", False), '"text_y_2" = 0.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"z", False), '"text_z_2" = -0.400000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_x", False), '"text_tilt_x_2" = 0.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_y", False), '"text_tilt_y_2" = 45.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_z", False), '"text_tilt_z_2" = 0.000000')
        
    def test_ignoring_config(self):
        # test using config number
        s = Surface(0, np.array([0.1,0.,-0.4]), np.array([0.,45.,0.]), config=2, name='text')
        
        self.assertEqual(Prescription_Writer.get_sw_line(s,"x", False, use_config=False), '"text_x" = 0.100000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"z", False, use_config=False), '"text_z" = -0.400000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"y", False, use_config=False), '"text_y" = 0.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_x", False, use_config=False), '"text_tilt_x" = 0.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_y", False, use_config=False), '"text_tilt_y" = 45.000000')
        self.assertEqual(Prescription_Writer.get_sw_line(s,"tilt_z", False, use_config=False), '"text_tilt_z" = 0.000000')


if __name__ == '__main__':
    unittest.main()