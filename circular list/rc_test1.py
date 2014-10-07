#!/usr/bin/env python
# -*- coding: utf-8 -*-

is_answer_exist = False

def main(L):
 import time

 Ln =L*(L-1)+1
 max_candidate = calc_candidate_range(L)
 depth = L-1
 selected_values =[1]
 candidate_values = [x for x in range(2,max_candidate+1)]

 time1 = time.clock()

 for i in candidate_values:
    local_selected_values = selected_values[:]
    local_candidate_values = candidate_values[:]
    local_selected_values.append(i)
    local_candidate_values.remove(i)

    calc_squence_tree(depth-1,local_selected_values,local_candidate_values,Ln)
 if is_answer_exist==False:
    print('Anser do not exist.')

 time2 = time.clock()
 time = time2-time1
 time = int(time)
 time = str(time)
 print ('処理時間は' + time + '秒でした')

def calc_squence_tree(depth,selected_values,candidate_values,Ln):

    if depth ==0:
        if selected_values[1]<selected_values[-1]: #問題要件：「２番目の要素＜末尾の要素」を実装
            #print(selected_values)
            NX = cal_NX(selected_values)
            if len(NX)==Ln:
                print("ANS:" + str(selected_values))
                global is_answer_exist
                is_answer_exist= True
        return
    if sum(selected_values)>=Ln:#合計がn(L)をすでに超えているので、これ以上計算を行わない
        return


    sum_rest = Ln-sum(selected_values)
    if depth ==1:
        #最後の候補値の時はn(L)に合うように調整する。ただし、既に使用されている場合はこれ以上計算を行うわない
        if sum_rest in candidate_values:
            candidate_values =[sum_rest]
        else:
            return
    else:#いままで選択された値の合計し、候補値と足した場合にn(L)を超える値を除去する
        candidate_values =[x for x in candidate_values if x <=sum_rest]

    for i in candidate_values:
        local_selected_values = selected_values[:]
        local_selected_values.append(i)
        #要素を２つ足して、すでに選択された要素と同じ数字になった場合は題意を満たすN（X）を生成できないのでこれ以上計算を行わない
        if len(local_selected_values)>=3:
            if has_same_number(local_selected_values):
                continue
        local_candidate_values = candidate_values[:]
        local_candidate_values.remove(i)

        calc_squence_tree(depth-1,local_selected_values,local_candidate_values,Ln)

def has_same_number(local_selected_values):
    for i in range(len(local_selected_values)-1):
        if local_selected_values[i]+local_selected_values[i+1] in local_selected_values:
                    return True
    return False
    #for i in range(len(local_selected_values)-2):
    #    for j in range(len(local_selected_values)-i-1):
    #        if sum(local_selected_values[j:j+i+2]) in local_selected_values:
    #            return True
    #return False

def calc_candidate_range(L):
    return sum([x for x in range(1,L)])+1

def cal_NX(l):
 N_X =set()
 for sum_range in range(1,len(l)):
    for j in range(len(l)):
        subset_sum =sum(l[:sum_range])
        if subset_sum in N_X:#要素が重複してあらわれた場合は題意を満たすN（X）を生成できないのでこれ以上計算を行わない
            return N_X
        N_X.add(subset_sum)
        l=rotate(l)
 N_X.add(sum(l))
 return N_X


def rotate(l):
    return l[1:]+l[:1]

if __name__ == '__main__':

 import sys
 main(int(sys.argv[1]))
