#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import copy

from Cell_Matrix import Cell_Matrix

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




