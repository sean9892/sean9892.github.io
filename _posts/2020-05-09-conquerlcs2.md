---
title: "LCS 정복하기 2"
date: 2020-05-09
categories:
- TUTORIAL
tags:
- LCS
- DP
---

[BOJ9252 LCS 2](https://www.acmicpc.net/problem/9252)

NM lcs backtracking 문제입니다.

2166번에서 구한 대로 dp table을 작성한 후 점화식의 특징을 이용하여 backtrack할 수 있습니다.

길이 a,b인 문자열 A,B에 대해 (a,b)에서 시작해 (0,t) 또는 (t,0) 꼴의 좌표에 도달할 때까지 다음의 세 행동 중 하나를 취하며 추적하여 LCS로 가능한 문자열을 추출할 수 있습니다.

1. **(x,y)=>(x-1,y)** when dp [x] [y] == dp [x-1] [y]
2. **(x,y)=>(x,y-1)** when dp [x] [y] == dp [x] [y-1]
3. **(x,y)=>(x-1,y-1)** when a [x] == b [y]

dp 점화식에 의해 위 세 가지 중 하나는 성립한다는 것을 알 수 있으며 3보다는 1 또는 2를 먼저 취하는 것이 유리하다는 것 또한 [1..x] [1..y]이 [1..x+1] [1..y]와 [1..x] [1..y+1]에 완전히 포함된다는 점에서 알 수 있습니다.

이에 따라 다음과 같은 코드로 AC를 받을 수 있습니다.

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
    cout<<lcs[as][bs]<<"\n";
    stack<char> s;
    int p=as,q=bs;
    while(p&&q){
        if(lcs[p][q]==lcs[p][q-1]){
            q--;
        }
        else if(lcs[p][q]==lcs[p-1][q]){
            p--;
        }
        else{
            s.push(a[p]);
            p--;q--;
        }
    }
    while(!s.empty()){
        cout<<s.top();s.pop();
    }
}
```

