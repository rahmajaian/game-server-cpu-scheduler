def calculate_fcfs(at, bt):

    n = len(at)

    p = [i + 1 for i in range(n)]

    ct = [0] * n
    tat = [0] * n
    wt = [0] * n


    # Sort by arrival time
    for i in range(n - 1):
        for j in range(i + 1, n):
            if at[i] > at[j] or (
                at[i] == at[j] and p[i] > p[j]
            ):
                at[i], at[j] = at[j], at[i]
                bt[i], bt[j] = bt[j], bt[i]
                p[i], p[j] = p[j], p[i]


    time = 0
    gantt = []


    for i in range(n):

        # CPU idle before process arrives
        if time < at[i]:
            gantt.append(
                ("IDLE", time, at[i])
            )
            time = at[i]


        start = time

        time += bt[i]


        gantt.append(
            (f"P{p[i]}", start, time)
        )


        ct[i] = time
        tat[i] = ct[i] - at[i]
        wt[i] = tat[i] - bt[i]


    return {
        "p": p,
        "at": at,
        "bt": bt,
        "ct": ct,
        "tat": tat,
        "wt": wt,
        "avgWT": round(sum(wt) / n, 2),
        "avgTAT": round(sum(tat) / n, 2),
        "gantt": gantt
    }