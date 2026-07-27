````markdown
---
layout: post
slug: new-unsafe-primes
jektex: true
title: "(Ko) [Paper Review] A New Class of Unsafe Primes"
---

## Intro

> 본 글은 Qi Cheng의 논문 [A New Class of Unsafe Primes](https://eprint.iacr.org/2002/109.pdf)을 한글로 풀어 설명하는 글입니다. 글에 소개되지 않은 자세한 내용은 원본 논문을 참고해주세요.

RSA를 포함하여, 소인수분해가 풀기 어렵다는 사실은 암호학에서 자주 인용되는 일방향함수입니다.   계산이 단순하며 빠른 돌파구가 없는 문제는 매력적이기 마련입니다.

이런저런 이유로 이후 등장한 비대칭키 암호는 훨씬 복잡한 구조를 갖고 있기에, 개발자의 입장에서 이해하기 어려운 편입니다. 물론, 누구나 구조를 이해하기 쉽다는 것은 함부로 수정을 감행할 수 있다는 점에서 RSA의 큰 단점입니다.

일반적인 조건의 소인수분해를 해결하는 다항시간 알고리즘은 아직 존재하지 않습니다. 현재 가장 강력한 알고리즘은 **General Number Field Sieve (GNFS)**로,  \(L_n\left[1/3,(64/9)^{1/3}\right]\), Big-O 표기법으로는 \(\operatorname{exp}\left(\left((64/9)^{1/3}+o(1)\right)(\lg n)^{1/3}(\lg\lg n)^{2/3}\right)\)의 시간복잡도를 가지고 있습니다. 지수 시간복잡도보다는 빠르지만 다항 시간복잡도보다는 느리기 때문에, 충분히 큰 수의 소인수분해는 현실적으로 불가능합니다.

일반적인 조건에서 불가능하다면, 특정한 조건을 만족할 때 빠르게 소인수분해할 수 있는 알고리즘을 생각해볼 차례입니다. 암호 체계가 소인수분해를 쓴다면 정말로 무작위한 수를 뽑기보다는 특정한 구성 알고리즘을 사용하여 수를 선택할 것이고, 이는 생성된 수에 무작위에서 벗어난, 특수한 성질을 부여할 것입니다.

그러한 알고리즘은 종류가 매우 다양합니다.

- Fermat factorization

- Pollard's \(p-1\) method

- Williams's \(p+1\) method

- Factoring with cyclotomic polynomials

- **Lenstra Elliptic-Curve Method (Lenstra-ECM)**

- Return of Coppersmith Attack (ROCA)

- ...

이번 글은 **Lenstra Elliptic-Curve Method**에서 시작하여, \(4p-1\) method라는 소인수분해 알고리즘에 대해 알아보겠습니다.

---

## Lenstra Elliptic-Curve Method

RSA의 공개키 \(N\)은 두 큰 소수 \(p,q\)의 곱 \(N=pq\)로 정의됩니다. 이때, 어떤 타원 곡선 \(E:y^2=x^3+Ax+B\)가 \(\mathbb{F}_p\) 상에서 smooth한 위수 \(K:=\#E(\mathbb{F}_p)\)를 갖는다고 가정해 봅시다. 조금 더 엄밀하게, 어떤 자연수 \(U\)에 대해 다음 조건을 만족한다고 생각해 봅시다.

$$
\forall \text{prime }q\mid K,\quad q\le U
$$

\(q^{\left\lfloor\lg_q{K}\right\rfloor+1}> K\)이므로, \(K\)의 소인수분해에서 \(q\)의 최대 지수 \(\nu_q(K)\)는 다음을 만족합니다.

$$
\nu_q(K)\le \left\lfloor\lg_q{K}\right\rfloor
$$

이를 이용해 다음 수식이 성립함을 알 수 있습니다. 이때 \(S\)는 \(K\)의 모든 소인수의 집합입니다.

$$
K = \prod_{q\in S} q^{\nu_q(K)} \mid \prod_{q\in S} q^{\left\lfloor\lg_q{K}\right\rfloor}\\
K \mid \prod_{q\in S} q^{\left\lfloor\lg_q{K}\right\rfloor}
$$

(라그랑주의 정리) 타원 곡선 \(E\) 위의 임의의 점 \(P\) 에 대해, \(KP=\left\vert E(\mathbb{F}_p)\right\vert P=\mathcal{O}\)가 성립합니다.

무한 원점은 임의의 정수를 곱하여도 무한 원점이므로, \(E\) 위의 임의의 점 \(P\)에 대해 \(\left(\prod_{q\in S} q^{\left\lfloor\lg_q{K}\right\rfloor}\right)P=\mathcal{O}\)임을 알 수 있습니다.

위 성질을 이용하여, Lenstra Elliptic-Curve Method는 다음과 같은 과정으로 \(n\)의 소인수를 찾습니다.

1. \(\mathbb{Z}/n\mathbb{Z}\)의 임의의 타원 곡선 \(E: y^2=x^3+Ax+B\)와 그 위의 점 \(P=(x_0,y_0)\)를 선택합니다.

2. \((U!)P\)을 계산합니다. \(U!\)을 직접 계산할 필요는 없으며, 다음과 같이 절차적으로 계산할 수 있습니다.
   
   1. \(P_2 := 2P\)를 계산합니다.
   
   2. \(P_3 := 3P_2\)를 계산합니다.
   
   3. ...
   
   4. \(P_U := UP_{U-1}\)을 계산합니다. \(P_U=(U!)P\)입니다.

3. 덧셈 계산 중 \(\lambda\)의 분모가 \(n\)과 서로소가 아닌 경우가 없다면, \(\left\vert E(\mathbb{F}_p)\right\vert\)의 소인수 중 \(U\)보다 큰 수가 존재한다는 의미입니다. 이 경우 1회의 시도가 실패한 것이므로, 1번으로 돌아가 다시 시도합니다.

4. 덧셈 계산 중 \(\lambda\)의 분모 \(v\)가 \(n\)과 서로소가 아닌 경우가 있었다면, \(\gcd(v,n)\)을 계산합니다. 이 값이 \(n\)이 아니라면 \(p\) 또는 \(q\)이므로 \(n\)을 소인수분해할 수 있습니다.

이번 글에서 소개하는 소인수분해 알고리즘은 Lenstra Elliptic-Curve Method에 기반합니다. 차이점이라면, 

----

## Division Polynomial

타원 곡선 \(y^2=x^3+Ax+B\) 상의 점 \(P:=(x_P,y_P)\)에 대해, \(2P\)의 좌표는 다음과 같이 계산할 수 있습니다.

$$
\begin{align*}
    \lambda &= \frac{3{x_P}^2+A}{2{y_P}}\\
    x_{2P} &= \lambda^2-2{x_P} = \frac{(3{x_P}^2+A)^2-8{x_P}{y_P}^2}{4{y_P}^2}\\
    y_{2P} &= \lambda(x_{P}-x_{2P})-y_{P} = \frac{(3{x_P}^2+A)(x_P-x_{2P})-2{y_P}^2}{2{y_P}}
\end{align*}
$$

\(\lambda\)의 정의 중 분모의 \(2y_P\)가 만약 0이라면 \(2P\)의 x좌표와 y좌표는 정의할 수 없을 것입니다. 타원 곡선에서 그러한 점은 오직 **무한 원점** \(\mathcal{O}\) 뿐이므로, \(2y_P=0\)인 점 \(P\)에 대해 \(2P\)를 계산하면 \(\mathcal{O}\)가 된다는 의미입니다.

이를 임의의 자연수 \(n\)에 대해 확장시켜봅시다. \(nP\)를 계산할 때 \(\lambda\)의 분모를 \(\psi_n\)이라고 하면, 처음 몇 개의 \(\psi_n\)은 다음과 같습니다.

$$
\begin{align*}
    \psi_1 &= 1\\
    \psi_2 &= 2y\\
    \psi_3 &= 3x^4+6Ax^2+12bx-A^2\\
    \psi_4 &= 4y(x^6+5Ax^4+20Bx^3-5A^2x^2-4ABx-8B^2-A^3)\\
\end{align*}
$$

이러한 다항식을 **division polynomial**이라고 합니다. 이는 \(nP=\mathcal{O}\)를 충족하는 점 \(P\)들, 즉 \(n\)-torsion과 큰 관련이 있다고도 볼 수 있습니다.

다음은 division polynomial 사이에 성립하는 점화식입니다.

$$
\begin{align*}
    \psi_{2m+1} &= \psi_{m+2}{\psi_{m}}^3-\psi_{m-1}{\psi_{m+1}}^3\\
    \psi_{2m} &= \left(\frac{\psi_m}{2y}\right)\cdot\left(\psi_{m+2}{\psi_{m-1}}^3-\psi_{m-2}{\psi_{m+1}}^3\right)
\end{align*}
$$

---

## Some stuffs on Elliptic Curves...

타원 곡선에는 **j-invariant**라는 개념이 있습니다. 등장한 배경은 다소 복잡하므로 생략하고, *대수적으로 닫힌 체*에서는 <u>두 타원 곡선이 서로 isomorphic하다</u>는 <u>두 타원 곡선의 j-invariant가 동일하다</u>와 동치입니다.

$$
E : y^2=x^3+Ax+B\\
j(E) := 1728\cdot\frac{4A^2}{4A^2+27B^3}\\[2em]
K : \text{algebraically closed field}\\[2em]
E_1/K \simeq E_2/K \Leftrightarrow j(E_1/K) = j(E_2/K)
$$

처    음 등장한 두 단어의 정의를 간단하게 짚고 넘어가겠습니다.

**대수적으로 닫힌 체(algebraically closed field)**는 임의의 다항방정식이 근을 가지는 체를 말합니다. 복소수의 집합 \(\mathbb{C}\)는 임의의 다항방정식이 근을 가지므로, 대수적으로 닫힌 체입니다.

$$
\forall f\in\mathbb{C}[X] \quad \exists r\in\mathbb{C} \quad f(r)=0
$$

두 타원 곡선(혹은 일반적인 맥락에서 두 군)이 **homomorphic**하다는 것은 다음을 조건하는 함수 \(\phi\)가 존재한다는 뜻입니다. 이러한 \(\phi\)를 **homomorphism**이라고 부릅니다.

$$
\forall P,Q\in E_1 \quad \phi(P)+\phi(Q)=\phi(P+Q)
$$

만약 homomorphism \(\phi\)가 일대일대응 함수라면 **isomorphism**이라 부르고, 두 타원 곡선이 **isomorphic**하다고 합니다.

Homomorphism의 정의역과 공역이 같은 타원 곡선이라면 그러한 \(\phi\)는 **endomorphism**이라고 부릅니다.

그런데 \(\mathbb{F}_p\)는 대수적으로 닫힌 계가 아니므로 앞서 설명한 동치 관계가 성립하지 않습니다. 그중 다음과 같은 한 방향만 성립합니다.

$$
E_1/\mathbb{F}_p \simeq E_2/\mathbb{F}_p \Rightarrow j(E_1/\mathbb{F}_p) = j(E_2/\mathbb{F}_p)
$$

따라서 동일한 j-invariant를 갖는 타원 곡선은 두 개 이상의 isomorphism class로 구성됩니다. j-invariant의 실제 값에 따라 경우의 수를 나누어 보면,

- \(j=0\)이면 최대 6개, (quadratic twist + cubic twist)

- \(j=1728\)이면 최대 4개, (quartic twist)

- 둘 모두 아니라면 정확히 2개 (quadratic twist)

의 isomorphism class가 존재합니다.

세 번째 경우가 일반적이며, 이 경우 해당 j-invariant 값을 갖는 타원 곡선의 isomorphism class는 다음과 같이 2개입니다. 이때 \(k=\frac{27j}{4(1728-j)}\), \(c\)는 \(p\)의 이차 비잉여입니다.

- \(E_1:y^2=x^3+kx+k\)와 isomorphic한 타원 곡선

- \(E_c:y^2=x^3+c^2kx+c^3k\)와 isomorphic한 타원 곡선

조금 변형하면, \(E_c\)가 곡선 \(y^2=c^3(z^3+kz+k)\)와 일대일대응이라는 사실을 알 수 있습니다.

이 형태에 르장드르 기호를 취하면 \(\#E_1(\mathbb{F}_p)+\#E_c(\mathbb{F}_p)=2p+2\)라는 사실을 관찰할 수 있습니다.

$$
\begin{align*}
    \#E_1(\mathbb{F}_p)
    &= 1 + \sum_{x\in\mathbb{F}_p} \left(1+\chi(x^3+kx+k)\right)\\
    &= (p+1) + \sum_{x\in\mathbb{F}_p} \chi(x^3+kx+k)\\
    \#E_c(\mathbb{F}_p)
    &= 1 + \sum_{x\in\mathbb{F}_p} \left(1+\chi(c^3(x^3+kx+k))\right)\\
    &= (p+1) + \sum_{x\in\mathbb{F}_p} \chi(c^3(x^3+kx+k))\\
    &= (p+1) + \sum_{x\in\mathbb{F}_p} \chi(c^3)\chi(x^3+kx+k)\\
    &= (p+1) - \sum_{x\in\mathbb{F}_p} \chi(x^3+kx+k)\\
\end{align*}\\[2em]
\begin{align*}
    \#E_1(\mathbb{F}_p)+\#E_c(\mathbb{F}_p)
    &= 2(p+1) + \sum_{x\in\mathbb{F}_p} \chi(x^3+kx+k) - \sum_{x\in\mathbb{F}_p} \chi(x^3+kx+k)\\
    &= 2p+2
\end{align*}
$$



---

## Some stuffs on Elliptic Curves... (continued)

**Hasse's bound**는 타원 곡선 \(E(\mathbb{F}_p)\)의 점 수 \(\#E(\mathbb{F}_p)\)의 상한과 하한을 보여주는 정리입니다. 구체적인 범위는 다음과 같습니다.

$$
\#E(\mathbb{F}_p)\in[p+1-2\sqrt{p},p+1+2\sqrt{p}]
$$

즉, \(\#E(\mathbb{F}_p)-(p+1)\)의 절댓값이 \(2\sqrt{p}\) 이하임을 나타내는 것이기도 합니다. 이 값을 타원 곡선의 **trace**라고 부릅니다. 흔히 \(\operatorname{tr}(E(\mathbb{F}_p))\)처럼 작성하거나, 문자 \(t\)로 표기하기도 합니다.

**Frobenius endomorphism** \(\pi\)는 다음과 같이 정의되는 endomorphism입니다. 확장된 체에서의 성질을 분석하는 등 타원 곡선을 연구할 때 자주 다루어지는 도구이나, 이번 글에서는 다음과 같은 정의와 성질만 기억하셔도 좋습니다.

$$
\pi: (x,y)\mapsto(x^p,y^p)\\
\pi^2-t\pi+p=0
$$

유리수의 집합 \(\mathbb{Q}\)에 대해, supersingular하지 않은 타원 곡선 \(E(\mathbb{F}_p)\)은 다음을 만족합니다. supersingular라는 새로운 단어가 등장했지만, 여기서는 대부분의 타원 곡선이 supersingular하지 않다는 사실만 알고 넘어갑시다.

$$
\begin{align*}
    \mathbb{Q}(\pi)
    :=& \{a_0+a_1\pi+a_2\pi^2+\cdots \vert a_i\in\mathbb{Q}\}\\
    =& \{a+b\pi\vert a,b\in\mathbb{Q}\} &&(\because \pi^2=t\pi-p)\\
    \simeq& \mathbb{Q}[X]/(X^2-tX+p)\\
    =& \mathbb{Q}\left(\sqrt{t^2-4p}\right)\\
    =& \mathbb{Q}\left(\sqrt{-D}\right) &&(D:=\text{sqaure-free part of }4p-t^2)
\end{align*}
$$

Hasse's bound에 의해 \(t^2\le4p\)이고 \(p\)는 소수이므로 \(t^2=4p\)일 수는 없습니다. 따라서 \(t^2<4p\)이고, \(t^2-4p<0\)이므로 위 식의 마지막 줄은 타당한 변환이라고 볼 수 있습니다.

자세한 과정은 생략하나, 다음과 같은 결과를 얻을 수 있습니다.

$$
\#E(\mathbb{F}_p) = p+1-\operatorname{tr}(\pi)
$$

<details markdown="1">
<summary markdown="span">자세한 과정 보기</summary>
Endomorphism의 덧셈, 뺄셈, 합성의 결과는 endomorphism이므로 \(\mathbb{Z}[\pi]\)의 모든 원소는 endomorphism이며, 이는 \(\mathbb{Z}[\pi]\sub\operatorname{End}_{\overline{\mathbb{F}}_p}(E)\)임을 의미합니다.

supersingular하지 않은 타원 곡선(즉 ordinary한 타원 곡선)은 정의 상 \(\operatorname{End}^0(E):=\operatorname{End}_{\overline{\mathbb{F}}_p}(E)\otimes_{\mathbb{Z}}\mathbb{Q}\)가 imaginary quadratic field(\(\mathbb{Q}\left(\sqrt{-D}\right)\) 꼴의 체)와 isomorphic합니다.

이는 즉 \(K\)(또는 \(\mathbb{Q}(\pi)\))와 동일하므로, ring of integers \(\mathcal{O}_K\)에 대해 \(\mathbb{Z}[\pi]\sub\operatorname{End}(E)\sub\mathcal{O}_K\)가 성립하므로 \(\operatorname{End}(E)\)는 ring of integers \(\mathcal{O}_K\)의 유한한 index를 갖는 subring입니다. 따라서 order입니다.

즉, 다음이 성립하는 conductor \(f\)가 존재합니다.

$$
\operatorname{End}(E) = \mathcal{O}_f = \mathbb{Z}+f\mathcal{O}_K
$$

이는 \(E\)가 Complex Multiplication을 갖는다는 것을 의미합니다.

Frobenius endomorphism \(\pi\)는 임의의 \(P\in E(\mathbb{F}_p)\)에 대해 \(\pi(P)=P\)를 만족하므로 다음 두 식이 성립합니다. 두 번째 줄은 \(1-\pi\)가 separable isogeny이기 때문에 성립합니다.

$$
E(\mathbb{F}_p)=\operatorname{ker}(1-\pi)\\
\#E(\mathbb{F}_p)=\operatorname{deg}(1-\pi)
$$

\(E\)가 CM을 갖기 때문에, 다음과 같은 성질이 성립합니다.

$$
\begin{align*}
    \#E(\mathbb{F}_p)
    &=\operatorname{deg}(1-\pi)\\
    &=N(1-\pi)\\
    &=(1-\pi)\overline{(1-\pi)}\\
    &=(1-\pi)(1-\overline{\pi})\\
    &=1-(\pi+\overline{\pi})+\pi\overline{\pi}\\
    &=1-(\pi+\overline{\pi})+N(\pi)\\
    &=1-(\pi+\overline{\pi})+p\\
    &=1-\operatorname{tr}(\pi)+p\\
    &=p+1-\operatorname{tr}(\pi)\\
\end{align*}
$$
</details>

---

## 4p-1 method

직전에 언급한 식을 다시 살펴보겠습니다. 아래 식에서 \(\left\vert\operatorname{tr}(\pi)\right\vert=1\)이라면 \(E_1\) 또는 \(E_c\)의 점이 정확히 \(p\)가 될 것입니다. RSA에서 공격자는 공개키이자 \(p\)의 배수인 \(N=pq\)을 알고 있으므로, 위수가 \(p\)인 타원 곡선에서 \(N\)을 곱하면 그 결과는 무한 원점 \(\mathcal{O}\)가 될 것입니다.

이는 타원 곡선의 임의의 점 \((x,y)\)를 골라도 division polynomial \(\psi_N(x)\text{ mod }p\)가 0이 됨을 의미합니다. 즉, \(\psi_N(x)\text{ mod }N\)은 \(p\)의 배수입니다. 이를 계산할 수만 있다면 \(\gcd(\psi_N(x),N)\)을 계산하여 \(p\)를 찾을 수 있을 것입니다.

논문의 Table 1에서는 공격에 사용할 수 있는 \(D\)와 대응되는 \(j_D\), 그리고 \(p\)의 꼴을 소개합니다.

| \(D\)   | \(j_D\)                                               | The form of \(p\) |
|:-----:|:---------------------------------------------------:|:---------------:|
| \(3\)   | \(0\)                                                 | \(4p-1=3b^2\)     |
| \(11\)  | \(\left(-2^5\right)^3\)                               | \(4p-1=11b^2\)    |
| \(19\)  | \(\left(-2^5\cdot 3\right)^3\)                        | \(4p-1=19b^2\)    |
| \(43\)  | \(\left(-2^5\cdot 3\cdot 5\right)^3\)                 | \(4p-1=43b^2\)    |
| \(67\)  | \(\left(-2^5\cdot 3\cdot 5\cdot 11\right)^3\)         | \(4p-1=67b^2\)    |
| \(163\) | \(\left(-2^6\cdot 3\cdot 5\cdot 23\cdot 29\right)^3\) | \(4p-1=163b^2\)   |

Division polynomial의 값을 계산할 때, 단순히 앞서 소개한 점화식을 사용한다면 계산해야 하는 항의 수가 지수적으로 증가한다면 이를 계산할 수 없을 것입니다. 저자는 연속한 인덱스의 division polynomial의 값을 계산할 때 필요한 항의 수가 \(O(\lg N)\)개임을 보입니다.

Division polynomial에 대해 다음의 점화식이 성립합니다.

$$
\begin{align*}
\psi_{4n+1}
    &= 16(x^3 + Ax + B)\psi_{2n+2}\psi{2n}^3
       - \psi_{2n-1}\psi_{2n+1}^3, \\
\psi_{4n+2}
    &= \psi_{2n+1}
       \left(
           \psi_{2n+3}\psi_{2n}^2
           - \psi_{2n-1}\psi_{2n+2}^2
       \right), \\
\psi_{4n+3}
    &= \psi_{2n+3}\psi_{2n+1}^3
       - 16(x^3 + Ax + B)\psi_{2n}\psi_{2n+2}^3, \\
\psi_{4n+4}
    &= \psi_{2n+2}
       \left(
           \psi_{2n+4}\psi_{2n+1}^2
           - \psi_{2n}\psi_{2n+3}^2
       \right).
\end{align*}
$$

이를 조금 일반화하면 다음과 같이 연속한 \(j+1\)개의 division polynomial을 계산하는데 필요한 division polynomial의 값을 찾을 수 있습니다.

$$
\psi_i(x),\ \psi_{i+1}(x),\ \cdots,\ \psi_{i+j}(x)\\
\text{depend on}\\

\psi_{\lceil i/2\rceil-2},\ 
\psi_{\lceil i/2\rceil-1},\ 
\cdots,\ 
\psi_{\lfloor(i+j)/2\rfloor+1},\ 
\psi_{\lfloor(i+j)/2\rfloor+2}
$$

전자의 항 개수는 \(j+1\)개, 후자의 항 개수는 \(5+\lfloor(i+j)/2\rfloor-\lceil i/2\rceil\)개입니다. 이 변환은 \(j\ge 10\)이라면 항 개수가 줄어들고, 그렇지 않은 경우 항의 수가 10개 이하로 상한이 정해져 있습니다. 실제로 그래프를 그려서 성립함을 확인할 수 있습니다.

<img title="" src="/assets/img/newunsafe_termcount.png" alt="" width="389" data-align="center">

인덱스는 대략 절반씩 줄어들고 있고, 각 스텝에서 필요한 연속한 division polynomial의 개수 역시 상한이 존재하므로, 대략 \(O(\lg n)\)개의 division polynomial을 계산하게 됩니다.

Division polynomial의 값 역시 특정 x좌표에서 계산한 값을 \(N\)으로 나눈 나머지만 계산한다면 무한정 발산하지 않으므로, 구하려는 division polynomial의 값을 \(O(\lg N)\)번의 ring operation으로 계산할 수 있습니다.

정리한 알고리즘의 의사코드입니다.

```
For each j in {j_D values in Table 1}:
    compute a:=j/(1728-j) mod N
    randomly choose B1 integers c_1,...,c_B1
    randomly choose B2 integers x_1,...,x_B2
    For each c in {c_1,...,c_B1}:
        For each x in {x_1,...,x_B2}:
            compute z:= Ψ_N(x) mod N
                of the elliptic curve y^2=x^3+3ac^2x+2ac^3
            compute gcd(z,n)
            If the gcd is non-trivial, output the result and exit
        End For
    End For
End For
```
````
