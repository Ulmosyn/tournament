# coding: utf-8
# Your code here!
import sys

"""
１～Ｎまでの実力をもった２**Ｎ人でＩ回トーナメントを行った場合の、実力ごとの優勝回数を算出する
同実力の場合勝負は５分、実力差が１ある場合上位実力者がＢ％の確率で勝利する
データは以下の形で入力する
N B I
"""

# 標準入力を取り込む
line = []
for i in sys.stdin.readlines():
    line.append(i.rstrip())

# 入力されたデータの格納
data=line[0].split(" ")
max_power = int(data[0])
balance = int(data[1])
shouritu_count = int(data[2])
player_all =[[max_power-i] for i in range(max_power)]
for i in range(max_power):
    if i == 0:
        player_all[i].append(1)
    elif i < max_power-1:
        player_all[i].append((player_all[i-1][1])*2)
    else:
        player_all[i].append((player_all[i-1][1])*2+1)

# トーナメント参加者を出力
for i in player_all:
    print("実力:"+str(i[0])+"が"+str(i[1])+"人、", end="")
print("")
print("合計" + str(2**max_power) + "人で" + str(shouritu_count) + "回トーナメントを行います")

# ランダムなトーナメント表の作成
import random
def make_tornament(a=player_all):
    tornament_list = []
    for i in a:
        count = 0
        while (count < i[1]):
            ran_num = random.random()
            while (ran_num in tornament_list):
                ran_num = random.random()
            tornament_list.append([i[0],ran_num])
            count +=1
    tornament_list.sort(key = lambda x:x[1])
    for i,j in enumerate(tornament_list):
        j.insert(0,i+1)
        del j[2]
    return tornament_list

# プレイヤー、実力値、実力上位者の勝率、を引き値にして、勝者プレイヤーを返す
def battle(player_a , skill_a , player_b , skill_b , shouritu = balance):

    flag = 0
    if skill_a > skill_b:
        flag = 1
        for i in range(skill_a - skill_b):
            ran_num_a = shouritu
            ran_num_b = random.random()*100
            while (ran_num_b == ran_num_a):
                ran_num_a = random.random()*100
                ran_num_b = random.random()*100
            if ran_num_a > ran_num_b:
                flag = 0
    elif skill_a < skill_b:
        for i in range(skill_b - skill_a):
            ran_num_b = shouritu
            ran_num_a = random.random()*100
            while (ran_num_b == ran_num_a):
                ran_num_a = random.random()*100
                ran_num_b = random.random()*100
            if ran_num_b > ran_num_a:
                flag = 1
    else:
        ran_num_b = random.random()*100
        ran_num_a = random.random()*100
        while (ran_num_b == ran_num_a):
            ran_num_b = random.random()*100
        if ran_num_b > ran_num_a:
                flag = 1
    if flag ==0:
        return player_a
    else:
        return player_b


import copy

# 実力ごとの勝利回数を格納するリスト
shouritu_list = [0 for i in range(max_power)]

# トーナメントが開かれる回数Ｉだけループする
count = 1
while(count <= shouritu_count):

    # 新規トーナメント表の作成
    tornament_list = make_tornament(player_all)

    # トーナメントの勝者が決まるまでループする
    while (len(tornament_list)>1):

        # 試合の敗者を格納する
        loser_list=[]
        battle_count =0

        # 敗者が決まるまでループする
        while (battle_count<len(tornament_list)):
            winner = battle(tornament_list[battle_count][0],tornament_list[battle_count][1],tornament_list[battle_count+1][0],tornament_list[battle_count+1][1])
            if  winner == tornament_list[battle_count][0]:
                loser_list.append(tornament_list[battle_count+1])
            else:
                loser_list.append(tornament_list[battle_count])
            battle_count +=2

        # 敗者をトーナメント表から削除する
        for i in loser_list:
            if i in tornament_list:
                tornament_list.remove(i)

    # 勝者の実力のカウントを1増やす
    shouritu_list[tornament_list[0][1]-1]+=1
    count += 1

# 解答
for i,j in enumerate(shouritu_list):
    print("実力：" + str(i+1) + "の人は" + str(j) + "回優勝しました、勝率は" + str(round(j/shouritu_count*100, 1)) + "％です")
