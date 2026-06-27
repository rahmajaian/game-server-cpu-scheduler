def calculate_sjf(at, bt):

    n = len(at)

    p = [i + 1 for i in range(n)]

    ct = [0] * n
    tat = [0] * n
    wt = [0] * n

    completed = [False] * n

    time = 0
    completed_count = 0

    gantt = []
    idle_start = None


    while completed_count < n:

        idx = -1
        shortest = float("inf")


        for i in range(n):

            if (
                at[i] <= time
                and not completed[i]
                and bt[i] < shortest
            ):
                shortest = bt[i]
                idx = i


        # CPU is idle
        if idx == -1:

            if idle_start is None:
                idle_start = time

            time += 1
            continue


        # Close idle block
        if idle_start is not None:

            gantt.append(
                ("IDLE", idle_start, time)
            )

            idle_start = None


        start = time
        time += bt[idx]


        gantt.append(
            (f"P{p[idx]}", start, time)
        )


        ct[idx] = time
        tat[idx] = ct[idx] - at[idx]
        wt[idx] = tat[idx] - bt[idx]


        completed[idx] = True
        completed_count += 1


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