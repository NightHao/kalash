import copy
import heapq
ans_action = 0
upper = 0
index_check = 0

def relocate(house, picked_house): #撒種子
    tmp_remain = remain = house[picked_house]
    start = index = picked_house
    check = False
    while remain > 1:
        index += 1
        if index >= 14:
            index = 0
        if 0 <= start < 6 and index == 13:
            index = 0
        elif 7 <= start < 13 and index == 6:
            index += 1
        house[index] += 1
        remain -= 1
    index += 1
    if index > 13: index = 0
    if 0 <= start < 6:
        if index == 13:
            index = 0
        if index == 6:
            house[index] += 1
            check = True
        else:
            if 0 <= index < 6 and house[index] == 0:
                if house[12-index]==0:
                    house[index] += 1
                else:
                    house[6] += house[12-index] + 1
                    house[12-index] = 0
            else:
                house[index] += 1
    elif 7 <= start < 13:
        if index == 6:
            index += 1
        if index == 13:
            house[index] += 1
            check = True
        else:
            if 7 <= index < 13 and house[index] == 0:
                if house[12-index] == 0:
                    house[index] += 1
                else:
                    house[13] += house[12-index] + 1
                    house[12-index] = 0
            else:
                house[index] += 1
    house[start] -= tmp_remain
    transfer = True
    for i in range(6):
        if house[i] != 0:
            transfer = False
    if transfer:
        for i in range(7,13):
            house[13] += house[i]
            house[i] = 0
    transfer = True
    for i in range(7,13):
        if house[i] != 0:
            transfer = False
    if transfer:
        for i in range(6):
            house[6] += house[i]
            house[i] = 0
    if check:
        return True
    else:
        return False

def change_player(turn) -> int:
    if turn == 0:
        return 1
    else:
        return 0

def check_end(house): #是否結束
    for i in range(13):
        if house[i] > 0:
            return False
        if i == 5:
            i = 6
    return True

def search(house, action, depth, alpha, beta, turn, who, skip):
    if depth == 0 or check_end(house):
        if turn == 0:
            return house[6] - house[13]
        else:
            return house[13] - house[6]
    global ans_action
    global upper
    global index_check
    state = []
    if who == turn: #要max
        if skip: #被跳過
            tmp_skip = False
            child = search(house, action, depth - 1, alpha, beta, change_player(turn), who, tmp_skip)
            if child > alpha:
                alpha = child
        else:
            if turn == 0:
                for i in range(6):
                    if house[i] > 0:
                        tmp_house = copy.deepcopy(house)
                        if relocate(tmp_house,i):
                            state.append((tmp_house[6]-tmp_house[13], i, tmp_house, True))
                        else:
                            state.append((tmp_house[6]-tmp_house[13], i, tmp_house, False))
                state = sorted(state, reverse=True, key = lambda state: state[0])
                for p, i, tmp_house, tmp_skip in state:
                    child = float('-inf')
                    child = search(tmp_house, i, depth - 1, alpha, beta, change_player(turn), who, tmp_skip)
                    if child > alpha:
                        alpha = child
                        if depth == upper:
                            ans_action = i
                    if alpha >= beta:
                        break
                    
            else:
                for i in range(7,13):
                    if house[i] > 0:
                        tmp_house = copy.deepcopy(house)
                        if relocate(tmp_house,i):
                            state.append((tmp_house[13]-tmp_house[6], i, tmp_house, True))
                        else:
                            state.append((tmp_house[13]-tmp_house[6], i, tmp_house, False))
                state = sorted(state, reverse=True, key= lambda state: state[0])
                for p, i, tmp_house, tmp_skip in state:
                    child = float('-inf')
                    child = search(tmp_house, i, depth - 1, alpha, beta, change_player(turn), who, tmp_skip)
                    if child > alpha:
                        alpha = child
                        if depth == upper:
                            ans_action = i
                    if alpha >= beta:
                        break
        return alpha
    else: #要min
        if skip:#被跳過
            tmp_skip = False
            child = search(house, action, depth - 1, alpha, beta, change_player(turn), who, tmp_skip)
            if child < beta:
                beta = child
        else:
            if turn == 0:
                for i in range(6):
                    if house[i] > 0:
                        tmp_house = copy.deepcopy(house)
                        if relocate(tmp_house,i):
                            state.append((tmp_house[6]-tmp_house[13], i,tmp_house, True))
                        else:
                            state.append((tmp_house[6]-tmp_house[13], i,tmp_house, False))
                state = sorted(state, key = lambda state: state[0])
                for p, i, tmp_house, tmp_skip in state:
                    child = float('inf')
                    child = search(tmp_house, i, depth - 1 , alpha, beta, change_player(turn), who, tmp_skip)
                    if child < beta:
                        beta = child
                    if alpha >= beta:
                        break
            else:
                for i in range(7,13):
                    if house[i] > 0:
                        tmp_house = copy.deepcopy(house)
                        if relocate(tmp_house,i):
                            state.append((tmp_house[13]-tmp_house[6], i,tmp_house, True))
                        else:
                            state.append((tmp_house[13]-tmp_house[6], i,tmp_house, False))
                state = sorted(state, key = lambda state: state[0])
                for p, i, tmp_house, tmp_skip in state:
                    child = float('inf')
                    child = search(tmp_house, i, depth - 1, alpha, beta, change_player(turn), who, tmp_skip)
                    if child < beta:
                        beta = child
                    if alpha >= beta:
                        break
        return beta

n = int(input())
for i in range(n):
    state = str(input())
    limit = len(state)
    turn = int(input())
    depth_max = int(input())
    state = state[1:-1].split(' ')
    state = [int(x) for x in state]
    upper = depth_max
    alpha = search(state, 0, depth_max, float("-inf"), float("inf"), turn, turn, False)
    print(ans_action)