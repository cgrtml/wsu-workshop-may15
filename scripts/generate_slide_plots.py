"""Generate all plot images embedded into the step-by-step slides."""
import os
import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from neural_trees import SoftDecisionTree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, 'data')
OUT = os.path.join(ROOT, 'slides', 'img')
os.makedirs(OUT, exist_ok=True)

# --- Load training data ---
cols = ['engine_id', 'cycle'] + [f'op{i}' for i in range(1, 4)] + [f's{i}' for i in range(1, 22)]
train = pd.read_csv(os.path.join(DATA, 'train_FD001.txt'), sep=r'\s+', header=None, names=cols)
max_cycles = train.groupby('engine_id')['cycle'].max().rename('max_cycle')
train = train.merge(max_cycles, on='engine_id')
train['RUL'] = (train['max_cycle'] - train['cycle']).clip(upper=125)

def bin_rul(r):
    if r < 30: return 0
    if r < 80: return 1
    return 2

train['health'] = train['RUL'].apply(bin_rul)

all_sensors = [f's{i}' for i in range(1, 22)]
informative = [s for s in all_sensors if train[s].std() > 0.001]
scaler = StandardScaler().fit(train[informative].values)
X = scaler.transform(train[informative].values)
y = train['health'].values
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# --- Plot 1: Engine 1 sensor trajectories ---
engine = train[train['engine_id'] == 1].set_index('cycle')
fig, axes = plt.subplots(2, 2, figsize=(11, 6))
for ax, sensor in zip(axes.flat, ['s2', 's7', 's11', 's14']):
    ax.plot(engine.index, engine[sensor], color='#4FC3F7', linewidth=1.5)
    ax.set_title(f'Engine 1 — {sensor}', color='#EEE')
    ax.set_xlabel('cycle', color='#BBB')
    ax.tick_params(colors='#BBB')
    ax.set_facecolor('#1a1a1a')
fig.patch.set_facecolor('#0a0a0a')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'step4_engine1.png'), dpi=110, bbox_inches='tight', facecolor='#0a0a0a')
plt.close()
print('Saved: step4_engine1.png')

# --- Train models ---
tree = SoftDecisionTree(depth=4, max_epochs=30, learning_rate=0.01, penalty_coef=1e-3, verbose=False)
tree.fit(X_tr, y_tr)
rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_tr, y_tr)

# --- Plot 2: Confusion matrix (dark facecolor to match slide) ---
labels = ['Critical', 'Caution', 'Healthy']
y_pred = tree.predict(X_te)
cm = confusion_matrix(y_te, y_pred)
fig, ax = plt.subplots(figsize=(7, 5.5))
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#1a1a1a')
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=labels, yticklabels=labels, ax=ax,
            cbar_kws={'shrink': 0.7},
            annot_kws={'color': '#FFF', 'size': 14})
ax.set_xlabel('Predicted', color='#EEE'); ax.set_ylabel('True', color='#EEE')
ax.set_title('Soft Decision Tree on CMAPSS FD001', color='#EEE')
ax.tick_params(colors='#BBB')
cbar = ax.collections[0].colorbar
cbar.ax.yaxis.set_tick_params(color='#BBB')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#BBB')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'step9_confusion.png'), dpi=110, bbox_inches='tight', facecolor='#0a0a0a')
plt.close()
print('Saved: step9_confusion.png')

# --- Plots 3-5: Attack overlays ---
clean = pd.read_csv(os.path.join(DATA, 'engine17_clean.csv'))
for letter, attack_file in [('A', 'attack_A.csv'), ('B', 'attack_B.csv'), ('C', 'attack_C.csv')]:
    attack = pd.read_csv(os.path.join(DATA, attack_file))
    fig, axes = plt.subplots(4, 4, figsize=(14, 9))
    for ax, s in zip(axes.flat, informative):
        ax.plot(clean['cycle'], clean[s], label='clean', alpha=0.8, linewidth=1.0, color='#4FC3F7')
        ax.plot(attack['cycle'], attack[s], label='attack', alpha=0.8, linewidth=1.0, color='#FFB74D')
        ax.set_title(s, fontsize=9, color='#EEE')
        ax.tick_params(labelsize=7, colors='#BBB')
        ax.set_facecolor('#1a1a1a')
    for ax in axes.flat[len(informative):]:
        ax.axis('off')
    axes.flat[0].legend(fontsize=8, facecolor='#222', labelcolor='#EEE')
    fig.patch.set_facecolor('#0a0a0a')
    plt.suptitle(f'Attack {letter} — clean (blue) vs attack (orange)', y=1.00, color='#EEE')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, f'attack_{letter}.png'), dpi=110, bbox_inches='tight', facecolor='#0a0a0a')
    plt.close()
    print(f'Saved: attack_{letter}.png')

print('\nAll slide images generated.')
print(f'Output dir: {OUT}')
