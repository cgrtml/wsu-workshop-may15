# WSU Data & Analytics Breakout, May 15 2026

**Students: click a button below to open the activity in Google Colab.**
Sign in with your Google account, then click **Copy to Drive** so you have
your own editable copy. The first cell installs everything you need
(about 20 seconds). Then follow along with the slides on the projector.

[![Open Activity 1 in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cgrtml/wsu-workshop-may15/blob/main/notebooks/activity1_student.ipynb) **Activity 1 — Train Your Own Neural Tree** (55 min, individual)

[![Open Activity 2 in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cgrtml/wsu-workshop-may15/blob/main/notebooks/activity2_student.ipynb) **Activity 2 — Adversarial Sensor Challenge** (25 min, team)

**Prerequisites (do this before May 15):**
- A Google account, for Colab. Personal Gmail or .edu both work.
- A GitHub account, for the closing 15-minute contribution sprint. Free signup at [github.com/signup](https://github.com/signup).

---

## About the workshop

The session runs 09:00 to 11:45, a single block of 165 minutes. The
hands-on portion uses NASA CMAPSS turbofan engine data to train an
explainable model (Soft Decision Tree), localize an adversarially
manipulated sensor, and contribute a real patch to the `neural-trees`
Python package as part of a closing GitHub sprint.

This README is a working document for the presenter. It assumes you have
read `PLAN.md` (Turkish, minute-by-minute) and have a working laptop with
a recent browser.

## Files

Everything needed to run the session is in this repository.

```
slides/
    slides.html                    Reveal.js deck, 56 slides, single file
    slides-joint-original.html     Earlier joint-deck draft, kept for reference
    img/                           Plot images embedded in step-by-step slides
notebooks/
    activity1_student.ipynb        Train Your Own Neural Tree (with TODOs)
    activity1_solution.ipynb
    activity2_student.ipynb        Adversarial Sensor Challenge
    activity2_solution.ipynb       Instructor key
data/
    train_FD001.txt                NASA CMAPSS training trajectories
    test_FD001.txt
    RUL_FD001.txt
    engine17_clean.csv             Reference engine for Activity 2
    attack_A.csv                   Drift injection, sensor 11
    attack_B.csv                   Stuck-at, sensor 14
    attack_C.csv                   Gaussian noise, sensor 9
scripts/
    generate_attack_files.py       Reproduces the three attack files
    rehearsal_activity1.py         Dry-run Activity 1 locally end to end
    generate_slide_plots.py        Regenerates plot images for the slides
landing/index.html                 Mobile landing page for QR-code onboarding
assets/qr_landing.png              QR code, points at this repository
PLAN.md                            Minute-by-minute scenario (Turkish)
```

## Before the day

Open `slides/slides.html` in Chrome, Safari, or Firefox. Press `F` for
fullscreen and use arrow keys to navigate. The deck is a single-file
Reveal.js page and works offline.

Open `landing/index.html` on a phone and confirm both Colab notebooks
launch from it. Print `assets/qr_landing.png` as a fallback in case the
projector blacks out or wifi drops.

If you want to dry-run the student flow yourself before stage day:

```
conda create -n wsu-workshop python=3.10 -y
conda activate wsu-workshop
pip install neural-trees pandas matplotlib seaborn scikit-learn jupyterlab "numpy<2"
python scripts/rehearsal_activity1.py
```

The rehearsal script walks Activity 1 end to end: loads CMAPSS, trains
the soft decision tree, prints test accuracy, saves the confusion matrix
and one engine's sensor trajectories under `rehearsal_output/`. It runs
in under a minute on a modern laptop CPU.

## On the day

Students scan the QR code, land on `index.html`, tap Activity 1, and
Colab opens the notebook. They tap "Copy to Drive" and run the first
cell. There is no local Python setup.

Timeline:

```
09:00 - 09:30   Lecture (slides 1 to 18)
09:30 - 10:25   Activity 1, 11 steps (slides 19 to 32)
10:25 - 10:35   Break
10:35 - 11:00   Activity 2, 7 steps (slides 33 to 44)
11:00 - 11:15   Answers and discussion (slides 45 to 47)
11:15 - 11:30   GitHub Contribution Sprint (slides 48 to 50)
11:30 - 11:45   Wrap-up and Q&A (slides 51 to 56)
```

## Activity 1 — Train Your Own Neural Tree

55 minutes, individual. Eleven copy-and-paste steps below. Each block is
designed to be pasted into a new Colab cell and run with `Shift+Enter`.
Variables persist across cells, so each step builds on the previous one.

### Step 1 — Imports

Bring in every library the activity needs. After this runs you should see
`All set.` in the output.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from neural_trees import SoftDecisionTree
print('All set.')
```

### Step 2 — Load CMAPSS FD001

Read the NASA training file as a pandas dataframe.

```python
cols = ['engine_id', 'cycle'] + [f'op{i}' for i in range(1, 4)] + [f's{i}' for i in range(1, 22)]
train = pd.read_csv('train_FD001.txt', sep=r'\s+', header=None, names=cols)
print(train.shape, '->', train['engine_id'].nunique(), 'engines')
train.head()
```

Expected: `(20631, 26) -> 100 engines`, plus the first five rows of engine 1.

### Step 3 — Compute Remaining Useful Life (RUL)

For each row, RUL = max cycle for that engine minus current cycle, capped at 125.

```python
max_cycles = train.groupby('engine_id')['cycle'].max().rename('max_cycle')
train = train.merge(max_cycles, on='engine_id')
train['RUL'] = (train['max_cycle'] - train['cycle']).clip(upper=125)
train[['engine_id', 'cycle', 'max_cycle', 'RUL']].head()
```

Expected: a five-row table with engine 1 showing `max_cycle = 192` and `RUL = 125`
for every early cycle (the cap is in effect).

### Step 4 — Visualize engine 1's sensor degradation

Plot four sensors across the engine's life. Sensors 2, 11, 14 trend up;
sensor 7 trends down. The data is telling the story of failure.

```python
engine = train[train['engine_id'] == 1].set_index('cycle')
engine[['s2', 's7', 's11', 's14']].plot(subplots=True, layout=(2, 2), figsize=(12, 6))
plt.suptitle('Engine 1 sensor degradation', y=1.02)
plt.tight_layout()
plt.show()
```

Expected: a 2x2 grid of line plots, one per sensor.

### Step 5 — Bin RUL into three health classes

Critical (RUL < 30), Caution (30 ≤ RUL < 80), Healthy (RUL ≥ 80).

```python
def bin_rul(rul):
    if rul < 30:
        return 0
    elif rul < 80:
        return 1
    return 2

train['health'] = train['RUL'].apply(bin_rul)
train['health'].value_counts().sort_index()
```

Expected:

```
health
0     3000
1     5000
2    12631
```

Roughly 14% Critical, 24% Caution, 61% Healthy.

### Step 6 — Build the feature matrix

Drop the six sensors that are constant (no signal). Standardize what remains.

```python
all_sensors = [f's{i}' for i in range(1, 22)]
informative = [s for s in all_sensors if train[s].std() > 0.001]
X = train[informative].values
y = train['health'].values
scaler = StandardScaler()
X = scaler.fit_transform(X)
print('X shape:', X.shape, '· y shape:', y.shape)
```

Expected: `X shape: (20631, 15) · y shape: (20631,)`.

### Step 7 — Train / test split

80 / 20 split, stratified by `y` so the class ratio is preserved in both halves.

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42,
)
print(X_train.shape, X_test.shape)
```

Expected: `(16504, 15) (4127, 15)`.

### Step 8 — Train the Soft Decision Tree

About 30 to 60 seconds on CPU. PyTorch runs backpropagation on 16,500 rows for
30 epochs.

```python
tree = SoftDecisionTree(
    depth=4,
    max_epochs=30,
    learning_rate=0.01,
    penalty_coef=1e-3,
    verbose=True,
)
tree.fit(X_train, y_train)
acc = (tree.predict(X_test) == y_test).mean()
print(f'Test accuracy: {acc:.3f}')
```

Expected: per-epoch loss decreasing, final `Test accuracy: ~0.84`.

### Step 9 — Confusion matrix and per-class report

Where does the model get it right, and where does it get it wrong?

```python
labels = ['Critical', 'Caution', 'Healthy']
y_pred = tree.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=labels, yticklabels=labels, ax=ax)
plt.title('Confusion matrix')
plt.show()
print(classification_report(y_test, y_pred, target_names=labels))
```

Expected: a Blues heatmap and a per-class precision / recall report. The
bottom-left cell should be 0 — no Healthy engine ever flagged as Critical.

### Step 10 — Inspect the split weights

For each of the 15 internal nodes, print the sensor with the largest absolute
weight. Some sensors will appear multiple times — these are the model's pillars.

```python
splits = tree.get_split_weights()
print(f'Internal nodes: {len(splits)}')
for i, w in enumerate(splits):
    dom = informative[np.argmax(np.abs(w))]
    print(f'  Node {i:2d} -> {dom}')
```

Expected: 15 lines, with `s14` and `s6` (or similar) appearing more than once.

### Step 11 — Read one prediction (the heart of the workshop)

Pick test sample 17 and ask the model: what did you predict, with what
confidence, and which sensor did you look at first?

```python
idx = 17
x = X_test[idx]
true = labels[y_test[idx]]
pred = labels[tree.predict([x])[0]]
proba = tree.predict_proba([x])[0]
root = informative[np.argmax(np.abs(splits[0]))]

print(f'True class:      {true}')
print(f'Predicted class: {pred}')
print(f'Probabilities:   Critical={proba[0]:.3f}  Caution={proba[1]:.3f}  Healthy={proba[2]:.3f}')
print(f'Root sensor:     {root}')
```

Expected output (approximately):

```
True class:      Caution
Predicted class: Healthy
Probabilities:   Critical=0.000  Caution=0.148  Healthy=0.852
Root sensor:     s7
```

Now the model can answer "why did you say Healthy?" with a specific sensor
and a specific threshold. An LSTM of equivalent accuracy cannot.

---

## Activity 2 — Adversarial Sensor Challenge

25 minutes, three to four students per team. Seven copy-and-paste steps. You
keep the `tree`, `informative`, `scaler`, `X_train`, `y_train` and `labels`
objects from Activity 1 — do not restart the notebook.

Each team gets three corrupted versions of one engine's telemetry. In each
file, exactly one sensor channel has been manipulated. The job: find which
sensor and which kind of attack.

### Step 1 — Add a RandomForest baseline

A black-box comparison for the explainable Soft Decision Tree.

```python
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
print(f'SoftTree accuracy: {(tree.predict(X_test) == y_test).mean():.3f}')
print(f'RandomForest     : {(rf.predict(X_test) == y_test).mean():.3f}')
```

Expected: roughly `0.841` and `0.843`. Essentially identical on clean data.

### Step 2 — Predict on clean engine 17

Establish a reference: what do both models say about the un-attacked engine?

```python
clean = pd.read_csv('engine17_clean.csv')
Xc = scaler.transform(clean[informative].values)
clean_tree_pred = tree.predict(Xc)
clean_rf_pred = rf.predict(Xc)
print(f'Engine 17 clean: {len(Xc)} cycles')
print(f'Tree vs RF agreement: {(clean_tree_pred == clean_rf_pred).mean():.2f}')
```

Expected: 276 cycles, agreement around `0.95`.

### Step 3 — How much did each attack change the predictions?

Run both models on each attack file and count cycle-by-cycle disagreement
against the clean baseline.

```python
for fname in ['attack_A.csv', 'attack_B.csv', 'attack_C.csv']:
    df = pd.read_csv(fname)
    Xa = scaler.transform(df[informative].values)
    pt = tree.predict(Xa)
    pr = rf.predict(Xa)
    tc = (pt != clean_tree_pred).sum()
    rc = (pr != clean_rf_pred).sum()
    print(f'{fname}: Tree changed {tc:3d}/{len(pt)} | RF changed {rc:3d}/{len(pr)}')
```

Expected:

```
attack_A.csv: Tree changed  18/276 | RF changed  14/276
attack_B.csv: Tree changed  33/276 | RF changed   8/276
attack_C.csv: Tree changed   8/276 | RF changed   1/276
```

On attack C the RandomForest barely notices. The Soft Tree does.

### Step 4 — Visualize Attack A (look for two parallel lines)

Plot every informative sensor twice — clean in blue, attack in orange.
Fourteen panels will show only one line. One panel will show two parallel
lines: that is the manipulated sensor.

```python
clean = pd.read_csv('engine17_clean.csv')
attack = pd.read_csv('attack_A.csv')
fig, axes = plt.subplots(4, 4, figsize=(16, 10))
for ax, s in zip(axes.flat, informative):
    ax.plot(clean['cycle'], clean[s], label='clean', alpha=0.7)
    ax.plot(attack['cycle'], attack[s], label='attack', alpha=0.7)
    ax.set_title(s)
axes.flat[0].legend()
plt.tight_layout()
plt.show()
```

Answer: sensor 11, drift.

### Step 5 — Visualize Attack B (look for a flat horizontal line)

Same plot for attack B. This time the orange line on the manipulated sensor
will be completely flat while the blue line keeps evolving.

```python
attack = pd.read_csv('attack_B.csv')
fig, axes = plt.subplots(4, 4, figsize=(16, 10))
for ax, s in zip(axes.flat, informative):
    ax.plot(clean['cycle'], clean[s], label='clean', alpha=0.7)
    ax.plot(attack['cycle'], attack[s], label='attack', alpha=0.7)
    ax.set_title(s)
axes.flat[0].legend()
plt.tight_layout()
plt.show()
```

Answer: sensor 14, stuck-at. Notice that sensor 14 was one of the model's
pillars in Activity 1 step 10 — attackers go for what the model relies on.

### Step 6 — Visualize Attack C (look for a noisier line)

Subtler. The trend is preserved; only the variance changes.

```python
attack = pd.read_csv('attack_C.csv')
fig, axes = plt.subplots(4, 4, figsize=(16, 10))
for ax, s in zip(axes.flat, informative):
    ax.plot(clean['cycle'], clean[s], label='clean', alpha=0.7)
    ax.plot(attack['cycle'], attack[s], label='attack', alpha=0.7)
    ax.set_title(s)
axes.flat[0].legend()
plt.tight_layout()
plt.show()
```

Answer: sensor 9, Gaussian noise. This is why the RandomForest missed it —
trend was right, so it kept saying "fine".

### Step 7 — Quantify the divergence

Confirm the visual answer with numbers. For each attack file, compute mean
absolute difference per sensor and show the top three.

```python
clean = pd.read_csv('engine17_clean.csv')
for fname in ['attack_A.csv', 'attack_B.csv', 'attack_C.csv']:
    a = pd.read_csv(fname)
    d = {s: float(np.mean(np.abs(clean[s].values - a[s].values))) for s in informative}
    top = sorted(d.items(), key=lambda kv: -kv[1])[:3]
    print(f'{fname} top 3: {top}')
```

Expected:

```
attack_A.csv top 3: [('s11', 0.367), ('s2', 0.0), ('s3', 0.0)]
attack_B.csv top 3: [('s14', 19.89), ('s2', 0.0), ('s3', 0.0)]
attack_C.csv top 3: [('s9',  6.42), ('s2', 0.0), ('s3', 0.0)]
```

Only one sensor differs in each file. The other fourteen are identical
between clean and attack. The instructor's answer key is
`notebooks/activity2_solution.ipynb`. Final answers, in order:

| File | Sensor | Attack type |
|---|---|---|
| `attack_A.csv` | s11 (Ps30) | Drift |
| `attack_B.csv` | s14 (NRc) | Stuck-at |
| `attack_C.csv` | s9 (Nc) | Gaussian noise |

## GitHub Contribution Sprint

15 minutes, the closing segment of the session. Students open
[github.com/cgrtml/neural-trees](https://github.com/cgrtml/neural-trees),
filter the Issues tab by `good first issue`, pick a 10 to 20 minute
task, comment "I'm taking this", fork, edit, and open a pull request.
The instructor reviews live from the stage and merges accepted PRs.
Merged contributors are credited under a `WSU Workshop Contributors`
section in the `neural-trees` README.

Roughly 18 `good first issue` tasks are seeded in the repository ahead
of the session. They cover documentation fixes, small runnable examples
under `examples/`, additional unit tests, and small quality-of-life
improvements such as input validation or a clearer error message when
PyTorch is missing.

## The library

The workshop runs on `neural-trees`, an MIT-licensed Python package that
implements soft decision trees, omnivariate trees, hierarchical mixture
of experts, and statistical tests for classifier comparison (5x2cv F
test, McNemar, paired t-test). Installation is one line, `pip install
neural-trees`. The PyTorch backend is required, CPU is sufficient for
all material in the workshop.

The CMAPSS-trained Temporal Neural Tree variant referenced in the
lecture slides lives in a companion repository,
[`turbofan-explainable-neural-trees`](https://github.com/cgrtml/turbofan-explainable-neural-trees),
together with the accompanying paper.

## Citation

```bibtex
@misc{temel2026wsu,
  author       = {Temel, Cagri},
  title        = {From Black Boxes to Glass Boxes:
                  An Explainable Neural Trees Workshop},
  howpublished = {Washington State University, Data \& Analytics Breakout},
  year         = {2026},
  month        = {May},
  url          = {https://github.com/cgrtml/wsu-workshop-may15}
}
```

## Contact

Cagri Temel, CTO at Hezarfen LLC, IEEE Senior Member.
[github.com/cgrtml/neural-trees](https://github.com/cgrtml/neural-trees) ·
[linkedin.com/in/cagritemel](https://www.linkedin.com/in/cagritemel)

Materials released under MIT License.
