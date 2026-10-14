def simulate_sir(n, i0, beta, gamma, days, dt=0.1):
    """Simulate the SIR model with Euler steps.

    Returns three lists (S, I, R) with one value per day.
    """
    s, i, r = n - i0, i0, 0
    S, I, R = [], [], []
    steps_per_day = round(1 / dt)
    for _ in range(days):
        for _ in range(steps_per_day):
            new_infected = beta * s * i / n * dt
            new_removed = gamma * i * dt
            s -= new_infected
            i += new_infected - new_removed
            r += new_removed
        S.append(s)
        I.append(i)
        R.append(r)
    return S, I, R
