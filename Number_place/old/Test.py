#!/usr/bin/env python
# -*- coding: utf-8 -*-

from NumberPlace import *
import unittest


class TestCase(unittest.TestCase):
    #cell_matrix =None

    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_get_samecolumn_cell_value(self):

        cell_matrix = Cell_Matrix('Input_Sample\sample5.txt')
        cell_matrix.init_Cell_Matrix()
        cell =Cell(5,0,0,3)
        self.assertEqual({'1','5','8','9'},cell_matrix.get_samecolumn_cell_value(cell))
        cell =Cell(5,0,5,3)
        self.assertEqual({'3','7','9'},cell_matrix.get_samecolumn_cell_value(cell))



    def test_has_no_value_and_no_candidate_cell(self):
        cell_matrix = Cell_Matrix('Input_Sample\sample5.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual(True,has_no_value_and_no_candidate_cell(cell_matrix))

        #cell_matrix = Cell_Matrix('Input_Sample\Cant_calc\test1.txt')
        #cell_matrix.init_Cell_Matrix()
        #self.assertEqual(True,has_no_value_and_no_candidate_cell(cell_matrix))

    def test_has_cell_matrix_againt_rules(self):
        cell_matrix = Cell_Matrix('Input_Sample\sample5.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual(False,has_cell_matrix_againt_rules(cell_matrix))

        cell_matrix = Cell_Matrix('Input_Sample\Cant_calc\sample_block_error1.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual(True,has_cell_matrix_againt_rules(cell_matrix))

        cell_matrix = Cell_Matrix('Input_Sample\Cant_calc\sample_column_error1.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual(True,has_cell_matrix_againt_rules(cell_matrix))

        cell_matrix = Cell_Matrix('Input_Sample\Cant_calc\sample_row_error1.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual(True,has_cell_matrix_againt_rules(cell_matrix))

if __name__ == "__main__":
    unittest.main()
