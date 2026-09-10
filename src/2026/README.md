** Ejemplo de MCWIS

En base al algoritmo de Sutton & Barto (2018) adaptado:

Initialize, for all s ∈ S, a ∈ A(s): 
Q(s,a) ← 0 (or arbitrary)
C(s,a) ← 0
π(s) ← a deterministic policy greedy with respect to Q 
Repeat until episode = 10:
  Generate an episode using any soft policy μ: S0, A0, R1, ..., ST−1, AT−1, RT, ST
  G←0
  W←1
  For t = T−1, T−2, ..., 0:
    G ← γG + R(t+1)
    C(St,At) ← C(St,At) + W
    Q(St,At) ← Q(St,At) + W / C(St,At) [G − Q(St,At)] π(St) ← argmax_a Q(St,a)
    W ← W * π(At|St) / μ(At|St)
    If W = 0 then ExitForLoop
