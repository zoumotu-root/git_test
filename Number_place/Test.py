#!/usr/bin/env python
# -*- coding: utf-8 -*-

from NumberPlace import *
from Cell_Matrix import *

import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_init_Cell_Matrix(self):
        cell_matrix = Cell_Matrix('test_files\sample0.txt')
        cell_matrix.init_Cell_Matrix()

        self.assertEqual(9,cell_matrix.matrix_size)
        self.assertEqual(3,cell_matrix.block_size)
        self.assertEqual({'1', '2', '3', '4', '5', '6', '7', '8', '9'},cell_matrix.value_set)
        self.assertEqual([1,  2,  4,  5,  6,  7,  9,  11,  12,  13,  16,  17,  18,  19,  21,  23,
                          24,  26,  27,  28,  30,  32,  33,  34,  35,  36,  38,  39,  40,  41,  43,
                          44,  46,  47,  49,  50,  51,  54,  55,  57,  58,  60,  61,  62,  63,  64,
                          65,  66,  68,  69,  71,  72,  74,  76,  77,  78,  79],cell_matrix.unsolved_index_list)
        self.assertEqual(0,cell_matrix.cell_matrix[0].row)
        self.assertEqual(0,cell_matrix.cell_matrix[0].column)
        self.assertEqual(0,cell_matrix.cell_matrix[0].block)
        self.assertEqual('6',cell_matrix.cell_matrix[0].value)
        self.assertEqual(8,cell_matrix.cell_matrix[80].row)
        self.assertEqual(8,cell_matrix.cell_matrix[80].column)
        self.assertEqual(8,cell_matrix.cell_matrix[80].block)
        self.assertEqual('1',cell_matrix.cell_matrix[80].value)

    def test_calc_all_cells_candidate(self):
        cell_matrix = Cell_Matrix('test_files\sample0.txt')
        cell_matrix.init_Cell_Matrix()
        cell_matrix.calc_all_cells_candidate()
        self.assertEqual({'2', '4', '9'},cell_matrix.cell_matrix[1].candidate_set)
        self.assertEqual({'2', '4','6', '7', '8'},cell_matrix.cell_matrix[69].candidate_set)
        self.assertEqual(set(),cell_matrix.cell_matrix[8].candidate_set)

    def test_get_sameblock_cell_value(self):
        cell_matrix = Cell_Matrix('test_files\sample0.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual({'2', '5', '7'},cell_matrix.get_sameblock_cell_value(cell_matrix.cell_matrix[6]))
        self.assertEqual({'1', '3'},cell_matrix.get_sameblock_cell_value(cell_matrix.cell_matrix[80]))
        self.assertEqual({'4', '6'},cell_matrix.get_sameblock_cell_value(cell_matrix.cell_matrix[30]))

    def testget_samerow_cell_value(self):
        cell_matrix = Cell_Matrix('test_files\sample0.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual({'1', '6', '7'},cell_matrix.get_samerow_cell_value(cell_matrix.cell_matrix[6]))
        self.assertEqual({'1', '5','7'},cell_matrix.get_samerow_cell_value(cell_matrix.cell_matrix[80]))
        self.assertEqual({'4', '3'},cell_matrix.get_samerow_cell_value(cell_matrix.cell_matrix[30]))

    def test_get_samecolumn_cell_value(self):
        cell_matrix = Cell_Matrix('test_files\sample0.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual({'9', '5'},cell_matrix.get_samecolumn_cell_value(cell_matrix.cell_matrix[6]))
        self.assertEqual({'1', '4' ,'7'},cell_matrix.get_samecolumn_cell_value(cell_matrix.cell_matrix[80]))
        self.assertEqual({'1', '6' ,'7'},cell_matrix.get_samecolumn_cell_value(cell_matrix.cell_matrix[30]))

    def test_get_sameblock_cells(self):
        cm = Cell_Matrix('test_files\sample0.txt')
        cm.init_Cell_Matrix()
        self.assertEqual([cm.cell_matrix[ 3],cm.cell_matrix[ 4],cm.cell_matrix[ 5],
                          cm.cell_matrix[12],cm.cell_matrix[13],cm.cell_matrix[14],
                          cm.cell_matrix[21],cm.cell_matrix[22],cm.cell_matrix[23]],cm.get_sameblock_cells(1))

    def test_get_samerow_cells(self):
        cm = Cell_Matrix('test_files\sample0.txt')
        cm.init_Cell_Matrix()
        self.assertEqual([cm.cell_matrix[36],cm.cell_matrix[37],cm.cell_matrix[38],
                          cm.cell_matrix[39],cm.cell_matrix[40],cm.cell_matrix[41],
                          cm.cell_matrix[42],cm.cell_matrix[43],cm.cell_matrix[44]],cm.get_samerow_cells(4))

    def test_get_samecolumn_cells(self):
        cm = Cell_Matrix('test_files\sample0.txt')
        cm.init_Cell_Matrix()
        self.assertEqual([cm.cell_matrix[ 8],cm.cell_matrix[17],cm.cell_matrix[26],
                          cm.cell_matrix[35],cm.cell_matrix[44],cm.cell_matrix[53],
                          cm.cell_matrix[62],cm.cell_matrix[71],cm.cell_matrix[80]],cm.get_samecolumn_cells(8))

#    def test_set_value_for_uniq_candidate_in_concern_candidate():
#        cm = Cell_Matrix('test_files\sample0.txt')
#        cm.init_Cell_Matrix()
#        cm.calc_all_cells_candidate()
#        cm.set_value_for_uniq_candidate_in_concern_candidate()


    def test_has_no_value_and_no_candidate_cell(self):
        cell_matrix = Cell_Matrix('test_files\sample5.txt')
        cell_matrix.init_Cell_Matrix()
        cell_matrix.calc_all_cells_candidate()
        self.assertEqual(False,has_no_value_and_no_candidate_cell(cell_matrix))

        cell_matrix = Cell_Matrix('test_files\Cant_calc\haxtupoufusagari.txt')
        cell_matrix.init_Cell_Matrix()
        cell_matrix.calc_all_cells_candidate()
        self.assertEqual(True,has_no_value_and_no_candidate_cell(cell_matrix))

    def test_has_cell_matrix_againt_rules(self):
        cell_matrix = Cell_Matrix('test_files\sample5.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual(False,has_cell_matrix_againt_rules(cell_matrix))

        cell_matrix = Cell_Matrix('test_files\Cant_calc\sample_block_error1.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual(True,has_cell_matrix_againt_rules(cell_matrix))

        cell_matrix = Cell_Matrix('test_files\Cant_calc\sample_column_error1.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual(True,has_cell_matrix_againt_rules(cell_matrix))

        cell_matrix = Cell_Matrix('test_files\Cant_calc\sample_row_error1.txt')
        cell_matrix.init_Cell_Matrix()
        self.assertEqual(True,has_cell_matrix_againt_rules(cell_matrix))

    def test_select_cell(self):
        cm = Cell_Matrix('test_files\sample0.txt')
        cm.init_Cell_Matrix()
        cm.calc_all_cells_candidate()
        self.assertEqual(cm.cell_matrix[21],cm.select_cell())

if __name__ == "__main__":
    unittest.main()
