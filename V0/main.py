from . import config #test model working or not
from .model import simulate_sir

S, I, R = simulate_sir(config.N, config.I0, config.BETA,
                       config.GAMMA, config.DAYS)

for day in range(0, config.DAYS, 10):
    print(day, round(S[day], 1), round(I[day], 1), round(R[day], 1))

assert all(abs(s + i + r - config.N) < 1e-6
           for s, i, r in zip(S, I, R))
print("conservation OK")