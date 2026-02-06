import glob
import pandas as pd
import matplotlib.pyplot as plt

def load_runs(pattern):
    files = sorted(glob.glob(pattern))
    if len(files) == 0:
        raise SystemExit(f"Aucun fichier trouvé avec le pattern: {pattern}")
    runs = []
    for f in files:
        df = pd.read_csv(f)
        # on garde juste eval, score, best
        df = df[["eval", "score", "best"]].copy()
        df["file"] = f
        runs.append(df)
    return runs

def plot_single_run(df, title):
    plt.figure()
    plt.plot(df["eval"], df["score"], label="score (courant/parent)")
    plt.plot(df["eval"], df["best"], label="best so far")
    plt.xlabel("evaluations")
    plt.ylabel("score")
    plt.title(title)
    plt.legend()
    plt.show()

def plot_mean_best(runs, title):
    # aligner toutes les runs sur la même longueur (min)
    min_len = min(len(r) for r in runs)
    best_matrix = []
    evals = runs[0]["eval"].iloc[:min_len].to_numpy()

    for r in runs:
        best_matrix.append(r["best"].iloc[:min_len].to_numpy())

    import numpy as np
    best_matrix = np.vstack(best_matrix)
    mean_best = best_matrix.mean(axis=0)
    std_best = best_matrix.std(axis=0)

    plt.figure()
    plt.plot(evals, mean_best, label="moyenne(best)")
    plt.fill_between(evals, mean_best - std_best, mean_best + std_best, alpha=0.2, label="± écart-type")
    plt.xlabel("evaluations")
    plt.ylabel("best score")
    plt.title(title)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # ---- RandomSearch2 ----
    rs_runs = load_runs("results_randomsearch2_*.csv")
    plot_single_run(rs_runs[0], f"RandomSearch2 - 1 run ({rs_runs[0]['file'][0] if False else ''})")
    plot_mean_best(rs_runs, "RandomSearch2 - moyenne best (10 runs)")

    # ---- Genetic ----
    ga_runs = load_runs("results_genetic_*.csv")
    plot_single_run(ga_runs[0], "Genetic (1+1) - 1 run")
    plot_mean_best(ga_runs, "Genetic (1+1) - moyenne best (10 runs)")
