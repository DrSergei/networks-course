import matplotlib.pyplot as plt
import numpy as np

F = 15 * (1000 ** 3)
us = 30 * (1000 ** 2)
d = 2 * (1000 ** 2)
U = [300 * 1000, 700 * 1000, 2 * (1000 ** 2)]
N = [10, 100, 1000]

for u in U:
    time = np.array([max(F / us, F / d, n * F / (us + n * u)) for n in N])
    plt.plot(N, time, marker='o', label = f"p2p with u = {u / 1000} Kbit/s")

time = np.array([max(n * F / us, F / d) for n in N])
plt.plot(N, time, marker='o', label = f"client-server")

plt.xscale('log', base=10)
plt.xlabel("N, number of users")
plt.yscale('log', base=10)
plt.ylabel("time, sec")
plt.legend()
plt.show()
