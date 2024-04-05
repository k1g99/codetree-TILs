N, M, K, C = list(map(int, input().split()))

board = []
able_year = [[0 for _ in range(N)] for _ in range(N)]
answer = 0 # 죽은 나무 수

dir = [[-1, 0], [0, 1], [1, 0], [0, -1]]
diag = [[-1, 1], [1, 1], [1, -1], [-1, -1]]

def check_bound(r, c):
    return r>=0 and c>=0 and r<N and c<N

for r in range(N):
    row = list(map(int, input().split()))
    board.append(row)

    for c in range(N):
        if(row[c] == -1):
            able_year[r][c] = 9999


for m in range(M):
    trees = []
    # 성장 & 번식
    seed_trees = [] # [r, c, [0, 1, 2]]
    for r in range(N):
        for c in range(N):
            if board[r][c] > 0: # [r][c]에 나무가 있으면 
                trees.append([r, c])
                near_empty_cell = []
                for di in range(4): # 네 방향 돌면서 나무 확인 ([r][c] > 0인지)
                    nr, nc = [r + dir[di][0], c + dir[di][1]]
                    if(check_bound(nr, nc)):
                        if(board[nr][nc] > 0): # 나무가 있으면 [r][c]에다 값 추가하고, 
                            board[nr][nc] += 1
                        elif(board[nr][nc] == 0 and able_year[nr][nc] <= m): # 나무가 없고, able_year<=m 이라면 주변 주소(뱡항 idx)를 seed_cell에 추가
                            trees.append([nr, nc])
                            near_empty_cell.append(di)
                
                if(near_empty_cell): # seed_trees +=  ([r, c, seed_cell])
                    seed_trees.append([r, c, near_empty_cell])

    # seed_trees 돌면서 번식 시작 -> 
    for r, c, dis in seed_trees:
        seed_cnt = board[r][c] // len(dis)
        for di in dis:
            nr, nc = [r + dir[di][0], c + dir[di][1]]
            board[nr][nc] += seed_cnt

    # 제초제 선정 -> 다 돌아야할듯
    kill_candiatae = []
    for r, c in trees:
        if(board[r][c] > 0):
            kills = board[r][c]
            for di in diag:
                for k in range(1, K+1):
                    nr, nc = [r + di[0]*k, c + di[1]*k]
                    if(not check_bound(nr, nc) or board[nr][nc] < 1):
                        break
                    kills += board[nr][nc]
            kill_candiatae.append([-1 * kills, r, c])

    kill_candiatae.sort()
    
    # 제초제 뿌리기 -> board 갱신 / able_year 갱신 (m + c + 1)
    kill_cnt, kr, kc = kill_candiatae[0]
    answer += (kill_cnt * -1)
    board[kr][kc] = 0
    able_year[kr][kc] = m + C + 1
    for di in diag:
        for k in range(1, K+1):
            nr, nc = [kr + di[0]*k, kc + di[1]*k]
            if(not check_bound(nr, nc) or board[nr][nc] < 1):
                break
            board[nr][nc] = 0
            able_year[nr][nc] =  m + C + 1

print(answer)