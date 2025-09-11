---
title: "Introduction and Proof for Tonelli-Shanks Algorithm"
description: "bsgs"
header: "Crypto"
lang: ko
---

CTF Crypto task를 풀다 보면, 간혹 $m^2 \text{ mod }p$ 값으로부터 $m$의 값을 복원해야 하는 경우가 존재하며, 이때 사용할 수 있는 알고리즘이 Tonelli-Shanks Algorithm이다.

Tonelli-Shanks Algorithm은 $\mathbb{Z}/p\mathbb{Z}$에서 제곱근을 $O(\log^2 p)$에 해결하는 알고리즘으로써, 조금 응용한다면 이차방정식까지도 동일한 시간복잡도에 해결 가능한 알고리즘이다.



주어진 홀수인 소수 $p$와 $n\in\mathbb{Z}/p\mathbb{Z}$에 대해 $x^2\equiv n\text{ }(\text{mod }p)$인 $x$를 출력하는 Tonelli-Shanks Algorithm은 다음과 같은 단계를 거쳐 진행된다.

1. $n^\frac{p-1}{2}\equiv1\text{ }(\text{mod }p)$인지 확인한다. 만약 아니라면 제곱근이 존재하지 않는다.
2. $p-1=Q\cdot2^S$인 홀수 $Q$와 음이 아닌 정수 $S$를 구한다.
3. $i:=2$로 $i$를 초기화한 후 $i^\frac{p-1}{2}\equiv1\text{ }(\text{mod }p)$이 아닐 때까지 $i$를 증가시키는 과정을 반복한다. \
종료 시점의 $i$ 값을 $z$라고 정의한다.
4. 다음과 같이 변수에 값을 대입한다. \
$M:= S$ \
$c:\equiv z^Q\text{ }(\text{mod }p)$ \
$t:\equiv n^Q\text{ }(\text{mod }p)$ \
$R:\equiv n^\frac{Q+1}{2}\text{ }(\text{mod }p)$
5. 다음 과정을 반복한다. \
$t=0$이면 $0$을 출력하고 종료한다. \
$t=1$이면 $R$을 출력하고 종료한다. \
$0<i<M$ 과 $t^{2^i}\equiv1\text{ }(\text{mod }p)$를 만족하는 최소의 자연수 $i$를 찾는다. \
$b:\equiv c^{2^{M-i-1}}\text{ }(\text{mod }p)$ \
$M:=i$ \
$c:\equiv b^2\text{ }(\text{mod }p)$ \
$t:\equiv tb^2\text{ }(\text{mod }p)$ \
$R:\equiv Rb\text{ }(\text{mod }p)$

---

### Tonelli-Shanks Algorithm의 정당성 증명

알고리즘의 정당성 증명은 다음과 같이 기술할 수 있다. 우선 다음의 두 명제를 확인하자.

#### Claim 1.

$\text{mod }p$에서 0이 아닌 quadratic residue는 정확히 $\frac{p-1}{2}$개 존재한다.

Proof)

$1\le k\le\frac{p-1}{2}$일 때 $k^2\equiv (p-k)^2\text{ }(\text{mod }p)$이다. 따라서 0이 아닌 quadratic residue는 최대 $\frac{p-1}{2}$개 존재한다.

$1\le a<b\le\frac{p-1}{2}$인 두 정수 $a,b$를 생각해보자.

$b^2-a^2\equiv (a+b)(a-b)\text{ }(\text{mod }p)$이고, $2\le a+b\le p-1$, $a\neq b$이므로 $b^2-a^2\not\equiv0\text{ }(\text{mod }p)$이다.

따라서 $1,2,3,...,\frac{p-1}{2}$는 제곱하였을 때 서로 다른 값을 가지므로 정확히 $\frac{p-1}{2}$개의 0이 아닌 quadratic residue가 존재한다.

#### Claim 2.

$n$이 $\text{mod }p$에서 quadratic residue이다 $\Leftrightarrow$ $n^\frac{p-1}{2}\equiv1\text{ }(\text{mod }p)$

Proof)

$n$이 $\text{mod }p$에서 quadratic residue인 것과 $x^2\equiv n\text{ }(\text{mod }p)$인 $x$가 존재하는 것은 동치이다.

이는 페르마 소정리에 의해 $n^\frac{p-1}{2}\equiv(x^2)^\frac{p-1}{2}\equiv x^{p-1}\equiv1\text{ }(\text{mod }p)$과 동치이다.

변수들의 초기값을 다시 기술하면 다음과 같다.

- $M=S$
- $c\equiv z^Q\text{ }(\text{mod }p)$
- $t\equiv n^Q\text{ }(\text{mod }p)$
- $R\equiv n^\frac{Q+1}{2}\text{ }(\text{mod }p)$

위 초기값에 관해 다음과 같은 사실을 알 수 있다.

- $z$는 quadratic non-residue이므로 $c^{2^{M-1}}\equiv z^{Q\cdot2^{S-1}}\equiv z^\frac{p-1}{2}\equiv -1\text{ }(\text{mod }p)$이 성립한다.
- $n$은 quadratic residue이므로 $t^{2^{M-1}}\equiv n^{Q\cdot2^{S-1}}\equiv n^\frac{p-1}{2}\equiv 1\text{ }(\text{mod }p)$이 성립한다.
- $R^2\equiv n^{Q+1}\equiv nt\text{ }(\text{mod }p)$이다.

한 번의 반복에서 $M,c,t,R$에 새로이 대입되는 값 $M^\prime,c^\prime,t^\prime,R^\prime$는 다음과 같이 정의됨을 기억하자.

- $b\equiv c^{2^{M-i-1}}\text{ }(\text{mod }p)$
- $M^\prime$은 $0<M^\prime<M$ 과 $t^{2^{M^\prime}}\equiv1\text{ }(\text{mod }p)$를 만족하는 최소의 자연수
- $c^\prime\equiv b^2\text{ }(\text{mod }p)$
- $t^\prime\equiv tb^2\text{ }(\text{mod }p)$
- $R^\prime\equiv Rb\text{ }(\text{mod }p)$

이러한 정의에 따라 변화한 값에 대해서도 초기값에서와 동일한 성질들이 몇가지 성립함을 확인할 수 있다.

- ${c^\prime}^{2^{M^\prime-1}}\equiv b^{2^i}\equiv c^{2^{M-1}}\equiv -1 \text{ }(\text{mod }p)$
- ${t^\prime}^{2^{M^\prime-1}}\equiv t^{2^{M^\prime-1}}b^{2^{M^\prime}}\equiv(-1)\times(-1)\equiv1\text{ }(\text{mod }p)$
- ${R^\prime}^2\equiv R^2b^2 \equiv ntb^2 \equiv nt^\prime\text{ }(\text{mod }p)$

이때 $t^{2^{M-1}}\equiv 1\text{ }(\text{mod }p)$이므로 $0<M^\prime<M$ 인 $M^\prime$은 항상 존재하며 $M$의 값이 항상 감소한다.

이러한 반복 과정에서 $M=1$이 되는 순간 $1\equiv t^{2^{M-1}}\equiv t^1 \text{ }(\text{mod }p)$이므로 $t\equiv1\text{ }(\text{mod }p)$이며, $R^2\equiv nt\equiv n\text{ }(\text{mod }p)$이므로 $R$은 $x^2\equiv n\text{ }(\text{mod }p)$의 해가 된다.

---

#### Tonelli-Shanks Algorithm의 시간복잡도 증명

위에서 기술한 알고리즘의 동작 과정 중 1., 2., 4.는 거듭제곱 연산과 대입 연산만으로 구성되므로 분할정복을 이용한 거듭제곱을 사용하면 $O(\log p)$에 수행 가능함을 알 수 있다.

3.의 경우 가장 작은 quadratic non-residue $x$에 대해 $O(x)$의 시간에 수행되는데, Claim 2에서 증명하였듯 어떤 residue가 quadratic non-residue일 확률은 50%이므로 평균 2회의 반복으로 quadratic non-residue를 찾을 수 있다. 최악의 경우에도 $\sqrt{p}$ 이하의 quadratic non-residue가 존재함이 보장된다. 본 글에서 다루기에는 다소 글이 난잡해지므로 생략한다. (증명)

5.에서 $i$를 찾는 과정은 $O(M)$의 시간을 소요하며 $M=O(\log p)$이므로 이 과정은 $O(\log p)$의 시간 내에 종결된다. 이외의 과정 역시 $O(\log p)$에 종료됨을 간단히 확인할 수 있으며, 이러한 과정이 최대 $O(\log p)$번 반복되므로 $O(\log^2 p)$의 시간에 종결됨을 알 수 있다.

따라서 3.의 소요 시간을 평균적인 상수 시간으로 가정한다면 $O(\log p+1+\log^2 p)=O(\log^2 p)$의 시간에 Tonelli-Shanks 알고리즘이 종료됨을 알 수 있다.

---

#### Tonelli-Shanks Algorithm의 구현

CTF 암호학에서 자주 사용되는 언어는 SageMath, Python이다. SageMath에서는 sage.rings.finite_rings.integer_mod의 square_root_mod_prime을 통해 간단하게 Tonelli-Shanks 알고리즘을 사용할 수 있으며, square_root_mod_prime_power와 같은 확장 또한 사용 가능하다. 따라서 개인적으로 SageMath를 이용하길 권장하나, 그렇지 못하는 경우를 위해 Python에서 Tonelli-Shanks를 구현하는 코드를 간단하게 소개한다.

```python
def tonelli_shanks(n,p):
    def isQR(x,p):# check whether x is quadratic residue
        return pow(x,(p-1)//2,p)==1
    # (1.)
    if not isQR(n,p):
        return -1

    # (2.)
    Q,S=p-1,0
    while Q%2==0:
        S+=1
        Q//=2

    # (3.)
    z=None
    for x in range(2,p):
        if not isQR(x,p):
            z=x
            break
    # (4.)
    M,c,t,R=S,pow(z,Q,p),pow(n,Q,p),pow(n,(Q+1)//2,p)

    # (5.)
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

# test
if __name__=='__main__':
    n,p=map(int,input().split())
    print("STARTED")
    print(tonelli_shanks(n,p))
```