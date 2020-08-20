---
title: "LCS 정복하기 3"
date: 2020-05-09
categories:
- TUTORIAL
tags:
- LCS
- DP
---

[BOJ1958 LCS 3](https://www.acmicpc.net/problem/1958)

단순히 생각해서 LCS(A,B,C) = LCS(LCS(A,B),C)라고 생각할 수 있으나 두 문자열의 LCS가 하나가 아닐 수 있다는 점에서 무수히 많은 반례를 만들 수 있습니다.

2166번과 같은 근본적인 접근으로 다음과 같은 점화식을 세울 수 있습니다.

**DP [i] [j] [k] = DP [i-1] [j-1] [k-1] + 1** *when A [i] == B [j] and B[j] == C[k]*

**DP [i] [j] [k] = max(DP [i-1] [j] [k], DP [i] [j-1] [k], DP [i] [j] [k-1])** *otherwise*

점화식만 정확하게 구현해주면 간단히 구해줄 수 있습니다.

+) 9252번(LCS 2)에서 활용한 아이디어대로 문자열 3개일 때도 확장해주면 backtrack 또한 간단하게 해결 가능합니다.

```cpp
#include<bits/stdc++.h>
using namespace std;

int dp[110][110][110];

int main(void){
	ios::sync_with_stdio(0);cin.tie(0);
	string a,b,c;
	cin>>a>>b>>c;
	const int as=a.size();
	const int bs=b.size();
	const int cs=c.size();
	a="|"+a;
	b="|"+b;
	c="|"+c;
	for(int i=1;i<=as;i++){
		for(int j=1;j<=bs;j++){
			for(int k=1;k<=cs;k++){
				if(a[i]==b[j]&&b[j]==c[k])dp[i][j][k]=dp[i-1][j-1][k-1]+1;
				else dp[i][j][k]=max({dp[i-1][j][k],dp[i][j-1][k],dp[i][j][k-1]});
			}
		}
	}
	cout<<dp[as][bs][cs];
}
```

