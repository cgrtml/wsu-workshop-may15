# WSU Data & Analytics Breakout, May 15 2026

Workshop materials for the breakout session at Washington State University.
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

## Activity 1

55 minutes, individual. Students load CMAPSS FD001 (100 turbofan engines,
21 sensors per timestep), compute remaining useful life per cycle, bin
into three health classes (Critical, Caution, Healthy), train a
`SoftDecisionTree` from `neural-trees` on a stratified 80/20 split, and
inspect the confusion matrix. They then read the model's split weights
at every internal node and traverse one specific test sample end to end.

The point of the session lands here: the trained model can defend its
decision sensor by sensor, while an LSTM of equivalent accuracy cannot.

## Activity 2

25 minutes, three to four students per team. Each team receives three
corrupted versions of one engine's telemetry. In each file a single
sensor has been manipulated, either by a constant offset (drift on
sensor 11), by freezing at one value (stuck-at on sensor 14), or by
Gaussian noise injection (sensor 9). They compare predictions from the
soft decision tree they trained in Activity 1 with a RandomForest
baseline, observe how each model's behavior shifts under attack, and
use the soft tree's split weights to localize the faulty sensor in
each file.

The teaching point: the RandomForest changes its prediction but cannot
tell you which sensor caused the change. The explainable model can.

The instructor's answer key is `notebooks/activity2_solution.ipynb`.
Expected answers, in order: sensor 11 (drift), sensor 14 (stuck-at),
sensor 9 (noise).

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
[linkedin.com/in/cagritemel](https://www.linkedin.com/in/cagritemel) ·
cagritemelusa@gmail.com

Materials released under MIT License.
