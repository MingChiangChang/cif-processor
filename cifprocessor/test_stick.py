''' unit tests '''
import unittest

class test(unittest.Testcase):
    
    def __init__(self):

        self.phase_dict={'Qs': [10, 20, 30], 
                         'IS': [1, 0.4, 0.6]}
        self.Q_range = (8, 45)
        self.arr_size = 1024
        self.peak_width = 20


