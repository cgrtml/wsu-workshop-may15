"""
Build clean student notebooks (activity1_student.ipynb, activity2_student.ipynb)
where each step in the slides / README maps to exactly one empty code cell
preceded by a markdown header. Students paste step N from the slide into cell N.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, 'notebooks')


def md_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True) if source else [""],
    }


def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True) if source else [""],
    }


NOTEBOOK_METADATA = {
    "kernelspec": {
        "name": "python3",
        "display_name": "Python 3",
        "language": "python",
    },
    "language_info": {
        "name": "python",
        "version": "3.10",
    },
}


# ============ ACTIVITY 1 ============

a1_cells = []

a1_cells.append(md_cell(
    "# Activity 1 — Train Your Own Neural Tree\n"
    "\n"
    "**Workshop:** From Black Boxes to Glass Boxes  \n"
    "**Instructor:** Cagri Temel — Hezarfen LLC  \n"
    "**Venue:** Washington State University · May 15, 2026\n"
    "\n"
    "---\n"
    "\n"
    "## How to use this notebook\n"
    "\n"
    "There are **11 steps** below. Each step has a markdown header and one empty code cell.\n"
    "\n"
    "1. Watch the slide for the current step.\n"
    "2. Paste the code from the slide into the empty cell below the matching header.\n"
    "3. Run it with **Shift+Enter** (or click the ▶ button).\n"
    "4. Check that the output matches what's on the slide.\n"
    "5. Move to the next step.\n"
    "\n"
    "Run cells **in order** from top to bottom. Variables defined in earlier steps "
    "are used by later steps.\n"
    "\n"
    "If you get stuck, the full solution is in `activity1_solution.ipynb`.\n"
))

a1_steps = [
    ("Step 1 — Imports",
     "Pull in every library this activity uses. After this runs you should see `All set.`"),
    ("Step 2 — Load CMAPSS FD001",
     "Read the NASA training file as a pandas dataframe. Expected output: `(20631, 26) -> 100 engines` plus the first five rows."),
    ("Step 3 — Compute Remaining Useful Life (RUL)",
     "For each row, RUL = max cycle for that engine minus current cycle, capped at 125. Expected: a five-row table with `RUL = 125` for engine 1's earliest cycles."),
    ("Step 4 — Visualize engine 1's sensor degradation",
     "Plot four sensors across the engine's life. Sensors 2, 11, 14 trend up; sensor 7 trends down. The data is telling the story of failure."),
    ("Step 5 — Bin RUL into three health classes",
     "Critical (RUL < 30), Caution (30 ≤ RUL < 80), Healthy (RUL ≥ 80). Expected: roughly 14% Critical, 24% Caution, 61% Healthy."),
    ("Step 6 — Build the feature matrix",
     "Drop the six sensors that are constant (no signal). Standardize what remains. Expected: `X shape: (20631, 15) · y shape: (20631,)`."),
    ("Step 7 — Train / test split",
     "80/20 split, stratified by `y` so the class ratio is preserved in both halves. Expected: `(16504, 15) (4127, 15)`."),
    ("Step 8 — Train the Soft Decision Tree",
     "About 30 to 60 seconds on CPU. While you wait: PyTorch is running backpropagation on 16,500 rows for 30 epochs. Expected: per-epoch loss decreasing, final `Test accuracy: ~0.84`."),
    ("Step 9 — Confusion matrix and per-class report",
     "Where does the model get it right, where does it get it wrong? Expected: a Blues heatmap and a per-class precision/recall report. The bottom-left cell should be 0 — no Healthy engine flagged as Critical."),
    ("Step 10 — Inspect the split weights",
     "For each of the 15 internal nodes, print the sensor with the largest absolute weight. Some sensors will appear more than once — those are the model's pillars."),
    ("Step 11 — Read one prediction (the heart of the workshop)",
     "Pick test sample 17 and ask the model: what did you predict, with what confidence, and which sensor did you look at first? This is the output you would give a regulator."),
]

for title, desc in a1_steps:
    a1_cells.append(md_cell(f"## {title}\n\n{desc}\n"))
    a1_cells.append(code_cell(f"# Paste the code for {title.split(' — ')[0]} from the slide here, then Shift+Enter\n"))

a1_cells.append(md_cell(
    "---\n"
    "\n"
    "## You made it.\n"
    "\n"
    "By now you should have a trained model, an accuracy above 80%, and a printed decision path for one engine.\n"
    "Take a 10-minute break, then come back for the team competition in Activity 2.\n"
))

activity1 = {
    "cells": a1_cells,
    "metadata": NOTEBOOK_METADATA,
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open(os.path.join(OUT_DIR, 'activity1_student.ipynb'), 'w') as f:
    json.dump(activity1, f, indent=1)
print(f"Wrote: activity1_student.ipynb ({len(a1_cells)} cells)")


# ============ ACTIVITY 2 ============

a2_cells = []

a2_cells.append(md_cell(
    "# Activity 2 — Adversarial Sensor Challenge\n"
    "\n"
    "**Workshop:** From Black Boxes to Glass Boxes  \n"
    "**Instructor:** Cagri Temel — Hezarfen LLC  \n"
    "**Format:** Team competition · 3 to 4 students per team · 25 minutes\n"
    "\n"
    "---\n"
    "\n"
    "## The scenario\n"
    "\n"
    "You are the data science team at an airline. Maintenance ops sends you three\n"
    "suspicious test files for engine 17. In each file, **exactly one sensor channel\n"
    "has been manipulated**. Your job: find which sensor and what kind of attack.\n"
    "\n"
    "**Three attack types:**\n"
    "- Drift — a constant offset added\n"
    "- Stuck-at — frozen at a single value\n"
    "- Gaussian noise — random noise injected\n"
    "\n"
    "First team to identify all three correctly wins.\n"
    "\n"
    "## How to use this notebook\n"
    "\n"
    "There are **7 steps**. Each step has a markdown header and one empty code cell.\n"
    "Paste from the slide, run with **Shift+Enter**.\n"
    "\n"
    "**Important:** You will reuse the `tree`, `informative`, `scaler`, `X_train`, `y_train`,\n"
    "`X_test`, `y_test`, and `labels` variables from Activity 1. Keep that notebook open in\n"
    "another tab, or run the setup cell below first.\n"
))

a2_cells.append(md_cell(
    "### Setup (only if you closed the Activity 1 notebook)\n"
    "\n"
    "If your Activity 1 variables are still in memory, **skip this cell**. Otherwise,\n"
    "running this re-creates everything you need from scratch.\n"
))

a2_cells.append(code_cell(
    "# Setup cell — only run if you lost the Activity 1 kernel state\n"
    "import numpy as np\n"
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "from sklearn.model_selection import train_test_split\n"
    "from sklearn.preprocessing import StandardScaler\n"
    "from neural_trees import SoftDecisionTree\n"
    "\n"
    "cols = ['engine_id', 'cycle'] + [f'op{i}' for i in range(1, 4)] + [f's{i}' for i in range(1, 22)]\n"
    "train = pd.read_csv('train_FD001.txt', sep=r'\\s+', header=None, names=cols)\n"
    "max_cycles = train.groupby('engine_id')['cycle'].max().rename('max_cycle')\n"
    "train = train.merge(max_cycles, on='engine_id')\n"
    "train['RUL'] = (train['max_cycle'] - train['cycle']).clip(upper=125)\n"
    "\n"
    "def bin_rul(r):\n"
    "    if r < 30: return 0\n"
    "    if r < 80: return 1\n"
    "    return 2\n"
    "\n"
    "train['health'] = train['RUL'].apply(bin_rul)\n"
    "all_sensors = [f's{i}' for i in range(1, 22)]\n"
    "informative = [s for s in all_sensors if train[s].std() > 0.001]\n"
    "scaler = StandardScaler().fit(train[informative].values)\n"
    "X = scaler.transform(train[informative].values)\n"
    "y = train['health'].values\n"
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)\n"
    "tree = SoftDecisionTree(depth=4, max_epochs=30, learning_rate=0.01, penalty_coef=1e-3, verbose=False)\n"
    "tree.fit(X_train, y_train)\n"
    "labels = ['Critical', 'Caution', 'Healthy']\n"
    "print('Setup done. tree, scaler, informative, labels are ready.')\n"
))

a2_steps = [
    ("Step 1 — Add a RandomForest baseline",
     "A black-box comparison for the explainable Soft Decision Tree. Expected: both models around 0.84 accuracy. Essentially identical on clean data."),
    ("Step 2 — Predict on clean engine 17",
     "Establish a reference: what do both models say about the un-attacked engine? Expected: 276 cycles, agreement around 0.95."),
    ("Step 3 — How much did each attack change the predictions?",
     "Run both models on each attack file and count cycle-by-cycle disagreement against the clean baseline. Watch Attack C carefully: the RandomForest barely notices it."),
    ("Step 4 — Visualize Attack A (look for two parallel lines)",
     "Plot every informative sensor twice — clean in blue, attack in orange. Fourteen panels overlap. One panel shows two separate lines: that is the manipulated sensor."),
    ("Step 5 — Visualize Attack B (look for a flat horizontal line)",
     "Same plot for attack B. The orange line on the manipulated sensor will be completely flat while the blue line keeps evolving."),
    ("Step 6 — Visualize Attack C (look for a noisier line)",
     "Attack C is subtler. The trend is preserved; only the variance changes. Look for the panel where orange is noticeably more jagged than blue."),
    ("Step 7 — Quantify the divergence",
     "Confirm the visual answer with numbers. For each attack file, the top-divergent sensor is the manipulated one. The other 14 sensors are identical between clean and attack."),
]

for title, desc in a2_steps:
    a2_cells.append(md_cell(f"## {title}\n\n{desc}\n"))
    a2_cells.append(code_cell(f"# Paste the code for {title.split(' — ')[0]} from the slide here, then Shift+Enter\n"))

a2_cells.append(md_cell(
    "---\n"
    "\n"
    "## Your team's answers\n"
    "\n"
    "Fill in the dictionary below before time is up. The instructor will collect.\n"
))

a2_cells.append(code_cell(
    "TEAM_NAME = ''  # e.g. 'Team Cougar'\n"
    "\n"
    "answers = {\n"
    "    'attack_A': {'sensor': 's??', 'type': 'drift / stuck-at / noise'},\n"
    "    'attack_B': {'sensor': 's??', 'type': 'drift / stuck-at / noise'},\n"
    "    'attack_C': {'sensor': 's??', 'type': 'drift / stuck-at / noise'},\n"
    "}\n"
    "\n"
    "print(f'Team: {TEAM_NAME}')\n"
    "for k, v in answers.items():\n"
    "    print(f'  {k}: sensor={v[\"sensor\"]:4s}  type={v[\"type\"]}')\n"
))

a2_cells.append(md_cell(
    "---\n"
    "\n"
    "## Wrap-up question\n"
    "\n"
    "Discuss with your team:\n"
    "\n"
    "> *In a real predictive-maintenance system, would you rely on the model's prediction, on its explanation, or both? When would you trust one over the other?*\n"
))

activity2 = {
    "cells": a2_cells,
    "metadata": NOTEBOOK_METADATA,
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open(os.path.join(OUT_DIR, 'activity2_student.ipynb'), 'w') as f:
    json.dump(activity2, f, indent=1)
print(f"Wrote: activity2_student.ipynb ({len(a2_cells)} cells)")
