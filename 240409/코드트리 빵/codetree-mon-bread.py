# 1. 최단거리로 움직임, 상 좌 우 하 순서
# 2. 편의점에 도착한다면, 해당 칸은 이동 불가 (단, 해당 "분"이 끝난 다음부터)
# 3. [시작위치] 선정 t <= m 이라면, t번 사람은 가장 가까운 베이스캠프에 들어감. (행이작음, 열이작음) (해당 "분"이 끝난 다음부터 해당 칸 이동 불가)
from collections import deque

dir = [[-1, 0], [0, -1], [0, 1], [1, 0]]
dir_2 = [[1, 0], [0, 1], [0, -1], [-1, 0]]

N, M = list(map(int, input().split()))

board = [list(map(int, input().split())) for _ in range(N)]  # -1이면 못감
# can_go = [[True for _ in range(N)] for _ in range(N)]
man_target_store = []
for _ in range(M):
    r, c = list(map(int, input().split()))
    man_target_store.append([r - 1, c - 1])
man_path_to_store = [deque() for _ in range(M)]
man_current = [[] for _ in range(M)]
man_in_store = 0
man_end = [False for _ in range(M)]


def check_bound(cell):
    r, c = cell
    return r >= 0 and c >= 0 and r < N and c < N


def find_basecamp(start):
    visited = [[False for _ in range(N)] for _ in range(N)]
    back_track = [[[] for _ in range(N)] for _ in range(N)]
    que = deque()
    visited[start[0]][start[1]] = True
    que.append([start[0], start[1], 0])
    bc_depth = 99999999
    bc_candidate = []
    ret = deque()

    while (que):
        cr, cc, depth = que.popleft()
        if (depth > bc_depth):
            break
        for d in dir_2:  # 꺼꾸로
            nr, nc = [cr + d[0], cc + d[1]]
            if (check_bound([nr, nc]) and board[nr][nc] != -1 and not visited[nr][nc]):
                if (board[nr][nc] == 1):  # 베이스캠프인 경우!
                    if (bc_depth == 99999999):
                        bc_depth = depth + 1
                        bc_candidate.append([nr, nc])
                        back_track[nr][nc] = [cr, cc]
                    elif (bc_depth == depth + 1):
                        bc_candidate.append([nr, nc])
                        back_track[nr][nc] = [cr, cc]
                    # else:
                    #     print("무슨경우지")
                else:
                    visited[nr][nc] = True
                    que.append([nr, nc, depth + 1])
                    back_track[nr][nc] = [cr, cc]

    bc_candidate.sort()
    bc_r, bc_c = bc_candidate[0]
    ret.append([bc_r, bc_c])
    bc_nr, bc_nc = back_track[bc_r][bc_c]
    ret.append([bc_nr, bc_nc])

    while ([bc_nr, bc_nc] != start):
        bc_nr, bc_nc = back_track[bc_nr][bc_nc]
        ret.append([bc_nr, bc_nc])

    return ret


def find_path(start, end):
    visited = [[False for _ in range(N)] for _ in range(N)]
    back_track = [[[] for _ in range(N)] for _ in range(N)]

    que = deque()
    que.append(start)
    visited[start[0]][start[1]] = True

    while (que):
        cr, cc = que.popleft()

        for dr, dc in dir:
            nr, nc = [cr + dr, cc + dc]
            if (check_bound([nr, nc]) and board[nr][nc] != -1 and not visited[nr][nc]):
                visited[nr][nc] = True
                que.append([nr, nc])
                back_track[nr][nc] = [cr, cc]

                if ([nr, nc] == end):
                    break
    ret = deque()
    bc_r, bc_c = end
    bc_nr, bc_nc = back_track[bc_r][bc_c]
    ret.append([bc_r, bc_c])
    ret.append([bc_nr, bc_nc])

    while ([bc_nr, bc_nc] != start):
        bc_nr, bc_nc = back_track[bc_nr][bc_nc]
        ret.append([bc_nr, bc_nc])

    return ret


t = 0
while man_in_store < len(man_target_store):
    fix_cell = []
    for m in range(M):
        if(man_end[m]):
            continue

        if (t > m):
            # 최단거리 -> 가지고 있기
            cr, cc = man_current[m]

            # 최단거리로 1칸 움직일 수 있는지 확인
            nr, nc = man_path_to_store[m][0]

            # 만약 편의점 도착했다면, man_in_store += 1
            if ([nr, nc] == man_target_store[m]):
                fix_cell.append([nr, nc])
                # 이번 t 끝나고 못움직일 칸 표시하기
                man_in_store += 1
                man_end[m] = True
                continue

            if (board[nr][nc] == -1):
                # 못움직이면 해당 칸에서 다시 dfs 실시 후 이동 + paths 업데이트
                new_route = find_path([cr, cc], man_target_store[m])
                man_path_to_store[m] = new_route

                nr, nc = man_path_to_store[m][0]

                # 이동
            man_current[m] = [nr, nc]
            man_path_to_store[m].popleft()

        elif (t == m):
            # 처음 베이스 캠프에 들어가는거
            target_store = man_target_store[m]

            # 베이스캠프 찾기 (여러 가지인 경우에는 그 중 행이 작은 베이스캠프, 행이 같다면 열이 작은 베이스 캠프)
            route = find_basecamp(target_store)
            bc = route.popleft()
            man_path_to_store[m] = route

            # 이번 t 끝나고 못움직일 칸(베이스캠프) 표시하기
            fix_cell.append(bc)
            man_current[m] = bc
        else:
            continue

    # 못움직일 칸 고정하기
    for fr, fc in fix_cell:
        board[fr][fc] = -1
    # print(t)
    # print(man_current)
    # print('-' * 10)
    t += 1

print(t)