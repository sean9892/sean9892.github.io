---
layout: post
slug: cyclotomic2
jektex: true
title: "(Ko) Factoring with Cyclotomic polynomials - indices with a single prime factor"
---

이전 글에서는 cyclotomic polynomial에 관한 정보를 알 때 소인수분해를 빠르게 할 수 있는, 일반적인 알고리즘에 대해 이야기했었습니다.

그러니까, \(N\)의 소인수 \(p\)에 대해 \(\Phi_n(p)\)의 배수를 안다면 \(\Phi_n(p)\)를 위수로 갖는 특정한 군을 생성해 \(p\)에 대한 정보를 추출할 수 있다는 것이었죠.

해당 논문에서는 Frobenius trace가 automorphism group을 생성한다는 사실을 이용해 generator를 완전탐색하여 맞는 케이스를 항상 순회하도록 구성한 알고리즘이었습니다.

이는 다소 복잡하고 일반적인 케이스를 설명하며, 구현하기가 다소 어려운 알고리즘입니다. 이번 글에서는 \(n\)이 특정한 조건을 만족할 때 간단한 군을 만들어 factoring with cyclotomic polynomial을 쉽게 구현할 수 있는 방법을 살펴보겠습니다.

### \(n\)이 소수라면

\(n\)이 소수라면 \(\Phi_n(x)=x^{n-1}+x^{n-2}+\cdots+1=\frac{x^n-1}{x-1}\)입니다. 자연스럽게 다음과 같은 군을 생각해볼 수 있습니다.

$$
G = \mathbb{F}_{\ell^r}^\times/\mathbb{F}_{\ell}^\times
$$

\(|G|\)는 \(\Phi_n(\ell)\)이 된다는 것을 쉽게 확인할 수 있습니다. 문제는 \(G\)를 어떻게 구현하는가지만, 이는 \(G\)를 구현하지 않으면 해결됩니다. 바로, 다음의 \(H\)를 사용하는 것입니다.

$$
H=\mathbb{F}_{\ell^n}^\times
$$

\(H\)의 임의의 원소 \(x\)에 대해, \(\Phi_n(\ell)\) 거듭제곱을 계산하면, \(|H|=(\ell-1)\Phi_n(\ell)\)이므로 \(x^{\Phi_n(\ell)}\)은 크기 \((\ell-1)\)의 부분군에 위치하게 됩니다. 즉, \(y=x^{\Phi_n(\ell)}\)는 \(y^\ell=y\)를 만족하고, 이는 Frobenius mapping의 고정점이라는 것을 의미합니다. \(H\)에서 Frobenius mapping의 고정점은 \(\mathbb{F}_\ell\)의 원소뿐이므로, \(H\)를 \(n\)차 기약다항식 \(f\)에 대해 \((\mathbb{F}_\ell[\alpha]/f(\alpha))^	imes\)로 인지한다면, 상수항을 제외한 항의 계수가 전부 0임을 의미합니다.

따라서, 실제로는 다음과 같은 군을 사용합니다.

$$
H^\prime = (\mathbb{Z}/N\mathbb{Z})[\alpha]/f(\alpha)
$$

이는 공개된 정보만으로 완전히 계산 가능하며, \(H\)를 포함합니다. 임의의 원소를 고르고 \(\Phi_n(p)\) 거듭제곱하였을 때 \(H\)에서는 상수항이 아닌 항의 계수가 \(0\)이 되므로, \(H^\prime\)에서도 상수항이 아닌 항의 계수가 \(\ell\)의 배수가 됩니다.

무작위한 monic polynomial이 기약 다항식일 확률은 대략 \(n\)에 반비례하므로, 평균 \(n\)회 시도하여 얻을 수 있습니다. 대부분의 경우 \(n\)은 그리 크지 않으므로 충분히 반복할만한 횟수입니다.

## \(n\)이 소수의 제곱이라면

이 경우는 유명한 예시가 하나 있는데, [WACon 2023 Quals - Cry](https://github.com/pcw109550/my-ctf-challenges/tree/master/WACon2023/Qual/cry)입니다. \(N\)의 소인수 \(\ell\)에 대해 \(\ell^2+1\)의 배수가 주어지는 경우입니다.

\(\Phi_4(\ell)=\ell^2+1\)이고, \(\mathbb{F}_{\ell^4}^	imes\)의 유일한 크기 \((\ell^2-1)\)의 부분군은 \(\mathbb{F}_{\ell^2}^	imes\)와 isomorphic합니다. 이 점을 활용하여, 다음과 같은 꼴의 \(\mathbb{F}_{\ell^4}\)에서의 기약다항식 \(f\)를 생각해봅시다.

$$
f(\ell)=\ell^4+a\ell^2+b
$$

한국 고교 수학에서는 **복이차식**이라는 이름으로도 불리는 형태입니다.

\(\mathbb{F}_{\ell^4}^	imes\simeq (\mathbb{F}_{\ell}[\alpha]/f(\alpha))^	imes\)라면 \((\mathbb{F}_{\ell}[\beta]/f(\sqrt{\beta}))^	imes\)는 어떨까요? \(f(\sqrt{\beta})=\beta^2+a\beta+b\)가 되고, 이 다항식이 근을 갖는다면 \(\mathbb{F}_{\ell^4}\)에서도 근을 가져야 하므로, 귀류법에 의해 \(f(\sqrt{\beta})\)도 기약다항식이라는 것을 알 수 있습니다.

따라서 \(\beta=\alpha^2\) 치환을 생각하면 \(\beta\)가 생성하는 부분군은 \((\mathbb{F}_{\ell}[\beta]/f(\sqrt{\beta}))^	imes\simeq(\mathbb{F}_{\ell^2})^	imes\)가 됩니다.

즉, 임의의 원소를 \((\ell^2+1)\)승하면 1차, 3차항의 계수는 \(0\)이 되어야 합니다. 다음의 군으로 계산할 수 있습니다.

$$
((\mathbb{Z}/N\mathbb{Z})[\alpha]/f(\alpha))^\times
$$

## \(n\)이 소수의 거듭제곱이라면

직전 문단의 아이디어를 활용하면, 소수의 거듭제곱인 경우로도 확장할 수 있습니다. \(n=p^k\)일 때 다음 꼴의 기약다항식을 생각해봅시다.

$$
f(\ell) = \ell^{p^k}+a_{p-1}\ell^{(p-1)p^{k-1}}+\cdots+a_{1}\ell^{p^{k-1}}+a_0
$$

굳이 이름붙인다면 복\(p^{k-1}\)차식이라고 할 수 있을 법한 형태죠. \((\mathbb{F}_{\ell}[\alpha]/f(\alpha))^	imes\)는 \(\mathbb{F}_{\ell^{p^k}}\)와 isomorphic하지만, \(\beta=\alpha^{p^{k-1}}\)로 치환한다면, \((\mathbb{F}_{\ell}[\beta]/f(\beta^{1/p^{k-1}}))^	imes\)는 \(\mathbb{F}_{\ell^{p}}\)와 isomorphic하다고 볼 수 있겠습니다.

즉, \(\Phi_{n}(\ell)\) 거듭제곱하게 된다면, 차수가 \(p^{k-1}\)의 배수인 항을 제외하고는 모두 계수가 \(0\)이 되어야 함을 의미합니다.

마찬가지로 다음 군에서 온전히 계산할 수 있겠죠.

$$
((\mathbb{Z}/N\mathbb{Z})[\alpha]/f(\alpha))^\times
$$

## 정리

Factoring with cyclotomic polynomial은 무시할 수 없을 만큼 많은 경우에 이런 특수한 군 형성 방법을 갖고 있습니다. 특히 실용적인 경우는 대다수 \(n\)이 매우 작으므로 일반적인 군 형성 알고리즘보다 단순하게 구현할 수 있습니다.

이번 글에서는 \(n\)이 하나의 소인수만을 갖는 경우를 살펴보았습니다. 이번 글에서 활용한 아이디어와, cyclotomic polynomial 사이의 관계를 이용하면 이런 결과를 좀더 확장할 수 있습니다.

다음 글에서는 소인수가 두 개인 경우에 어떤 성질을 활용하여 단순한 군으로 factoring with cyclotomic polynomial을 구현할 수 있는지 살펴보겠습니다.
