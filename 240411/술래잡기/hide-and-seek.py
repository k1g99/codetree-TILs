from collections import deque

answer = 0
N, M, H, K = list(map(int, input().split()))

dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # 상 / 우 / 하 / 좌 (시계방향)

runner_loc = []
runner_dir = []
runner_alive = M
runner_board = [[[] for _ in range(N)] for _ in range(N)]

tree_board = [[False for _ in range(N)] for _ in range(N)]

sul_loc = [N // 2, N // 2]
sul_dir = 0
sul_path_board = [[False for _ in range(N)] for _ in range(N)]
sul_clock = True

for m in range(M):
    x, y, d = list(map(int, input().split()))
    runner_loc.append([x - 1, y - 1])
    runner_dir.append(d)
    runner_board[x - 1][y - 1].append(m)

for h in range(H):
    x, y = list(map(int, input().split()))
    tree_board[x - 1][y - 1] = True


###### 알고리즘
def check_border(a):
    r, c = a
    return r >= 0 and c >= 0 and r < N and c < N


def bfs(curr):
    ret = []
    que = deque()
    visited = [[False for _ in range(N)] for _ in range(N)]

    cr, cc = curr
    que.append([cr, cc, 0])
    visited[cr][cc] = True

    while (que):
        tr, tc, depth = que.popleft()
        if (runner_board[tr][tc]):
            for rid in runner_board[tr][tc]:
                ret.append(rid)

        if (depth == 3):
            continue

        for dr, dc in dirs:
            nr, nc = [tr + dr, tc + dc]

            if (check_border([nr, nc]) and not visited[nr][nc]):
                que.append([nr, nc, depth + 1])
                visited[nr][nc] = True

    return ret


def init_sul_path():
    sr, sc = [N // 2, N // 2]
    sul_path_board[sr][sc] = True
    sul_path_board[0][0] = True
    s_dir = 0

    for i in range(1, N):
        sr, sc = [sr + dirs[s_dir][0] * i, sc + dirs[s_dir][1] * i]
        sul_path_board[sr][sc] = True
        s_dir = (s_dir + 1) % 4

        sr, sc = [sr + dirs[s_dir][0] * i, sc + dirs[s_dir][1] * i]
        sul_path_board[sr][sc] = True
        s_dir = (s_dir + 1) % 4



def move_sul():
    global sul_dir, sul_loc, sul_clock
    sr, sc = sul_loc
    nr, nc = [sr + dirs[sul_dir][0], sc + dirs[sul_dir][1]]

    if([nr, nc] == [0,0]):
        sul_dir = 2
        sul_clock = False # 시계방향으로 돌고있는지,
    elif([nr, nc] == [N//2,N//2]):
        sul_dir = 0
        sul_clock = True

    elif(sul_path_board[nr][nc]):
        # 방향 바꾸기
        if(sul_clock):
            sul_dir = (sul_dir + 1) % 4
        else:
            sul_dir = (sul_dir - 1) % 4

    sul_loc = [nr, nc]


init_sul_path()
# print(sul_path_board)
for k in range(1, K + 1):
    if runner_alive == 0:
        break
    # 1. 도망자 움직임

    # - 술래와의 거리가 3 이하인 도망자만 선정 -> bfs()로 선정
    move_runner = bfs(sul_loc)
    # print(t, move_runner)
    for runner_id in move_runner:
        #     - 바라보고 있는 방향으로 1 이동이 불가한 경우, 반대로 방향을 틀기
        rr, rc = runner_loc[runner_id]
        rd = runner_dir[runner_id]
        nr, nc = [rr + dirs[rd][0], rc + dirs[rd][1]]
        if (not check_border([nr, nc])):
            runner_dir[runner_id] = (runner_dir[runner_id] + 2) % 4
            rd = runner_dir[runner_id]
            nr, nc = [rr + dirs[rd][0], rc + dirs[rd][1]]

        #     - 다음 칸에 술래가 없는 경우만 이동
        if ([nr, nc] != sul_loc):
            runner_board[rr][rc].remove(runner_id)
            runner_board[nr][nc].append(runner_id)
            runner_loc[runner_id] = [nr, nc]

    # 2. 술래 움직임
    # - 술래 다음칸으로 이동 (달팽이모양)
    move_sul()
    # print(sul_loc, dirs[sul_dir])

    # - 도망자 잡기 (현재 포함 3칸)
    for i in range(3):
        sr, sc = sul_loc
        catch_r, catch_c = [sr + dirs[sul_dir][0]*i, sc + dirs[sul_dir][1]*i]
        if(check_border([catch_r, catch_c]) and not tree_board[catch_r][catch_c] and runner_board[catch_r][catch_c]):
            point = len(runner_board[catch_r][catch_c])
            answer += (k*point)
            runner_alive -= point
            runner_board[catch_r][catch_c] = []

print(answer)