### 가장 어려웠던 포인트 : 너무 복잡함 / stun을 나올 수 있는 턴으로 설정하는거! 

N, M, P, RP, SP = list(map(int, input().split()))
rudolf = list(map(int, input().split()))
santa = [[] for _ in range(P + 1)]  # 산타의 현재 위치가 담겨있음
board = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
score = [0 for _ in range(P + 1)]
stun = [0 for _ in range(P + 1)] # 나올 수 있는 턴 적기
alive = [True for _ in range(P + 1)]
alive[0] = False
distance = []  # 거리, -r, -c, 산타ID


def get_dist(a, b):
    ar, ac = a
    br, bc = b
    return (ar - br) ** 2 + (ac - bc) ** 2

def check_bound(pos):
    r, c = pos
    if(r < 1 or c < 1 or r > N or c > N):
        return False
    return True

def get_rudolf_dir(r, s):
    if(r > s):
        return -1
    if(r < s):
        return 1
    return 0

def get_santa_dir(sid):
    dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]] # 상우하좌
    # 현재 위치 계산
    ret = [0, 0]
    min_dist = get_dist(rudolf, santa[sid])

    for di in dirs:
        # 방향으로 갈 수 있는지 확인
        nr = di[0] + santa[sid][0]
        nc = di[1] + santa[sid][1]
        if(check_bound([nr, nc]) and board[nr][nc] == 0):
            # 옮길 위치에서 거리 계산 -> 더 작은 경우에만 이동!
            check_dist = get_dist(rudolf, [nr, nc])
            if(min_dist > check_dist):
                min_dist = check_dist
                ret = di

    return ret


for p in range(P):
    santa_id, santa_r, santa_c = list(map(int, input().split()))
    santa[santa_id] = [santa_r, santa_c]
    # distance.append(get_dist(santa[santa_id], rudolf), santa_r * -1, santa_c * -1, santa_id)
    board[santa_r][santa_c] = santa_id

for m in range(M):
    # 살아있는 산타만 distance 계산
    for idx in range(1, P + 1):
        if (alive[idx]):
            s_r, s_c = santa[idx]
            distance.append([get_dist(santa[idx], rudolf), s_r * -1, s_c * -1, idx])

    # distance가 없다면 끝난거!
    if (not distance):
        break

    # 루돌프 이동
    # 가장 가까운 산타 찾기
    distance.sort()
    _, santa_r, santa_c, santa_id = distance[0]
    santa_r *= -1
    santa_c *= -1
    # 그 산타로 이동할 방향 찾기
    rudolf_dr = get_rudolf_dir(rudolf[0], santa_r)
    rudolf_dc = get_rudolf_dir(rudolf[1], santa_c)
    # 이동
    rudolf = [rudolf[0] + rudolf_dr, rudolf[1] + rudolf_dc]

    # 충돌 -> 기절 -> 점수 추가 -> 상호작용(이동만)
    if(board[rudolf[0]][rudolf[1]] > 0): # 산타가 이미 있다면,
        # 1. 일단 점수 추가
        score[santa_id] += RP
        # 2. 기절로 표시
        stun[santa_id] = m + 2
        # 3. 산타 날라감
        board[santa_r][santa_c] = 0

        # 4. after_santa_pos = [] 루돌프가 이동한 방향으로 산타가 밀려남
        santa_jump_d = [rudolf_dr * RP, rudolf_dc * RP]
        after_santa_pos = [santa_r + santa_jump_d[0], santa_c + santa_jump_d[1]]
        santa[santa_id] = after_santa_pos

        # while after_santa_pos가 범위 내부일 때
        while (check_bound(after_santa_pos)):
            # after_santa_pos에 산타가 있는 경우 -> 산타 밀어내야함!
            if (board[after_santa_pos[0]][after_santa_pos[1]]):
                # 밀어날 산타 id 저장
                leave_santa_id = board[after_santa_pos[0]][after_santa_pos[1]]
                # board 갱신
                board[after_santa_pos[0]][after_santa_pos[1]] = santa_id
                # 다시 밀어낼 산타 위치 확인
                after_santa_pos = [after_santa_pos[0] + rudolf_dr, after_santa_pos[1] + rudolf_dc]
                santa_id = leave_santa_id
                santa[santa_id] = after_santa_pos
            else: # after_santa_pos에 산타가 없는 경우
                board[after_santa_pos[0]][after_santa_pos[1]] = santa_id
                break
        else: # 범위 내부가 아닐 때,
            # 산타 죽음
            alive[santa_id] = False

    # 루돌프 끝

    # 산타 이동 (1 ~ P번까지)
    for s_id in range(1, P+1):
        # 산타 생사 / 기절 확인
        if(not alive[s_id]):
            continue
        if(stun[s_id] > m):
            continue
        # 4 방향 모두 가보고, 루돌프랑 가장 가까운 거리로 이동 (가만히 있을 수도 있음)
        santa_dr = get_santa_dir(s_id)
        # 이동
        board[santa[s_id][0]][santa[s_id][1]] = 0
        santa[s_id] = [santa[s_id][0] + santa_dr[0], santa[s_id][1] + santa_dr[1]]
        board[santa[s_id][0]][santa[s_id][1]] = s_id

        # 충돌 -> 기절 -> 점수 추가 -> 상호작용(이동만)
        # 옮기고보니 루돌프랑 충돌
        if ([rudolf[0],rudolf[1]] == santa[s_id]):
            santa_id = s_id
            # 1. 일단 점수 추가
            score[s_id] += SP
            # 2. 기절
            stun[s_id] = m + 2
            # 3. 반대방향으로 밀려남
            santa_r, santa_c = santa[santa_id]
            board[santa_r][santa_c] = 0
            santa_dr[0] *= -1
            santa_dr[1] *= -1
            # 4. after_santa_pos 계산
            after_santa_pos = [santa_r + santa_dr[0] * SP, santa_c + santa_dr[1] * SP]
            # 5. santa[]는 미리 변경
            santa[santa_id] = after_santa_pos
            # 6. 기존 위치는 0으로 초기화
            # while 범위 내부일 떄
            while (check_bound(after_santa_pos)):
                # if 이미 다른 산타가 있으면,
                if(board[after_santa_pos[0]][after_santa_pos[1]]):
                    leave_santa_id = board[after_santa_pos[0]][after_santa_pos[1]]
                    board[after_santa_pos[0]][after_santa_pos[1]] = santa_id
                    # 7. after_santa_pos 계산
                    after_santa_pos = [after_santa_pos[0] + santa_dr[0], after_santa_pos[1] + santa_dr[1]]
                    # 8. santa_id 갱신
                    santa_id = leave_santa_id
                    # 9. santa[] 미리 갱신
                    santa[santa_id] = after_santa_pos
                    # 10. board 갱신

                # else 다른 산타가 없으면
                else:
                    board[after_santa_pos[0]][after_santa_pos[1]] = santa_id
                    break
            else:
                alive[santa_id] = False

    for s_id in range(1, P+1):
        if(alive[s_id]):
            score[s_id] += 1

    distance = []

print(" ".join(map(str, score))[2:])