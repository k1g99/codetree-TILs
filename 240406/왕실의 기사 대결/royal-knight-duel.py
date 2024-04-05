L, N, Q = list(map(int, input().split()))
dir = [[-1, 0], [0, 1], [1, 0], [0, -1]]

answer = 0  # 생존한 기사들이 총 받은 대미지의 합을 출력

# 체스판 (1 : 함정, 2 : 벽)
board = [[0] * L]
for l in range(L):
    row = list(map(int, input().split()))
    board.append([0] + row)

# 초기 기사들의 정보
knight_board = [[0 for _ in range(L + 1)] for _ in range(L + 1)]
alive = [True for _ in range(N + 1)]
hp = [0 for _ in range(N + 1)]
knights = [[] for _ in range(N + 1)]  # [[1,2],[2,2]]] [모든 칸[]]
for n in range(1, N + 1):
    r, c, h, w, k = list(map(int, input().split()))
    # 세로 길이가 h, 가로 길이가 w, 체력 k
    occ = []
    for rr in range(h):
        for cc in range(w):
            occ.append([r + rr, c + cc])
    knights[n] = occ
    for ocr, occ in occ:
        knight_board[ocr][occ] = n
    hp[n] = k

# 왕의 명령 (위쪽, 오른쪽, 아래쪽, 왼쪽)
orders = []
for q in range(Q):
    i, d = list(map(int, input().split()))
    orders.append([i, d])
    # 이미 사라진 기사 번호가 주어질 수도 있음

damage = [0 for _ in range(N + 1)]

def check_border(r, c):
    return r > 0 and c > 0 and r <= L and c <= L


next_knights = []

def push(k_id, p_d):
    target = []  # 이동 후 위치
    # target 계산
    move_knights = []
    can_move = True
    for kr, kc in knights[k_id]:
        nr, nc = [kr + dir[p_d][0], kc + dir[p_d][1]]
        if (not check_border(nr, nc)):
            can_move = False
            continue
        target.append([nr, nc])

        if (knight_board[nr][nc] not in [0, k_id]):
            move_knights.append(knight_board[nr][nc])
        if(board[nr][nc] == 2):
            can_move = False

    if (can_move):  # 움직일 수 있다 (벽돌은 없고 범위 내에 있다)
        if (move_knights):  # 옮겨야할 다른 기사들이 있다면
            for new_k_id in move_knights:
                if(not push(new_k_id, p_d)):
                    return False
            next_knights.append([k_id, target])  # 임시 저장
        else:
            next_knights.append([k_id, target])  # 임시 저장
            return True
    else:
        return False
    return True


for knight_id, push_d in orders:
    next_knights = []

    if (alive[knight_id]):
        if(push(knight_id, push_d)):
            # print(next_knights)
            # knight_board 업데이트
            for k_id, new_cells in next_knights:
                for kr, kc in knights[k_id]:
                    knight_board[kr][kc] = 0
                for nr, nc in new_cells:
                    knight_board[nr][nc] = k_id
                    if(board[nr][nc] == 1 and k_id != knight_id):
                        damage[k_id] += 1
                        hp[k_id] -= 1
                        if(hp[k_id] <= 0):
                            alive[k_id] = False
                if(not alive[k_id]):
                    for nr, nc in new_cells:
                        knight_board[nr][nc] = 0
                knights[k_id] = new_cells # knights 업데이트

for i in range(1, N+1):
    if(alive[i]):
        answer += damage[i]
print(answer)