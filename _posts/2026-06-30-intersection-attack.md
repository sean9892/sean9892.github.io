---
layout: post
slug: intersection-attack
jektex: true
title: "Intersection attack from the scratch"
---

## Introduction

In this post, we are going to illustrate how interesection attack on UOV works, from Kipnis-Shamir attack.

It involves some concepts from linear algebra:

- quadratic forms,
- characteristic polynomial,
- Cayley-Hamilton theorem.

The goal is to explain why UOV-like trapdoors can be viewed as hidden linear subspaces with special bilinear-algebraic properties. This viewpoint is one of the basic insights behind several attacks on multivariate-quadratic cryptosystems.

## Preliminaries

### Quadratic form

Let \(V\) be a finite-dimensional vector space over a field \(K\). A quadratic form is a map

$$
    Q:V\rightarrow K
$$

such that for all \(\lambda\in K\),

$$
    Q(\lambda x) = \lambda^2 Q(x).
$$

A polar form associated to \(Q\) is defined by

$$
    B_Q(x,y) = Q(x+y)-Q(x)-Q(y)
$$

and it is bilinear. After choosing a basis of \(V\simeq K^n\), every quadratic polynomial can be represented as

$$
    Q_M(x)=x^T M x
$$

for some matrix \(M\in K^{n	imes n}\). Expanding this expression gives

$$
    x^T Mx  = \sum_i m_{ii}x_i^2 + \sum_{i<j}(m_{ij}+m_{ji})x_ix_j.
$$

Therefore, the individual entries \(m_{ij}\) and \(m_{ji}\) are not independently visible in the quadratic polynomial; only their sum \(m_{ij}+m_{ji}\) appears.

### Symmetric invariance

The polar form of \(Q_M(x)=x^T M x\) is

$$
    B_M(x,y) = Q_M(x+y) - Q_M(x) - Q_M(y) = x^T(M+M^T)y.
$$

So the bilinear information attached to \(Q_M\) is represented by \(M+M^T\).

When the field characteristic \(\operatorname{char}(K)\) is not \(2\), we may replace \(M\) by the symmetric matrix \(\frac{M+M^T}{2}\) without changing th equadratic form. Equivalently, the skew-symmetric party of \(M\) does not contribute to \(x^TMx\).

Since there's a critical attack on UOV-like schemes over an even characteristic called [wedge product attack](https://eprint.iacr.org/2025/1143.pdf), so we don't consider the even characteristic one in this post.

### UOV

UOV stands for **Unbalanced Oil and Vinegar**. In secret coordinates, the variables are split into **vinegar** variables and **oil** variables:

$$
    x=(x_V,x_O), \qquad x_V\in K^{n-m}, \qquad x_O\in K^m.
$$

The central quadratic map is

$$
    F=(F_1,\ldots,F_m):K^n\to K^m.
$$

The defining UOV property is that the central polynomials contain **no oil-oil quadratic terms**. A typical component has the form

$$
    F_\ell(x_V,x_O) = \underbrace{\sum_{a,b}\alpha^{(\ell)}_{ab}x_{V,a}x_{V,b}}_{\text{vinegar-vinegar terms}} + \underbrace{\sum_{a,b}\beta^{(\ell)}_{ab}x_{V,a}x_{O,b}}_{\text{vinegar-oil terms}}.
$$

There are vinegar-vinegar terms and vinegar-oil terms, but no terms of the form

$$
    x_{O,a}x_{O,b}.
$$

Equivalently, the matrix of the quadratic part of \(F_\ell\) has block shape

$$
F_\ell =
    \begin{pmatrix}
        A_\ell & B_\ell\\
        C_\ell & 0
    \end{pmatrix},
$$

where the lower-right block corresponds to oil-oil products.

The oil subspace in secret coordinates is

$$
    O_0=\{(0,x_O):x_O\in K^m\}.
$$

Since there are no oil-oil terms, every central component vanishes on this subspace:

$$
    F_\ell(o)=0
    \qquad
    \text{for all }o\in O_0.
$$

More importantly for the attacks, the polar form also vanishes on pairs of oil vectors:

$$
    F_\ell'(o_1,o_2)=0
    \qquad
    \text{for all }o_1,o_2\in O_0.
$$

The public key hides this structure by composing the central map with invertible linear or affine maps. In the homogeneous linearized notation, one may write

$$
    P=S\circ F\circ T,
$$

where \(T\) hides the variables and \(S\) mixes the output equations. The hidden public oil subspace is then

$$
    O=T^{-1}(O_0).
$$

Recovering \(O\) is essentially a **key-recovery attack**: once the attacker knows the oil subspace, the signing trapdoor can be reconstructed or simulated.

The standard UOV trapdoor view is precisely that the public quadratic map vanishes on a secret \(m\)-dimensional oil subspace, and after fixing a vinegar component, signing reduces to solving a linear system in the oil variables.

### Characteristic polynomial

For a square matrix \(A\in K^{n	\times n}\), its characteristic polynomial is

$$
    \chi_A(t)=\det(tI_n-A).
$$

The Cayley-Hamilton theorem says that every square matrix satisfies its own characteristic polynomial:

$$
    \chi_A(A)=0.
$$

If

$$
\chi_A(t)=\prod_r f_r(t)^{e_r}
$$

is the factorization into irreducible factors over \(K\), then the kernels

$$
    \ker f_r(A)^{e_r}
$$

give \(A\)-invariant subspaces. In particular, if \(f_r(t)=t-\lambda\), then

$$
    \ker(A-\lambda I)
$$

is the eigenspace of \(A\) for the eigenvalue \(\lambda\).

This is useful because the Kipnis-Shamir attack constructs matrices for which the hidden oil subspace is invariant. Factoring characteristic polynomials then gives candidate invariant subspaces, which can be tested against the oil-space condition \(P'(O,O)=0\).

## Kipnis-Shamir attack

Let \(P=(p_1,\ldots,p_m)\) be the public homogeneous quadratic map, and let \(M_i\) be the matrix of the polar form of the \(i\)-th public component:

$$
    p_i'(x,y)=x^TM_i y.
$$

The oil-space property gives

$$
    M_iO\subseteq O^\perp
$$

for every \(i\).

Now consider the **balanced** Oil and Vinegar case, where \(n=2m\).

Then

$$
    \dim O=m,
    \qquad
    \dim O^\perp=n-m=m.
$$

If \(M_i\) is invertible, then

$$
    \dim M_iO=m.
$$

Since \(M_iO\subseteq O^\perp\) and both spaces have dimension \(m\), we obtain

$$
    M_iO=O^\perp.
$$

Therefore, for two invertible matrices \(M_i\) and \(M_j\),

$$
    M_j^{-1}M_iO = M_j^{-1}O^\perp = O.
$$

So the hidden oil space \(O\) is an invariant subspace of

$$
    W_{ij}=M_j^{-1}M_i.
$$

This is the key observation of the Kipnis-Shamir attack: recover \(O\) by finding a common invariant \(m\)-dimensional subspace of several matrices \(W_{ij}\).

In practice, one factors the characteristic polynomial of \(W_{ij}\), obtains candidate invariant subspaces from the factors using Cayley-Hamilton, combines them when necessary, and tests whether the resulting subspace satisfies

$$ 
    P'(o_1,o_2)=0
    \qquad
    \text{for all }o_1,o_2\in O.
$$

The balanced case \(n=2m\) is weak because \(M_iO=O^\perp\) becomes an equality. For unbalanced UOV, where \(n>2m\), we still have

$$
    M_iO\subseteq O^\perp,
$$

but now

$$
\dim O^\perp=n-m>m.
$$

Thus \(M_iO\) is usually only a proper subspace of \(O^\perp\), and different images \(M_iO\) and \(M_jO\) no longer have to be equal. This is why the direct Kipnis-Shamir invariant-subspace argument stops working cleanly in the unbalanced case.

In the balanced case \(M_iO=O^\perp\), while for \(n>2m\) the equality need not hold, so \(M_j^{-1}M_i\) no longer necessarily preserves \(O\).

**Caveat**: This doesn't mean Kipnis-Shamir cannot applied on the unbalanced case. One may consider some probabilistic relation and seek for the instance where his assumption holds. However, since the success rate exponentially decreases as the imbalance \(n-2m\) grows.

## Intersection attack

The intersection attack generalizes the Kipnis-Shamir idea to the unbalanced case.

Even when

$$
    M_iO\neq M_jO,
$$

both spaces still lie inside \(O^\perp\):

$$
M_iO\subseteq O^\perp,
\qquad
M_jO\subseteq O^\perp.
$$

Each of \(M_iO\) and \(M_jO\) has dimension \(m\), while \(O^\perp\) has dimension \(n-m\). Therefore, by a dimension count,

$$
    \dim(M_iO\cap M_jO)
    \ge
    \dim(M_iO)+\dim(M_jO)-\dim(O^\perp).
$$

Hence

$$
    \dim(M_iO\cap M_jO)
    \ge
    m+m-(n-m)=3m-n.
$$

So if \(n<3m\), then the intersection

$$
    M_iO\cap M_jO
$$

is expected to contain nonzero vectors. The attack searches for a vector

$$
    x\in M_iO\cap M_jO.
$$

If such an \(x\) is found, then

$$
    M_i^{-1}x\in O,
    \qquad
    M_j^{-1}x\in O.
$$

Because elements of \(O\) vanish under \(P\), and pairs of elements of \(O\) vanish under the polar form, \(x\) must satisfy

$$
    P(M_i^{-1}x)=0, \qquad P(M_j^{-1}x)=0, \qquad P'(M_i^{-1}x,M_j^{-1}x)=0.
$$

This gives a system of quadratic equations in the coordinates of \(x\). Once a nonzero oil vector is recovered, additional oil vectors can be found more easily by imposing the linear conditions

$$
    P'(o,z)=0
$$

for already-known oil vectors \(o\). Repeating this process allows the attacker to reconstruct the whole oil subspace.

The same idea can be extended from two matrices to \(k\) matrices. Let \(L_1,\ldots,L_k\) be invertible matrices obtained from public components or invertible linear combinations of them. The attack looks for

$$
    x\in \bigcap_{r=1}^k L_rO.
$$

A dimension count gives

$$
    \dim\left(\bigcap_{r=1}^k L_rO\right)\ge km-(k-1)(n-m) = (2k-1)m-(k-1)n.
$$

Thus the intersection is expected to be nontrivial when

$$
    (2k-1)m-(k-1)n>0, \qquad \text{or} \qquad n<\frac{2k-1}{k-1}m.
$$

For example:

$$
    k=2 \quad\Rightarrow\quad n<3m,
$$

and


$$
    k=3 \quad\Rightarrow\quad n<\frac{5}{2}m.
$$

Here is a table for a few of the first ratio values.

| k | r |
|-----|-----|
| 2   | 3 |
| 3   | 5/2 |
| 4   | 7/3 |
| 5   | 9/4 |

Note that the ratio approaches to \(2\). So we cannot increase the value of \(k\) infinitely, as it fallbacks to the balanced case.

## Summary

Intersection attack is a kind of generalization of Kipnis-Shamir attack, as they use the same idea of the image of \(M_i\)'s. The core difference comes from lower-bound observation on the image intersection, and it allows the attacker reduces the difficulty of direct MQ solve.

However, this statement on the dimension lower-bound makes sense on a tight upperbound on imbalance. So the intersection attack is not a general breakdown on UOV.
