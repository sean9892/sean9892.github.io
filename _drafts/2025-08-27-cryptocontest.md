---
title: "2025년 암호분석경진대회 write-up"
description: "2025 cryptocontest"
header: "crypto"
lang: ko
---

2025년도 암호분석경진대회에 참여했습니다. 2022년 최우수상 수상 이후로는 처음 참여하는데, 해가 지날 수록 대회 퀄리티가 개선되는 것 같아 참가 경험이 즐거웠던 것 같습니다.

금년도 출제된 문제는 다음과 같은 주제의 6개 문제이며, 그중 제가 담당한 2,4,5번 문제의 풀이에 관해 이야기하려 합니다.

1) AES를 포함하는 해시의 최적화 (SIMD)
2) 국산암호 LEA에 대한 차분공격경로 자동탐색 ...★
3) Whitebox-AES 구현에 대한 키 복구 공격
4) 위성통신암호 A5-GMR-1에 대한 ciphertext-only 키 복구 공격 ...★
5) ECDH/ECDSA 비밀키 복구 ...★
6) 포렌식→암호학 연계

---

## 5번 - ECDH/ECDSA 비밀키 복구

5번은 금년도 출제된 6개 문제 중 가장 쉬운 문제였습니다.

문제는 Alice와 Bob이 ECDH를 이용해 키를 공유하고, ECDSA를 이용하여 공유한 키를 서명하는 과정을 담고 있습니다.

> 한 가지 재밌는 점은 ECDSA에서 서명하는 메세지를 감추지 않았으므로 ECDH를 이용해 키를 공유한 이점이 사라진다는 것입니다. 도청자는 ECDH를 깨기 위해 ECDLP를 풀 필요 없이 ECDSA의 메세지를 확인하면 됩니다. Bob이 ECDSA로 메세지를 서명하자고 제안하고 Alice가 이것을 받아들인 것은 상황상 조금 어색하다고 볼 수 있겠습니다.

문제에서 제시한 정보는 다음과 같습니다.

- ECDH 및 ECDSA는 표준곡선 중 하나인 [P-521](https://neuromancer.sk/std/nist/P-521)을 사용
- Alice, Bob의 ECDH 공개키
- Alice가 계산한 ECDH 공유비밀
- Alice가 계산한 ECDH 공유비밀의 ECDSA 서명

P-521은 표준 타원곡선 중 하나로, order가 소수이며 군으로써의 구조에 대해 별다른 문제가 알려지지 않은 타원곡선입니다.

해당 곡선과 관련하여 알려진 이슈 중에는 [CVE-2024-31497(PuTTY 관련)](https://nvd.nist.gov/vuln/detail/cve-2024-31497)이 있습니다만, 이는 다수의 서명이 필요한 취약점이므로 본 문제에서는 고려할 수 없습니다.

그렇다면 어딘가에 숨은 조건이 있음을 짐작할 수 있습니다. 아니나 다를까, Bob의 public key가 P-521에 존재하지 않는 점입니다.

```
TypeError: Coordinates [..., 1] do not define a point on Elliptic Curve defined by ... over Finite Field of size ...
```

Bob은 공유비밀을 ECDSA로 서명하자는 수상한 제안을 하고, ECDH에서 P-521 상에 없는 점을 제시했습니다. 이는 Alice에 대한 모종의 공격 시도라 생각할 수 있으며 마침 이러한 정보를 사용하는 공격 기법이 있습니다. 바로 Invalid Curve Attack입니다.

#### Invalid Curve Attack

Weierstrass form의 타원곡선에서, 두 점 $(x_P,y_P)$와 $(x_Q,y_Q)$의 덧셈은 다음과 같이 계산할 수 있습니다.

$$
s = \frac{y_P-y_Q}{x_P-x_Q} \\
x_R = s^2-x_P-x_Q \\
y_R = y_P-s(x_P-x_R)
$$

위의 계산법에서 식의 어느 부분에도 타원곡선 $y^2=x^3+ax+b$의 상수항 $b$를 이용하는 계산이 없습니다.

이는 doubling에서도 마찬가지입니다.

$$
s = \frac{3{x_P}^2+a}{2y_P} \\
x_R = s^2-2x_P \\
y_R = y_P-s(x_P-x_R)
$$

따라서 만약 곡선 상에 실제로 존재하는 점인지 확인하지 않는다면 공격자는 기존의 $b$ 대신 임의의 $b^\prime$을 사용하여 ECDLP가 쉽거나 order가 작은 소인수를 포함하는 등 취약한 타원곡선 $y^2=x^3+ax+b^\prime$ 에서의 계산 결과를 얻도록 유도할 수 있습니다.

본 문제에서는 Bob의 공개키가 order가 $2^{512}$인 타원곡선에 존재합니다. 곡선이 smooth order를 가지므로 부분군의 ECDLP를 해결하고 이를 elaborate하는 방식의 알고리즘을 사용할 수 있으며, 이는 다음과 같은 의사코드로 표현할 수 있습니다.

```
Input: DLP base point G, DLP target point P
answer ← 0
For e ← 0,1,2,...,520
    For bit ← 0,1
        If 2^520-e×(P-(bit×2^e+answer)×G) is the point at infinity Then
            answer ← (bit×2^e+answer)
            Break For
        End If
    End For
End For
Return answer
```

