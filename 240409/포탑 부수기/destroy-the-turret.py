from collections import deque

N, M, K = list(map(int, input().split()))

board = []
# bfs_paths = [[[]] for _ in range(M)] for _ in range(N)]
pt_counter = N * M
last_attack = [[0 for _ in range(M)] for _ in range(N)]
free_this_turn = [[True for _ in range(M)] for _ in range(N)]

for n in range(N):
    row = list(map(int, input().split()))
    for m in range(M):
        if (row[m] == 0):
            pt_counter -= 1
    board.append(row)

dir = [[0, 1], [1, 0], [0, -1], [-1, 0]]  # 우/하/좌/상
every_dir = [[-1, -1], [0, -1], [1, -1], [0, -1], [0, 1], [-1, 1], [0, 1], [1, 1]]


def check_bound(a):
    c, r = a
    return c >= 0 and r >= 0 and r < N and c < N


def bfs(start, end):
    bfs_paths = [[[] for _ in range(M)] for _ in range(N)]

    que = deque()
    que.append(start)
    bfs_paths[start[0]][start[1]].append(start)

    while (que):
        cr, cc = que.popleft()
        for d in dir:
            nr, nc = [(cr + d[0]) % N, (cc + d[1]) % M]
            if (len(bfs_paths[nr][nc]) == 0 and board[nr][nc] > 0):
                bfs_paths[nr][nc] = bfs_paths[cr][cc][:]
                bfs_paths[nr][nc].append([nr, nc])
                que.append([nr, nc])
            if ([nr, nc] == end):
                return bfs_paths[nr][nc]

    return []


for k in range(1,K+1):
    # 턴 - 부서지지 않은 포탑이 1개가 된다면 그 즉시 중지
    if (pt_counter == 1):
        break
    free_this_turn = [[True for _ in range(M)] for _ in range(N)]

    attacker = []
    target = []
    # 1. 공격자, 타겟 선정 | 0이 아닌 가장 약한 포탑, 가장 강한 포탑
    for n in range(N):
        for m in range(M):
            if (board[n][m] > 0):
                # [공격력, -최근 공격, -(행+열), -열]
                attacker.append([board[n][m], -1 * last_attack[n][m], -1 * (m + n), -1 * n])
                # [-공격력, 최근 공격, 행+열, 열]
                target.append([-1 * board[n][m], last_attack[n][m], (m + n), n])
    attacker.sort()
    target.sort()

    attack_r, attack_c = [-1 * attacker[0][3], attacker[0][3] - attacker[0][2]]
    target_r, target_c = [target[0][3], target[0][2] - target[0][3]]
    last_attack[attack_r][attack_c] = k
    free_this_turn[attack_r][attack_c] = False
    free_this_turn[target_r][target_c] = False

    # 2. 공격자가 공격
    #     (N+M만큼 공격력 증가)
    board[attack_r][attack_c] += (N + M)
    attack_pow = board[attack_r][attack_c]
    #     2.0 최단경로 확인
    shortest_path = bfs([attack_r, attack_c], [target_r, target_c])

    if (shortest_path != []):
        #     2.1 최단경로가 있다면, 레이저 공격 먼저 시도
        #         피해 : 경로 상 포탑 (공격력//2) (우/하/좌/상의 우선순위대로 경로)
        for pr, pc in shortest_path[1:-1]:
            if(board[pr][pc] < 0):
                continue
            board[pr][pc] -= (attack_pow // 2)
            free_this_turn[pr][pc] = False
            if (board[pr][pc] <= 0):
                pt_counter -= 1
        board[target_r][target_c] -= attack_pow
        if (board[target_r][target_c] <= 0):
            pt_counter -= 1
    #     2.2 최단경로가 없다면, 포탄 공격
    #         피해 : 타켓의 주변 모든 포탑 (공격력//2)
    #         단, 공격자는 타격 없음
    else:
        board[target_r][target_c] -= attack_pow
        for ed in every_dir:
            nr, nc = [(target_r + ed[0])%N, (target_c + ed[1])%M]
            if check_bound([nr, nc]) and board[nr][nc] > 0 and [nr, nc] != [attack_r, attack_c]:
                board[nr][nc] -= (attack_pow // 2)
                free_this_turn[nr][nc] = False
                if (board[nr][nc] <= 0):
                    pt_counter -= 1

    # 3. 포탑 부서짐

    # 4. 포탑 정비 -> 공격도 안하고, 타격도 없는 포탑은 +1
    for r in range(N):
        for c in range(M):
            if (free_this_turn[r][c] and board[r][c] > 0):
                board[r][c] += 1

print(max(map(max, board)))