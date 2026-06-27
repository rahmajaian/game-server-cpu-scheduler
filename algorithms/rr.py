from collections import deque


def calculate_rr(at, bt, quantum):

    n = len(at)

    p = [i + 1 for i in range(n)]

    rt = bt.copy()

    ct = [0] * n
    tat = [0] * n
    wt = [0] * n

    visited = [False] * n

    ready = deque()

    time = 0
    completed = 0

    gantt = []
    idle_start = None


    while completed < n:


        # Add arrived processes
        for i in range(n):

            if at[i] <= time and not visited[i]:

                ready.append(i)
                visited[i] = True


        # CPU idle
        if not ready:

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


        idx = ready.popleft()


        start = time


        execute = min(quantum, rt[idx])


        time += execute

        rt[idx] -= execute


        gantt.append(
            (f"P{p[idx]}", start, time)
        )


        # Add newly arrived processes
        for i in range(n):

            if at[i] <= time and not visited[i]:

                ready.append(i)
                visited[i] = True


        # Put process back if unfinished
        if rt[idx] > 0:

            ready.append(idx)

        else:

            completed += 1

            ct[idx] = time

            tat[idx] = ct[idx] - at[idx]

            wt[idx] = tat[idx] - bt[idx]


    return {
        "p": p,
        "at": at,
        "bt": bt,
        "ct": ct,
        "tat": tat,
        "wt": wt,
        "quantum": quantum,
        "avgWT": round(sum(wt) / n, 2),
        "avgTAT": round(sum(tat) / n, 2),
        "gantt": gantt
    }