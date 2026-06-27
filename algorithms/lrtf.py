def calculate_lrtf(at, bt):

    n = len(at)

    p = [i + 1 for i in range(n)]

    rt = bt.copy()

    ct = [0] * n
    tat = [0] * n
    wt = [0] * n

    time = 0
    completed = 0

    gantt = []

    last_process = None
    start_time = 0


    while completed < n:

        longest = -1
        max_rt = -1


        for i in range(n):

            if (
                at[i] <= time
                and rt[i] > 0
                and rt[i] > max_rt
            ):
                max_rt = rt[i]
                longest = i


        current = longest


        # Process changed
        if current != last_process:

            if last_process is not None:

                name = "IDLE" if last_process == -1 else f"P{p[last_process]}"

                gantt.append(
                    (name, start_time, time)
                )


            start_time = time
            last_process = current


        # CPU idle
        if current == -1:
            time += 1
            continue


        # Execute 1 unit
        rt[current] -= 1
        time += 1


        # Finished
        if rt[current] == 0:

            completed += 1

            ct[current] = time
            tat[current] = ct[current] - at[current]
            wt[current] = tat[current] - bt[current]


    # Close final block
    if last_process is not None:

        name = "IDLE" if last_process == -1 else f"P{p[last_process]}"

        gantt.append(
            (name, start_time, time)
        )


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