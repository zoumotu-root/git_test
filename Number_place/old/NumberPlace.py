#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import copy

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


class Cell_Matrix:
    """数独表の管理クラス"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.matrix_size = 0                 #数独表の行（列）数
        self.block_size = 0                   #ブロックのサイズ　基本は3
        self.cell_matrix = []
        self.value_set = set()                #Cellに入力されるべき数字の集合
        self.unsolved_index_list = []       #このリストが空になれば解決できたと判定する
        self.is_cell_value_updated = False  #チェック項目を１通り回しても１つも値を更新できた場合はTrueとなる

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


def cell_matrix_show(cell_matrix):
    """debug用Status出力関数"""
    for cell in cell_matrix:
        cell.showinfo()


def print_answer(cell_matrix):
    """debug用結果出力関数"""
    for i, cell in enumerate(cell_matrix.cell_matrix):
        print(cell.value, end='')
        if (i+1) % cell_matrix.matrix_size == 0:
            print('')
    print("--------------------------------------")


def output_answer(cell_matrix, file_path):
    """結果出力関数 「入力ファイルPath＋入力ファイル名＋answer」で出力"""
    with open(file_path+"answer", 'w') as f:
        for i, cell in enumerate(cell_matrix.cell_matrix):
            f.write(cell.value)
            if (i+1) % cell_matrix.matrix_size == 0:
                f.write('\n')
    print('calc end. File output finished.')


def has_cell_matrix_againt_rules(cell_matrix):
    """与えられた数独表自体に整合性がない場合は計算ができないので整合性を検査する
        整合性が取れない状態とは同じブロック（列、行）に同じ数字が存在しているものとする。"""
    for i in range(cell_matrix.matrix_size):
        if has_violation(cell_matrix.get_sameblock_cells(i)) or \
           has_violation(cell_matrix.get_samerow_cells(i))   or \
           has_violation(cell_matrix.get_samecolumn_cells(i)):
            return True
    return False


def has_violation(cells):
    """引数であたえられたセルにおいて、数字の重複を判定。重複している場合は真を返す"""
    original_set = set()
    for cell in cells:
        if cell.value != '0':
            if cell.value in original_set:
                return True
            else:
                original_set.add(cell.value)
    return False


def has_no_value_and_no_candidate_cell(cell_matrix):
    """セルの値が’0’かつ候補値がないものが無いかの検査
    　　上記のセルがあった場合にTrueを返す。（推測した値をいれた場合このようなセルが生じる可能性がある）
    """
    for cell in cell_matrix.cell_matrix:
        if cell.value == '0' and len(cell.candidate_set) == 0:
            return True
    return False


def ending_process(cell_matrix):
    print("***************Solve this matrix********************")
    print_answer(cell_matrix)   #debug用
    output_answer(cell_matrix, sys.argv[1])
    sys.exit()


def recursive_calc_cell_matrix(cell_matrix, select_cell=None, candidate=set()):
    """引数で与えられたセル行列の計算を再帰的に行う。
    　　1つでも解が出れば解をファイルに出力し、プログラムを終了する。
        解法としては以下の手順になります。（手順の中で、不整合が生じた場合は呼び出し元関数に戻る）
        1:論理でセルを埋めれるだけうめる
    　　2:候補値から値を選んで１つだけセルを埋める。
        3:論理でセルを埋めれるだけうめる
        4:2に戻る
    """
    if select_cell is not None:
        #推測したセルがある場合はその値をセルに強制的に書き込む
        cell_matrix.force_update_candidate(select_cell.index, candidate.pop())

    #推定をおこなった結果不整合が生じたまたは、八方ふさがりの状態になった場合はリターン
    if has_cell_matrix_againt_rules(cell_matrix) or \
       has_no_value_and_no_candidate_cell(cell_matrix):
        return

    #推測に失敗した場合に備えて既存の状態を保存
    backup_cell_matrix = copy.deepcopy(cell_matrix)

    while True:
        if cell_matrix.is_completed():
            ending_process(cell_matrix)

        #論理1　候補が１つしかないセルを埋める
        cell_matrix.set_value_for_single_candidate()
        #論理2　ブロック、行、列の中でuniqな候補値をもつセルを埋める
        cell_matrix.set_value_for_uniq_candidate_in_concern_candidate()

        if cell_matrix.should_calculation_stopped():
        #論理で埋められる部分がなくなり、セルの値を推測する必要がある場合の処理
            select_cell = cell_matrix.select_cell()
            if select_cell is None:
            #推測できるセルがない場合はリターン
                return

            candidate_set = set(copy.deepcopy(select_cell.candidate_set))
            #推測できる候補値を算出
            for v in candidate_set:
                recursive_calc_cell_matrix(cell_matrix, select_cell, {v})
                #推定した候補で再帰的に計算：解がみつかればこれ以降には行かない
                cell_matrix = backup_cell_matrix
                #推測した候補値が間違えていたので、現状復帰
            else:
                return

if __name__ == '__main__':
    import sys

    #ファイルからの値の読込と初期化を行う
    cell_matrix = Cell_Matrix(sys.argv[1])
    cell_matrix.init_Cell_Matrix()

    if has_cell_matrix_againt_rules(cell_matrix):
    #計算以前に整合性がとれていないファイルが入力された場合は終了する。
        print('This file against rules. Interrupt calculation.')
        sys.exit()

    cell_matrix.calc_all_cells_candidate()
    #全てのセルに対して入力できる可能性のある候補値を算出する
    recursive_calc_cell_matrix(cell_matrix)
    #
    print("This matrix(input file) can not solve. I think ")




