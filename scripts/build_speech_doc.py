"""
Build a Word document containing the full speech Cagri will deliver to students,
slide by slide, from opening line to closing line. Designed to be read off a
tablet or printed handout while presenting.
"""
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_PATH = os.path.join(ROOT, 'WSU-Workshop-Speech.docx')

doc = Document()

# Page margins (slightly tighter than default so the text breathes per slide)
for section in doc.sections:
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

# Default font for the document
style = doc.styles['Normal']
style.font.name = 'Georgia'
style.font.size = Pt(13)


def add_title_page():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('From Black Boxes to Glass Boxes')
    r.font.size = Pt(28); r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('Full Presentation Script')
    r.font.size = Pt(18); r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    doc.add_paragraph()
    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('Washington State University · Data and Analytics Breakout')
    r.font.size = Pt(14); r.italic = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('May 15, 2026 · 09:00 – 11:45 (165 minutes)')
    r.font.size = Pt(14); r.italic = True

    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('Cagri Temel')
    r.font.size = Pt(16); r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('CTO, Hezarfen LLC  ·  IEEE Senior Member')
    r.font.size = Pt(12); r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()

    # How to use
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run('How to use this script')
    r.font.size = Pt(14); r.font.bold = True

    intro = (
        "Read this script aloud at a natural conversational pace. "
        "Each slide is a numbered section. The heading shows the slide number and the running time so you can "
        "stay on schedule. Bold lines are emphasis — pause briefly before and after them. Italic notes in square brackets "
        "[like this] are stage directions, not spoken. Everything else is your speech, word for word."
    )
    p = doc.add_paragraph(intro)
    p.paragraph_format.space_after = Pt(6)

    doc.add_page_break()


def add_section_heading(text, time_marker=None):
    """Top-level section divider, e.g. BLOCK 2 - ACTIVITY 1."""
    p = doc.add_paragraph()
    r = p.add_run(text.upper())
    r.font.size = Pt(20); r.font.bold = True
    r.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    if time_marker:
        p = doc.add_paragraph()
        r = p.add_run(time_marker)
        r.font.size = Pt(11); r.font.italic = True
        r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
        p.paragraph_format.space_after = Pt(12)
    # Add a thin horizontal rule via bottom border on a paragraph
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'cccccc')
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_slide_header(slide_num, slide_title, time_clock):
    """e.g. 'Slide 5 — STAKES   |   09:08'."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(f'Slide {slide_num}  ·  {slide_title}')
    r.font.size = Pt(15); r.font.bold = True
    r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    r = p.add_run(f'        {time_clock}')
    r.font.size = Pt(11); r.font.italic = True
    r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)


def add_speech(text):
    """The speech body. Plain readable paragraph."""
    p = doc.add_paragraph(text)
    p.paragraph_format.line_spacing = 1.45
    p.paragraph_format.space_after = Pt(8)
    for r in p.runs:
        r.font.size = Pt(13)


def add_emphasis(text):
    """A line of strong emphasis — what NOT to misspeak."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.size = Pt(13); r.font.bold = True
    r.font.color.rgb = RGBColor(0x14, 0x14, 0x14)


def add_direction(text):
    """A stage direction in italics + brackets, not spoken."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(f'[{text}]')
    r.font.size = Pt(11); r.italic = True
    r.font.color.rgb = RGBColor(0x99, 0x66, 0x00)


# ===== content =====

add_title_page()

# ============ BLOCK 1 - LECTURE ============
add_section_heading('Block 1 — Lecture (slides 1 to 19)', 'Running time 09:00 to 09:30 · 30 minutes')

add_slide_header(1, 'Cover', '09:00')
add_speech(
    "Good morning everyone. I'm Cagri Temel, CTO at Hezarfen LLC. "
    "For the next two hours and forty-five minutes you're going to do something most people don't get to do until they're in industry. "
    "You're going to train a real machine learning model on real NASA data. You're going to break it on purpose. "
    "And then you're going to explain exactly how it makes its decisions."
)
add_speech(
    "By the end of the session, you'll have a working model on your laptop. You'll know which sensor failed on an aircraft engine. "
    "And many of you will have your first open-source contribution on GitHub. Let's get started."
)

add_slide_header(2, 'Who I am', '09:01')
add_speech(
    "Quick about me. I'm CTO of a company called Hezarfen, where we build explainable AI for industries that have to answer to regulators. "
    "Banks. Insurers. Healthcare. Aviation. I'm an IEEE Senior Member. I also maintain a Python package called neural-trees, "
    "and that's what we'll use today."
)
add_emphasis(
    "Don't try to memorize any of this. The only thing I want you to take away from this slide is the bottom line: "
    "in the next two hours and forty-five minutes, you build, you break, and you explain a real model."
)

add_slide_header(3, "Today's Mission", '09:02')
add_speech(
    "For the next few hours we're going to look at one specific question. "
    "How do we make data-driven systems trustworthy in places where getting them wrong is expensive?"
)
add_speech(
    "Our case study today is a turbofan engine — the kind that powers passenger jets — "
    "that has to predict its own failure before it happens. "
    "By the end of the session, you'll understand why this is harder than it looks, and why being accurate is not enough."
)

add_slide_header(4, 'Hook', '09:04')
add_emphasis("So. A turbofan engine. The question is — when will it fail?")
add_direction("Pause for two full seconds. Let the question hang.")
add_speech(
    "Think about it for a moment. If you knew with certainty — exactly when this engine would fail — "
    "what would you do differently than what airlines do today?"
)
add_direction("Don't call on anyone. Just let them think for a beat.")

add_slide_header(5, 'Stakes', '09:05')
add_speech("Here's why this is hard. There are three ways to be wrong, and all three are expensive.")
add_speech("One. You predict too late. The engine fails in flight. You lose lives.")
add_speech("Two. You predict too early. You pull a perfectly good engine out of service. Each engine is about a hundred million dollars.")
add_speech(
    "Three — and this is the one engineers forget. You predict accurately, but you can't explain how. "
    "In that case, the FAA refuses to certify your system. You can have the best model in the world; "
    "if you can't defend it, it doesn't fly."
)
add_emphasis(
    "That's the whole point. Accuracy by itself is not enough. You also need to be able to defend the prediction."
)

add_slide_header(6, 'NASA CMAPSS', '09:08')
add_speech(
    "The dataset we'll use is called NASA CMAPSS. It's open, it's free, and it's been the standard benchmark "
    "in predictive maintenance for about fifteen years now."
)
add_speech(
    "A hundred turbofan engines, each one simulated all the way to failure. Twenty-one sensors per timestep: "
    "temperatures, pressures, fan speeds, fuel flow. Each engine logs hundreds of flight cycles before it dies. "
    "You'll be working with this data on your own laptop in twenty minutes."
)

add_slide_header(7, 'Remaining Useful Life', '09:10')
add_speech(
    "The thing we're going to predict is called RUL — Remaining Useful Life. It's the number of flight cycles left "
    "before the engine fails."
)
add_speech(
    "So if an engine fails at cycle 192: at cycle 100, its RUL is 92. At cycle 190, it's 2. At failure, it's zero. "
    "We cap RUL at 125 because predicting further out than that isn't useful. "
    "Past a hundred and twenty-five cycles, you're just guessing about the future."
)

add_slide_header(8, '21 Sensors', '09:12')
add_speech(
    "For every cycle, we get twenty-one sensor readings. Don't try to memorize them all."
)
add_speech(
    "But three of them I want you to notice right now, because they'll come back later. "
    "Sensor seven — high-pressure compressor outlet pressure. "
    "Sensor eleven — static pressure. "
    "Sensor fourteen — corrected core speed."
)
add_emphasis(
    "These three are the model's favorites. Remember those names. They show up again in Activity 2, "
    "when one of them gets attacked."
)

add_slide_header(9, 'LSTM Result', '09:14')
add_speech(
    "Here's the modern approach. We throw an LSTM at it. A two-layer recurrent neural network. "
    "After training, the LSTM gets an RMSE of fifteen-point-four-nine cycles. R-squared 0.855."
)
add_speech("That's pretty good. About fifteen cycles off, on average.")
add_emphasis("So. We ship it to the FAA, right?")

add_slide_header(10, 'Regulator Problem', '09:16')
add_emphasis("No.")
add_direction("Two-second pause.")
add_speech(
    "Regulators don't ask, 'how accurate is your model?' They ask, 'why did your model say that?' "
    "And if you can't answer that question in a way a non-engineer can follow, your model doesn't ship."
)
add_speech(
    "FAA for aviation. FDA for medical devices. OCC for banking. EU AI Act for anything that touches a European customer. "
    "This isn't theory. This is what actually blocks AI systems from being deployed in regulated industries."
)

add_slide_header(11, 'Black Box vs Glass Box', '09:18')
add_speech(
    "So you're stuck between two worlds. On one side: black-box models like LSTMs and transformers. High accuracy, "
    "but you can't explain why. On the other side: glass-box models like classic decision trees or linear regression. "
    "Fully explainable, but lower accuracy."
)
add_speech("Regulators love glass boxes. Engineers prefer black boxes.")
add_emphasis("So the question today is: can we have both?")

add_slide_header(12, 'Classic Decision Tree', '09:20')
add_speech(
    "You've all seen a decision tree before. Beautiful structure. Sensor eleven is above the threshold, go left. "
    "Below, go right. It's the most explainable model that exists."
)
add_speech(
    "But classic decision trees often have worse accuracy than neural networks. Why? Because the splits are hard. "
    "A 0.01 difference in a sensor value flips the entire path. That brittleness is what limits accuracy."
)

add_slide_header(13, 'Hard Split', '09:22')
add_speech("This is the code for a hard split.")
add_emphasis("And you are NOT typing this. It's here for illustration.")
add_speech(
    "If x is bigger than the threshold, return 'right'. Otherwise, return 'left'. "
    "The output is a string. Discrete. No gradient."
)
add_speech(
    "And no gradient means no backpropagation. You build the tree node by node, greedily. "
    "You cannot train it end to end like a neural network."
)

add_slide_header(14, 'Soft Split', '09:23')
add_speech("Now look at this. Same function. One substitution. The if-else becomes a sigmoid.")
add_speech(
    "Now the output is a probability — somewhere between zero and one. Continuous. "
    "And because it's continuous, gradient flows through it."
)
add_emphasis(
    "That single change is what makes everything we do today possible. A tree you can train with backpropagation, "
    "just like a neural network."
)

add_slide_header(15, 'Soft Decision Tree', '09:25')
add_speech(
    "Here's what the whole tree looks like. Every internal node is a sigmoid split. "
    "Every leaf has a class distribution — Critical, Caution, Healthy probabilities."
)
add_speech(
    "The final prediction is a weighted sum of all the leaves, weighted by the probability of reaching each leaf. "
    "Mathematically, it's smooth. Fully differentiable end to end."
)

add_slide_header(16, 'Best of Both', '09:26')
add_speech(
    "And here's the win. From the tree side, you keep path traceability, per-feature thresholds, human-readable rules. "
    "From the network side, you get end-to-end training and the accuracy that comes with it."
)
add_emphasis("You get both. That's why soft decision trees matter for regulated industries.")

add_slide_header(17, 'Three Properties', '09:27')
add_speech("Three properties make this approach work for safety-critical AI.")
add_speech("One. Explainability. Every prediction comes with the path that produced it.")
add_speech("Two. Noise robustness. Soft splits don't break when a sensor wobbles a little.")
add_speech(
    "Three. Sensor failure tolerance. When you train with channel-level dropout, the model learns to operate "
    "even when some sensors are missing."
)
add_emphasis("You'll see all three in the next ninety minutes. Not on a slide. On your own laptop.")

add_slide_header(18, 'Paper Numbers', '09:28')
add_speech(
    "These are the numbers from my paper. On clean CMAPSS data, an LSTM gets an RMSE of fifteen-point-four-nine cycles. "
    "The Temporal Neural Tree — the variant we use — gets fifteen-point-seven-eight. Essentially equal."
)
add_speech(
    "Now look at the next column. When thirty percent of the sensors are missing — which happens in real aircraft, "
    "sensors break — the LSTM degrades by eighty-nine percent. The Temporal Neural Tree degrades by only seventeen percent."
)
add_emphasis("Five times more robust. And it's fully explainable. That's the headline.")

add_slide_header(19, 'neural-trees Package', '09:29')
add_speech(
    "The tool you're going to use is called neural-trees. I wrote it. It's on PyPI, MIT licensed, open source."
)
add_speech(
    "The API follows scikit-learn, so if you've used scikit-learn before, you already know how to use this. "
    "Fit. Predict. Predict probability. Score. The backend is PyTorch. You don't need a GPU; CPU is fine for everything we do today."
)
add_speech("And at the end of the workshop, you'll get a chance to contribute back to it.")

doc.add_page_break()

# ============ BLOCK 2 - ACTIVITY 1 ============
add_section_heading('Block 2 — Activity 1: Train Your Own Neural Tree', 'Running time 09:30 to 10:25 · 55 minutes')

add_slide_header(20, 'Activity 1 Intro', '09:30')
add_speech(
    "Okay. We're moving from lecture to hands-on now. The next fifty-five minutes are yours."
)
add_speech(
    "You're going to train your own neural tree on the NASA data we just talked about. "
    "I'm going to walk around. If you get stuck, raise a hand, I'll come help."
)
add_speech(
    "There are eleven steps. Each step is on its own slide. You paste the code, run it, and check that the output "
    "matches what I'm showing on screen. Ready? Let's go."
)

add_slide_header(21, 'QR Code', '09:31')
add_speech("Pull out your phones and scan this QR code. It opens our workshop landing page.")
add_speech(
    "Tap Activity 1. That opens a Google Colab notebook on your laptop. Sign in with your Gmail. "
    "Then click 'Copy to Drive' so you have your own editable copy. Run the first cell to make sure everything works."
)
add_direction("Watch the room for two minutes. Help anyone who's stuck. Do not advance until ~80% are on the notebook.")

add_slide_header(22, 'Activity 1 Overview', '09:33')
add_speech("Quick overview of the next fifty-five minutes. Six main stages.")
add_speech(
    "We load CMAPSS and look at it. Bin the labels into three classes. Train the Soft Decision Tree — that takes about a minute. "
    "Evaluate it with a confusion matrix."
)
add_emphasis(
    "And then — this is the step that matters most — we traverse one prediction. We literally read out the rule the model used. "
    "If you remember one thing from this entire workshop, it should be that step. Let's start."
)

add_slide_header(23, 'Step 1 — Imports', '09:34')
add_speech("First step: imports. Paste this code into a fresh cell. Hit Shift+Enter. You should see 'All set.'")
add_speech(
    "If you get an IndentationError, that means one of your lines has a stray space at the beginning. "
    "Copy-paste does that sometimes. Click into the cell, hit Command-A to select everything, then Shift+Tab to clear indentation, "
    "and run again."
)

add_slide_header(24, 'Step 2 — Load Data', '09:37')
add_speech(
    "Now we load the data. CMAPSS comes as a plain text file with no headers, so we tell pandas what to call the columns."
)
add_speech(
    "After this runs, you should see two things. The shape — twenty thousand six hundred and thirty-one rows by twenty-six columns. "
    "And the number of engines — one hundred. The first five rows show engine one at cycles one through five."
)
add_emphasis(
    "Those numbers — temperatures, pressures, fan speeds — those are exactly what a real flight data recorder logs."
)

add_slide_header(25, 'Step 3 — Compute RUL', '09:41')
add_speech(
    "Step three computes the label we're trying to predict. For each row, RUL equals the engine's maximum cycle minus the current cycle. "
    "We cap it at a hundred and twenty-five."
)
add_speech(
    "After this runs, you'll see five rows of engine one. All five show RUL equal to a hundred and twenty-five — "
    "because at the very start of the engine's life, the real RUL is way above a hundred and twenty-five, but we capped it. That's expected."
)

add_slide_header(26, 'Step 4 — Plot Engine 1', '09:44')
add_speech(
    "Now we visualize. We're going to plot four sensors for engine one across its entire one-hundred-and-ninety-two-cycle life."
)
add_speech(
    "After this runs, you should see a two-by-two plot. Look at it closely. "
    "Sensor two — temperature — goes up over time. Sensor eleven — pressure — goes up. Sensor fourteen — corrected core speed — goes up. "
    "But sensor seven — pressure at the HPC outlet — goes down."
)
add_emphasis(
    "That's the engine wearing out. Temperatures rising, compressor pressure dropping. The data is telling us the story of failure. "
    "Now we have to teach a model to see it."
)

add_slide_header(27, 'Step 5 — Bin RUL', '09:49')
add_speech(
    "We're going to turn this into a classification problem. RUL is a number, but in real aviation operations, no one says "
    "'this engine has forty-seven cycles left.' They say 'this engine is healthy', 'caution', or 'critical.'"
)
add_speech(
    "So we bin RUL into three classes. Below thirty is Critical. Thirty to eighty is Caution. Above eighty is Healthy. "
    "When you run this, you should see roughly fourteen percent Critical, twenty-four percent Caution, sixty-one percent Healthy. "
    "The classes are imbalanced. That's reality. Most of the time the engine is fine."
)

add_slide_header(28, 'Step 6 — Feature Matrix', '09:53')
add_speech(
    "Now we drop the six sensors that are constant. They carry no information. That leaves fifteen informative sensors. "
    "Then we standardize — every column gets zero mean and unit variance."
)
add_speech(
    "Soft decision trees don't strictly require standardization, but the sigmoid splits behave much better when the input is on a consistent scale. "
    "After this runs, you should see X shape twenty-thousand-six-hundred-and-thirty-one by fifteen. Y shape twenty-thousand-six-hundred-and-thirty-one."
)

add_slide_header(29, 'Step 7 — Train/Test Split', '09:57')
add_speech("Standard train-test split. Eighty percent training, twenty percent test.")
add_speech(
    "Two things matter here. Stratify equals y — that preserves the class ratio in both sets. "
    "And random state equals forty-two — so everyone in this room gets the exact same numbers. If yours don't match, you typed something wrong."
)
add_speech(
    "After this runs you should see sixteen thousand five hundred and four rows for training. Four thousand one hundred and twenty-seven for test."
)

add_slide_header(30, 'Step 8 — Train SDT', '10:00')
add_speech("Okay, this is the slow one. About thirty to sixty seconds on CPU.")
add_speech(
    "While we wait, let me tell you what's happening. PyTorch is doing backpropagation on sixteen thousand rows for thirty epochs. "
    "Every epoch, the loss should come down a little."
)
add_speech(
    "When it finishes, you should see a test accuracy around 0.84. If yours lands anywhere between 0.82 and 0.86, that's normal — "
    "randomness in training varies a little across machines."
)
add_speech(
    "While we wait — quick question. What do you think an LSTM would get on the same problem?"
)
add_direction("Let them shout out a number. Most will guess around 0.85.")
add_emphasis("Right. About the same. The point is not accuracy. The point is what we can do with the model next.")

add_slide_header(31, 'Step 9 — Confusion Matrix', '10:05')
add_speech("Now we look at where the model is right and where it's wrong.")
add_speech("You should see a confusion matrix. Three by three. Color-coded.")
add_emphasis(
    "Look at the bottom-left cell. It should say zero. That means: out of every Healthy engine in the test set, "
    "the model wrongly flagged zero of them as Critical. We never raised a false alarm."
)
add_speech(
    "Now look at the top row. Out of six hundred Critical engines, we caught about four hundred and ninety. We missed some — "
    "but only five of those misses went all the way to Healthy."
)
add_emphasis(
    "In aviation language: we don't miss many dangerous engines, and we don't waste healthy ones. That's a useful model."
)

add_slide_header(32, 'Step 10 — Split Weights', '10:10')
add_speech(
    "Now we peek inside the model. Soft decision trees have fifteen internal nodes — one root, then it branches out. "
    "For each internal node, we ask: which sensor does this node lean on the most?"
)
add_speech(
    "When you run this, you'll see fifteen nodes and their dominant sensors. "
    "Notice some sensors show up multiple times. Sensor fourteen and sensor six, in particular."
)
add_emphasis(
    "Those are the pillars of the model. If those sensors go bad, the model is in trouble. Remember sensor fourteen. It comes back in Activity 2."
)

add_slide_header(33, 'Step 11 — Traverse Prediction', '10:15')
add_emphasis("This is the step that matters most.")
add_speech(
    "We pick one specific test sample — sample seventeen — and we ask the model: what did you predict, "
    "with what confidence, and which sensor did you look at first?"
)
add_speech(
    "When you run this, you should see four lines. Read them out loud to yourself. "
    "The model predicted Healthy with eighty-five percent confidence. Zero percent Critical. "
    "The root node leaned on sensor seven — HPC outlet pressure."
)
add_emphasis(
    "Now imagine you have to explain this prediction to a regulator. With this output, you can say: "
    "'My model classified this engine as Healthy because the static pressure at the high-pressure compressor outlet "
    "was above its decision threshold.' "
    "An LSTM cannot give you this answer. That is why we did all of this."
)

add_slide_header(34, 'Checkpoint', '10:23')
add_speech("Okay. Take a breath.")
add_speech(
    "By now you should have three things on your screen. A trained Soft Decision Tree. "
    "Test accuracy above eighty percent. A printed decision path for engine seventeen."
)
add_speech(
    "If you're missing any of those, find me during the break and we'll catch up. "
    "Ten minutes break. Get coffee. Stretch. When you come back at ten thirty-five, we run the team competition."
)

doc.add_page_break()

# ============ BLOCK 3 - ACTIVITY 2 ============
add_section_heading('Block 3 — Activity 2: Adversarial Sensor Challenge', 'Running time 10:35 to 11:00 · 25 minutes')

add_slide_header(35, 'Activity 2 Intro', '10:35')
add_speech("Okay, we're back. Activity 2 is different. This is a competition. You'll work in teams.")
add_speech("The first team to identify all three attacks correctly gets bragging rights for the day.")
add_emphasis(
    "Here's the setup. One of engine seventeen's sensors is reporting bad data. You don't know which sensor. "
    "You don't know what kind of attack. Your job is to find both."
)

add_slide_header(36, 'Scenario', '10:36')
add_speech("Imagine you're the data science team at an airline. Maintenance ops just sent you a message.")
add_emphasis(
    "'Something is wrong with engine seventeen. The pattern looks like a sensor drift, a frozen sensor, or noise spikes, "
    "but we can't tell which channel is at fault. Localize the faulty sensor before the next flight.'"
)
add_speech(
    "You have two tools. Your Soft Decision Tree from Activity 1, which is explainable. "
    "And we'll add a RandomForest baseline, which is more accurate but opaque. Use both. See which one is actually useful."
)

add_slide_header(37, 'Teams', '10:37')
add_speech("Okay. Form groups of three to four people. Pick the people next to you. Thirty seconds.")
add_direction("Walk to the back of the room while teams form. Come back.")
add_speech(
    "Use one notebook per team. One person types, the others think and argue. "
    "Once we start the clock, you have seventeen minutes for analysis. "
    "First team to identify all three correctly — sensor and attack type for each file — wins."
)

add_slide_header(38, 'Three Attack Files', '10:38')
add_speech("Three files.")
add_speech("Attack A is a drift — a sensor with a constant offset added.")
add_speech("Attack B is stuck-at — a sensor frozen at a single value.")
add_speech("Attack C is Gaussian noise — a sensor with random noise injected.")
add_emphasis(
    "All three files are copies of clean engine seventeen data. But in each one, exactly one sensor channel has been manipulated. "
    "Find which one."
)

add_slide_header(39, 'A2 Step 1 — RF Baseline', '10:40')
add_speech("First, we add a RandomForest baseline. Same data, same labels.")
add_speech(
    "When you run this, you should see two accuracies. SoftTree around 0.841. RandomForest around 0.843. "
    "Essentially identical on clean data."
)
add_emphasis("The whole point of this activity is showing what happens when we move OFF clean data.")

add_slide_header(40, 'A2 Step 2 — Clean Baseline', '10:42')
add_speech(
    "Now we load the clean engine seventeen file. This is the reference — the un-attacked version. "
    "We run both models on it and store the predictions."
)
add_speech(
    "After this you should see two hundred and seventy-six cycles. And the two models agree on ninety-five percent of them. "
    "That's our baseline. When reality is normal, the two models say the same thing."
)

add_slide_header(41, 'A2 Step 3 — Score Attacks', '10:44')
add_speech(
    "Now we run both models on each of the three attack files, and compare against the clean baseline."
)
add_speech("Read your output carefully.")
add_speech("Attack A: tree changed eighteen cycles, RandomForest changed fourteen.")
add_speech("Attack B: tree changed thirty-three, RandomForest changed eight.")
add_emphasis("Attack C — and this is the one — tree changed eight, RandomForest changed only one.")
add_speech(
    "The RandomForest barely noticed Attack C. It says 'everything looks fine' when in reality a sensor is broken. "
    "The Soft Tree caught eight cycles."
)
add_emphasis(
    "The explainable model is also the more sensitive one to subtle manipulations. That's not a coincidence."
)

add_slide_header(42, 'A2 Step 4 — Attack A', '10:48')
add_speech("Now we visualize Attack A. We plot each sensor twice. Clean in blue. Attack in orange.")
add_speech(
    "Fourteen of the fifteen panels will show only one line — because the blue and orange overlap exactly. "
    "But ONE panel will show two separate lines. That's your manipulated sensor."
)
add_speech("Look carefully. Which sensor is it?")
add_direction("Pause. Let teams whisper to each other.")
add_emphasis("If you see two parallel lines — same shape, just shifted — that's drift. A constant offset. The answer is sensor eleven.")

add_slide_header(43, 'A2 Step 5 — Attack B', '10:51')
add_speech("Same plot. Same logic. For Attack B.")
add_speech(
    "Look for the sensor where blue and orange diverge. This time the orange line will be completely flat — "
    "frozen at one value, while the blue line keeps evolving."
)
add_speech("That's stuck-at. Which sensor?")
add_emphasis("Sensor fourteen.")
add_speech(
    "Now think about this. Sensor fourteen was a pillar of our model in Activity 1, Step 10. "
    "Whoever attacked engine seventeen went after exactly what the model relies on the most."
)
add_emphasis("That's not a coincidence. That's how adversarial attacks work.")

add_slide_header(44, 'A2 Step 6 — Attack C', '10:54')
add_speech("Attack C is the subtlest one.")
add_speech(
    "Look at all fifteen panels. In one of them, the orange line follows the same trend as blue — but it's noticeably more jagged. "
    "More wobbly. Same average. Much higher variance. That's Gaussian noise."
)
add_speech("Which sensor?")
add_emphasis("Sensor nine.")
add_speech(
    "This one is the hardest to catch visually because the overall trend is preserved. Only the noise level changes. "
    "That's why the RandomForest missed it. The trend was right, so it kept saying 'fine.'"
)

add_slide_header(45, 'A2 Step 7 — Quantify', '10:57')
add_speech("Last step. Let's quantify what we just saw with our eyes.")
add_speech(
    "For each attack file, we compute the mean absolute difference between clean and attack for every sensor. "
    "Then we print the top three sensors that differ."
)
add_speech("After this runs, you should see:")
add_speech("Attack A — sensor eleven first, the rest zero.")
add_speech("Attack B — sensor fourteen first with a huge number, nineteen-point-eight-nine. The rest zero.")
add_speech("Attack C — sensor nine first, six-point-four-two. The rest zero.")
add_emphasis(
    "Notice that for each attack, only ONE sensor differs at all. The other fourteen are perfectly identical. "
    "Attackers don't manipulate everything. They go after one sensor and try to stay hidden. Our model caught them anyway."
)

doc.add_page_break()

# ============ BLOCK 4 - CLOSE OF ACTIVITY 2 ============
add_section_heading('Block 4 — Live Answers and Discussion', 'Running time 11:00 to 11:15')

add_slide_header(46, 'Time on Clock', '10:42 — actually start')
add_direction("This is the SLIDE that's up while teams work for 17 minutes. Start the timer here, do not skip.")
add_speech(
    "Okay, seventeen minutes on the clock starting now. Open activity-two-student-dot-ipynb on your laptop. "
    "Discuss with your team. I'm walking around. If you have questions, raise a hand."
)
add_emphasis("I'll give hints, but I won't give you the answer. Go.")

add_slide_header(47, 'Answers', '11:00')
add_speech("Okay, time's up. Here are the answers.")
add_speech("Attack A is sensor eleven. Drift.")
add_speech("Attack B is sensor fourteen. Stuck-at.")
add_speech("Attack C is sensor nine. Gaussian noise.")
add_emphasis("Show of hands — which team got all three?")
add_direction("Acknowledge the winning team by name. Lead a round of applause.")

add_slide_header(48, 'What Just Happened', '11:03')
add_speech("Here's what we just demonstrated.")
add_speech(
    "The RandomForest changed its prediction under attack, but it couldn't tell you which sensor caused the change. "
    "The Soft Decision Tree's split weights shifted in a sensor-specific way. That shift IS the explanation. "
    "It's a fingerprint of which sensor the model is leaning on."
)
add_emphasis(
    "And here's the lesson. Explainability isn't just for regulatory compliance. It's also a debugging tool. "
    "The same property that lets you defend a model to the FAA also helps your maintenance engineers find the broken hardware. "
    "That's the takeaway."
)

doc.add_page_break()

# ============ BLOCK 5 - GITHUB SPRINT ============
add_section_heading('Block 5 — GitHub Contribution Sprint', 'Running time 11:15 to 11:30 · 15 minutes')

add_slide_header(49, 'Sprint Intro', '11:15')
add_speech("Okay, last fifteen minutes. This part is different from everything else.")
add_emphasis(
    "You're going to make a real open-source contribution to a real Python library that's on PyPI. "
    "Not a workshop exercise. A real pull request that I will review and merge live, in front of you, right now. "
    "Your name on it. Forever."
)

add_slide_header(50, 'Sprint Mechanics', '11:17')
add_speech("Here's how it works. Seven steps.")
add_speech("One. Open github-dot-com slash cgrtml slash neural-trees. Go to the Issues tab.")
add_speech("Two. Filter by 'good first issue.' Pick one — they're all ten to twenty minute scope.")
add_speech("Three. Comment 'I'm taking this' so two people don't pick the same one.")
add_speech("Four. Click the Fork button — top right of the page. That gives you your own copy of the repo.")
add_speech("Five. Open the file you want to edit — in YOUR fork, not in mine.")
add_emphasis(
    "And here's the trick that saves you ten minutes: press the dot key on your keyboard. "
    "GitHub's full web editor opens, right there in the browser. You can edit like you're in VS Code."
)
add_speech("Six. Commit your change on a new branch. Then click 'Compare and pull request,' add a short description, and submit.")
add_speech("Seven. I'll review it from my laptop right here on stage. If it's correct, I merge it on the spot.")
add_emphasis(
    "No local git. No clone. No tokens. Everything in the browser. "
    "About twenty issues are waiting. Pick what fits your level."
)

add_slide_header(51, 'Why Do It', '11:20')
add_speech("Why is this worth fifteen minutes of your day? Three reasons.")
add_speech(
    "One. Your contribution shows up on your GitHub profile. That's visible to recruiters, internship coordinators, grad school admissions. "
    "It's a credential that is much harder to fake than a tutorial certificate."
)
add_speech("Two. You become part of a Python package that other people install with pip. Your code runs on their machines.")
add_speech(
    "Three. Every merged PR will be credited in the neural-trees README under a section called 'WSU Workshop Contributors.' "
    "That section will exist after today, with your names on it."
)
add_emphasis("Open the repo. Pick an issue. Go.")
add_direction("Walk to your laptop on stage. Start reviewing PRs as they come in. Merge live where possible.")

doc.add_page_break()

# ============ BLOCK 6 - WRAP UP ============
add_section_heading('Block 6 — Wrap-up and Q&A', 'Running time 11:30 to 11:45 · 15 minutes')

add_slide_header(52, 'EU AI Act', '11:30')
add_speech("Quick context for why all of this matters in the real world.")
add_speech(
    "The EU AI Act took effect in 2025. If your AI system serves any European customer, three articles apply. "
    "Article 13: transparency. Article 14: human oversight. Article 15: robustness against adversarial inputs and faults. "
    "The exact things we did today."
)
add_emphasis(
    "And the US is moving in the same direction. SR 11-7 for banking. FDA for medical devices. FAA for aviation. "
    "The era of 'just ship the LSTM' is ending. The era of 'show your work' is starting."
)

add_slide_header(53, 'Wrap-Up', '11:33')
add_speech("Three things to take with you.")
add_speech("One. In safety-critical AI, explainability is not optional. It's a regulatory requirement.")
add_speech("Two. Soft Decision Trees give you both worlds. Neural-network-level accuracy with tree-level interpretability.")
add_emphasis(
    "Three. You actually did this. Not me. Not a video. You. "
    "You trained a model, you localized a sensor fault, and many of you just shipped your first open-source contribution."
)

add_slide_header(54, 'Career Bridge', '11:36')
add_speech("Where does this work go next?")
add_speech(
    "Banks, insurers, healthcare, aerospace. Every regulated industry needs explainable AI right now."
)
add_speech(
    "My company Hezarfen builds compliance-ready AI for US mid-market banks under SR 11-7 and the EU AI Act."
)
add_emphasis(
    "If anything you saw today interests you — a thesis topic, an open-source contribution, internship questions, "
    "or just a conversation about where to go after graduation — reach out. My email and LinkedIn are on the next slide."
)

add_slide_header(55, 'Links', '11:39')
add_speech("Here are the three things worth bookmarking.")
add_speech("My GitHub — where neural-trees lives.")
add_speech("My LinkedIn — happy to connect with any of you.")
add_speech(
    "And the workshop repo on GitHub. Everything we did today is there: the data, the notebooks, the slides. "
    "Take a photo of this slide if you want."
)

add_slide_header(56, 'Thank You', '11:42')
add_speech("Thank you.")
add_speech("Special thanks to Dr. Sergey Lapin, and to Jeremy, for the invitation. Without them this wouldn't have happened.")
add_speech("I'll stay for five minutes after the official close. If you have questions, come up to the stage.")
add_emphasis("If you want to follow up later, you have my email. Have a great rest of the week.")

doc.save(OUT_PATH)
print(f"Saved: {OUT_PATH}")
