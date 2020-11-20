---
title: "Tonelli-Shanks 알고리즘 구현"
date: 2020-11-20
categories:
- cryptography
tags:
- cryptography
---

Tonelli-Shanks 알고리즘은 mod p에서 Quadratic Residue에 대해 그 제곱근을 구하는 알고리즘이다.

```python
def tonelli_shanks(n,p):
    def isQR(x,p):
        return pow(x,(p-1)//2,p)==1
    if not isQR(n,p):
        return -1
    Q,S=p-1,0
    while Q%2==0:
        S+=1
        Q//=2
    z=None
    for x in range(2,p):
        if not isQR(x,p):
            z=x
            break
    M,c,t,R=S,pow(z,Q,p),pow(n,Q,p),pow(n,(Q+1)//2,p)
    while True:
        if t==0:
            return 0
        elif t==1:
            return R
        k=t*t%p
        ii=None
        for i in range(1,M):
            if k==1:
                ii=i
                break
            k*=k
            k%=p
        b=pow(c,2**(M-i-1),p)%p
        M=ii%p
        c=b*b%p
        t=t*c%p
        R=R*b%p

if __name__=='__main__':
    n,p=map(int,input().split())
    print("STARTED")
    print(tonelli_shanks(n,p))
```





