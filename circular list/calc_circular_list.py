#!/usr/bin/env python
# -*- coding: utf-8 -*-
import doctest

#題意の循環リストが見つかれば入れていく
answer_list = []


def main(L):
    import time
    global answer_list
    answer_list = []

    nL = L*(L-1)+1
    #循環リストで作れる足し合わせの総パターン数 : n(L)
    max_candidate = calc_candidate_range(L)
    depth = L-1
    #木構造の深さ制御変数
    selected_values = [1]
    #循環リスト 題意の通り最初の要素は[1]
    candidate_values = [x for x in range(2, max_candidate+1)]
    #循環リストに入る値の候補

    time1 = time.clock()

    for i in candidate_values:
        local_selected_values = selected_values[:]
        local_candidate_values = candidate_values[:]
        local_selected_values.append(i)
        local_candidate_values.remove(i)

        calc_squence_tree(depth-1, local_selected_values, local_candidate_values, nL)
    if not answer_list:
        print('Answer do not exist.')

    time2 = time.clock()
    time = time2-time1
    time = int(time)
    time = str(time)
    print('処理時間は' + time + '秒でした')
    return answer_list


def calc_squence_tree(depth, selected_values, candidate_values, nL):
    """
    循環リストを木構造を通して作成し必要に応じて枝刈りをして計算時間の短縮をはかる。
    枝刈りの条件は以下の３つ
    ・循環リストの各値を合計しn(L)を超えている場合
    ・循環リストの候補値がすでに循環リストにあるものしか選択できない場合
    ・循環リスト内の各値を足しあわせて、その数値が既に循環リストにあった場合
    """
    if depth == 0:
        if selected_values[1] < selected_values[-1]:
        #問題要件：「２番目の要素＜末尾の要素」を実装
            NX = cal_NX(selected_values)
            if len(NX) == nL:
                print("ANS:" + str(selected_values))
                global answer_list
                answer_list.append(selected_values)
        return
    if sum(selected_values) >= nL:
    #合計がn(L)をすでに超えているので、これ以上計算を行わない
        return


    sum_rest = nL - sum(selected_values)
    if depth == 1:
        #最後の候補値の時はn(L)に合うように調整する。ただし、既に使用されている場合はこれ以上計算を行うわない
        if sum_rest in candidate_values:
            candidate_values =[sum_rest]
        else:
            return
    else:
    #いままで選択された値の合計し、候補値と足した場合にn(L)を超える値を除去する
        candidate_values = [x for x in candidate_values if x <= sum_rest]

    for i in candidate_values:
        local_selected_values = selected_values[:]
        local_selected_values.append(i)
        #要素を２つ足して、すでに選択された要素と同じ数字になった場合は題意を満たすN（X）を生成できないのでこれ以上計算を行わない
        if len(local_selected_values) >= 3:
            if has_same_number(local_selected_values):
                continue
        local_candidate_values = candidate_values[:]
        local_candidate_values.remove(i)

        calc_squence_tree(depth-1, local_selected_values, local_candidate_values, nL)


def has_same_number(local_selected_values):
    """
    与えられた循環リストの隣合う数値を足して、自身の循環リストにその数値が無いか判定する。
    True：これ以上木構造を計算する必要がない
    （足しあわせた数値が自身の循環リストに存在する場合は題意のN(X)をみたさない）
    >>> has_same_number([1,2,3])
    True
    >>> has_same_number([1, 3, 2, 7, 8, 10])
    False
    """
    for i in range(len(local_selected_values)-1):
        if local_selected_values[i]+local_selected_values[i+1] in local_selected_values:
                    return True
    return False


def calc_candidate_range(L):
    """
    葉の要素としての最大値の計算を行う。
    L=3 ：[1,2,4] 　　　　=>4が最大値
    L=5 ：[1,2,3,4,11]　　=>11が最大値
    >>> calc_candidate_range(3)
    4
    >>> calc_candidate_range(5)
    11
    """
    return sum([x for x in range(1, L)])+1


def cal_NX(l):
    """
    題意のN(X)を計算する。N(X)：全部分リストの和の集合
    重複が現れた場合は題意にそぐわないのでリターン
    下記の例はL=3 の時の正解の例
    >>> cal_NX([1, 2, 4])
    {1, 2, 3, 4, 5, 6, 7}
    """
    N_X = set()
    for sum_range in range(1, len(l)):
    #足算を行う範囲を決める
        for i in range(len(l)):
        #足算を行う回数を制御
            subset_sum = sum(l[:sum_range])
            #要素が重複してあらわれた場合は題意を満たすN（X）を生成できないのでこれ以上計算を行わない
            if subset_sum in N_X:
                return N_X
            N_X.add(subset_sum)
            l = rotate(l)
            #リストをローテンションさせる
    N_X.add(sum(l))
    return N_X


def rotate(l):
    """
    リストをローテーションさせる。
    >>> rotate([1,2,3,4,5])
    [2, 3, 4, 5, 1]
    """
    return l[1:]+l[:1]

if __name__ == '__main__':
    import sys
    doctest.testmod()
    main(int(sys.argv[1]))
