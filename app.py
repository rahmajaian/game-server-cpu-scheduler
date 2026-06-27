from flask import Flask, render_template, request, session, redirect

from algorithms.fcfs import calculate_fcfs
from algorithms.sjf import calculate_sjf
from algorithms.ljf import calculate_ljf
from algorithms.srtf import calculate_srtf
from algorithms.lrtf import calculate_lrtf
from algorithms.rr import calculate_rr
from algorithms.priority import calculate_priority

app = Flask(__name__)
app.secret_key = "gaming_scheduler_secret"


# =========================
# GAME MODES DATA
# =========================
game_modes = {
    "FPS": {
        "slug": "FPS",
        "description": "Fast-paced shooter gameplay with quick player actions, frequent interrupts, and response-sensitive tasks.",
        "workload": "Highly interactive, short and medium tasks, response-critical",
        "requirements": [
            "Very fast response time",
            "Smooth CPU sharing between active tasks",
            "Low waiting time for urgent actions",
            "Fairness during heavy gameplay load"
        ],
        "suggested": ["RR", "SRTF", "Priority"]
    },

    "Battle Royale": {
        "slug": "Battle-Royale",
        "description": "Large multiplayer environment with many simultaneous player actions, loot events, and combat tasks.",
        "workload": "Highly dynamic and concurrent workload",
        "requirements": [
            "Handle many active tasks at once",
            "Fast scheduling during intense combat",
            "Low waiting time",
            "Good responsiveness under heavy load"
        ],
        "suggested": ["RR", "SRTF", "Priority"]
    },

    "MOBA": {
        "slug": "MOBA",
        "description": "Team-based strategy gameplay with real-time actions, skill effects, background map events, and continuous player interaction.",
        "workload": "Mixed interactive and background tasks",
        "requirements": [
            "Balanced execution between short and long tasks",
            "Fair task scheduling among players/events",
            "Stable performance during team fights",
            "Good handling of repeated interactive events"
        ],
        "suggested": ["RR", "Priority", "FCFS"]
    },

    "RPG": {
        "slug": "RPG",
        "description": "Role-playing gameplay with exploration, quests, NPC actions, inventory updates, and background world events.",
        "workload": "Mixed long and short tasks with background processing",
        "requirements": [
            "Balanced handling of long and short tasks",
            "Stable execution for background game systems",
            "Reasonable waiting time",
            "Smooth progression for quest and event processing"
        ],
        "suggested": ["FCFS", "SJF", "Priority"]
    },

    "Racing": {
        "slug": "Racing",
        "description": "Fast racing gameplay with frequent real-time input, lap updates, collision checks, and timing-sensitive events.",
        "workload": "Short, fast, real-time tasks",
        "requirements": [
            "Quick response to player input",
            "Fast handling of repeated short tasks",
            "Low delay in timing-sensitive operations",
            "Smooth execution under continuous updates"
        ],
        "suggested": ["SRTF", "RR", "SJF"]
    },

    "Strategy": {
        "slug": "Strategy",
        "description": "Resource management, AI actions, unit control, and background simulations running together in strategy games.",
        "workload": "Mixed long background tasks with interactive commands",
        "requirements": [
            "Stable execution for large background tasks",
            "Fair handling of multiple concurrent events",
            "Efficient processing of AI/resource tasks",
            "Balanced scheduling for command responsiveness"
        ],
        "suggested": ["Priority", "FCFS", "RR"]
    }
}


# =========================
# BENCHMARK ALGORITHMS
# =========================
benchmarks = {
    "FPS": "RR",
    "Battle Royale": "RR",
    "MOBA": "Priority",
    "RPG": "FCFS",
    "Racing": "SRTF",
    "Strategy": "Priority"
}


# =========================
# HELPER FUNCTIONS
# =========================
def get_mode_by_slug(mode_slug):
    for mode_name, mode_data in game_modes.items():
        if mode_data["slug"] == mode_slug:
            return mode_name, mode_data
    return None, None


def calculate_score(result, benchmark_result):
    score_wt = (
        (benchmark_result["avgWT"] / result["avgWT"]) * 100
        if result["avgWT"] != 0 else 100
    )

    score_tat = (
        (benchmark_result["avgTAT"] / result["avgTAT"]) * 100
        if result["avgTAT"] != 0 else 100
    )

    score = (score_wt + score_tat) / 2

    if score > 100:
        score = 100

    return round(score, 2)


def get_advice(score):
    if score >= 90:
        return (
            "This algorithm is highly suitable for the selected game mode. "
            "It delivers strong scheduling efficiency with balanced waiting and turnaround performance, "
            "making it a reliable choice for this workload."
        )
    elif score >= 75:
        return (
            "This algorithm performs well for the selected game mode and provides a stable scheduling outcome. "
            "However, some other algorithms may offer slightly better responsiveness or overall efficiency."
        )
    elif score >= 55:
        return (
            "This algorithm is moderately suitable for the selected game mode. "
            "While it can handle the workload, its performance is not optimal compared to stronger alternatives."
        )
    else:
        return (
            "This algorithm is not well suited for the selected game mode. "
            "Its scheduling behavior may lead to higher waiting time or reduced responsiveness, "
            "so a different algorithm would be a better choice for this scenario."
        )


def get_mode_verdict(mode_name, algorithm):
    suggestions = game_modes[mode_name]["suggested"]

    if algorithm == benchmarks[mode_name]:
        return (
            f"{algorithm} is the benchmark algorithm for {mode_name} mode, "
            f"so it is expected to perform very well here."
        )
    elif algorithm in suggestions:
        return (
            f"{algorithm} is one of the suggested algorithms for {mode_name} mode "
            f"because it matches the workload characteristics of this game type."
        )
    else:
        return (
            f"{algorithm} is not among the main recommended algorithms for {mode_name} mode, "
            f"so its performance may be weaker compared to better-suited schedulers."
        )


def get_benchmark_result(at, bt):
    if "mode" not in session:
        return None

    benchmark = benchmarks[session["mode"]]

    if benchmark == "FCFS":
        return calculate_fcfs(at.copy(), bt.copy())

    elif benchmark == "SJF":
        return calculate_sjf(at.copy(), bt.copy())

    elif benchmark == "LJF":
        return calculate_ljf(at.copy(), bt.copy())

    elif benchmark == "SRTF":
        return calculate_srtf(at.copy(), bt.copy())

    elif benchmark == "LRTF":
        return calculate_lrtf(at.copy(), bt.copy())

    elif benchmark == "RR":
        if "quantum" not in session or str(session["quantum"]).strip() == "":
            return None
        return calculate_rr(at.copy(), bt.copy(), int(session["quantum"]))

    elif benchmark == "Priority":
        if "priorities" not in session or str(session["priorities"]).strip() == "":
            return None

        priorities = list(map(int, session["priorities"].split(",")))

        if len(priorities) != len(at):
            return None

        return calculate_priority(at.copy(), bt.copy(), priorities)

    return None


# =========================
# ROUTES
# =========================

# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Step 1: Show all game modes
@app.route("/modes")
def modes_page():
    return render_template("modes.html", modes=game_modes)


# Step 2: Show selected game mode details
@app.route("/mode/<mode_slug>")
def mode_details(mode_slug):
    mode_name, mode_data = get_mode_by_slug(mode_slug)

    if not mode_data:
        return redirect("/modes")

    session["mode"] = mode_name
    session["mode_slug"] = mode_slug

    return render_template(
        "mode_details.html",
        mode_name=mode_name,
        mode_slug=mode_slug,
        mode=mode_data,
        benchmark=benchmarks[mode_name]
    )


# Step 3: Algorithm list page
@app.route("/algorithms")
def algorithms_page():
    if "mode" not in session:
        return redirect("/modes")

    return render_template(
        "algorithms.html",
        mode_name=session.get("mode", ""),
        mode_slug=session.get("mode_slug", "")
    )


# Step 4: Run one algorithm
@app.route("/run/<algo>", methods=["GET", "POST"])
def run_algorithm(algo):
    if "mode" not in session:
        return redirect("/modes")

    if request.method == "GET":
        return render_template(
            "input.html",
            algorithm=algo,
            mode=session.get("mode", ""),
            mode_slug=session.get("mode_slug", ""),
            old_n=session.get("n", ""),
            old_at=session.get("at", ""),
            old_bt=session.get("bt", ""),
            old_priorities=session.get("priorities", ""),
            old_quantum=session.get("quantum", "")
        )

    try:
        n = int(request.form["n"])
        at_text = request.form["arrival_times"].replace(" ", "")
        bt_text = request.form["burst_times"].replace(" ", "")

        at = list(map(int, at_text.split(",")))
        bt = list(map(int, bt_text.split(",")))

        if len(at) != n or len(bt) != n:
            return "Error: Number of processes must match arrival times and burst times."

        session["n"] = n
        session["at"] = at_text
        session["bt"] = bt_text

        if algo == "FCFS":
            result = calculate_fcfs(at.copy(), bt.copy())

        elif algo == "SJF":
            result = calculate_sjf(at.copy(), bt.copy())

        elif algo == "LJF":
            result = calculate_ljf(at.copy(), bt.copy())

        elif algo == "SRTF":
            result = calculate_srtf(at.copy(), bt.copy())

        elif algo == "LRTF":
            result = calculate_lrtf(at.copy(), bt.copy())

        elif algo == "RR":
            quantum = int(request.form["quantum"])
            session["quantum"] = quantum
            result = calculate_rr(at.copy(), bt.copy(), quantum)

        elif algo == "Priority":
            priorities_text = request.form["priorities"].replace(" ", "")
            priorities = list(map(int, priorities_text.split(",")))

            if len(priorities) != n:
                return "Error: Number of priorities must match number of processes."

            session["priorities"] = priorities_text
            result = calculate_priority(at.copy(), bt.copy(), priorities)

        else:
            return redirect("/algorithms")

        benchmark_name = benchmarks[session["mode"]]
        benchmark_result = get_benchmark_result(at, bt)

        if benchmark_result:
            score = calculate_score(result, benchmark_result)
            advice = get_advice(score)
        else:
            score = None
            advice = (
                "Extra information is required to compare with the benchmark algorithm. "
                "Use Compare All to provide the required data."
            )

        verdict = get_mode_verdict(session["mode"], algo)

        return render_template(
            "result.html",
            result=result,
            algorithm=algo,
            mode_name=session.get("mode", ""),
            mode_slug=session.get("mode_slug", ""),
            benchmark=benchmark_name,
            score=score,
            advice=advice,
            verdict=verdict
        )

    except Exception as e:
        return f"Input Error: {str(e)}"


# Step 5: Compare all algorithms
@app.route("/compare", methods=["GET", "POST"])
def compare():
    if "mode" not in session:
        return redirect("/modes")

    if request.method == "GET":
        return render_template(
            "compare_input.html",
            mode_name=session.get("mode", ""),
            mode_slug=session.get("mode_slug", ""),
            old_n=session.get("n", ""),
            old_at=session.get("at", ""),
            old_bt=session.get("bt", ""),
            old_quantum=session.get("quantum", ""),
            old_priorities=session.get("priorities", "")
        )

    try:
        n = int(request.form["n"])
        at_text = request.form["arrival_times"].replace(" ", "")
        bt_text = request.form["burst_times"].replace(" ", "")
        quantum = int(request.form["quantum"])
        priorities_text = request.form["priorities"].replace(" ", "")

        at = list(map(int, at_text.split(",")))
        bt = list(map(int, bt_text.split(",")))
        priorities = list(map(int, priorities_text.split(",")))

        if len(at) != n or len(bt) != n or len(priorities) != n:
            return "Error: Number of processes must match AT, BT, and Priorities."

        session["n"] = n
        session["at"] = at_text
        session["bt"] = bt_text
        session["quantum"] = quantum
        session["priorities"] = priorities_text

        results = {
            "FCFS": calculate_fcfs(at.copy(), bt.copy()),
            "SJF": calculate_sjf(at.copy(), bt.copy()),
            "LJF": calculate_ljf(at.copy(), bt.copy()),
            "SRTF": calculate_srtf(at.copy(), bt.copy()),
            "LRTF": calculate_lrtf(at.copy(), bt.copy()),
            "RR": calculate_rr(at.copy(), bt.copy(), quantum),
            "Priority": calculate_priority(at.copy(), bt.copy(), priorities)
        }

        benchmark = benchmarks[session["mode"]]
        benchmark_result = results[benchmark]

        for name, data in results.items():
            data["score"] = calculate_score(data, benchmark_result)
            data["advice"] = get_advice(data["score"])

        # ranking highest score first
        sorted_results = sorted(
            results.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )

        ranked_results = []
        for i, (name, data) in enumerate(sorted_results, start=1):
            data["rank"] = i
            ranked_results.append((name, data))

        best_algorithm = ranked_results[0][0]

        return render_template(
            "compare_result.html",
            results=ranked_results,
            mode_name=session.get("mode", ""),
            mode_slug=session.get("mode_slug", ""),
            benchmark=benchmark,
            best=best_algorithm
        )

    except Exception as e:
        return f"Input Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)