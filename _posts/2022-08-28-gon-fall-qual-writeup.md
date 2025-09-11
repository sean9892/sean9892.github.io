---
title: "2022 Fall GoN Qual CTF write-up"
description: "2022 fall gon qual writeup"
header: "CTF"
lang: ko
---

KAIST의 정보보안 동아리인 GoN에서는 매 정규학기 초에 동아리 정규회원 자격 유지를 위한 Qual을 진행한다. GoN의 정규회원은 이에 의무적으로 참가해 학기차 별로 특정한 문제 수를 풀어야 하는데, 최근에는 드림핵에서 해당 Qual이 Open Contest 형태로 진행한다.

이번 학기에는 2학기차 정규회원으로서 Qual에 참가하여 Crypto 3문제, Forensic 1문제를 해결하였으며 아래 기술된 내용은 내가 해결한 문제에 대한 write-up이다.

---

### N. Private Storage - Crypto

제공된 oracle은 임의의 plaintext에 대한 encrypt oracle 정도로 요약할 수 있고, flag와 key에 대한 암호화 정보를 받을 수 있다. 보통의 crypto task라면 key를 조작하는 등의 연산을 사용하는 것이 정해이고 거기에 cryptographic한 제약조건이 달려있겠지만, 놀랍게도 그냥 ARC4가 취약하기 때문에 여기서 key recovery를 시도하는 것이 풀이이다. 구글링을 통해 간단하게 key recovery에 대한 코드를 얻을 수 있으므로 이하의 풀이는 생략한다.

---

### O. Checkers - Crypto

Checker이라는 처음 보는 게임에 관한 얘기도 있고, 무언가 열심히 구현되어있지만 크게 중요하지 않다.

문제에서 제공되는 oracle은 flag의 ciphertext, 임의의 plaintext에 대한 encrypt oracle이며 이들을 내가 원하는 대로 무한히 호출할 수 있다.

중요한 것은 encrypt 함수의 구조인데, straddling_checkerboard, substitute, straddling_checkerboard_inv라는 연산을 차례로 적용하는 것이 하나의 encrypt이다. 편의상 straddling_checkerboard를 $C$, substitute를 $S$, straddling_checkerboard_inv를 $C^I$로 표기하자. 이때 $S$에 대해서 먼저 관찰해보자. $S$ 함수는 두 10진수를 인자로 받아 non-carry add, 즉 받아올림이 없는 덧셈을 진행한다. 이는 각 자릿수를 값으로 가지는 임의 차원의 벡터를 mod 10에서 더하는 것과 같으며, 호출되는 $S$ 함수는 키를 반복하여 평문에 더하는 것이므로 평문 한 자리와 이에 더해지는 키 한 자리의 벡터 꼴의 표현 $p,k$에 대해서 동일한 평문을 $n$번 더한 중간 결과물은 $p+n\times k$로 표현할 수 있다.

$S$ 연산을 평문에 여러번 적용하는 것을 특정한 꼴로 압축할 수 있다는 것을 발견하였으니, 이것이 공격에 사용될 수 있는지를 고려해 보아야 한다. encrypt 함수는 $C$, $S$, $C^I$를 차례로 적용하는데, encrypt 함수를 여러번 실행한다면 $C$, $S$, $C^I$, $C$, $S$, $C^I$, ... 꼴로 함수가 적용될 것이다. 이때 $C^I$와 $C$가 연속적으로 실행되어 상쇄되고, 결국 $C$, $S$, $S$, ..., $S$, $C^I$ 순서로 실행된 결과물과 같은 암호문을 얻는다. 만일 연속된 $S$ 연산의 결과가 연산을 하지 않았을 때와 같다면, 즉 $C$, $S$, $S$, ..., $S$, $C^I$ 연산의 결과가 $C$, $C^I$ 연산의 결과와 같다면 encrypt 함수의 입력과 출력은 동일하다.

연속된 $S$ 연산의 결과가 연산을 하지 않았을 때와 같기 위해서 생각할 수 있는 간단한 방법은 $p+n\times k$에서 $n$이 10이면 mod 10에서 $p$와 $p+n\times k$가 동일하다는 것을 활용하는 것이다. 따라서, 우리는 flag의 암호문을 받아 9번 더 암호화하면 그 결과로 flag를 찾을 수 있다.

---

### C. pprintable - Crypto

흔한 RSA task의 코드와 유사하게 생겼다. 랜덤한 두 소수 $p,q$를 생성하고 $N=pq$를 계산 후, $c=m^e \mod N$을 계산한다. 문제에서는 $N,e,c$를 제공한다. 이 문제에서 추가적으로 제공하는 정보는 두 소수의 각 비트의 값을 0.35의 확률로 노출하는 mask와 그 마스크를 씌운 redacted prime의 값, 그리고 두 소수는 printable character로만 구성되었다는 것이다. 이걸 대체 어떻게 찾았나 싶지만 아무튼 만들어서 문제를 출제했으니 문제에만 집중해보자.

문제의 주석에서도 언급하듯이 빠르게 풀 수 있는 비트 노출의 확률은 0.5가 하한선이다. 그렇지 않을 경우 bruteforce에서 가지치기가 가능한 경우가 충분히 많지 않아 시간이 오래 걸리게 되는데, 이 문제에서는 printable character라는 조건으로 이를 잘 보완해보라는 것이 출제 의도이다.

확률이 충분히 클 경우의 solution은 $\mod 2^k$에서 $pq\equiv N$을 만족하는 p, q의 값을 찾아 bruteforce하는 것이다. k의 값을 점점 키워나가며 두 소수의 원본 값을 찾는 형태로 solution이 동작한다. 이 풀이를 약간 변형하면 printable이라는 조건을 활용할 수 있다.

우리는 바이트 단위로 bruteforce를 진행하여도 가능한 p,q의 값의 수는 최대 $256\times256=65536$으로 충분히 작고, mask에서 제공된 정보와 printable이라는 조건을 통해 후보를 filtering하면 가능한 p,q의 수가 많지 않고 여럿 존재하더라도 금방 배제될 수 있음을 짐작할 수 있다. 따라서 바이트 단위로 printable character만을 대상으로 bruteforce하면 flag를 찾을 수 있다.

---

### S. sleepingshark - Forensic

문제에서는 수많은 패킷이 포함된 pcap 파일이 제공된다. 어떠한 두 장치의 HTTP 통신을 캡쳐한 것으로 보이며, 종종 broadcast 등의 잡다한 패킷도 포함되어있는 것을 확인할 수 있다. 패킷을 조금 살펴보면, POST를 통해 질의를 보내는 패킷을 발견할 수 있다. 해당 패킷들의 query string을 url decode해보면 flag의 어떤 인덱스의 한 글자를 특정한 문자와 비교하고 동일하다면 3초간 sleep, 그렇지 않다면 그냥 종료하는 query임을 확인할 수 있다. 이를 이용하여, 이 쿼리의 response가 약 3초 이상 경과한 시점에 캡쳐되었다면 비교했던 두 문자가 동일했다는 정보로 간주할 수 있다. 이를 이용하여 POST와 그 response에 해당하는 패킷만 골라내어 캡쳐된 시각의 차이를 근거로 flag를 복원하면 된다. 플래그의 모든 문자에 대한 정보가 없을 수 있는데, 패킷이 워낙 많기도 하고 적은 수의 글자만이 누락되었다면 게싱 혹은 flag bruteforcing으로 해결할 수 있을 것이다. 다행히도 모든 문자에 대한 정보가 포함되어 있으므로  이를 그대로 제출하면 된다.

이때, 수많은 패킷 중에서 POST와 그 response에 해당하는 패킷을 손으로 골라내기란 현실적으로 불가능한 일이다. 실제로 패킷을 필터링한 후에도 약 만개의 패킷을 분석해야 한다. 따라서 이러한 패킷을 찾는데에는 약간의 게싱이 필요한데, 초반의 몇십 패킷을 관찰하면 우리가 원하는 패킷만 그 길이가 300~400 정도로 다른 패킷에 비해 길다는 사실을 확인할 수 있다. 따라서 통신하는 장치의 ip와 패킷 길이로 필터링하면 우리가 원하는 패킷만을 얻을 수 있다. 이후에는 csv로 export하여서 python을 통해 위에서 언급한 solution을 구현하면 flag를 쉽게 얻을 수 있다.