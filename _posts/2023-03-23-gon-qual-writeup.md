---
title: "2023 GoN Spring Qual writeup"
description: "2023 Spring GoN Qual"
categories: [CTF,writeup,GoNQual]
tag: [CTF,writeup]
math: true
mermaid: false
---

사실 ctf를 참가하려 하면 막상 귀찮아 열심히 풀지 않는 경향이 있는데, 동아리 내부 퀄은 나름의 의무감을 핑계로 시간투자를 할 수 있어 공부하기에 괜찮은 시기인것 같다.

![solved](/img/2023-spring-gon-qual/solved.png)

#### baby_crypto - Crypto

$q$가 $p$의 next prime이니, $N$을 fermat factorization하면 될 것 같다. 문제는 $N$이 주어져있지 않다. 따라서 $N$을 구해야 하는데, $c\equiv m^e\text{ }(mod\text{ }N)$이라는 점을 활용할 수 있다. 주어진 평문 2개와 그 암호문에 대해서, $m^e-c$는 $N$으로 나눈 나머지가 $0$이므로 $N$의 배수이다. 따라서 $\gcd(m_1^e-c_1,m_2^e-c_2)$는 $N$의 배수이며, 일반적으로 $N$을 얻는다. $N$을 구한 후에는 간단한 fermat factorization을 시행하면 $p,q$를 얻을 수 있고, $d$를 계산하여 플래그를 복구할 수 있다.

#### Monopoly - Crypto

auth에서는 mod $(2^130-5)$에서, 입력을 16바이트단위로 끊어 $r$에 대한 다항식의 계수로 차용하고, 마지막엔 상수항으로 $s$를 더하여 그 suffix 128bit를 추출하여(mod $2^128$) 반환한다. 데이터에 패딩이 들어가긴 하나, 그 앞의 내용을 자유롭게 변형 가능하다는 점에서 문제를 쉽게 만든다. 마지막을 제외한 모든 블럭을 널바이트로 채우면 $r$에 대한 2차 이상의 항은 모두 소거되므로, $kr+s\mod (2^130-5)$의 suffix 128bit를 알 수 있다. 이때 잘린 비트는 고작해야 2개비트이므로, 많아야 4가지 경우의 수가 존재한다. 따라서 $k_1r+s=x_1\text{ }(mod\text{ }2^130-5)$과 $k_2r+s=x_2\text{ }(mod\text{ }2^130-5)$를 연립하여 $r,s$의 후보 최대 16개를 알 수 있으며 이를 모두 get flag에 시도하여 flag를 얻을 수 있다.

#### Penguin - Crypto

뭔가 펭귄이 보여야할 것 같은 문제이다. 제목부터 ECB 취약점을 써야할 것 같은데, 우선 염두하고 첨부파일을 확인하면 타원곡선을 가장한 무언가가 보인다. chunkwise encryption이며, 각 청크는 청크의 값 $x$에 대해 $\left(g^x+f(i+a+b+gx+gy)+gy\right)\mod N$을 계산한다. 이때 $f$는 계수가 알려진 3차 다항함수이므로 아무 암호학적 기능을 하지 못한다. 따라서, 주어진 암호화에서 $x$는 구할 수 없으나, $g^x$까지는 구할 수 있다는 사실을 확인했다. 이때 $x$가 같으면 $g^x$도 같으므로, "펭귄이 보였던 것처럼" $g^x$로 작성된 bmp파일을 확인하면 flag를 읽을 수 있다.

#### Triple RSA - Crypto

$d\mod (p-1)(q-1)$은 $\mod pq$에서의 $e$의 modular inverse이므로, $\mod pq$에서 $2^(e\times hint)$를 계산하면 $2^{p+\text{ironore15}}$이다. $\text{ironore15}$는 알려진 상수값이므로, 우리는 $2^p$의 값을 계산할 수 있다. $2^p$는 $\mod p$에서 2와 같으므로, $2^p-2$는 $p$의 배수이다. 따라서 $pqr$과 $2^p-2$의 gcd를 계산하면 $p$를 계산할 수 있다. 이번엔 $\mod N$에서 $2^(e\times hint)$를 계산하면 이 값은 $kpq+2^{p+\text{ironore15}}$과 같으므로, $2^(e\times hint)-2^{p+\text{ironore15}}$와 $N$의 gcd로 $pq$의 값을 구할 수 있다. 즉, $q,r$의 값을 계산하여 flag를 복구할 수 있다.

#### Circle Crypto - Crypto

hyperbolic curve over finite field의 대표적 예시 중 하나인 circle curve를 제시하였다. 해당 집합에서의 additive DLP는 정수 유한체에서의 multiplicative DLP로 치환 가능하며, $p-1$이 smooth하기 때문에 쉽게 해결 가능하다.