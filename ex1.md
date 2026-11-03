# Exercise 1: The Forward Algorithm

**Notation.** Hidden states $X_1,\dots,X_T$, observations $O_1,\dots,O_T$, with
$\pi_j = P(X_1=j)$, $a_{ij} = P(X_{t+1}=j \mid X_t=i)$, $b_j(o) = P(O_t=o \mid X_t=j)$, and

$$\alpha_t(j) = P(O_1=o_1,\dots,O_t=o_t,\ X_t=j)$$

which is the probability of seeing the first $t$ observations **and** being in state $j$ at time $t$.

**HMM assumptions used in the proof:**

- **(M) Markov property:** the next state depends only on the current state:
  $P(X_t=j \mid X_{t-1}=i,\ O_{1:t-1}) = a_{ij}$
- **(E) Emission independence:** an observation depends only on the current state:
  $P(O_t=o_t \mid X_t=j,\ X_{t-1},\ O_{1:t-1}) = b_j(o_t)$

---

## a) Initialization

By the chain rule, $P(A,B) = P(A)\,P(B \mid A)$:

$$\alpha_1(j) = P(X_1=j)\cdot P(O_1=o_1 \mid X_1=j) = \pi_j\, b_j(o_1)$$

*The chain starts in state $j$, and then $j$ emits $o_1$.*

## b) Recursion ($t \ge 2$)

To be in state $j$ at time $t$, the chain must have been in some state $i$ at time $t-1$. The events $\{X_{t-1}=i\}$, $i=1,\dots,N$, form a partition, so by the law of total probability:

$$\alpha_t(j) = \sum_i P(O_{1:t},\ X_{t-1}=i,\ X_t=j)$$

Applying the chain rule, each term splits into three factors:

| Factor | Equals | Why |
|---|---|---|
| $P(O_{1:t-1},\ X_{t-1}=i)$ | $\alpha_{t-1}(i)$ | by definition |
| $P(X_t=j \mid X_{t-1}=i,\ O_{1:t-1})$ | $a_{ij}$ | by (M) |
| $P(O_t=o_t \mid X_t=j,\ X_{t-1}=i,\ O_{1:t-1})$ | $b_j(o_t)$ | by (E) |

Hence $\alpha_t(j) = \sum_i \alpha_{t-1}(i)\, a_{ij}\, b_j(o_t)$. Since $b_j(o_t)$ does not depend on $i$, it can be taken out of the sum:

$$\boxed{\alpha_t(j) = b_j(o_t)\sum_i \alpha_{t-1}(i)\, a_{ij}} \qquad \blacksquare$$

*Previous state $i$ ($\alpha_{t-1}$), then the move $i \to j$ ($a_{ij}$), then $j$ emits $o_t$ ($b_j$), summed over all possible $i$.*

## c) Termination

The final state $X_T$ takes exactly one of the values $1,\dots,N$, so the events $\{X_T=j\}$ form a partition. Summing the joint probability over them removes the state (law of total probability):

$$P(O_1=o_1,\dots,O_T=o_T) = \sum_j P(O_{1:T},\ X_T=j) = \sum_j \alpha_T(j) \qquad \blacksquare$$

## Why it matters

Summing directly over all hidden sequences costs about $N^T$ terms ($3^{12} = 531{,}441$ for this homework). Because each $\alpha_t$ reuses $\alpha_{t-1}$, the Forward algorithm costs about $N^2 T$ operations ($3^2 \cdot 12 = 108$).
