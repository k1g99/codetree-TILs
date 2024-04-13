# # 1. 초밥 회전 (1초에 1칸씩 시계방향)

# # 2. 주방장의 초밥 만들기 (t시각에 x(벨트)의 앞에 있는 벨트에 name부착한 초밥 놓기)
# # - 같은 위치에 여러 회전 초밥이 올라갈 수 있으며
# # - 자신의 이름이 적혀 있는 초밥이 같은 위치에 여러 개 놓여 있는 것 역시 가능함

# # 2. 손님 입장
# # - name인 사람이 t시각에 x(의자)로 가서 앉음
# # - 위치 x 앞으로 오는 초밥들 중 자신의 이름이 적혀있는 초밥을 정확히 n개를 먹고 자리를 떠납

# # 3. 먹음
# # - 자리에 착석하는 즉시 먹을 수 있음. (여러개 먹기도 가능)

# # 4. 사진 촬영
# # - 2, 3끝나고 사진  (오마카세 집에 있는 사람 수와 남아 있는 초밥 수)
# import sys
# sys.stdin=open("input.txt", "r")

L, Q = list(map(int, input().split()))
make_susi = dict()  # "sam" : [[들어온 시간, 놓은 위치], [들어온 시간, 놓은 위치], [들어온 시간, 놓은 위치]]
eat_time = dict()  # "sam" : [먹을 수 있는 시점, 먹을 수 있는 시점]
eat_amount = dict()  # "sam" : [먹어야할 양]
entered = dict()  # "sam" : [들어온 시간, 앉은 자리]

count_man = 0
count_susi = 0

for _ in range(Q):
    order = list(input().split())

    if (order[0] == '100'):  # 주방장 초밥 만들기
        # dict 사용해서, "sam" : [[초, 자리]] 순서대로 정리하기
        # 만약 이미 입장해있는 손님이라면, [먹을 수 있게 되는 시점]에다 값 넣기

        _, t, x, name = order
        t = int(t)
        x = int(x)

        if (name in eat_time):  # 이미 입장해있다면, 바로 EAT_TIME으로 적기
            cir, sq = entered[name]
            val = cir + ((sq - ((cir - (t - x)) % L)) % L)
            while (val < t):
                val += L
            eat_time[name].append(val)
            count_susi += 1
        else:
            if (name in make_susi):
                make_susi[name].append([t, x])
                count_susi += 1
            else:
                make_susi[name] = [[t, x]]
                count_susi += 1



    elif (order[0] == '200'):  # 손님 입장
        # dict 사용해서 "sam" : [먹을 수 있게 되는 시점] 순서대로 정리하기

        _, t, x, name, n = order
        t = int(t)
        x = int(x)
        n = int(n)

        entered[name] = [t, x]
        count_man += 1

        eat_amount[name] = n

        eat_time[name] = []

        for susi in make_susi[name]:
            tt, xx = susi
            cir, sq = entered[name]
            val = cir + ((sq - ((cir - (tt - xx)) % L)) % L)
            while (val < t):
                val += L
            eat_time[name].append(val)

        make_susi[name] = []

    elif (order[0] == '300'):  # 사진촬영
        _, t = order
        t = int(t)

        for names in entered:
            if (not eat_time[names]):
                continue

            eat_time[names].sort()  # 정렬 [0,1,2,3 ...]

            idx = 0
            while (idx < len(eat_time[names])):
                if (eat_time[names][idx] > t):
                    break
                idx += 1
            eat_time[names] = eat_time[names][idx:]
            count_susi -= idx
            eat_amount[names] -= idx

            # for names in eat_time:
            if (eat_amount[names] == 0):
                # eat_time.pop(names)
                # # entered.pop(names)
                # eat_amount.pop(names)
                # if(names in make_susi):
                #     make_susi.pop(names)
                count_man -= 1

        print(count_man, count_susi)

# i = 0
# while ( i < 5):
#     print(i)
#     i+=1
# print(i)