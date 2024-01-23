def convol_model(x, h, N, M):
    out_data = []
    for k in range(N):
        y = 0
        for m in range(M):
            y += x[k - m] * h[m]
        out_data.append(y)
    return out_data
