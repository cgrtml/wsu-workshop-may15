# WSU Data & Analytics Breakout — May 15, 2026

**Co-presenters:**
- **Cagri Temel** — Founder, Hezarfen LLC · IEEE Senior Member
- **Sundar Krishnamurthy** — Security Engineering Leader, Expedia Group · CISSP

**Venue:** Washington State University · Data & Analytics Breakout
**Date:** May 15, 2026 · 09:00–11:45

**Cagri's segment (~95 min):** *From Black Boxes to Glass Boxes — Building Explainable Neural Trees for Safety-Critical Decisions.* Hands-on workshop using NASA CMAPSS turbofan engine data to train soft decision trees, traverse model explanations, and detect faulty sensors with explainability.

This repository contains everything needed to run the 2-hour-45-minute workshop:
slides, two student notebooks (Colab-ready), the NASA CMAPSS data, three
adversarial test files for the team competition, and a landing page with QR-code
onboarding.

---

## Repo layout

```
wsu-workshop-may15/
├── PLAN.md                              # Minute-by-minute scenario (Turkish)
├── slides/
│   └── slides.html                      # Reveal.js single-file deck — open in any browser
├── notebooks/
│   ├── activity1_student.ipynb          # Train Your Own Neural Tree (with TODOs)
│   ├── activity1_solution.ipynb
│   ├── activity2_student.ipynb          # Adversarial Sensor Challenge (team comp.)
│   └── activity2_solution.ipynb
├── data/
│   ├── train_FD001.txt                  # NASA CMAPSS training trajectories
│   ├── test_FD001.txt
│   ├── RUL_FD001.txt
│   ├── engine17_clean.csv               # Reference engine for Activity #2
│   ├── attack_A.csv                     # Drift on Sensor 11 (Ps30)
│   ├── attack_B.csv                     # Stuck-at on Sensor 14 (NRc)
│   └── attack_C.csv                     # Gaussian noise on Sensor 9 (Nc)
├── scripts/
│   └── generate_attack_files.py         # Reproduces the three attack files
├── landing/
│   └── index.html                       # Mobile-friendly landing for QR onboarding
└── assets/
    └── qr_landing.png                   # QR code → github.com/cgrtml/wsu-workshop-may15
```

---

## Running the workshop

### Before the day

1. Open `slides/slides.html` in Chrome / Safari / Firefox. Press `F` for
   fullscreen, arrow keys to navigate.
2. Confirm both Colab notebooks open from the landing page on a phone.
3. Print the QR code (`assets/qr_landing.png`) as a backup if the projector
   blacks out.

### Setup the room sees

Students scan the QR code → land on `index.html` → tap *Activity 1* → Colab
opens with the notebook → "Copy to Drive" → run the first cell. No installs,
no Python environment, no manual file uploads. Total onboarding time is under
a minute per student.

---

## The two activities at a glance

**Activity 1 — Train Your Own Neural Tree (55 min, individual)**

Students load NASA CMAPSS turbofan data, bin RUL into 3 health classes, train a
`SoftDecisionTree` from the `neural-trees` package, evaluate it, and traverse
one prediction to read out the rule the model used.

**Activity 2 — Adversarial Sensor Challenge (35 min, team competition)**

3–4 student teams investigate three attack files (drift, stuck-at, gaussian
noise) on one engine. They use the soft tree's split weights to localize the
compromised sensor, then compare against a RandomForest baseline that can
change its prediction but cannot point to the cause. First team to identify
all three correctly wins.

Answer key (instructor only): see `notebooks/activity2_solution.ipynb`.

---

## The library

The workshop uses [`neural-trees`](https://github.com/cgrtml/neural-trees)
(MIT, on PyPI). All dependencies install with one cell:

```bash
pip install neural-trees
```

This is a soft decision tree implementation with a scikit-learn–compatible
API and a PyTorch backend. The CMAPSS-trained Temporal Neural Tree variant
referenced in the slides lives in a companion repository
([`turbofan-explainable-neural-trees`](https://github.com/cgrtml/turbofan-explainable-neural-trees))
and is the subject of the accompanying workshop paper.

---

## Citation

If you build on the workshop materials:

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

---

## Contact

- GitHub: [@cgrtml](https://github.com/cgrtml)
- LinkedIn: [linkedin.com/in/cagritemel](https://www.linkedin.com/in/cagritemel)
- Email: cagritemelusa@gmail.com

© 2026 Hezarfen LLC. Materials released under MIT License.
