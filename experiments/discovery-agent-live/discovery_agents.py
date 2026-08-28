import math, random, statistics
from dataclasses import dataclass

@dataclass
class Candidate:
    name: str
    score: float
    rationale: str

def corr(xs, ys):
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x-mx)**2 for x in xs))
    dy = math.sqrt(sum((y-my)**2 for y in ys))
    return 0.0 if dx == 0 or dy == 0 else num/(dx*dy)

def mse(actual, pred):
    return statistics.mean((a-p)**2 for a, p in zip(actual, pred))

def regression_ols(features, target):
    X = [[1.0] + list(row) for row in features]
    y = list(target)
    p = len(X[0])
    A = [[0.0]*(p+1) for _ in range(p)]
    for i in range(len(X)):
        for j in range(p):
            A[j][-1] += X[i][j] * y[i]
            for k in range(p):
                A[j][k] += X[i][j] * X[i][k]
    for i in range(p):
        A[i][i] += 1e-6
    for col in range(p):
        pivot = max(range(col, p), key=lambda r: abs(A[r][col]))
        A[col], A[pivot] = A[pivot], A[col]
        div = A[col][col]
        if abs(div) < 1e-12:
            continue
        A[col] = [v/div for v in A[col]]
        for r in range(p):
            if r == col:
                continue
            f = A[r][col]
            A[r] = [a-f*b for a,b in zip(A[r], A[col])]
    return [A[i][-1] for i in range(p)]

def generate_data(n=300, seed=7):
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        A, B, C, D = [rng.uniform(-2, 2) for _ in range(4)]
        H = 0.8*C - 0.5*D + rng.gauss(0, 0.12)
        Y = 1.8*A*H + 0.35*B + rng.gauss(0, 0.30)
        rows.append({"A":A,"B":B,"C":C,"D":D,"Y":Y})
    return rows

def baseline_agent(data):
    y = [r["Y"] for r in data]
    scores = {v: abs(corr([r[v] for r in data], y)) for v in "ABCD"}
    best = max(scores, key=scores.get)
    beta = regression_ols([[r[best]] for r in data], y)
    pred = [beta[0] + beta[1]*r[best] for r in data]
    return {"best_variable": best, "mse": mse(y,pred), "correlations": scores}

def unknown_agent(data):
    y = [r["Y"] for r in data]
    scores = {v: abs(corr([r[v] for r in data], y)) for v in "ABCD"}
    return {"marginal_correlations": scores, "unknown_signal": max(scores.values()) < 0.40}

def representation_agent(data):
    y = [r["Y"] for r in data]
    out = []
    for i, x in enumerate("ABCD"):
        for z in "ABCD"[i+1:]:
            out.append(Candidate(f"{x}*{z}", abs(corr([r[x]*r[z] for r in data], y)), "Alternative interaction representation."))
    return sorted(out, key=lambda c:c.score, reverse=True)

def contradiction_agent(data, interaction):
    y = [r["Y"] for r in data]
    additive = [[r[v] for v in "ABCD"] for r in data]
    ab = regression_ols(additive,y)
    ap = [ab[0]+sum(a*b for a,b in zip(ab[1:],row)) for row in additive]
    x,z = interaction.split("*")
    inter = [[r[v] for v in "ABCD"]+[r[x]*r[z]] for r in data]
    ib = regression_ols(inter,y)
    ip = [ib[0]+sum(a*b for a,b in zip(ib[1:],row)) for row in inter]
    am, im = mse(y,ap), mse(y,ip)
    return {"additive_mse":am,"interaction_mse":im,"improvement":am-im}

def latent_variable_agent(data):
    y = [r["Y"] for r in data]
    best = None
    for a in [i/10 for i in range(-12,13)]:
        for b in [i/10 for i in range(-12,13)]:
            H = [a*r["C"]+b*r["D"] for r in data]
            feats = [[r["A"],r["B"],r["A"]*h] for r,h in zip(data,H)]
            beta = regression_ols(feats,y)
            pred = [beta[0]+sum(k*x for k,x in zip(beta[1:],row)) for row in feats]
            err = mse(y,pred)
            if best is None or err < best[0]: best=(err,a,b)
    err,a,b=best
    return {"estimated_latent":f"H ~= {a:.1f}*C + {b:.1f}*D","fit_mse":err,"coefficients":{"C":a,"D":b}}

def experiment_selector(data):
    latent = latent_variable_agent(data)
    a,b = latent["coefficients"]["C"], latent["coefficients"]["D"]
    H = [a*r["C"]+b*r["D"] for r in data]
    y = [r["Y"] for r in data]
    scores={}
    for v in "ABCD":
        feats=[[r[v],h,r[v]*h] for r,h in zip(data,H)]
        beta=regression_ols(feats,y)
        scores[f"intervene_{v}"]=abs(beta[3])
    return max(scores,key=scores.get),scores

def specialized_pipeline(data):
    unknown=unknown_agent(data)
    reps=representation_agent(data)
    best_inter=reps[0]
    contradiction=contradiction_agent(data,best_inter.name)
    latent=latent_variable_agent(data)
    experiment,exp_scores=experiment_selector(data)
    y=[r["Y"] for r in data]
    x,z=best_inter.name.split("*")
    feats=[[r[v] for v in "ABCD"]+[r[x]*r[z]] for r in data]
    beta=regression_ols(feats,y)
    pred=[beta[0]+sum(k*x for k,x in zip(beta[1:],row)) for row in feats]
    return {"unknown_agent":unknown,"best_representation":best_inter.name,"representation_score":best_inter.score,"contradiction":contradiction,"latent_variable_agent":latent,"selected_experiment":experiment,"experiment_scores":exp_scores,"final_mse":mse(y,pred)}

def run(seed=7):
    data=generate_data(seed=seed)
    return baseline_agent(data),specialized_pipeline(data)

if __name__ == "__main__":
    results=[]
    for seed in range(20):
        b,s=run(seed)
        results.append((b,s))
    print("DISCOVERY AGENT BENCHMARK")
    print(f"Seeds tested: {len(results)}")
    print(f"A*C discovered: {sum(s['best_representation']=='A*C' for _,s in results)}/{len(results)}")
    print(f"A intervention selected: {sum(s['selected_experiment']=='intervene_A' for _,s in results)}/{len(results)}")
    print(f"Pipeline beats baseline MSE: {sum(s['final_mse']<b['mse'] for b,s in results)}/{len(results)}")
    b,s=run(7)
    print(f"Baseline MSE: {b['mse']:.4f}")
    print(f"Pipeline MSE: {s['final_mse']:.4f}")
    print(f"Interaction: {s['best_representation']}")
    print(f"Latent estimate: {s['latent_variable_agent']['estimated_latent']}")
    print(f"Selected experiment: {s['selected_experiment']}")
    print("\nCaveat: synthetic benchmark; this validates the software loop, not novel science.")
