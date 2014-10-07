#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calc_circular_list
import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main(self):
        self.assertEqual([[1, 3, 10, 2, 5]], main(5))
        self.assertEqual([[1, 2, 5, 4, 6, 13],
                          [1, 2, 7, 4, 12, 5],
                          [1, 3, 2, 7, 8, 10],
                          [1, 3, 6, 2, 5, 14],
                          [1, 7, 3, 2, 4, 14]], main(6))
        self.assertEqual([], main(7))

    def test_has_same_number(self):
        self.assertEqual(False, calc_circular_list.has_same_number([1, 3, 10, 2, 5]))
        self.assertEqual(True, calc_circular_list.has_same_number([1, 2, 3]))

    def test_calc_candidate_range(self):
        self.assertEqual(11, calc_candidate_range(5))
        self.assertEqual(1, calc_candidate_range(-1))

    def test_cal_NX(self):
        #NXがただしく計算できた場合　（入力が5,8の時の解）
        self.assertEqual({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21}, cal_NX([1, 3, 10, 2, 5]))
        self.assertEqual({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57},
                          cal_NX([1, 2, 10, 19, 4, 7, 9, 5]))

        #途中で重複（3が重複）が発覚し中断した特の例
        self.assertEqual({1, 2, 3},cal_NX([1,2,3]))
        #これも途中で計算がおわった時(5が重複した場合)
        self.assertEqual({1, 2, 3, 4, 5, 10}, cal_NX([1, 3, 2, 5, 10]))

    def test_rotate(self):
        self.assertEqual([2, 3, 4, 5, 1],rotate([1, 2, 3, 4, 5]))
        self.assertEqual([1], rotate([1]))

if __name__ == "__main__":
    unittest.main()
