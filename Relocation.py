n, times = int(input()), 0
for i in range(n):
    state = str(input())
    limit = len(state)
    state = state[1:limit-2].split(' ')
    state = [int(x) for x in state]
    picked_house = int(input())
    tmp_remain = remain = state[picked_house]
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
        state[index] += 1
        remain -= 1
    index += 1
    if index > 13: index = 0
    if 0 <= start < 6:
        if index == 13:
            index = 0
        if index == 6:
            state[index] += 1
            check = True
        else:
            if 0 <= index < 6 and state[index] == 0:
                if state[12-index]==0:
                    state[index] += 1
                else:
                    state[6] += state[12-index] + 1
                    state[12-index] = 0
            else:
                state[index] += 1
    elif 7 <= start < 13:
        if index == 6:
            index += 1
        if index == 13:
            state[index] += 1
            check = True
        else:
            if 7 <= index < 13 and state[index] == 0:
                if state[12-index] == 0:
                    state[index] += 1
                else:
                    state[13] += state[12-index] + 1
                    state[12-index] = 0
            else:
                state[index] += 1
    state[start] -= tmp_remain
    state = [str(x) for x in state]
    state = "["+" ".join(state)+"]"
    print(state)
    if check:
        print("YES")
    else:
        print("NO")