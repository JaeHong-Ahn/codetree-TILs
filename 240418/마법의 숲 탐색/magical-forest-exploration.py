from collections import deque

def down(g):
    while True:
        
        d0_condition = g[0] <= R

        if not d0_condition:
            return False

        d1_condition = v[g[0] + 2][g[1]] == 0
        if not d1_condition:
            return False

        d2_condition = v[g[0] + 1][g[1] - 1] == 0
        if not d2_condition:
            return False

        d3_condition = v[g[0] + 1][g[1] + 1] == 0
        if not d3_condition:
            return False

        g[0] += 1

#서쪽 한칸이 싹 비어 있어야 함
def turn_left(g):
    while True:
        # 조건이 하나라도 맞지 않으면 바로 return False 하는 걸로 수정
        l1_condition = g[0] <= R
        if not l1_condition:
            return False

        l2_condition = g[1] >= 2
        if not l2_condition:
            return False

        l3_condition = v[g[0]+1][g[1]-1] == 0
        if not l3_condition:
            return False

        l4_condition = v[g[0]+2][g[1]-1] == 0
        if not l4_condition:
            return False

        l5_condition = v[g[0]+1][g[1]-2] == 0
        if not l5_condition:
            return False

        l6_condition = v[g[0]][g[1] - 2] == 0
        if not l6_condition:
            return False

        l7_condition = v[g[0]-1][g[1] - 1] == 0
        if not l7_condition:
            return False

        g[0] += 1
        g[1] -= 1

        if g[2] == 0:
            g[2] = 3

        elif g[2] == 1:
            g[2] = 0

        elif g[2] == 2:
            g[2] = 1

        elif g[2] == 3:
            g[2] = 2

#동쪽 한칸이 싹 비어 있어야 함
def turn_right(g):
    while True:
        l1_condition = g[0] <= R
        if not l1_condition:
            return False

        l2_condition = (g[1] + 3) <= C
        if not l2_condition:
            return False

        l3_condition = v[g[0] + 1][g[1] + 1] == 0
        if not l3_condition:
            return False

        l4_condition = v[g[0] + 2][g[1] + 1] == 0
        if not l4_condition:
            return False

        l5_condition = v[g[0] + 1][g[1] + 2] == 0
        if not l5_condition:
            return False

        l6_condition = v[g[0]][g[1] + 2] == 0
        if not l6_condition:
            return False

        l7_condition = v[g[0] - 1][g[1] + 1] == 0
        if not l7_condition:
            return False

        g[0] += 1
        g[1] += 1

        if g[2] == 0:
            g[2] = 1

        elif g[2] == 1:
            g[2] = 2

        elif g[2] == 2:
            g[2] = 3

        elif g[2] == 3:
            g[2] = 0

#평범한 길은 1, 출구는 2, 중앙 지점은 3
# 3 -> 2 -> 1 -> 3 -> 2 -> 1 순으로 나아가야 함 !!
def locate(g, v):
    #골렘 중앙
    v[g[0]][g[1]] = 3

    #골렘의 가장 좌측
    if g[2] == 3:
        v[g[0]][g[1] - 1] = 2
    else:
        v[g[0]][g[1] - 1] = 1

    # 골렘의 가장 우측
    if g[2] == 1:
        v[g[0]][g[1] + 1] = 2
    else:
        v[g[0]][g[1] + 1] = 1

    #골렘의 가장 윗부분
    if g[2] == 0:
        v[g[0] - 1][g[1]] = 2
    else:
        v[g[0] - 1][g[1]] = 1

    #골렘의 가장 아랫부분
    if g[2] == 2:
        v[g[0] + 1][g[1]] = 2
    else:
        v[g[0] + 1][g[1]] = 1

#v[:3] -> 이중 1인 값이 하나라도 있으면 refresh()
def refresh(v):
    for visited in v[:3]:
        if 1 in visited or 2 in visited:
            return True

#중앙에서 출구로 향할 때보다 그냥 아랫 방향으로 가는 경우도 있음
def total_score(g, v):
    dr = [0, 0, 1, -1]
    dc = [1, -1, 0, 0]
    row, col = g[0], g[1]
    q = deque()
    q.append((row, col))

    new_map = [[0 for _ in range(C)] for _ in range(R + 3)]
    new_map[row][col] = 1
    max_row = row

    while q:
        r, c = q.popleft()
        new_max = -1e9

        for j in range(4):
            nr = r + dr[j]
            nc = c + dc[j]

            move_condition1 = 0 <= nr < (R+3) and 0 <= nc < C

            # 평범한 길은 1, 출구는 2, 중앙 지점은 3
            # 3 -> 2 -> 1 -> 3 -> 2 -> 1 순으로 나아가야 함 !!
            if move_condition1:
                move_condition2 = new_map[nr][nc] == 0 and v[nr][nc] != 0
                if move_condition2:
                    # 현재 위치가 평범한 길 1, 2 -> 다음 길은 중앙 3
                    if (v[r][c] == 1 or v[r][c] == 2) == 1 and v[nr][nc] == 3:
                        new_map[nr][nc] = 1
                        q.append((nr, nc))

                    # 현재 위치가 출구 2 -> 다음 길은 출구가 될 수도 있고 평범한 길이 될 수도 있음 3, 1
                    elif v[r][c] == 2 and (v[nr][nc] == 3 or v[nr][nc] == 1):
                        new_map[nr][nc] = 1
                        q.append((nr, nc))

                    # 현재 위치가 중앙 3 -> 다음 길은 출구 2
                    elif v[r][c] == 3 and v[nr][nc] == 2:
                        new_map[nr][nc] = 1
                        q.append((nr, nc))

                    max_row = nr if max_row < nr else max_row


    return max_row - 2

R, C, K = map(int, input().split())

#골렘의 위치가 순서대로 들어옴
#[골렘 중심의 열, 출구 방향]
gollem = []
for _ in range(K):
    c, exit = map(int, input().split())
    gollem.append([1, c-1, exit])

#골렘이 있는 칸 -> 1 비어있는 칸 -> 0
v = [[0 for _ in range(C)] for _ in range(R+3)]
ans = 0
for k in range(K):
    down(gollem[k])
    turn_left(gollem[k])
    turn_right(gollem[k])
    locate(gollem[k], v)

    #refresh가 잘 안돼고 있음
    if refresh(v):
        v = [[0 for _ in range(C)] for _ in range(R + 3)]
        continue
    ans += total_score(gollem[k], v)

print(ans)