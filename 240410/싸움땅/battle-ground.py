# 1. 플레이어 본인이 향하고 있는 방향대로 1칸 이동 / 격자를 넘어가는 경우 방향을 바꿔서 1칸 이동
# 2. 플레이어가 없다면, 해당 칸에 총이 있는지 확인 
#     2.1 총이 있음 -> 총 획득 (가장 공격력이 쎈걸로 / 나머지는 해당 격자에 놔둠)
# 3. 플레이어가 있다면, 싸움! (능력치 + 총의 공격력의 합을 비교 (같을 경우 초기 능력치 높은게 이김), 차이만큼 포인트)

# 4. 진 플레이어 -> 원래 가던 방향대로 1칸 이동 / 오른쪽으로 90도씩 이동하면서 빈칸이 보이는 순간 이동
#     마찬가지로 총이 있으면 공격력이 높은 총 획득

# 5. 이긴 플레이어 -> 현재 칸에서 가장 공격력이 높은 총 획득

import heapq as hq

N, M, K = list(map(int, input().split()))
guns = [[[] for _ in range(N)] for _ in range(N)]
board = [[-1 for _ in range(N)] for _ in range(N)]
p_attack = [0 for _ in range(M)]
p_gun = [0 for _ in range(M)]
p_point = [0 for _ in range(M)]
p_dir = [0 for _ in range(M)]
p_position = [[] for _ in range(M)]

dir = [[-1,0],[0,1],[1,0],[0,-1]]

for r in range(N):
    row = list(map(int, input().split()))
    for c in range(N):
        if(row[c]):
            guns[r][c].append(row[c])


for i in range(M):
    r, c, d, s = list(map(int, input().split()))
    r -= 1
    c -= 1
    p_position[i] = [r,c]
    p_attack[i] = s
    p_dir[i] = d
    board[r][c] = i

def check_border(a):
    r, c = a
    return r>=0 and c>=0 and r<N and c<N


for k in range(K):
    for pid in range(M):
        # 본인 방향대로 1칸 이동 / 격자를 넘어가는 경우 방향 바꿔서 1칸 이동
        cr, cc = p_position[pid]
        nr, nc = [cr + dir[p_dir[pid]][0], cc + dir[p_dir[pid]][1]]
        if(not check_border([nr, nc])): # 격자 넘어가는 경우 방향 바꿔서 2칸 이동
            p_dir[pid] = (p_dir[pid]+2) % 4
            nr, nc = [cr + dir[p_dir[pid]][0], cc + dir[p_dir[pid]][1]]
        # board 갱신, p_position 갱신 (p_dir 필요하면 갱신)
        board[cr][cc] = -1 # 일단 -1으로 바꿔놓고, 싸움하고 나서 갱신! 
        # board[nr][nc] = 0
        # p_position[i] = [nr,nc]
        # print(nr, nc)
        # print('-'*10)
        # for b in board:
        #     print(b)
        # print('-'*10)
        
        if (board[nr][nc] > -1): # 플레이어가 있다면, 싸움
            # (능력치 + 총의 공격력의 합을 비교) (같을 경우 초기 능력치 비교)
            p_a = pid # 굴러들어온 돌
            p_b = board[nr][nc] # 박힌 돌

            winner = p_a
            looser = p_b
            if((p_attack[p_a] + p_gun[p_a]) < (p_attack[p_b] + p_gun[p_b])):
                winner = p_b
                looser = p_a
            elif((p_attack[p_a] + p_gun[p_a]) == (p_attack[p_b] + p_gun[p_b])): # 무승부인 경우
                if(p_attack[p_a] < p_attack[p_b]):
                    winner = p_b
                    looser = p_a
            
            # print(winner, looser, (p_attack[winner] + p_gun[winner]) - (p_attack[looser] + p_gun[looser]))
            # winner 먼저 board 박아놓기
            board[nr][nc] = winner
            # print("battle", winner, looser)

            # 차이만큼 포인트
            p_point[winner] += (p_attack[winner] + p_gun[winner]) - (p_attack[looser] + p_gun[looser])

            # looser
            # 총 내려놓기
            guns[nr][nc].append(p_gun[looser])
            guns[nr][nc].sort()
            p_gun[looser] = 0

            # 가고 있던 방향대로 1칸 이동 (이동 불가하면 90도씩 회전)
            l_r,l_c = [nr, nc]
            l_nr, l_nc = [l_r + dir[p_dir[looser]][0], l_c + dir[p_dir[looser]][1]]
            while((not check_border([l_nr, l_nc])) or board[l_nr][l_nc] > -1):
                p_dir[looser] = (p_dir[looser] + 1) % 4
                l_nr, l_nc = [l_r + dir[p_dir[looser]][0], l_c + dir[p_dir[looser]][1]]
            board[l_nr][l_nc] = looser
            p_position[looser] = [l_nr,l_nc]
            
            # 총 들기
            if(guns[l_nr][l_nc]):
                p_gun[looser] = guns[l_nr][l_nc][-1]
                guns[l_nr][l_nc] = guns[l_nr][l_nc][:-1]

            # winner
            board[nr][nc] = winner
            # 다시 총 고르기 (최고 높은걸로)
            if(guns[nr][nc][-1] > p_gun[winner]):
                temp = p_gun[winner]
                p_gun[winner] = guns[nr][nc][-1]
                guns[nr][nc] = guns[nr][nc][:-1]
                guns[nr][nc].append(temp)
                guns[nr][nc].sort()

            # board 갱신해야됨! -> 했음
            p_position[winner] = [nr, nc]

        elif (guns[nr][nc]): # 플레이어는 없고 총만 있다면,
            board[nr][nc] = pid 
            p_position[pid] = [nr,nc]
            # 가장 능력치 좋은 총을 선택 / 가지고 있던 총(있다면)은 내려놓기
            if(p_gun[pid] > 0): # 총 들고있는 상태
                if(p_gun[pid] < guns[nr][nc][-1]): # 총 바꾸기
                    temp = p_gun[pid]
                    p_gun[pid] = guns[nr][nc][-1]
                    guns[nr][nc] = guns[nr][nc][:-1]
                    guns[nr][nc].append(temp)
                    guns[nr][nc].sort()
            else: # 총 없는 상태:
                # 총 들기
                p_gun[pid] = guns[nr][nc][-1]
                guns[nr][nc] = guns[nr][nc][:-1]
                guns[nr][nc].sort()
        else:
            board[nr][nc] = pid 
            p_position[pid] = [nr,nc]


print(" ".join(map(str, p_point)))