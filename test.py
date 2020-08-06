import unittest

from unittest import TestCase
from utils import delta_to_matrix

class DeltaToVectorCase(TestCase):

    def test_real_examples(self):
        '''
        1. hello -> hello!
        2. hello -> hell
        3. hello -> hey apollo
        4. hello -> he -> the
        '''
        deltas = [
            [
                {'retain': 5, 'insert': '!'}
            ],
            [
                {'retain': 4, 'delete': 1}
            ],
            [
                {'retain': 2, 'insert': 'y apo'}
            ],
            [
                {'retain': 2, 'delete': 3},
                {'insert': '1', 'retain': 2}
            ],
            [
                {'retain': 2, 'insert': '!!?'},
                {'delete': 5, 'retain': 3},
                {'retain': 6, 'insert': '555'}
            ]
        ]
        for delta in deltas:
            print(delta_to_matrix(delta))

if __name__ == "__main__":
    unittest.main()
