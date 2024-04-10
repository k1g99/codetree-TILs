from collections import deque

N, M, H, K = list(map(int, input().split()))

runner = [[-1, -1]]  # runner 들의 현재 좌표 (rid 0은 없음)
runner_dir = [0]  # 바라보고 있는 방향
runner_alive = [True for _ in range(M + 1)]  # runner 생존 여부
runner_alive[0] = False
runner_board = [[[] for _ in range(N)] for _ in range(N)]  # runner 보드
dir = [[0, 1], [1, 0], [0, -1], [-1, 0]]  # 우 하 좌 상

tree_board = [[False for _ in range(N)] for _ in range(N)]

soolae = [N // 2, N // 2]  # 술래 현재 좌표
soolae_dir = 0  # 술래 바라보는 방향
s_dir = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # 상 우 하 좌
s_moves = 1
soolae_dir_board = [[False for _ in range(N)] for _ in range(N)]
order = 0

for m in range(1, M + 1):
    x, y, d = list(map(int, input().split()))
    #  1인 경우 좌우로 움직임을, 2인 경우 상하로만 움
    runner.append([x - 1, y - 1])
    if (d == 1):
        runner_dir.append(0)
    else:
        runner_dir.append(1)
    runner_board[x - 1][y - 1].append(m)

for h in range(H):
    x, y = list(map(int, input().split()))
    tree_board[x - 1][y - 1] = True

answer = 0


def get_dir(a, b):
    ar, ac = a
    br, bc = b
    return abs(ar - br) + abs(ac - bc)


def check_border(a):
    r, c = a
    return r >= 0 and c >= 0 and r < N and c < N


def init_soolae_path():
    point_dir = 0

    sr, sc = [N // 2, N // 2]
    soolae_dir_board[sr][sc] = True

    for i in range(1, N):
        sr, sc = [sr + s_dir[point_dir][0] * i, sc + s_dir[point_dir][1] * i]
        point_dir = (point_dir + 1) % 4
        soolae_dir_board[sr][sc] = True

        sr, sc = [sr + s_dir[point_dir][0] * i, sc + s_dir[point_dir][1] * i]
        point_dir = (point_dir + 1) % 4
        soolae_dir_board[sr][sc] = True

    soolae_dir_board[0][0] = True


def bfs(s):
    visited = [[False for _ in range(N)] for _ in range(N)]
    ret = []

    que = deque()
    que.append([s[0], s[1], 0])
    visited[s[0]][s[1]] = True

    while (que):
        cr, cc, depth = que.popleft()
        if (runner_board[cr][cc]):
            for x in runner_board[cr][cc]:
                ret.append(x)

        if (depth >= 3):
            continue

        for dr, dc in dir:
            nr, nc = [cr + dr, cc + dc]
            if (check_border([nr, nc]) and not visited[nr][nc]):
                visited[nr][nc] = True
                que.append([nr, nc, depth + 1])

    return ret


def sool_move(s):
    r, c = s
    global order, soolae_dir

    if (order == 0):  # 정방향
        nr, nc = [r + s_dir[soolae_dir][0], c + s_dir[soolae_dir][1]]
        if ([nr, nc] == [0, 0]):
            soolae_dir = 2
            order = 1

        if (soolae_dir_board[nr][nc] == True):
            soolae_dir = (soolae_dir + 1) % 4
        return [nr, nc]

    if (order == 1):  # 역방향
        nr, nc = [r + s_dir[soolae_dir][0], c + s_dir[soolae_dir][1]]
        if ([nr, nc] == [N // 2, N // 2]):
            soolae_dir = 0
            order = 0

        if (soolae_dir_board[nr][nc] == True):
            soolae_dir = (soolae_dir - 1) % 4
        return [nr, nc]

init_soolae_path()
for k in range(1, K + 1):
    # 1. 도망자 이동
    # - 현재 술래와 거리가 3 이하인 도망자만 선정 (술래 좌표를 기준으로 거리가 3인 지점들만 찾는 게 좋을듯) bfs 쓰자
    move_runner = bfs(soolae)
    for rid in move_runner:
        cr, cc = runner[rid]
        rd = runner_dir[rid]
        nr, nc = [cr + dir[rd][0], cc + dir[rd][1]]
        # - 현재 바라보고 있는 방향으로 1 이동할 때, 격자 밖인경우
        if (not check_border([nr, nc])):
            # - 반대로 방향을 튼다
            runner_dir[rid] = (runner_dir[rid] + 2) % 4
            rd = runner_dir[rid]
            # -> 1 이동하려고 한다
            nr, nc = [cr + dir[rd][0], cc + dir[rd][1]]

        # - 술래가 있다 -> 가만히 있는다.
        # - 술래가 없다 -> 움직인다.
        if ([nr, nc] != soolae):
            runner[rid] = [nr, nc]
            runner_board[cr][cc].remove(rid)
            runner_board[nr][nc].append(rid)

    # 2. 술래 이동
    # - 달팽이 모양 이동 ([n//2, n//2] -> 위1 -> 오른1 -> 아래2 -> 왼2)
    # - 이동 방향이 틀어지는 지점이라면 술래가 바라보는 방향 바로 틀기
    soolae = sool_move(soolae)

    # - 바라보는 방향으로 3칸 (0, 1, 2)동안
    for i in range(3):
        watching = [soolae[0] + s_dir[soolae_dir][0] * i, soolae[1] + s_dir[soolae_dir][1] * i]
        # - 나무가 있는 칸이 아니라면 도망자 잡기
        if (not tree_board[watching[0]][watching[1]]):
            if (runner_board[watching[0]][watching[1]]):
                for rid in runner_board[watching[0]][watching[1]]:
                    runner_alive[rid] = False
                    rid_r, rid_c = runner[rid]
                    runner_board[rid_r][rid_c].remove(rid)
                    answer += k

print(answer)