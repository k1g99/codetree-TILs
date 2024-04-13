import heapq as hq

N, M, P, C, D = list(map(int, input().split()))
rudolf_loc = list(map(int, input().split())) # 루돌프 초기 위치
rudolf_loc = [rudolf_loc[0] - 1, rudolf_loc[1] - 1]
# rudolf_dirr = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]

santa_loc = [[] for _ in range(P+1)]
santa_board = [[0 for _ in range(N)] for _ in range(N)]
santa_score = [0 for _ in range(P+1)]
santa_stun = [1 for _ in range(P+1)] # round보다 santa_stun값이 큰 경우에만 예외
santa_dirr = [[-1,0],[0,1],[1,0], [0,-1]] # (상우하좌)
santa_dead = [False for _ in range(P+1)]
for p in range(1, P+1):
    sid, r, c = list(map(int, input().split()))
    santa_loc[sid] = [r-1,c-1]
    santa_board[r-1][c-1] = sid

#### 알고리즘

def get_dist(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2 

def get_rudolf_dir(rd, sa):
    ret = [0,0]
    if (rd[0] < sa[0]):
        ret[0] = 1
    elif(rd[0] > sa[0]):
        ret[0] = -1

    if (rd[1] < sa[1]):
        ret[1] = 1
    elif(rd[1] > sa[1]):
        ret[1] = -1
    
    return ret

def check_bound(a):
    r, c = a
    return r>=0 and c>=0 and r<N and c<N

def move(sid, loc, rdir):
    # 옮길 위치가 밖이면 sid 죽음 (loc랑 dead 갱신 (board는 어차피 뒤집어씌워짐))
    if(not check_bound(loc)):
        santa_dead[sid] = True
        santa_loc[sid] = loc
        return 
    
    # 이미 산타가 있으면 연쇄 move
    if(santa_board[loc[0]][loc[1]] > 0):
        new_sid = santa_board[loc[0]][loc[1]]
        new_loc = [loc[0] + rdir[0], loc[1] + rdir[1]]
        move(new_sid, new_loc, rdir)

    # 산타 이동
    santa_board[loc[0]][loc[1]] = sid
    santa_loc[sid] = loc
    

for m in range(1, M+1):
    # 루돌프 이동 pq (거리 작은, r 좌표가 큰 ,  좌표가 큰 )
    rpq = []
    for santa_id in range(1, P+1):
        if(santa_dead[santa_id]):
            continue
        hq.heappush(rpq, [get_dist(rudolf_loc, santa_loc[santa_id]), -1*santa_loc[santa_id][0], -1*santa_loc[santa_id][1], santa_id])

    if(not rpq): # 살아있는 산타가 없음
        break

    # 가장 가까운 산타 선정 / 방향 선정
    _, scr, scc, closest_santa_id = rpq[0]
    rudolf_dirr = get_rudolf_dir(rudolf_loc, [-1*scr, -1*scc])
    # 돌진
    rudolf_loc = [rudolf_loc[0] + rudolf_dirr[0], rudolf_loc[1] + rudolf_dirr[1]]
    
    # 산타와 만났다면, 충돌 -> 산타 점수 추가 / 기절
    if(santa_board[rudolf_loc[0]][rudolf_loc[1]] > 0):
        winner_sid = santa_board[rudolf_loc[0]][rudolf_loc[1]]
        santa_score[winner_sid] += C
        santa_stun[winner_sid] = m + 2

        # 산타 연쇄 이동
        new_winner_loc = [santa_loc[winner_sid][0] + C*rudolf_dirr[0], santa_loc[winner_sid][1] + C*rudolf_dirr[1]]
        santa_board[santa_loc[winner_sid][0]][santa_loc[winner_sid][1]] = 0 # 어차피 산타 이동할거잖아!
        move(winner_sid, new_winner_loc, rudolf_dirr)

    # print(rudolf_loc, rudolf_dirr, [scr, scc])
    # for b in santa_board:
    #     print(b)

    # 산타들 이동
    for sid in range(1, P+1):
        # 기절 / 게임 탈락인 경우 continue
        if(santa_dead[sid] or santa_stun[sid] > m ):
            continue

        # 루돌프에게 가까워지는 방향 선정 (우선순위 필요함 (상우하좌))
        cur_dist = get_dist(rudolf_loc, santa_loc[sid])
        santa_move_dir = -1
        cr, cc = santa_loc[sid]
        for di in range(4):
            nr, nc = [cr + santa_dirr[di][0], cc + santa_dirr[di][1]]
            if(check_bound([nr, nc])):
                # 현재 위치와 이동했을 때 거리 비교 후, 가까워질 수 없다면 이동 불가
                if(santa_board[nr][nc] == 0 and cur_dist > get_dist(rudolf_loc, [nr, nc])):
                    cur_dist = get_dist(rudolf_loc, [nr, nc])
                    santa_move_dir = di
        
        if(santa_move_dir == -1): # 움직일 필요가 없음!
            continue 

        # 이동
        santa_board[santa_loc[sid][0]][santa_loc[sid][1]] = 0
        santa_loc[sid] = [cr + santa_dirr[santa_move_dir][0], cc + santa_dirr[santa_move_dir][1]]
        santa_board[santa_loc[sid][0]][santa_loc[sid][1]] = sid
        
        # 루돌프와 만났다면, 충돌 -> 산타 점수 추가 / 기절
        if(santa_loc[sid] == rudolf_loc):
            santa_jump_dir = (santa_move_dir + 2) % 4
            santa_score[sid] += D
            santa_stun[sid] = m + 2

            # 산타 연쇄 이동
            new_santa_loc = [santa_loc[sid][0] + D*santa_dirr[santa_jump_dir][0], santa_loc[sid][1] + D*santa_dirr[santa_jump_dir][1]]
            santa_board[santa_loc[sid][0]][santa_loc[sid][1]] = 0 # 어차피 이동할거임
            move(sid, new_santa_loc, santa_dirr[santa_jump_dir])
        # 산타 연쇄 이동

    # 아직 탈락하지 않은 산타들에게는 1점씩을 추가로 부여
    for sid in range(1, P+1):
        if(not santa_dead[sid]):
            santa_score[sid] += 1
    
    # print('-'*10)
    # for b in santa_board:
    #     print(b)


#  각 산타가 얻은 최종 점수를 1번부터 P번까지 순서대로 공백을 사이에 두고 출력
print(" ".join(map(str, santa_score[1:])))