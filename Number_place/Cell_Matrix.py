#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from Cell import Cell

class Cell_Matrix:
    """数独表の管理クラス"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.matrix_size = 0
        #数独表の行（列）数
        self.block_size = 0
        #ブロックのサイズ　基本は3
        self.cell_matrix = []
        self.value_set = set()
        #Cellに入力されるべき数字の集合
        self.unsolved_index_list = []
        #このリストが空になれば解決できたと判定する
        self.is_cell_value_updated = False
        #チェック項目を１通り回しても１つも値を更新できた場合はTrueとなる

    def init_Cell_Matrix(self):
        """数独表の作成並びにブロックサイズ、表のサイズの計算、未解決セル一覧作成を行う"""
        with open(self.file_path,'r') as f:
            self.matrix_size = len(f.readline())-1 #改行コードは計算に入れない
            self.block_size  = int(math.sqrt(self.matrix_size))
            self.value_set   = set(str(i+1) for i in range(self.matrix_size))

            f.seek(0)
            for line_number, line in enumerate(f):
                for column_number, value in enumerate(line):
                    if value != '\n':
                        self.cell_matrix.append(Cell(value, line_number, column_number, self.block_size))
        self.calc_unsolved_index_list()

    def is_completed(self):
        """未解決のセルが無くなった場合、真を返す（解答が作成できた場合：真を返す）"""
        return True if len(self.unsolved_index_list) ==0 else False

    def calc_unsolved_index_list(self):
        """未解決セルリストの作成（値が0であるものを未解決であるとする）"""
        self.unsolved_index_list = [cell.index for cell in self.cell_matrix if cell.value == '0']

    def calc_all_cells_candidate(self):
        """全ての未解決セルの入力候補値を計算する"""
        for cell in self.cell_matrix:
            if cell.value == '0':
                self.calc_cell_candidate(cell)

    def calc_cell_candidate(self, cell):
        """引数のセルの関連するブロック、行、列のセルから候補値の集合和を取り、
        　 引数のセルの候補値を算出する"""
        not_candidates = self.get_sameblock_cell_value(cell)
        not_candidates |= self.get_samerow_cell_value(cell)
        not_candidates |= self.get_samecolumn_cell_value(cell)
        cell.candidate_set = self.value_set-not_candidates

    def get_sameblock_cell_value(self, cell):
        """引数のセルが属するブロックの確定した値の集合を返す"""
        cells = self.get_sameblock_cells(cell.block)
        return set(cell.value for cell in cells if cell.value != '0')

    def get_samerow_cell_value(self, cell):
        """引数のセルが属する行の確定した値の集合を返す"""
        cells = self.get_samerow_cells(cell.row)
        return set(cell.value for cell in cells if cell.value != '0')

    def get_samecolumn_cell_value(self, cell):
        """引数のセルが属する列の確定した値の集合を返す"""
        cells = self.get_samecolumn_cells(cell.column)
        return set(cell.value for cell in cells if cell.value != '0')

    def get_sameblock_cells(self, block_number):
        """引数で指定したブロック番号のセルのリストを返す"""
        return [cell for cell in self.cell_matrix if cell.block == block_number]

    def get_samerow_cells(self,row):
        """引数で指定した行番号のセルのリストを返す"""
        return [cell for cell in self.cell_matrix if cell.row == row]

    def get_samecolumn_cells(self, column):
        """引数で指定した列番号のセルのリストを返す"""
        return [cell for cell in self.cell_matrix if cell.column == column]

    def set_value_for_uniq_candidate_in_concern_candidate(self):
        """関連するブロック毎（列毎、行毎）の候補が唯一であったセルは更新する"""
        for i in range(self.matrix_size):
            cells = self.get_sameblock_cells(i)
            self.update_uniq_candidate(cells)
            cells = self.get_samerow_cells(i)
            self.update_uniq_candidate(cells)
            cells = self.get_samecolumn_cells(i)
            self.update_uniq_candidate(cells)

    def update_uniq_candidate(self, cells):
        """引数のセル(未解決セル)で候補が１つしかないものを更新する"""
        for cell in cells:
            if cell.value == '0':
                candidate = set(self.get_uniq_cadidate_in_cells(cells, cell))
                if len(candidate) == 1:
                    self.update_cell_value(cell, candidate)

    def get_uniq_cadidate_in_cells(self, cells,target_cell):
        """与えられたセル集合から対象となるセルのユニークな候補を探す"""

        target_candidate = set(target_cell.candidate_set)
        for cell in cells:
            if cell != target_cell: #自分自身の候補集合から自身の候補集合を引かないようにする。
                target_candidate -= cell.candidate_set
        return target_candidate

    def update_cells_candidate(self, target_cell):
        """更新されたセルに関連するblock、行、列のCellの候補値の再計算する
    　　　（更新された値を関連するblock、行、列のCellの候補値から削除）"""
        cells = self.get_sameblock_cells(target_cell.block)
        cells += self.get_samerow_cells(target_cell.row)
        cells += self.get_samecolumn_cells(target_cell.column)
        self.discard_candidate(target_cell, cells)

    def discard_candidate(self, target_cell, cells):
        """引き数のセル列から不要な候補値を削除する"""
        for cell in cells:
            if cell.value == '0':
                cell.candidate_set.discard(target_cell.value)

    def set_value_for_single_candidate(self):
        """候補が１つしかないセルに対して値を確定させる"""
        for cell in self.cell_matrix:
            if cell.value == '0' and len(cell.candidate_set) == 1:
                self.update_cell_value(cell)

    def update_cell_value(self, cell, candidate=set()):
        """セルの値を確定させ、後処理を行う"""
        if len(candidate) == 0:
            cell.value = cell.candidate_set.pop()
        else:
            cell.value = candidate.pop()
        #後処理
        cell.candidate_set.clear()                      #値確定後に候補値がは不要であるのでクリアする
        if cell.index in self.unsolved_index_list:
            self.unsolved_index_list.remove(cell.index) #未解決リストから削除する
        self.update_cells_candidate(cell)               #更新されたセルに関連するセルの候補値を更新する
        self.is_cell_value_updated = True               #値が更新できたので、推測をおこなわず、論理でセルを埋める方向で解決を目指す

    def force_update_candidate(self, index, candidate):
        """引数で指定されたインデックスのセルの候補値を書き換え値の更新を行う"""
        self.cell_matrix[index].candidate_set.clear()
        self.cell_matrix[index].candidate_set.add(candidate)
        self.set_value_for_single_candidate()

    def should_calculation_stopped(self):
        """論理で埋められるセルが全て埋めてしまったかの判定を行う。
         　判定の条件として以下の関数を実行し、１つもセルが更新出来ない場合とする。
            cell_matrix.set_value_for_single_candidate()
            cell_matrix.set_value_for_uniq_candidate_in_concern_candidate()
        """
        if self.is_cell_value_updated:
            self.is_cell_value_updated = False
            return False
        return True

    def select_cell(self):
        """本関数は論理で埋められる全てのセルが埋まった場合に次の一手を決める為に使用される
        　 次の一手は未解決のセルの中で以下の基準で決定される。
        　   ・リストの最初の方にある候補値集合のサイズが最小のセル"""
        for candidate_size in range(2, 10):
            for i in self.unsolved_index_list:
                if len(self.cell_matrix[i].candidate_set) == candidate_size:
                    return self.cell_matrix[i]
        return None

