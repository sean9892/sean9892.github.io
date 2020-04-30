---
title: "LCS 정복하기 (1/7)"
date: 2020-05-01
categories:
- OJ
tags:
- LCS
- DP
---

[BOJ9251 LCS](https://www.acmicpc.net/problem/9251)

LCS 정복하기, 그 첫 번째.

가장 기초적인 $O(NM)$ dp로 LCS 길이 구하기입니다.



LCS란 **Longest Common Subsequence**의 약자로, 두 수열의 공통된 부분수열을 의미합니다.

이때 부분수열은 연속하지 않아도 됩니다.

예를 들어 **IHATEPIZZA**와 **ILOVEPIZZA**의 LCS는 길이 7인 **IEPIZZA**라고 할 수 있겠죠.

같은 두 문자열이라고 해도, LCS는 여러 개일 수도 있습니다.

**IEATCHICKEN**과 **IAETCHICKEN**이 그 예시인데요, 길이 7의 **IECHICKEN**과 **IACHICKEN** 모두 LCS임을 알 수 있습니다.



그렇다면 LCS의 길이는 어떻게 구할까요?

DP로 생각해봅시다. 

**DP [i] [j] = (A[1..i]와 B[1..j]의 LCS 길이)**

로 정의하면 다음과 같은 점화식이 성립합니다.

**DP [i] [j] = DP [i-1] [j-1]** *when A[i]==B[j]*

**DP [i] [j] = max( DP [i-1] [j] , DP [i] [j-1] )** *otherwise*

이를 이용하면 $O(N^2)$에 LCS의 길이를 구할 수 있습니다.



```cpp
#include<bits/stdc++.h>
using namespace std;

string a,b;
int lcs[1010][1010];
int main(void){
    cin>>a>>b;
    int as=a.size(),bs=b.size();
    a="_"+a;
    b="_"+b;
    for(int i=1;i<=as;i++){
        for(int j=1;j<=bs;j++){
            if(a[i]==b[j])lcs[i][j]=lcs[i-1][j-1]+1;
            else lcs[i][j]=max(lcs[i-1][j],lcs[i][j-1]);
        }
    }
    cout<<lcs[as][bs];
}
```

