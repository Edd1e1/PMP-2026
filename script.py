import numpy as np

# ---------- a) Model ----------
states = ["D", "M", "U"]              # difficult, medium, easy
grades = ["FB", "B", "S", "NS"]       # very good, good, satisfactory, unsatisfactory

pi = np.array([1/3, 1/3, 1/3])

A = np.array([
    [0.00, 0.50, 0.50],   # from D
    [0.50, 0.25, 0.25],   # from M
    [0.50, 0.25, 0.25],   # from U
])

B = np.array([
    [0.10, 0.20, 0.40, 0.30],   # D
    [0.15, 0.25, 0.50, 0.10],   # M
    [0.20, 0.30, 0.40, 0.10],   # U
])


obs_names = ["FB", "FB", "S", "B", "B", "S", "B", "B", "NS", "B", "B", "S"]
obs = [grades.index(g) for g in obs_names]
T, N = len(obs), len(states)

# ---------- b) + c) Viterbi ----------
delta = np.zeros((T, N))             # best probability of a path ending in state j at time t
psi = np.zeros((T, N), dtype=int)    # back-pointer: best previous state

delta[0] = pi * B[:, obs[0]]         # b) initialization

for t in range(1, T):
    for j in range(N):
        cand = delta[t - 1] * A[:, j]          # delta_{t-1}(i) * a_ij for every i
        psi[t, j] = np.argmax(cand)
        delta[t, j] = B[j, obs[t]] * np.max(cand)

# ---------- d) Intermediate check ----------
print("delta_1 =", dict(zip(states, delta[0])))
print("delta_2 =", dict(zip(states, delta[1])))
print("psi_2   =", dict(zip(states, [states[k] for k in psi[1]])))

# hand check of delta_2(D): b_D(FB) * max(delta_1(M)*a_MD, delta_1(U)*a_UD)
hand = B[0, grades.index("FB")] * max(delta[0][1] * A[1, 0], delta[0][2] * A[2, 0])
print("hand-check delta_2(D) =", hand, "| matches code:", np.isclose(hand, delta[1, 0]))

# ---------- e) Backtracking ----------
last = int(np.argmax(delta[-1]))
best_prob = delta[-1, last]
path_idx = [last]
for t in range(T - 1, 0, -1):
    path_idx.append(psi[t, path_idx[-1]])
path_idx.reverse()
path = [states[i] for i in path_idx]

print("\nMost probable difficulty sequence:", path)
print("max P(x_1..x_12, o_1..o_12) =", best_prob)

# ---------- Optional: Forward and conditional probability ----------
alpha = pi * B[:, obs[0]]
for t in range(1, T):
    alpha = (alpha @ A) * B[:, obs[t]]
p_obs = alpha.sum()
print("\nP(o) (Forward)          =", p_obs)
print("P(x* | o) = P(x*,o)/P(o) =", best_prob / p_obs)


