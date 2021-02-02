---
title: "RSA Puzzles (1)"
date: 2021-02-02
categories:
- cryptography
tags:
- cryptography
- RSA
---

[이전 글 - RSA 원리와 구현](https://sean9892.github.io/cryptography/2021/01/18/RSA-idea_implement/)

이전 글에서는 RSA의 원리와 그 구현에 대해 간단히 소개하였으며, 이번 글에서는 ctf의 RSA Puzzle들에 적용할 수 있는 방법들을 몇가지 소개할 예정이다.

(RSA Puzzle이라는 용어를 사용하는 이유에 관해서는 [secmem - RSA Puzzles](https://www.secmem.org/blog/2020/07/19/RSA-Puzzles/)를 참고)

## Weak N

RSA의 여러 인자 중 N은 RSA의 원리와 안전성 보장에 직결되어있는 요소이다. 이러한 N이 특정한 취약점을 지녀 쉽게 인수분해되거나 phi(N)이 쉽게 계산되어, RSA 암호화 전체를 파훼할 수 있게 되어버린다.

다음은 N에 발생할 수 있는 취약점 중 몇가지이다.

### Small N

N이 작을 경우, N을 쉽게 인수분해할 수 있다는 것은 자명하다.

현재의 경우 N이 100비트 정도의 수라면 가정용 데스크탑에서도 거의 즉시 인수분해되며, 더 많은 시간과 더 좋고 많은 장비를 투자한다면 조금 더 큰 수도 인수분해가 충분히 될 수 있다.

### N with weak factors

현실에서는 존재하지 않는 경우이나, CTF에서는 간혹 기본문제로 등장할 가능성이 있는 경우이다.

- N이 소수 : N이 소수임을 확인하는 것은 빠르게 확인할 수 있고, $\phi(N) = N-1$임을 쉽게 알 수 있기 때문에 RSA의 보안성이 깨지게 된다.
- N이 제곱수 : 마찬가지로, N이 제곱수인지 판별하고 제곱근을 구하는 것은 매우 쉬운 일이다. 이 경우 $\sqrt{N}$이 소수인지를 판별하거나 인수분해하면 되므로, 의도한 것보다 안전하지 않을 수 있다.
- N의 소인수가 다수 : 소인수가 k개일 경우, naive한 방법으로도 소인수분해에 필요한 시간은 최대 $O(N^{1/k})$이므로 의도한 것보다 취약한 조건이 된다.

마지막으로 위 세 경우보다 자주 등장하는 경우로, 두 소인수의 크기가 비슷한 경우 [fermat factorization](https://en.wikipedia.org/wiki/Fermat%27s_factorization_method)을 사용하여 N을 인수분해할 수 있다.

자세히 알아보자면, 우선 N의 인수로 2를 사용하는 경우는 거의 없으며, 그렇지 않더라도 쉽게 전처리가 가능하다. 따라서 N을 홀수라고 가정하고, 홀수 N에 대해 두 약수 p, q는 $N=pq$를 만족한다.

p와 q 모두 홀수이다. 따라서 차이가 짝수이므로, 차이를 2a라 하면 p=k+a, q=k-a라고 가정할 수 있다.

식을 조금 정리하면, $N+a^2=k^2$임을 알 수 있으며 a를 0부터 1씩 증가시키는 것으로 p와 q를 찾을 수 있다.

## Small Public Exponent

### Cuberoot Attack

흔히 Cuberoot attack이라고 부르나, 굳이 e=3인 경우는 아니어도 성립할 수 있는 공격법이다.

공개 지수 e가 작고 메세지가 적당히 짧을 경우, $M^e<N$일 가능성이 존재한다. 이 경우 C의 e제곱근을 구하기만 하면 M을 복원할 수 있다.

반드시 $M^e<N$가 아니더라도 $M^e$를 N으로 나눈 몫이 충분히 작다면 $kN+C$의 e제곱근을 구해 M을 복원할 가능성이 충분히 존재한다.

### Hastad's Broadcast Attack

[CRT](https://ko.wikipedia.org/wiki/%EC%A4%91%EA%B5%AD%EC%9D%B8%EC%9D%98_%EB%82%98%EB%A8%B8%EC%A7%80_%EC%A0%95%EB%A6%AC)는 정수론에서 종종 강력하게 활용되는 아이디어이다. 마찬가지로 RSA를 공격할 때에도 강력하게 작용하는데, 공개지수가 작고 여러 메세지-암호문 쌍을 습득했을 때 그러하다.

위의 Cuberoot attack의 경우 메세지-암호문 쌍이 단 하나여도 된다는 장점이 존재하나, $M^e$를 N으로 나눈 몫이 충분히 작아야한다. 반면 Hastad's Broadcast Attack은 CRT를 활용하여 N의 크기를 키우고, $M^e$가 N보다 작도록 만드는 것이 핵심이다.

Cuberoot Attack에 비해 $M^e$가 커도 된다는 장점이 있으며, 단점은 여러 메세지-암호문 쌍이 필요하다는 것이라고 요약할 수 있다.

이전에는 공개지수로 3과 65537을 함께 자주 사용하였다. 3을 사용하던 이유는 거듭제곱에 필요한 시간이 적기 때문이었으나, 위의 Cuberoot Attack과 Hastad's Broadcast Attack 등 위험성이 널리 알려져 있기 때문에, 더 이상 사용하지 않는다. 마찬가지로 N이 메세지에 비해 크기가 너무 클 경우 이러한 공격법이 허용될 수 있기 때문에, RSA를 공격하거나 구축할 때 고려해야할 요소이다. 요즈음에는 대부분 e=65537을 사용하여 이 공격들을 쉽게 차단하고 있다. CTF의 경우, e=3, e=11, e=17 등 e가 20보다 작다면 한 번쯤 의심해볼만한 공격법이라고 할 수 있겠다.

## End Card

### Summary

- Weak N - 취약한 소인수 및 작은 N, Fermat Factorization
- Small Public Exponent - Cuberoot Attack, Hastad's Broadcast Attack

### Next Post

- Wiener Attack
- Boneh-Durfree Attack