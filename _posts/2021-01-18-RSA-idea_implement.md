---
title: "RSA 원리와 구현"
date: 2021-01-18
categories:
- cryptography
tags:
- cryptography
- RSA
---

## RSA란?

고전 암호와는 달리, RSA, ECC 등은 [계산 이론](https://ko.wikipedia.org/wiki/%EA%B3%84%EC%82%B0_%EC%9D%B4%EB%A1%A0)에서 다루는 '어려운 문제'에 기반하여 암호화를 진행합니다. 이러한 '어려운 문제'는 소인수분해 문제, 이산 로그 문제 등이 있는데, RSA는 그 중 소인수분해가 어려운 문제라는 점을 활용하는 암호화방식입니다.

RSA는 1978년 로널드 라이베스트(Ron **R**ivest), 아디 샤미르(Adi **S**hamir), 레너드 애들먼(Leonard **A**dleman)의 연구에 의해 체계화되어, 이 세 연구자의 이름 앞글자를 따 RSA라는 이름이 붙었습니다.

암호화뿐만 아니라 전자서명이 가능한 최초의 알고리즘으로 알려졌다고 합니다.

양자 컴퓨터가 실용화된 후에는 [쇼어 알고리즘](https://ko.wikipedia.org/wiki/%EC%87%BC%EC%96%B4_%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98)을 이용하여 RSA를 무력화할 수 있을 것으로 알려졌으나, 아직 그러한 시기에 도달하지 않아 많이 사용되고 있습니다.

## RSA의 원리와 구현

다음은 RSA의 동작을 파이썬 코드로 나타낸 것입니다.

```python
from Crypto.Util.number import bytes_to_long, getPrime

bits=1024

def RSA_encrypt(M):
    p=getPrime(bits)
    q=getPrime(bits)
    N=p*q
    e=0x10001
    C=pow(M,e,N)
    return N,e,C

M=bytes_to_long(input("Input Plain Text >> ").encode())
RSA=RSA_encrypt(M)
print(f"""N : {str(RSA[0])}...
e : {str(RSA[1])}
Cipher Text : {hex(RSA[2])}""")
```

아래는 실행 결과이며, N와 암호문은 길이가 길어 앞부분만 출력하고 생략하였습니다.

```
Input Plain Text >> Hello World!
N : 1815770945...
e : 65537
Cipher Text : 0x10c4942a...
```

위 코드의 동작과 결과를 한 번 살펴 봅시다.

우선 RSA의 암호화에서는 특정 비트의 두 소수 p, q를 생성합니다.  약수가 적을 수록 큰 수의 소인수분해는 어렵기 때문에, $N=p \times q$로 정의되는 N을 RSA 암호화에서 활용하게 됩니다.

N과 e의 순서쌍인 $(N,e)$를 공개키라고 부르는데, 이것은 N와 e가 외부 사용자에게 공개되어도 RSA 암호를 쉽게 깰 수 없으므로 공개되어있기 때문입니다.

e를 **공개 지수(public exponent)**라고 부르며 RSA 암호화는 간단하게 평문인 숫자 M에 대해 $M^e$ $mod$ $N$으로 정의됩니다.

하지만 복호화에는 **비밀 지수(private exponent)**라고 불리는 d라는 수가 필요합니다. (N과 d의 순서쌍인 (N,d)는 비밀키라고 부릅니다.)

e와 d는 $ed$ $mod$ $\phi (N) = 1$을 만족하는 수로, 암호문 C에 대해 $C^d$ $mod$ $N$을 계산하면 M과 같아지게 됩니다.

이 사실은 오일러의 정리에 기반합니다. 오일러의 정리는 서로소인 a, n 에 대해 다음이 성립함을 의미합니다.

$a^\phi(n) mod n = 1$

이 때 a=M, n=N인 상황을 생각해본다면 $C^d$ $mod$ $N =$ $M^{ed}$ $mod$ $N =$ $M^{k \times \phi (N) +1}$ $mod$ $N = M$이므로 정상적인 복호화가 가능함을 알 수 있습니다.

## End Card

본 글에서는 다음과 같은 사실을 다뤘습니다.

- RSA는 소인수분해의 어려움에 기반한다
- 공개키, 비밀키는 각각 (N,e)와 (N,d)로 정의된다.
- RSA 암호화는 평문을 e제곱함으로써 구현된다.
- RSA 복호화는 평문을 d제곱함으로써 구현된다.
- 이러한 암호화/복호화가 가능한 것은 오일러의 정리에 기반한다.

다음 글에서는 RSA의 인자가 특정 조건을 만족할 때 사용할 수 있는 공격법에 대해 다룰 예정입니다.