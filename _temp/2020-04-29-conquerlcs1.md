```
---
title: "LCS 정복하기 (1/7)"
date: 2020-04-29
categories:
- OJ
tags:
- LCS
- DP
---
```

[BOJ9251 LCS](https://www.acmicpc.net/problem/9251)

LCS 정복하기, 그 첫 번째.

가장 기초적인 N^2 dp로 LCS 구하기입니다.



LCS란 **Longest Common Subsequence**의 약자로, 두 수열의 공통된 부분수열을 의미합니다.

이때 부분수열은 연속하지 않아도 됩니다.

예를 들어 **IHATEPIZZA**와 **ILOVEPIZZA**의 LCS는 길이 7인 **IEPIZZA**라고 할 수 있겠죠.

같은 두 문자열이라고 해도, LCS는 여러 개일 수도 있습니다.

**IEATCHICKEN**과 **IAETCHICKEN**이 그 예시인데요, 길이 7의 **IECHICKEN**과 **IACHICKEN** 모두 LCS임을 알 수 있습니다.



그렇다면 LCS는 어떻게 구할까요?

DP로 생각해봅시다. 

