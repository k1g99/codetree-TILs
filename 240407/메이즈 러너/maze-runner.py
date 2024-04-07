N, M, K = list(map(int, input().split()))

answer_moves = 0  # 모든 참가자들의 이동 거리 합

wall_board = []
game_board = [[[] for _ in range(N )] for _ in range(N )]
game = [[0, 0] for _ in range(M + 2)]  # 0 / 1~M : 참가자 / M+1 : exit
# exit = []   # 출구 좌표 [r,c]
isAlive = [True for _ in range(M + 2)]
isAlive[0] = False
isAlive[M+1] = False

for r in range(N):
    row = list(map(int, input().split()))
    wall_board.append(row)

for m in range(M):
    r, c = list(map(int, input().split()))
    game_board[r - 1][c - 1].append(m+1)
    game[m + 1] = [r - 1, c - 1]
_exit = list(map(int, input().split()))
game[M + 1] = [_exit[0] - 1, _exit[1] - 1]
game_board[_exit[0] - 1][_exit[1] - 1].append(M+1)

dir = [[-1, 0], [1, 0], [0, -1], [0, 1]]
rotate_dir_s = [[0, 1], [1, 0], [0, -1], [-1, 0]]
rotate_dir_t = [[1, 0], [0, -1], [-1, 0], [0, 1]]


def check_bound(a):
    r, c = a
    return r >= 0 and c >= 0 and r < N and c < N


def get_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_width(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

### 여기가 문제였음!!! 생각했던 알고리즘이 제대로 동작하지 않은 엣지 케이스들이 있을 수 있음
### 처음부터 최적화하려하지 말고, 일단 BF으로 찾는다고 생각해보기 -> 2번 생각
def get_start(sq_start, find_width): 
    for sq_r in range(sq_start[0], game[M+1][0]+1):
        for sq_c in range(sq_start[1], game[M + 1][1] + 1):
            sq_end = [sq_r + sq_width, sq_c + sq_width]
            for fw, fr, fc in find_width:
                if(sq_start[0] <= fr and sq_start[1]<=fc and sq_end[0]>=fr and sq_end[1]>=fc):
                    return [sq_r, sq_c]

def rotate(start, width):
    sr, sc = start
    tr, tc = [sr, sc + width - 1]
    if (width == 1):
        wall_board[sr][sc] = max(0, wall_board[sr][sc] - 1)
        return

    for rdi in range(4):
        for i in range(width - 1):
            wall_board[tr][tc] = max(0, wall_board_cp[sr][sc] - 1)
            if (game_board_cp[sr][sc]):  # 좌표 갱신
                game_id = game_board_cp[sr][sc]
                for gi in game_id:
                    game[gi] = [tr, tc]
            game_board[tr][tc] = game_board_cp[sr][sc]
            sr, sc = [sr + rotate_dir_s[rdi][0], sc + rotate_dir_s[rdi][1]]
            tr, tc = [tr + rotate_dir_t[rdi][0], tc + rotate_dir_t[rdi][1]]


game_board_cp = []
wall_board_cp = []

for k in range(K):
    # 1. 참가자 이동
    for pid, pp in enumerate(game):
        if (not isAlive[pid]):
            continue
        pr, pc = pp

        # 1-1. 출구와 가까워지는 방향 구하기 
        # next_move = [100, [0, 0]]  # [최솟값, [r,c]]
        # for d in dir:
        #     nr, nc = [pr + d[0], pc + d[1]]
        #     if (check_bound([nr, nc])):
        #         dist = get_dist(game[M+1], [nr, nc])
        #         if (next_move[0] > dist):
        #             next_move = [dist, [nr, nc]]
        next_move = []
        cur_dist = get_dist(game[M + 1], [pr, pc])
        for di, d in enumerate(dir):
            nr, nc = [pr + d[0], pc + d[1]]
            if (check_bound([nr, nc])):
                dist = get_dist(game[M + 1], [nr, nc])
                if(dist < cur_dist):
                    next_move.append([dist, di, [nr, nc]])
        next_move.sort()

        # 1-2. 이동하기 -> people 갱신 (exit 도달하는 경우 확인하기)

        same_dist = next_move[0][0]
        for dist, di, nn in next_move:
            if(same_dist != dist):
                break
            nr, nc = nn
            if ([nr, nc] == game[M+1]):  # 플레이어 삭제
                isAlive[pid] = False
                game_board[pr][pc].remove(pid)
                game[pid] = [-1, -1]
                answer_moves += 1
                break
            elif(wall_board[nr][nc] == 0):
                game_board[pr][pc].remove(pid)
                game_board[nr][nc].append(pid)
                game[pid] = [nr, nc]
                answer_moves += 1
                break


    # 2. 회전
    # 2-1. exit, 참가자를 포함하는 가장 작은 정사각형 구하기 (크기, r, c)우선순위 
    find_width = []
    for i in range(1, M + 1):
        if (isAlive[i]):
            find_width.append([get_width(game[M+1], game[i]), game[i][0], game[i][1]])
    if (not find_width):
        break
    find_width.sort()
    sq_width, peo_r, peo_c = find_width[0]

    sq_start = [max(0, game[M+1][0] - sq_width), max(0, game[M+1][1] - sq_width)]
    sq_start = get_start(sq_start, find_width)
    # for sq_r in range(sq_start[0], game[M+1][0]+1):
    #     for sq_c in range(sq_start[1], game[M + 1][1] + 1):
    #         sq_end = [sq_r + sq_width, sq_c + sq_width]
    #         for fw, fr, fc in find_width:
    #             if(sq_start[0] <= fr and sq_start[1]<=fr and sq_end[0]>=fr and sq_end[1]>=fc):
    #                 sq_start = [sq_r, sq_c]
    #                 break
    sq_width += 1

    game_board_cp = [gb[:] for gb in game_board]
    wall_board_cp = [wb[:] for wb in wall_board]

    # 2-2. 시계방향 회전하기 -> people, exit, board 모두 갱신
    while (sq_width > 0):
        rotate(sq_start, sq_width)
        sq_start = [sq_start[0] + 1, sq_start[1] + 1]
        sq_width -= 2

print(answer_moves)
for g in game[M+1]:
    print(g + 1, end=" ")