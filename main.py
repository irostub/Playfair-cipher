from collections import OrderedDict  # 요소 중복제거를 위해 OrderedDict 모듈 사용
import numpy as np  # 2차원 배열 전환을 위해 numpy 모듈 사용

key = input()  # 암호화에 필요한 키
key = key.replace(" ", "")  # 키에서 공백제거
key = key.upper()  # 키를 모두 대문자로 변환
key = list(OrderedDict.fromkeys(key))  # 순서를 유지하고 중복제거

key_table = list()  # 키값 리스트 변수 (1차원)
for attr in key:  # Q를 Z로 대체
    if attr not in key_table:  # key_table에 key의 요소가 없다면
        if attr == 'Q':  # 요소가 Q라면
            key_table.append('Z')  # Z로 대체
        else:
            key_table.append(attr)  # 요소가 Q가 아니라면 key의 요소를 key_table로 append
key_table = list(OrderedDict.fromkeys(key_table))  # key_table에서 중복되는 요소를 순서를 유지하고 제거

for i in range(65, 91):  # 아스키코드 값으로 key_table에 없는 나머지 알파벳을 찾으며 key_table에 append
    if chr(i) not in key_table:
        if i == 81:  # 아스키코드 dec 81은 chr Q
            pass
        else:
            key_table.append(chr(i))
key_matrix = np.asarray(key_table)  # key_table 리스트형을 numpy 배열형으로 형변환
key_matrix = key_matrix.reshape(5, 5)  # 5x5 행렬로 변환
key_matrix = key_matrix.tolist()  # numpy 배열형을 list 형으로 형변환

msg = input()  # 평문 변수
msg = msg.replace(" ", "")  # 평문에서 공백제거
msg = msg.upper()  # 평문을 모두 대문자로 변환

for i in range(0, len(msg) + 1, 2):  # 두글자씩 조사, 같은 글자가 있다면 앞글자의 뒤에 X를 삽입
    if i < len(msg) - 1:
        if msg[i] == msg[i + 1]:  # 앞자와 뒷자가 같다면
            msg = msg[:i + 1] + 'X' + msg[i + 1:]  # 중간에 X를 삽입

if len(msg) % 2 != 0:  # 모든 과정 이후 변환된 평문이 짝수개가 아닌 홀수개로 짝이 안맞으면 맨 뒤에 X를 삽입
    msg = msg + 'X'


def locIndex(c):  # 평문의 해당 글자가 암호화 키의 어느 인덱스에 해당하는지 반환해줄 함수
    v = c
    loc = list()  # [행, 렬] 인덱스를 담을 리스트
    if v == 'Q':  # 만약 평문에 Q문자가 나온 경우 Z로 치환
        v = 'Z'
    for i, j in enumerate(key_matrix):  # key_matrix는 2차원 리스트, 행에 해당하는 index를 i로, 요소 리스트를 j로 꺼내서 반복문 실행
        for k, l in enumerate(j):  # j는 이제 실제 암호문 값이 담긴 리스트, k는 열에 해당하는 index, l은 암호문 값을 꺼내서 반복문 실행
            if v == l:  # 평문 요소와 암호문 값이 일치하면
                loc.append(i)  # 행 append
                loc.append(k)  # 열 append
                return loc  # 행, 렬 정보가 담긴 list를 반환


i = 0  # 반복문 idx
while i < len(msg):  # i가 평문 길이보다 크지않을 때까지 반복
    loc = list()  # 쌍 지어진 평문의 쌍 중 앞문자
    loc = locIndex(msg[i])  # 앞문자의 암호문에서의 행렬 정보
    loc1 = list()  # 쌍 지어진 평문의 쌍 중 뒷문자
    loc1 = locIndex(msg[i + 1])  # 뒷문자의 암호문에서의 행렬 정보
    if loc[1] == loc1[1]:  # 앞문자와 뒷문자의 암호문에서의 열이 같은 경우
        print("{}{}".format(key_matrix[(loc[0] + 1) % 5][loc[1]], key_matrix[(loc1[0] + 1) % 5][loc1[1]]), end="")  # key_matrix에서의 평문의 해당 문자의 한 행 아래에 있는 문자를 출력
    elif loc[0] == loc1[0]:  # 앞문자와 뒷문자의 암호문에서의 행이 같은 경우
        print("{}{}".format(key_matrix[loc[0]][(loc[1] + 1) % 5], key_matrix[loc1[0]][(loc1[1] + 1) % 5]), end="")  # key_matrix에서의 평문의 해당 문자의 한 열 옆에 있는 문자를 출력
    else:  # 앞문자와 뒷문자의 암호문에서의 행 또는 열이 같지 않는 모든 경우
        print("{}{}".format(key_matrix[loc[0]][loc1[1]], key_matrix[loc1[0]][loc[1]]), end="")  # key_matrix에서 각 문자의
        # 행과 열의 인덱스 서로 바꿔서 넣어주는 것으로 두문자가 행렬 상 만나는 문자는 문자 출력
    i = i + 2  # 두글자씩 쌍지어 진행하기 위해 i는 2씩 증가
