---
title: "LCS 정복하기 (4/7)"
date: 2020-05-15
categories:
- TUTORIAL
tags:
- LCS
- DP
- Hirschberg
---

[BOJ18438 LCS 5](https://www.acmicpc.net/problem/18438)

이전에 풀이를 작성한 LCS 1/2/3에 비해 갑자기 난이도가 수직 상승한 문제입니다. 

(LCS 4는 특수한 케이스니 제외합니다. LCS 4의 풀이는 나중에 다른 글에서 소개하도록 하겠습니다.)

최대 길이 7000의 문자열 두 개의 LCS를 TL 1s, ML 7MB에 구해야합니다.

TL은 그럭저럭 평범한 것 같은데, ML이 심상치 않다. 이 ML이 난이도를 D2까지 올려놓은 원인인 셈이죠.

LCS 2 문제에서 한 대로 공간복잡도 $O(NM)$에 역추적하려고 하면 최대한 크기가 작은 short형을 사용하더라도 MLE는 피할 수 없습니다.

만약 길이만을 구하는 것이었다면 토글링을 통해 공간복잡도 $O(min(N,M))$ 정도에 해결하는 것은 할만 할텐데, 역추적이 요구되어 토글링만으로는 해결이 불가능합니다.

이 때 사용하는 것이 바로 **Hirschberg's Algorithm**입니다.



LCS의 기본적인 점화식은

**DP [i] [j] = DP [i-1] [j-1] + 1** *when A[i]==B[j]*

**DP [i] [j] = max( DP [i-1] [j] , DP [i] [j-1] )** *otherwise*

라는 것을 수차례 언급했었습니다.

점화식을 잘 살펴보면 DP [i] [j]가 DP [i-1] [j], DP [i] [j-1], DP [i-1] [j-1] 중 하나의 값에 의존적이라는 걸 알 수 있습니다.

DP table의 각 칸을 노드로 삼는 그래프를 생각해봅시다.

DP [i] [j]가 DP [a] [b] ((a,b)는 (i-1,j), (i,j-1),(i-1,j-1) 중 하나) 의 값에 의존적일 때 (i,j) -> (a,b)의 간선을 추가한다고 생각해봅시다.

이 DP table은  사이클이 없는 평면 방향 그래프, 즉 planar DAG입니다.

이 DAG에서의 최장경로의 길이가 두 문자열의 LCS인거죠.

이 최장경로는 DP table의 모든 행과 열을 한 번 이상 지나는데, 이를 이용하여 분할정복을 적용하겠습니다.

그렇다면 탐색하는 table의 넓이가 매 호출마다 절반으로 줄어드므로 재귀호출에 사용하는 메모리는 $O(logM)$이고, 매 호출마다 토글링에 필요한 메모리는 $O(M)$, 답 저장에는 $O(N)$의 메모리가 필요하므로 전체 공간 복잡도는 $O(M)$ 또는 $O(N)$에 지배적입니다.



*2020/05/18 수정 - 시간복잡도 관련 내용 추가*

LCS 역추적에 꽤나 복잡한 로직을 사용하여 메모리를 최적화하였는데, 혹시 시간복잡도가 naive한 방법에 비해 커지거나 더 작아지진 않았을까 하는 의문이 들 수 있습니다.

분석해보자면, 결국에는 역추적을 위해 모든 행에 대해 함수가 호출될 것이고(즉 $O(M)$번 호출됨) 매 호출마다 $O(N)$의 시간이 소요되므로 $O(NM)$의 시간이 필요합니다. 상수에 의해 실행시간이 차이가 날 수 있으나 시간복잡도는 naive한 방법과 일치합니다.



이를 잘 구현한다면 다음과 같은 코드를 작성할 수 있습니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

template <typename it, typename bi>
void _set(it x,vector<bool> const &in,bi lcs){
    for(vector<bool>::const_iterator xs=in.begin();xs!=in.end();++xs,++x)if(*xs)*lcs++ = *x;
}

template <typename it>
void llen(it xl,it xh,it yl,it yh,vector<int> &l){
    vector<int> cur(distance(yl, yh)+1,0);
    vector<int> prv(cur);
    for(it x=xl;x!=xh;++x){
        swap(prv, cur);
        int i=0;
        for(it y = yl;y!=yh;++y,++i)
            cur[i+1]=*x==*y?prv[i]+1:max(cur[i],prv[i+1]);
    }
    l=cur;
}

template <typename it>
void _calc(it xo,it xl,it xh,it yl,it yh,vector<bool> &in){
    const int s=distance(xl,xh);
    if(!s)return;
    if(s==1){
        in[distance(xo,xl)]=find(yl,yh,*xl)!=yh;
        return;
	}
    it xm=xl+s/2;
    vector<int> vb,ve;
	reverse_iterator<it> hx(xh),mx(xm),hy(yh),ly(yl);
    llen(xl,xm,yl,yh,vb);
    llen(hx,mx,hy,ly,ve);
    vector<int>::const_reverse_iterator e=ve.rbegin();
    int lm=-1;
    it y=yl,ym=yl;
    for (vector<int>::const_iterator b=vb.begin();b!=vb.end();++b,++e){
        if (*b+*e>lm){
    		lm=*b+*e;
        	ym = y;
    	}
        if (y!=yh)y++;
    }
    _calc(xo,xl,xm,yl,ym,in);
    _calc(xo,xm,xh,ym,yh,in);
}

void lcs(string const &xs,string const &ys,string &res){
    vector<bool> in(xs.size(),false);
    _calc(xs.begin(),xs.begin(),xs.end(),ys.begin(), ys.end(),in);
    _set(xs.begin(),in,back_inserter(res));
}

int main(void){
	ios::sync_with_stdio(0);cin.tie(0);
	string a,b,res;
	cin>>a>>b;
	lcs(a,b,res);
	cout<<res.size()<<"\n";
	cout<<res;
}
```

