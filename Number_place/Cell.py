#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Cell:
    """数独表のセルの管理クラス"""
    def __init__(self, value, row, column, block_size):
        self.value = value                              #未確定の場合は　0
        self.row = row                                  #行番号　0スタート
        self.column = column                            #列番号　0スタート
        self.block = self.calc_block_index(block_size)  #ブロック番号　0スタート
        self.candidate_set = set()                      #入力候補集合
        self.index = column + row*(block_size**2)       #セルのインデックス9*9なら0－80

    def calc_block_index(self, block_size):
    """セルのブロック位置計算関数　"""
            return self.column//block_size+((self.row//block_size)*block_size)

    def showinfo(self):
        """debug用Status出力関数"""
        print('index' + str(self.index), end='')
        print('   value' + self.value)
        print('row' + str(self.row), end='')
        print('   column' + str(self.column), end='')
        print('   block' + str(self.block), end='')
        print('   candidate' + str(self.candidate_set))
        print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
