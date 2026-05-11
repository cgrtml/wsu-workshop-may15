"""
Activity 1 rehearsal — runs the full student flow end-to-end and saves outputs.
Use this to verify the workshop works on your machine before May 15.
"""
import os
import matplotlib
matplotlib.use('Agg')  # headless save, no GUI
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from neural_trees import SoftDecisionTree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, 'data')
OUT = os.path.join(ROOT, 'rehearsal_output')
os.makedirs(OUT, exist_ok=True)

print('=' * 60)
print('STEP 1 — Load CMAPSS FD001')
print('=' * 60)
cols = ['engine_id', 'cycle'] + [f'op{i}' for i in range(1, 4)] + [f's{i}' for i in range(1, 22)]
train = pd.read_csv(os.path.join(DATA, 'train_FD001.txt'), sep=r'\s+', header=None, names=cols)
print(f'Rows: {len(train):,} | Engines: {train.engine_id.nunique()} | Sensors: 21')
print(train.head(3))

print()
print('=' * 60)
print('STEP 2 — Compute RUL and bin into 3 health classes')
print('=' * 60)
max_cycles = train.groupby('engine_id')['cycle'].max().rename('max_cycle')
train = train.merge(max_cycles, on='engine_id')
train['RUL'] = (train['max_cycle'] - train['cycle']).clip(upper=125)

def bin_rul(rul):
    if rul < 30: return 0   # Critical
    if rul < 80: return 1   # Caution
    return 2                # Healthy

train['health'] = train['RUL'].apply(bin_rul)
labels = ['Critical', 'Caution', 'Healthy']
class_counts = train['health'].value_counts().sort_index()
for i, n in class_counts.items():
    print(f'  {labels[i]:9s}: {n:>6,} rows ({100*n/len(train):.1f}%)')

print()
print('=' * 60)
print('STEP 3 — Plot one engine\'s sensor trajectories')
print('=' * 60)
engine = train[train['engine_id'] == 24]
fig, axes = plt.subplots(2, 2, figsize=(12, 6))
for ax, sensor in zip(axes.flat, ['s2', 's7', 's11', 's14']):
    ax.plot(engine['cycle'], engine[sensor])
    ax.set_title(f'Engine 24 — {sensor}')
    ax.set_xlabel('cycle')
plt.tight_layout()
trajectory_path = os.path.join(OUT, '01_engine24_sensors.png')
plt.savefig(trajectory_path, dpi=110, bbox_inches='tight')
plt.close()
print(f'Saved: {trajectory_path}')

print()
print('=' * 60)
print('STEP 4 — Build features and stratified split')
print('=' * 60)
all_sensors = [f's{i}' for i in range(1, 22)]
informative = [s for s in all_sensors if train[s].std() > 0.001]
print(f'Informative sensors after dropping near-constant: {len(informative)} of 21')
print(f'  Dropped: {sorted(set(all_sensors) - set(informative))}')
X = StandardScaler().fit_transform(train[informative].values)
y = train['health'].values
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print(f'Train shape: {X_train.shape} | Test shape: {X_test.shape}')

print()
print('=' * 60)
print('STEP 5 — Train Soft Decision Tree (depth=4, 30 epochs)')
print('=' * 60)
tree = SoftDecisionTree(
    depth=4,
    max_epochs=30,
    learning_rate=0.01,
    penalty_coef=1e-3,
    verbose=False,
)
import time
t0 = time.time()
tree.fit(X_train, y_train)
elapsed = time.time() - t0
acc = (tree.predict(X_test) == y_test).mean()
print(f'Training time: {elapsed:.1f}s')
print(f'Test accuracy: {acc:.3f}')

print()
print('=' * 60)
print('STEP 6 — Confusion matrix and classification report')
print('=' * 60)
y_pred = tree.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=labels, yticklabels=labels, ax=ax)
ax.set_xlabel('Predicted'); ax.set_ylabel('True')
ax.set_title('Soft Decision Tree on CMAPSS FD001')
plt.tight_layout()
cm_path = os.path.join(OUT, '02_confusion_matrix.png')
plt.savefig(cm_path, dpi=110, bbox_inches='tight')
plt.close()
print(f'Saved: {cm_path}')
print()
print(classification_report(y_test, y_pred, target_names=labels))

print('=' * 60)
print('STEP 7 — Traverse one prediction (the heart of the workshop)')
print('=' * 60)
splits = tree.get_split_weights()
idx = 17
x = X_test[idx]
true_class = labels[y_test[idx]]
pred_class = labels[tree.predict([x])[0]]
proba = tree.predict_proba([x])[0]
root_dominant = informative[np.argmax(np.abs(splits[0]))]

print(f'Test sample index: {idx}')
print(f'True class:        {true_class}')
print(f'Predicted class:   {pred_class}')
print(f'Probabilities:     Critical={proba[0]:.3f}  Caution={proba[1]:.3f}  Healthy={proba[2]:.3f}')
print(f'Root node leans on: {root_dominant}')
print()
print('Dominant sensor at each internal node:')
for node_idx, w in enumerate(splits[:7]):
    dom = informative[int(np.argmax(np.abs(w)))]
    strength = float(np.max(np.abs(w)))
    print(f'  Node {node_idx:2d}: {dom:5s}  (weight magnitude: {strength:.3f})')

print()
print('=' * 60)
print('REHEARSAL COMPLETE')
print('=' * 60)
print(f'Outputs saved to: {OUT}')
print('Open the PNGs to see what students will produce.')
