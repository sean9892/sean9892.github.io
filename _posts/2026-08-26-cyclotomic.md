---
layout: post
slug: cyclotomic
jektex: true
title: "(Ko) [Paper Review] Factoring with Cyclotomic polynomials"
---

## Intro

[이전 글](https://sean9892.github.io/new-unsafe-primes/)에서 특수한 상황에 적용할 수 있는 소인수분해 알고리즘에 관해 이야기했었습니다. 해당 글에서 다룬 Lenstra-ECM과 마찬가지로, 특수한 조건의 소인수분해 알고리즘은 대개 특정한 군(group)의 위수의 배수를 안다는 가정을 합니다. 이번 글에서는 이러한 아이디어의 근간이 되는 Pollard's \(p-1\) algorithm, Williams's \(p+1\) algorithm과 그 일반화인 Factoring with cyclotomic polynomials에 대해 다루어 보겠습니다.

### Pollard's \(p-1\) algorithm

페르마 소정리에 기반한 알고리즘입니다. \(p-1\)의 배수 \(E\)를 알고 있다고 가정합니다. 페르마 소정리는 다음을 보장합니다.

$$
a^{p-1}\equiv 1\pmod p
$$

이는 \(a\)가 \(p\)의 배수일 때 성립하지 않지만, 그러한 경우는 일반적으로 마주하기 어려우며 마주하더라도 \(N=pq\)와 \(a\)의 gcd가 1이 아닌지 확인하여 \(p\)를 복구할 수 있기 때문에 고려하지 않습니다. \(E\)는 \(p-1\)의 배수이므로, 다음이 성립합니다.

$$
a^E\equiv \left(a^{p-1}\right)^z\equiv 1^z\equiv 1\pmod p
$$

즉 \(a^E-1\)은 \(p\)의 배수이며, 이는 \(N\)으로 나눈 나머지에 대해서도 성립합니다. \((a^E-1)\mod N\)은 쉽게 계산할 수 있으므로, \(\gcd((a^E-1)\mod N, N)\)을 계산하여 \(p\)를 얻을 수 있습니다.

### Williams's \(p+1\) algorithm

[영문 위키피디아](https://en.wikipedia.org/wiki/Williams%27s_p_%2B_1_algorithm)에서 정의하는 Williams's \(p+1\) algorithm을 알아봅시다. 이는 선형점화식을 활용합니다.

$$
V_0=2,\quad V_1=A,\quad V_j=AV_{j-1}-V_{j-2}
$$

선형점화식은 전이행렬을 통해서도 표현할 수 있는데, 여기서는 다음과 같은 식으로 표현할 수 있습니다.

$$
\begin{bmatrix}V_j\\V_{j-1}\end{bmatrix}
=
\begin{bmatrix}A & -1\\1 & 0\end{bmatrix}
\begin{bmatrix}V_{j-1}\\V_{j-2}\end{bmatrix}
$$

귀납적으로 적용하면 다음과 같습니다.

$$
\begin{bmatrix}V_j\\V_{j-1}\end{bmatrix}
=
\begin{bmatrix}A & -1\\1 & 0\end{bmatrix}^n
\begin{bmatrix}V_{j-n}\\V_{j-n-1}\end{bmatrix}
$$

이때 전이행렬의 특성다항식은 \(x^2-Ax+1\)이며, 이는 \(A^2-4\)가 \(\text{mod } p\)에서 이차잉여인지에 따라 대각화가 가능할 수도, 그렇지 않을 수도 있습니다.

\(\left(\frac{A^2-4}{p}\right)=1\)가 성립한다면 특성다항식의 두 근 \(\alpha,\beta\)는 \(\begin{bmatrix}A & -1\\1 & 0\end{bmatrix}\sim \begin{bmatrix}\alpha & 0\\0 & \beta\end{bmatrix}\)을 만족합니다. \(\alpha,\beta\)는 페르마 소정리에 따라 \(\alpha^{p-1}\equiv\beta^{p-1}\equiv1\pmod p\)을 만족하므로, 전이행렬의 multiplicative order는 \(p-1\), 즉 수열의 주기도 \(p-1\)이 됩니다.

\(\left(\frac{A^2-4}{p}\right)=-1\)로 \(\mathbb{F}_p\)에서 대각화가 불가능한 경우라도, \(\mathbb{F}_{p^2}\)에서는 대각화가 가능합니다. \(\mathbb{F}_{p^2}\)에서의 고유값 \(\alpha,\beta\)는 서로 (\(\mathbb{F}_{p^2}\simeq \mathbb{F}_p[\sqrt{D}]\)라는 관점에서) 켤레이고, Frobenius map \(x\mapsto x^p\)에 대해 \(\beta=\alpha^p\)를 만족합니다.

이차방정식의 근과 계수의 관계로부터 \(1=\alpha\beta=\alpha^{p+1}\)이므로 \(\alpha\)의 multiplicative order는 \(p+1\)의 약수입니다. 이는 \(\beta\)도 마찬가지이므로, 수열의 주기는 \(p+1\)의 약수가 됩니다.

즉 \(A^2-4\)가 이차잉여가 아닌 \(A\)를 찾는다면 주기가 \(p+1\)의 약수인 수열을 얻을 수 있습니다. 이차잉여는 약 50% 존재하므로, 평균 2번 정도 시도하면 적절한 \(A\)를 찾을 것이라고 기대할 수 있습니다.

\(p+1\)의 배수인 \(E\)를 안다면, \(V_E\equiv2\pmod p\)라는 것을 알 수 있으므로 \(\gcd(V_E-2,N)\)을 계산하여 \(p\)를 계산할 수 있습니다.

### Williams's \(p+1\) algorithm - alternative

직전 문단에서 설명한 알고리즘은 Pollard's \(p-1\) algorithm과 유사하다는 느낌은 잘 들지 않습니다. 본질적으로 군이지만, 수열을 사용하여 그 구조가 직관적으로 와닿지 않을 수 있기 때문일 것입니다. 이에 군에 집중한 방식의 Williams's \(p+1\) algorithm을 살펴보겠습니다.

1. \(t:=a+b\sqrt{d}\)

2. \(x:=\bar{t}/t\)

3. \(u+v\sqrt{d}:=x^E\)

4. \(\gcd(u-1,v,N)\)을 계산

\(d\)가 이차잉여가 아니라면 \(t\in\mathbb{F}_p[\sqrt{d}]\simeq\mathbb{F}_{p^2}\)이고, 따라서 Frobenius mapping에 의해 \(\bar{t}=t^p\)이므로 \(x=\bar{t}/t=t^{p-1}\)입니다. 즉, \(p+1\)의 배수 \(E\)에 대해 \(x^E=t^{E(p-1)}=\left(t^{p^2-1}\right)^z=1^z=1\)이 되므로, \(u=1,v=0\)이 됩니다. 따라서 \(\gcd(u-1,v,N)\)은 \(p\)가 될 것이라고 기대할 수 있습니다.

### Cyclotomic polynomials

위의 두 알고리즘을 관찰하면, 다음과 같은 조건을 만족해야 한다는 것을 알 수 있습니다.

- 위수의 배수를 아는 군을 선택할 것

- 선택한 군을 부분군으로 갖는 군을 공개된 정보만으로 구성할 수 있을 것

Pollard's \(p-1\) algorithm에서는 \(\mathbb{F}_p\)를, Williams's \(p+1\) algorithm에서는 \(\mathbb{F}_{p^2}\)를 선택했다고 볼 수 있습니다. 각각 quotient polynomal ring과 isomorphic하므로 \(\mathbb{Z}/\langle N,f\rangle\) 꼴의 군의 부분군이라 생각할 수 있습니다.

즉, 조금 더 일반화해보자면 \({\mathbb{F}_{p^k}}^\times\) 꼴의 군이라면 이러한 방식의 공격에 활용할 수 있다는 것입니다.

여기서 **cyclotomic polynomial**이 등장합니다. 군 \({\mathbb{F}_{p^k}}^\times\)의 위수는 \(p^k-1\)입니다. 이때, \(x^k-1\) 꼴의 다항식은 \(k\) 값에 따라 다양한 인수를 갖습니다. 이들은 각각 특정한 \(k^\prime\)에 대해 \(x^{k^\prime}-1\)의 약수인 기약다항식인데, 그러한 다항식을 cyclotomic polynomial이라고 합니다.

### Building a group

앞에서 확인했듯이 최종적으로 사용하고 싶은 것은 \(\mathbb{F}_{p^k}^\times\)입니다. 하지만 \(p\)는 우리가 구하려는 값이므로 \(\mathbb{F}_{p^k}\)를 직접 구성할 수는 없습니다. 임의의 \(k\)-degree 다항식 \(f(X)\)를 선택하여

$$
(\mathbb{Z}/N\mathbb{Z})[X]/(f(X))
$$

를 구성할 수는 있지만, \(f(X)\)가 \(\text{mod }p\)에서 기약이라는 보장은 없습니다. 또한 이후에 필요한 Frobenius map \(x\mapsto x^p\) 역시 \(p\)를 모르는 상태에서는 직접 계산할 수 없습니다.

논문은 이를 해결하기 위해 \(\mathbb{F}_{p^k}\)를 직접 구성하는 대신, 공개된 값만으로 위수가 \(k\)인 automorphism을 갖는 ring을 먼저 구성합니다. 이후 이 ring을 \(\text{mod }p\)에서 바라보았을 때 일부가 \(\mathbb{F}_{p^k}\)가 되고, 구성해 둔 automorphism의 어떤 거듭제곱이 Frobenius map이 되기를 기대합니다. 여기서 Galois group은 field의 연산을 보존하면서 여러 근을 서로 바꾸는 automorphism들의 군 정도로 이해해도 충분합니다.

먼저 다음을 만족하는 auxiliary prime \(m\)을 선택합니다.

$$
m\equiv1\pmod k
$$

\(\zeta_m\)을 primitive \(m\)-th root of unity라고 하면 cyclotomic field \(\mathbb{Q}(\zeta_m)\)의 Galois group은 다음과 같습니다.

$$
\operatorname{Gal}(\mathbb{Q}(\zeta_m)/\mathbb{Q})
\simeq(\mathbb{Z}/m\mathbb{Z})^\times
$$

\(m\)은 prime이므로 우변은 위수가 \(m-1\)인 cyclic group입니다. \(k\mid m-1\)이므로 이 군에는 index가 \(k\)인 부분군 \(H\)가 존재하고, Galois correspondence에 따라 그 fixed field

$$
K_m=\mathbb{Q}(\zeta_m)^H
$$

은 degree가 \(k\)인 cyclic field가 됩니다. 따라서

$$
\operatorname{Gal}(K_m/\mathbb{Q})\simeq C_k
$$

이고, 위수가 \(k\)인 automorphism \(\sigma\)를 얻을 수 있습니다.

이 field는 **Gaussian period**를 사용하여 구체적으로 표현할 수 있습니다. \(g\)를 \(\text{mod }m\)의 primitive root라 하고 \(H\)를 \((\mathbb{Z}/m\mathbb{Z})^\times\)의 \(k\)-th power들로 이루어진 부분군이라 하면,

$$
\eta_i=\sum_{a\in H}\zeta_m^{g^ia},
\qquad 0\le i<k
$$

를 정의할 수 있습니다. 이들은 서로 켤레이며, Galois group의 generator는 다음과 같이 작용합니다.

$$
\sigma(\eta_i)=\eta_{i+1\bmod k}
$$

즉 period basis \(\{\eta_0,\ldots,\eta_{k-1}\}\)를 사용하면 \(\sigma\)는 단순한 cyclic shift로 구현됩니다.

\(K_m\)의 ring of integers를 \(\mathcal{O}_m\)이라 하고 이를 \(\text{mod }N\)으로 내리면 실제 계산에 사용할 ring을 얻습니다.

$$
R_m=\mathcal{O}_m/N\mathcal{O}_m
$$

\(R_m\)의 element는 period basis에 대한 \(k\)개의 계수로 저장할 수 있으며, 각 계수는 \(\text{mod }N\)의 정수입니다. multiplication은 미리 계산한 multiplication table로 수행하고, \(\sigma\)는 계수들을 한 칸씩 순환시키는 linear transformation으로 수행합니다. Gaussian period \(\eta_0\)의 minimal polynomial \(f_m(X)\)를 사용하여 좀 더 익숙한 형태로 표현할 수도 있습니다.

$$
R_m\simeq(\mathbb{Z}/N\mathbb{Z})[X]/(f_m(X))
$$

이 경우 \(\sigma\)는 power basis 위의 \(k\times k\) matrix로 구현됩니다.

이제 \(N=pq\)라고 하면 중국인의 나머지 정리에 의해

$$
R_m\simeq
\mathcal{O}_m/p\mathcal{O}_m
\times
\mathcal{O}_m/q\mathcal{O}_m
$$

으로 생각할 수 있습니다. 선택한 \(m\)에 대해 \(f_m(X)\)가 \(\text{mod }p\)에서 기약이라면 첫 번째 component는 다음과 같이 됩니다.

$$
\mathcal{O}_m/p\mathcal{O}_m\simeq\mathbb{F}_{p^k}
$$

또한 \(\sigma\)를 \(\text{mod }p\)에서 본 automorphism은 \(\operatorname{Gal}(\mathbb{F}_{p^k}/\mathbb{F}_p)\)의 generator가 됩니다. 이 Galois group의 generator들은 Frobenius map의 거듭제곱이므로, 어떤 \(i\)에 대해서는

$$
\tau=\sigma^i,\qquad \gcd(i,k)=1
$$

가 정확히 \(x\mapsto x^p\)로 작용합니다. 어떤 \(i\)가 이에 해당하는지는 알 수 없으므로, 알고리즘에서는 \(\gcd(i,k)=1\)인 \(i\)를 모두 시도합니다.

이 automorphism을 사용하면 \(\Phi_k(p)\)의 배수를 \(p^k-1\)의 배수로 바꿀 수 있습니다. 다음과 같이 정의합시다.

$$
\Psi_k(X)=\frac{X^k-1}{\Phi_k(X)}
$$

그리고 다항식

$$
A(X)=a_0+a_1X+\cdots+a_dX^d
$$

과 automorphism \(\tau\)에 대해 symbolic exponent를 다음과 같이 정의합니다.

$$
z^{A(\tau)}
=
z^{a_0}\tau(z)^{a_1}\cdots\tau^d(z)^{a_d}
$$

\(\text{mod }p\)에서 \(\tau\)가 Frobenius map이라면 \(\tau^j(z)=z^{p^j}\)이므로,

$$
z^{A(\tau)}\equiv z^{A(p)}\pmod p
$$

가 됩니다.

이제 \(\Phi_k(p)\)의 배수 \(E\)가 주어졌다고 하고, random unit \(t\in R_m\)에 대해 \(x=t^E\)를 계산합니다. 올바른 \(\tau\)를 선택했다면

$$
\begin{aligned}
x^{\Psi_k(\tau)}
&\equiv x^{\Psi_k(p)}\\
&=t^{E\Psi_k(p)}\\
&\equiv1\pmod p
\end{aligned}
$$

가 성립합니다. 실제로 \(E=z\Phi_k(p)\)이므로

$$
E\Psi_k(p)
=
z\Phi_k(p)\Psi_k(p)
=
z(p^k-1)
$$

입니다.

마지막으로 \(y=x^{\Psi_k(\tau)}\)와 \(1\)을 같은 basis로 표현합니다.

$$
y=\sum_{j=0}^{k-1}y_j\beta_j,
\qquad
1=\sum_{j=0}^{k-1}c_j\beta_j
$$

그러면 올바른 \(p\)-component에서는 모든 \(c_j-y_j\)가 \(p\)의 배수가 됩니다. 반면 다른 인수 \(q\)에 대해서는 일반적으로 이 관계가 성립하지 않으므로,

$$
\gcd\left(N,c_0-y_0,\ldots,c_{k-1}-y_{k-1}\right)
$$

을 계산하여 \(p\)를 얻을 수 있습니다.

모든 auxiliary prime \(m\)이 원하는 성질을 갖는 것은 아니므로, 알고리즘은 \(m\equiv1\pmod k\)인 prime들을 바꾸어 가며 같은 과정을 반복합니다. 논문은 Chebotarev density theorem을 사용하여 이러한 \(m\)이 충분히 자주 존재함을 보입니다. 즉 이 construction은 \(\Phi_k(p)\) 위수의 군을 직접 만드는 방식이 아니라, 공개된 정보만으로 계산 가능한 군을 만들고 \(\text{mod }p\)에서 그 action이 Frobenius map이 되는 경우를 찾는 방식으로 동작합니다.
