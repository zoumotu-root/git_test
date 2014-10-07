#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import copy

#数独表のセルの管理クラス
class Cell:
    def __init__(self,value,row,column,block_size):
        self.value = value
        self.row = row
        self.column = column
        self.block = self.calc_block_index(block_size)
        self.candidate_set = set()
        self.index = column + row*(block_size**2)

    def calc_block_index(self,block_size):
        return self.column//block_size+((self.row//block_size)*block_size)

    """debug用Status出力関数"""
    def showinfo(self):
        print('index' + str(self.index),end ='')
        print('   value' + self.value)
        print('row' + str(self.row),end ='')
        print('   column' + str(self.column),end ='')
        print('   block' + str(self.block),end ='')
        print('   candidate' + str(self.candidate_set))
        print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')


#数独表の管理クラス
class Cell_Matrix:
    def __init__(self,file_path):
        self.file_path = file_path
        self.matrix_size =0                 #数独表の行（列）数
        self.block_size=0                   #ブロックのサイズ　基本は3
        self.cell_matrix =[]
        self.value_set=set()                #Cellに入力されるべき数字の集合
        self.unsolved_index_list = []       #このリストが空になれば解決できたと判定する
        self.is_cell_value_updated = False  #チェック項目を１通り回しても１つも値を更新できた場合はTrueとなる

    """数独表の作成並びにブロックサイズ、表のサイズの計算、未解決セル一覧作成を行う"""
    def init_Cell_Matrix(self):
        with open(self.file_path,'r') as f:
            self.matrix_size = len(f.readline())-1 #改行コードは計算に入れない
            self.block_size  = int(math.sqrt(self.matrix_size))
            self.value_set   = set(str(i+1) for i in range(self.matrix_size))

            f.seek(0)
            for line_number,line in enumerate(f):
                for column_number ,value in enumerate(line):
                    if value !='\n':
                        self.cell_matrix.append(Cell(value,line_number,column_number,self.block_size))
        self.calc_unsolved_index_list=self.calc_unsolved_index_list()

    """全てのセルに0以外の値が入力された場合、真を返す（解答が作成できた場合：真）"""
    def is_completed(self):
        return True if len(self.unsolved_index_list) ==0 else False

    """未解決セルリストの作成（値が0であるものを未解決であるとする）"""
    def calc_unsolved_index_list(self):
        self.unsolved_index_list = [cell.index for cell in self.cell_matrix if cell.value =='0']

    """全ての未解決セルの入力候補値を計算する"""
    def calc_all_cells_candidate(self):
        for cell in self.cell_matrix:
            if cell.value =='0':
                self.calc_cell_candidate(cell)

    """引数のセルの関連するブロック、行、列のセルから候補値の和を取り、引数のセルの候補値を算出する"""
    def calc_cell_candidate(self,cell):
        not_candidates=self.get_sameblock_cell_value(cell)
        not_candidates|=self.get_samerow_cell_value(cell)
        not_candidates|=self.get_samecolumn_cell_value(cell)
        cell.candidate_set= self.value_set-not_candidates

    """引数のセルが属するブロックの確定した値の集合を返す"""
    def get_sameblock_cell_value(self,cell):
        cells = self.get_sameblock_cells(cell.block)
        return set(cell.value for cell in cells if cell.value != '0')

    """引数のセルが属する行の確定した値の集合を返す"""
    def get_samerow_cell_value(self,cell):
        cells = self.get_samerow_cells(cell.row)
        return set(cell.value for cell in cells if cell.value != '0')

    """引数のセルが属する列の確定した値の集合を返す"""
    def get_samecolumn_cell_value(self,cell):
        cells = self.get_samecolumn_cells(cell.column)
        return set(cell.value for cell in cells if cell.value != '0')

    """引数で指定したブロック番号のセルのリストを返す"""
    def get_sameblock_cells(self,block_number):
        return [cell for cell in self.cell_matrix if cell.block==block_number]

    """引数で指定した行番号のセルのリストを返す"""
    def get_samerow_cells(self,row):
        return [cell for cell in self.cell_matrix if cell.row==row]

    """引数で指定した列番号のセルのリストを返す"""
    def get_samecolumn_cells(self,column):
        return [cell for cell in self.cell_matrix if cell.column==column]

    """関連するブロック毎（列毎、行毎）の候補が唯一であった場合は更新する"""
    def set_value_for_uniq_candidate_in_concern_candidate(self):
        for i in range(self.matrix_size):
            cells  = self.get_sameblock_cells(i)
            self.update_uniq_candidate(cells)
            cells = self.get_samerow_cells(i)
            self.update_uniq_candidate(cells)
            cells = self.get_samecolumn_cells(i)
            self.update_uniq_candidate(cells)

    """引数のセルの未解決セルで候補が１つしかないものを更新する"""
    def update_uniq_candidate(self,cells):
        for cell in cells:
            if cell.value =='0':
                candidate = set(self.get_uniq_cadidate_in_cells(cells,cell))
                if len(candidate)==1:
                    self.update_cell_value(cell,candidate)

    """与えられたセル集合から対象となるセルのユニークな候補を探す"""
    def get_uniq_cadidate_in_cells(self,cells,target_cell):
        target_candidate = set()
        target_candidate = set(target_cell.candidate_set)

        for cell in cells:
            if cell != target_cell: #自分自身の候補集合から自身の候補集合を引かないようにする。
                target_candidate-=cell.candidate_set
        return target_candidate

    """更新されたセルに関連するblock、行、列のCellの候補値の再計算
    　　（更新された値を関連するblock、行、列のCellの候補値から削除）"""
    def update_cells_candidate(self,target_cell):
        cells  = self.get_sameblock_cells(target_cell.block)
        cells += self.get_samerow_cells(target_cell.row)
        cells += self.get_samecolumn_cells(target_cell.column)
        self.discard_candidate(target_cell,cells)

    """各セルから確定したセルの値を候補値から削除"""
    def discard_candidate(self,target_cell,cells):
        for cell in cells:
            if cell.value =='0':
                cell.candidate_set.discard(target_cell.value)

    """候補が１つしかないセルに対して値を確定させる"""
    def set_value_for_single_candidate(self):
        for cell in self.cell_matrix:
            if cell.value =='0' and len(cell.candidate_set)==1:
                self.update_cell_value(cell)
    """セルの値を確定させ、後処理を行う"""
    def update_cell_value(self,cell,candidate=set()):
        if len(candidate)==0:
            cell.value =cell.candidate_set.pop()
        else:
            cell.value =candidate.pop()
        #後処理
        print("registedval  row " +str(cell.row) +" Col "+str(cell.column) +" V:"+cell.value)
        print_answer(self)
        cell.candidate_set.clear()                  #値確定後に候補値がは不要であるのでクリアする
        if cell.index in self.unsolved_index_list:
            self.unsolved_index_list.remove(cell.index) #未解決リストから削除する
        self.update_cells_candidate(cell)           #更新されたセルに関連するセルの候補値を更新する
        self.is_cell_value_updated = True           #値が更新できたので、このプログラムでも解決できる可能性がある
        #print_answer(self)
    def force_update_candidate(self,index,candidate):
        self.cell_matrix[index].candidate_set.clear()
        self.cell_matrix[index].candidate_set.add(candidate)
        self.set_value_for_single_candidate()

    """現在のアルゴリズムでは解けないものがある事は分かっているので、これ以上計算をすべきかの判定を行う
    　 判定の条件としてはチェック項目を１通り回しても１つも値を更新できない場合は終了とする。"""
    def should_calculation_stopped(self):
        if self.is_cell_value_updated:
            self.is_cell_value_updated = False
            return False
        return True

    def select_cell(self):
        """
        未解決セルの中で候補値集合のサイズが最小でかつ未解決リストの最初にあるセルを返す

        """
        for candidate_size in range(2,10):
            for i in self.unsolved_index_list:
                if len(self.cell_matrix[i].candidate_set)==candidate_size:
                    return self.cell_matrix[i]
        return None

    """debug用Status出力関数"""
def cell_matrix_show(cell_matrix):
    for cell in cell_matrix:
        cell.showinfo()

    """debug用結果出力関数"""
def print_answer(cell_matrix):
    for i,cell in enumerate(cell_matrix.cell_matrix):
        print(cell.value,end ='')
        if (i+1)%cell_matrix.matrix_size ==0:
            print('')
    print("--------------------------------------")
    """結果出力関数"""
def output_answer(cell_matrix,file_path):
    with open(file_path+"answer",'w') as f:
        for i,cell in enumerate(cell_matrix.cell_matrix):
            f.write(cell.value)
            if (i+1)%cell_matrix.matrix_size ==0:
                f.write('\n')
    print('calc end. File output finished.')

"""与えられた数独表自体に整合性がない場合は計算ができないので整合性を検査する
    整合性が取れない状態とは同じブロック（列、行）に同じ数字が存在しているものとする。"""
def has_cell_matrix_againt_rules(cell_matrix):
    for i in range(cell_matrix.matrix_size):
        if has_violation(cell_matrix.get_sameblock_cells(i)) or \
           has_violation(cell_matrix.get_samerow_cells(i))   or \
           has_violation(cell_matrix.get_samecolumn_cells(i)):
           return True
    return False
    """引数であたえられたセルにおいて、数字の重複を判定。重複している場合は真を返す"""
def has_no_value_and_no_candidate_cell(cell_matrix):
    """セルの値が’0’かつ候補値がないものが無いかの検査
    　　上記のセルがあった場合にTrueを返す。（推定した値をいれた場合このようなセルが生じる可能性がある）
    """
    for cell in cell_matrix.cell_matrix:
        if cell.value=='0' and len(cell.candidate_set)==0:
            return True
    return False

def has_violation(cells):
    orignal_set =set()
    for cell in cells :
        if cell.value !='0':
            if cell.value in orignal_set :
                return True
            else:
                orignal_set.add(cell.value)
    return False

def recursive_calc_cell_matrix(cell_matrix,select_cell=None,candidate=set(),depth =0):
    #print_answer(cell_matrix)
    if select_cell != None:
        print(select_cell.showinfo())

    if select_cell != None:
        cell_matrix.force_update_candidate(select_cell.index,candidate.pop())
        #cell_matrix.update_cell_value(select_cell,candidate)
        #cell_matrix.force_update_cell(select_cell,candidate.pop())
    backup_cell_matrix =copy.deepcopy(cell_matrix)


    print('BackUped cell_matrix'+str(depth))
    print_answer(backup_cell_matrix)

    if has_cell_matrix_againt_rules(cell_matrix):
        print('IN Recursive :cell_matrix  has againsts rules.')
        return
    if has_no_value_and_no_candidate_cell(cell_matrix):
        print('IN Recursive :cell has no value and no candidate.')
        return


    while True:
        if cell_matrix.is_completed():
            print("***************Solve this matrix********************")
            print_answer(cell_matrix)   #debug用
            output_answer(cell_matrix,sys.argv[1])
            sys.exit()


        cell_matrix.set_value_for_single_candidate()
        cell_matrix.set_value_for_uniq_candidate_in_concern_candidate()

        if cell_matrix.should_calculation_stopped():

            print('In should_calculation_stopped'+str(depth))
            print_answer(cell_matrix)   #debug用
            select_cell = cell_matrix.select_cell()
            if select_cell == None:
                print('Can not select next cell')
                return
            backup_select_cell = copy.deepcopy(select_cell)
            candidate_set=set()
            candidate_set = copy.deepcopy(select_cell.candidate_set)
            for i ,v in enumerate(candidate_set):
                print('In to recursive!('+str(i)+') next candidate ='+v +"row:"+str(select_cell.row)+"col:"+str(select_cell.column)+'val:'+select_cell.value)
                recursive_calc_cell_matrix(cell_matrix,select_cell,{v},depth+1)
                print("Return & Rollback 前"+str(depth))
                print_answer(cell_matrix)
                cell_matrix = backup_cell_matrix
                select_cell = backup_select_cell
                print("Return & Rollback 後"+str(depth))
                print_answer(cell_matrix)
            else:
                print('return')
                return

if __name__ == '__main__':
    import sys

    cell_matrix=Cell_Matrix(sys.argv[1])
    cell_matrix.init_Cell_Matrix()

    #整合性がとれていないファイルが入力された場合は終了する
    if has_cell_matrix_againt_rules(cell_matrix):
        print('This file againsts rules. Interrupt calculation.')
        exit()

    cell_matrix.calc_all_cells_candidate()

    #解答がでるか、計算してもこれ以上計算できないと判断されるまでループする。
    while True:
        if cell_matrix.is_completed():
            output_answer(cell_matrix,sys.argv[1])
            break

        cell_matrix.set_value_for_single_candidate()
        cell_matrix.set_value_for_uniq_candidate_in_concern_candidate()

        if cell_matrix.should_calculation_stopped():
            #print_answer(cell_matrix)
            recursive_calc_cell_matrix(cell_matrix)
            print("This matrix can not solve. I think ")
            print_answer(cell_matrix)   #debug用
            exit()




