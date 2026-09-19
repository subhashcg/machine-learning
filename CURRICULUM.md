# From Zero to Machine Learning

A 13-month, project-led curriculum: Python → machine learning → deployed systems.
Maths starts at zero and arrives exactly when a model needs it.

| | |
|---|---|
| **Duration** | 58 weeks |
| **Phases** | 10 |
| **Projects shipped** | 10 |
| **Pace** | 10–20 hrs/week |

---

## How this course works

**Derive → implement → compare.**
Every algorithm gets worked out on paper, written from scratch in NumPy, then
checked against scikit-learn or PyTorch. The library is where you arrive, never
where you start.

**Maths on demand, from zero.**
No prerequisite maths. Each phase carries a parallel maths lane holding exactly
what that phase's code needs — vectors before NumPy, the chain rule before backprop.

**Every phase ships.**
A phase ends when something works and is written up, not when the reading is done.
Ten artefacts, each harder than the last, become the portfolio.

**Writing is half the job.**
Every project closes with prose explaining the decisions and the limits. A model
nobody can interpret is a model nobody will trust — and the writeups are what get
read in interviews.

---

## Phase, step, topic

Three levels, and each one is a different unit of work.

| | what it is | how many | unit of work |
|---|---|---|---|
| **Phase** | a major area of the course | 10 | weeks; ends in a project |
| **Step** | a section within a phase | 39 | **one branch, one pull request** |
| **Topic** | one checklist item within a step | — | **one sitting, one commit** |

So `Phase 1 → Step 1.2 → "The dot product"` reads as: the linear algebra phase,
the from-nothing maths step, the topic you are working through today.

## How to work a step

A step is one branch. Everything for it lives in `phase-0N/step-N.M-slug/`, and
the branch stays open until every topic in the step is done.

```bash
git switch main
git switch -c step/1.2-linear-algebra-from-nothing   # the command is under each step
```

**Per topic — commit and push.** Finish a topic, tick its box, write it up in
`NOTES.md`, then commit and push to the step branch. Small commits, one per topic,
so the history shows the order you learned things in.

```bash
git add -A
git commit -m "Topic: the dot product"
git push
```

**Per step — open the pull request.** Only when every topic in the step is
finished. The PR is the step's review surface; merge it with `--no-ff` (or the
GitHub merge-commit button) so one merge bubble marks each completed step.

```bash
gh pr create --base main --title "Step 1.2 — Linear algebra, from nothing"
gh pr merge --merge --delete-branch
```

**A step is done when** every box in it is ticked, the code runs from a clean
checkout, and you could explain each topic to someone else without looking it up.
Tick the boxes in this file as you go and commit that too — the diff is your
progress log.

**What lives in a step directory**
- `README.md` — the step's topics
- `reference/NN-topic.md` — lookup cards: syntax, costs, gotchas
- `exercises/` — the code you wrote
- `NOTES.md` — your own words: what surprised you, what you got wrong first

**Steps ending in a 🔨 project** are the phase's payoff: they close the phase and
are the branch worth keeping tidy, since these are the ones other people read.

---

## Phase 0 — Python that holds up
`Weeks 1–3`

> Stop fighting the language. Everything after this assumes you can write,
> structure and test Python without thinking about it — so this is the only
> phase with no maths at all.

### Step 0.1 — The language

`git switch -c step/0.1-the-language`

- [x] **Data structures** — list, dict, set, tuple: what each costs and when to reach for it
- [x] **Comprehensions and generators** — `yield`, iterators, and why lazy evaluation matters on big data
- [x] **Functions** — `*args`/`**kwargs`, closures, scope, and the mutable-default trap
- [x] **Classes** — `__init__`, dunder methods, `@property`, `@dataclass`, inheritance and when to compose instead
- [x] **Modules and packages** — imports, `__main__`, how a project is laid out
- [x] **Exceptions** — try/except/finally, custom exceptions, failing loudly and usefully
- [ ] **Files and formats** — context managers, `pathlib`, csv, json
- [ ] **Type hints** — what they buy you and what they don't

### Step 0.2 — Working like an engineer

`git switch -c step/0.2-working-like-an-engineer`

- [ ] **pytest** — test functions, fixtures, `parametrize`, and what's worth testing
- [ ] **Debugging** — reading a traceback properly, `breakpoint()`, stepping through code
- [ ] **Environments** — `uv`, virtual environments, `pyproject.toml`, pinned dependencies
- [ ] **git** — branch, commit, diff, merge, and writing a message worth reading
- [ ] **Readable code** — naming, small functions, when a comment earns its place

### Step 0.3 — 🔨 Project: A command-line dataset inspector

`git switch -c step/0.3-project-a-command-line-dataset-inspector`

Point it at any CSV and it reports column types, missing-value counts, ranges and
a text histogram per column. No pandas — just the standard library, so you feel
exactly what pandas will do for you later.

*Ships: a tested, installable CLI tool.*

---

## Phase 1 — NumPy and the language of arrays
`Weeks 4–9`

> Learn to think in shapes instead of loops. Linear algebra is taught here from
> nothing, because a matrix multiply and a NumPy array are the same idea seen
> from two sides.

### Step 1.1 — NumPy

`git switch -c step/1.1-numpy`

- [ ] **The ndarray** — dtype, shape, ndim, and how it sits in memory
- [ ] **Creating arrays** — `arange`, `linspace`, `zeros`, `eye`, random
- [ ] **Indexing and slicing** — views versus copies, and the bug that costs everyone a day
- [ ] **Boolean masks and fancy indexing** — selecting by condition instead of by position
- [ ] **Broadcasting** — the rules, and why this is the single most important NumPy skill
- [ ] **Axis reductions** — `sum`, `mean`, `argmax` along an axis; `keepdims`
- [ ] **Reshaping** — `reshape`, `transpose`, `ravel`, `newaxis`
- [ ] **Joining and splitting** — `concatenate` versus `stack`, and what the axis argument does
- [ ] **Vectorisation** — replacing loops with ufuncs, `where`, `clip`, `select`
- [ ] **np.linalg** — `solve`, `inv`, `det`, `eig`, `svd`, `norm`
- [ ] **Random numbers** — `default_rng`, distributions, seeding and reproducibility
- [ ] **Performance** — strides, contiguity, and the cases where NumPy is genuinely slow

### Step 1.2 — 📐 Maths: Linear algebra, from nothing

`git switch -c step/1.2-linear-algebra-from-nothing`

*Everything below is taught assuming you have never seen it. Each idea is
implemented in NumPy the same day you meet it.*

- [ ] **Vectors** — what they are, addition, scaling, and what "span" means
- [ ] **The dot product** — the algebra and the geometry: projection, angle, similarity
- [ ] **Matrices as transformations** — not tables of numbers, but things that move space
- [ ] **Matrix multiplication as composition** — and why the inner dimensions must agree
- [ ] **Identity, inverse, determinant** — and when an inverse simply doesn't exist
- [ ] **Systems of equations** — Gaussian elimination by hand, then `np.linalg.solve`
- [ ] **Rank, column space, null space** — what a matrix can and cannot reach
- [ ] **Norms and distance** — L1, L2, unit vectors, and why models care
- [ ] **Eigenvectors and eigenvalues** — the directions a transformation leaves alone
- [ ] **Singular value decomposition** — the intuition; you will meet it again as PCA

### Step 1.3 — 🔨 Project: Image transforms and posterisation, from scratch

`git switch -c step/1.3-project-image-transforms-and-posterisation-from-scratch`

Load an image as an array and implement rotation, scaling and shear as matrix
multiplications you write yourself. Then implement k-means from scratch to reduce
it to eight colours. Rule: no Python loop may touch a pixel.

*Ships: a notebook proving you can think in arrays.*

---

## Phase 2 — Data that's actually messy
`Weeks 10–15`

> Real data arrives broken. This phase is about getting it into a shape a model
> can use — and being able to defend every judgement call you made along the way.

### Step 2.1 — pandas

`git switch -c step/2.1-pandas`

- [ ] **Series and DataFrame** — and why the index is the whole point
- [ ] **Reading data** — csv, parquet, json, SQL, Excel; controlling dtypes on the way in
- [ ] **Selection** — `.loc` versus `.iloc`, boolean filtering, `query`
- [ ] **dtypes** — numeric, string, categorical, datetime, and the memory they save
- [ ] **Missing data** — detection, imputation strategies, and the bias each one introduces
- [ ] **groupby** — split-apply-combine; `agg` versus `transform` versus `filter`
- [ ] **Merging** — join semantics, one-to-many blow-ups, and `validate=`
- [ ] **Reshaping** — `pivot`, `melt`, `stack`/`unstack`, long versus wide
- [ ] **Time series** — DatetimeIndex, `resample`, `rolling`, `shift`, lag features
- [ ] **apply versus vectorised** — and why `apply` is usually the wrong answer
- [ ] **Method chaining** — writing transformations someone else can follow
- [ ] **Polars** — what it is and when it's worth switching

### Step 2.2 — SQL

`git switch -c step/2.2-sql`

- [ ] **SELECT, WHERE, ORDER BY, LIMIT** — the shape of every query
- [ ] **JOINs** — inner, left, full, and why your row count just tripled
- [ ] **GROUP BY and HAVING** — aggregation, and filtering before versus after
- [ ] **Window functions** — `ROW_NUMBER`, `RANK`, `LAG`, running totals
- [ ] **CTEs and subqueries** — structuring a query so it can be read
- [ ] **Indexes and query plans** — why the query is slow and what to do about it

### Step 2.3 — 📐 Maths: Descriptive statistics

`git switch -c step/2.3-descriptive-statistics`

- [ ] **Centre** — mean, median, mode, and when the mean lies to you
- [ ] **Spread** — variance, standard deviation, IQR, range
- [ ] **Shape** — skew, kurtosis, and what a histogram is really showing
- [ ] **Outliers** — detecting them, and the harder question of whether to remove them
- [ ] **Percentiles and quantiles** — the summary that survives skewed data

### Step 2.4 — 🔨 Project: End-to-end analysis of a genuinely messy public dataset

`git switch -c step/2.4-project-end-to-end-analysis-of-a-genuinely-messy-public-dataset`

Pick something real and unclean — city open data, scraped listings, government
records. Ingest, clean, and document every decision, then write findings with
charts for a non-technical reader. This is the first piece that belongs in a portfolio.

*Ships: portfolio piece #1 — a written analysis.*

---

## Phase 3 — Seeing it and saying it
`Weeks 16–17`

> A chart is an argument. Learn to make one that changes a mind — and to
> recognise the moment a chart starts lying, including when it's yours.

### Step 3.1 — matplotlib and seaborn

`git switch -c step/3.1-matplotlib-and-seaborn`

- [ ] **The figure/axes model** — the thing everyone skips and later regrets skipping
- [ ] **Choosing the mark** — scatter, line, bar, histogram, box, violin, heatmap: when each is right
- [ ] **Multi-panel figures** — subplots, shared axes, annotation, direct labelling
- [ ] **Colour** — sequential, diverging, categorical, and why the rainbow map distorts
- [ ] **seaborn** — `displot`, `histplot`, `relplot`, `catplot`, `pairplot`
- [ ] **Plotly** — interactive charts, and when interactivity actually earns its cost
- [ ] **Accessibility** — colourblind-safe palettes, contrast, never relying on hue alone

### Step 3.2 — 📐 Maths: Distributions, visually

`git switch -c step/3.2-distributions-visually`

- [ ] **Histogram, KDE, ECDF** — three views of one distribution and what each hides
- [ ] **Binning** — how bin width manufactures patterns that aren't there
- [ ] **Truncated axes and dual axes** — the two most common ways charts mislead

### Step 3.3 — 🔨 Project: Rebuild a misleading chart

`git switch -c step/3.3-project-rebuild-a-misleading-chart`

Find a published chart that distorts its data. Reproduce it faithfully, then build
the honest version beside it, and write up precisely which choice did the
distorting. Short, sharp, and unusually memorable to a reader.

*Ships: a before/after visual essay.*

---

## Phase 4 — Probability and statistics
`Weeks 18–23`

> Learn when a result is real. This is the phase that separates someone who can
> run a model from someone who can be trusted with a decision — and it is the one
> people most often rush.

### Step 4.1 — 📐 Maths: Probability

`git switch -c step/4.1-probability`

- [ ] **Sample space and events** — the axioms, and counting properly
- [ ] **Conditional probability and independence** — the source of most wrong intuitions
- [ ] **Bayes' theorem** — the derivation, then the base-rate trap that fools doctors and juries
- [ ] **Random variables** — discrete versus continuous; PMF, PDF, CDF
- [ ] **Expectation and variance** — the two numbers that summarise a random quantity
- [ ] **Covariance and correlation** — what correlation measures and what it misses
- [ ] **The distributions worth knowing** — Bernoulli, binomial, Poisson, uniform, normal, exponential, and the process that generates each
- [ ] **Joint, marginal and conditional distributions** — reasoning about several variables at once
- [ ] **Law of large numbers and the CLT** — why the normal distribution is everywhere

### Step 4.2 — 📐 Maths: Inference

`git switch -c step/4.2-inference`

- [ ] **Sampling distributions and standard error** — the idea everything else rests on
- [ ] **Estimation** — point estimates, bias, and maximum likelihood
- [ ] **Confidence intervals** — what they mean, and the interpretation almost everyone gets wrong
- [ ] **Hypothesis testing** — null and alternative, test statistic, significance
- [ ] **What a p-value is not** — multiple comparisons, p-hacking, and the replication crisis
- [ ] **The standard tests** — t-test, chi-square, ANOVA, and the assumptions each makes
- [ ] **Bootstrap and permutation tests** — the resampling methods you'll reach for in practice
- [ ] **Effect size and statistical power** — how big a sample you actually need
- [ ] **Correlation versus causation** — confounders, Simpson's paradox, why randomisation works

### Step 4.3 — Doing it in Python

`git switch -c step/4.3-doing-it-in-python`

- [ ] **scipy.stats** — distributions, tests, fitting
- [ ] **statsmodels** — regression with the statistical output, not just predictions
- [ ] **Simulation as proof** — verifying every result above with NumPy rather than trusting the formula

### Step 4.4 — 🔨 Project: An A/B test, analysed end to end

`git switch -c step/4.4-project-an-a-b-test-analysed-end-to-end`

Design the experiment, compute the sample size the effect needs, analyse a real or
simulated result, and write the recommendation memo — including an explicit
statement of what evidence would have changed your conclusion.

*Ships: a decision memo, the format industry actually reads.*

---

## Phase 5 — Calculus and optimisation
`Weeks 24–27`

> Understand what "training a model" physically is. By the end you will have built
> the machinery that every model in the rest of this course runs on.

### Step 5.1 — 📐 Maths: Calculus, from nothing

`git switch -c step/5.1-calculus-from-nothing`

*Taught for the one purpose it serves here: knowing which way is downhill.
No integration techniques, no trigonometric identities.*

- [ ] **Functions, limits, continuity** — quickly, and only what's needed
- [ ] **The derivative** — slope, rate of change, and the geometric picture
- [ ] **The rules** — power, product, quotient
- [ ] **The chain rule** — spend real time here; backpropagation is nothing but this
- [ ] **Partial derivatives and the gradient** — the direction of steepest ascent
- [ ] **Jacobians and Hessians** — what they are, lightly; curvature and second-order methods
- [ ] **Convexity** — local versus global minima, saddle points, why deep learning still works

### Step 5.2 — Optimisation

`git switch -c step/5.2-optimisation`

- [ ] **Numerical differentiation** — finite differences, and where they break down
- [ ] **Gradient descent** — the update rule implemented by hand on a surface you can see
- [ ] **Learning rate** — too big, too small, and how to tell which you have
- [ ] **Batch, stochastic, mini-batch** — the trade-off between noise and speed
- [ ] **Momentum** — why it escapes the ravines plain descent gets stuck in
- [ ] **Visualising loss surfaces** — contour plots of the path your optimiser takes

### Step 5.3 — 🔨 Project: A tiny automatic differentiation engine

`git switch -c step/5.3-project-a-tiny-automatic-differentiation-engine`

Build a scalar `Value` class that records a computation graph and back-propagates
through it — roughly micrograd. Then fit a curve with it. You will extend this
exact engine into a neural network in Phase 7, which is when it stops feeling like
a toy.

*Ships: the engine every later phase builds on.*

---

## Phase 6 — Classical machine learning
`Weeks 28–37`

> The longest phase, and the core of the course. For every algorithm: derive the
> maths, implement it in NumPy, then match your implementation against
> scikit-learn. Nothing here stays a black box.
>
> Steps 6.1–6.4 are one repeated cycle: work out the maths, write it from scratch,
> then check it against the library and explain any difference.

### Step 6.1 — 📐 Linear models

`git switch -c step/6.1-linear-models`

- [ ] **Linear regression** — least squares, the normal equation, and the same thing by gradient descent
- [ ] **Bias–variance** — polynomial features, under- and overfitting, learning curves
- [ ] **Regularisation** — ridge, lasso, elastic net, and what each does geometrically
- [ ] **Logistic regression** — the sigmoid, log loss, and why squared error is the wrong loss here

### Step 6.2 — 📐 Trees and ensembles

`git switch -c step/6.2-trees-and-ensembles`

- [ ] **Decision trees** — entropy, Gini, information gain, pruning
- [ ] **Random forests** — bagging, feature randomness, out-of-bag error
- [ ] **Gradient boosting** — fitting residuals; then XGBoost and LightGBM in practice

### Step 6.3 — 📐 Distances, probabilities and margins

`git switch -c step/6.3-distances-probabilities-and-margins`

- [ ] **k-nearest neighbours** — and the curse of dimensionality it runs into
- [ ] **Naive Bayes** — the independence assumption and why it works anyway
- [ ] **Support vector machines** — margins, hinge loss, the kernel trick

### Step 6.4 — 📐 Unsupervised learning

`git switch -c step/6.4-unsupervised-learning`

- [ ] **Clustering** — k-means, hierarchical, DBSCAN, and how to tell if a clustering is real
- [ ] **PCA** — dimensionality reduction, and the moment the SVD from Phase 1 pays off
- [ ] **t-SNE and UMAP** — for looking at data, with a clear warning about over-reading them

### Step 6.5 — scikit-learn, done properly

`git switch -c step/6.5-scikit-learn-done-properly`

- [ ] **The estimator API** — fit/predict/transform, and why everything follows one shape
- [ ] **Pipelines and ColumnTransformer** — the structure that makes leakage hard
- [ ] **Validation** — train/validation/test, cross-validation, stratified and grouped splits
- [ ] **Data leakage** — the failure mode that quietly ruins real projects; how to spot it
- [ ] **Feature engineering** — scaling, one-hot/ordinal/target encoding, binning, interactions
- [ ] **Text as features** — bag of words and TF-IDF, the representation Step 8.2 builds on
- [ ] **Imbalanced classes** — resampling, class weights, and moving the threshold
- [ ] **Classification metrics** — where accuracy fails, precision/recall/F1, ROC-AUC versus PR-AUC
- [ ] **Calibration** — making predicted probabilities mean what they say
- [ ] **Regression metrics** — MAE, RMSE, R², and what each one punishes
- [ ] **Hyperparameter search** — grid, random, and Bayesian search with Optuna
- [ ] **Interpretation** — coefficients, permutation importance, partial dependence, SHAP
- [ ] **Baselines** — the dumb model you must beat before anything else counts

### Step 6.6 — 🔨 Project: A predictive model you can defend

`git switch -c step/6.6-project-a-predictive-model-you-can-defend`

One real problem, taken end to end: a stated baseline, a leakage-free pipeline,
honest validation, tuned but not tortured hyperparameters, and a writeup that
states plainly where the model fails and who it might fail for.

*Ships: portfolio centrepiece — the project you'll be asked about.*

---

## Phase 7 — Deep learning
`Weeks 38–47`

> Build a neural network out of the autodiff engine you wrote in Phase 5 — then
> rebuild it in PyTorch and understand exactly what the framework took over.

### Step 7.1 — From scratch first

`git switch -c step/7.1-from-scratch-first`

- [ ] **The neuron and the layer** — a weighted sum and a non-linearity, nothing more
- [ ] **The forward pass as matrix multiplication** — Phase 1 paying off again
- [ ] **Backpropagation by hand** — on your own Phase 5 engine, until it is genuinely obvious
- [ ] **Activation functions** — sigmoid, tanh, ReLU, and why ReLU won
- [ ] **Loss functions** — MSE and cross-entropy, and deriving their gradients
- [ ] **Initialisation** — why the starting weights decide whether training happens at all
- [ ] **Vanishing and exploding gradients** — seeing both happen in your own code

### Step 7.2 — The PyTorch training loop

`git switch -c step/7.2-the-pytorch-training-loop`

- [ ] **Tensors and autograd** — the same ideas as Step 7.1, with devices and speed
- [ ] **nn.Module** — and writing the training loop by hand before ever using a wrapper
- [ ] **Dataset and DataLoader** — batching, shuffling, and feeding a GPU properly
- [ ] **Optimisers** — SGD, momentum, RMSProp, Adam, AdamW: what each fixes
- [ ] **Debugging training** — overfit a single batch first; the loss curves and what they mean

### Step 7.3 — Making training converge

`git switch -c step/7.3-making-training-converge`

- [ ] **Regularisation** — dropout, weight decay, early stopping, augmentation
- [ ] **Normalisation** — batch norm and layer norm, and where each belongs
- [ ] **Learning-rate schedules** — warmup, decay, and finding a rate empirically
- [ ] **The economics** — GPUs, mixed precision, and what training actually costs

### Step 7.4 — Convolutional networks

`git switch -c step/7.4-convolutional-networks`

- [ ] **CNNs** — convolution, pooling, receptive fields, and the classic architectures
- [ ] **Transfer learning** — fine-tuning a pretrained model, and when to freeze what

### Step 7.5 — Sequences and transformers

`git switch -c step/7.5-sequences-and-transformers`

- [ ] **Sequence models** — RNN and LSTM briefly, and the limitation that motivated attention
- [ ] **Transformers** — self-attention, multi-head attention, positional encoding; build a small one
- [ ] **Embeddings** — what they are, how they're learned, why they transfer

### Step 7.6 — 🔨 Project: Two models and an honest comparison

`git switch -c step/7.6-project-two-models-and-an-honest-comparison`

Train an image classifier from scratch, then fine-tune a pretrained model on the
same task, and write up the accuracy, the compute cost and the engineering time
for each. Then train a small transformer on a text corpus you actually care about.

*Ships: portfolio piece #3 — a trained model plus a cost/benefit case.*

---

## Phase 8 — Building with foundation models
`Weeks 48–53`

> Use large language models as components in a system — and evaluate them
> properly, which is the part almost everyone skips and the part that makes the
> difference.

### Step 8.1 — The building blocks

`git switch -c step/8.1-the-building-blocks`

- [ ] **Tokenisation and context windows** — what the model actually receives
- [ ] **The Claude API** — messages, system prompts, streaming, tool use
- [ ] **Prompting as engineering** — versioned, tested, and measured, not folklore
- [ ] **Structured output** — schemas, validation, and handling the malformed case
- [ ] **Agents and tool loops** — what they add, and when a plain pipeline is the better answer

### Step 8.2 — Search and retrieval

`git switch -c step/8.2-search-and-retrieval`

*Lexical first, deliberately. Dense retrieval then arrives as the answer to a
problem you have already felt, rather than as the default everyone reaches for.*

- [ ] **Text as vectors** — bag of words, TF-IDF, and the vocabulary-mismatch problem that motivates everything else
- [ ] **BM25** — term saturation, length normalisation, and why it is still the baseline you must beat
- [ ] **Inverted indexes** — postings lists, and how lexical search stays fast at scale
- [ ] **Dense retrieval** — bi-encoders, contrastive training, and what embeddings catch that BM25 cannot
- [ ] **Approximate nearest neighbour** — HNSW, IVF, product quantisation, and the recall/latency trade
- [ ] **Learned sparse retrieval** — SPLADE, term expansion, sparse vectors with learned weights
- [ ] **Hybrid search** — reciprocal rank fusion, and when combining lexical and dense actually helps
- [ ] **Cross-encoder reranking** — why retrieval is two-stage: cheap recall, then expensive precision
- [ ] **Chunking** — the preprocessing choice that decides more than the model does
- [ ] **Evaluating retrieval** — recall@k, MRR, NDCG, and building a labelled judgement set
- [ ] **Putting it together: RAG** — retrieval as a system, and why naive RAG underperforms

### Step 8.3 — Making it trustworthy

`git switch -c step/8.3-making-it-trustworthy`

- [ ] **Building an eval set** — the discipline that turns prompting into engineering
- [ ] **LLM-as-judge** — how to use it and the biases it brings
- [ ] **Regression testing prompts** — catching the change that quietly broke everything
- [ ] **Fine-tune, retrieve, or prompt** — the actual decision tree, with costs attached
- [ ] **Cost, latency and caching** — the constraints that shape real systems
- [ ] **Failure modes** — hallucination, prompt injection, and practical mitigations

### Step 8.4 — 🔨 Project: A retrieval application with a real eval suite

`git switch -c step/8.4-project-a-retrieval-application-with-a-real-eval-suite`

Build RAG over a corpus you own and care about. Two requirements make it count:
an evaluation set that catches regressions, and a measured comparison against
both a no-retrieval baseline and a plain BM25 one. If BM25 wins, that is a
result worth reporting — and most such projects never find out.

*Ships: a working app plus the evals that prove it works.*

---

## Phase 9 — Production
`Weeks 54–58`

> Ship something other people can use and you can maintain. A model in a notebook
> has produced no value yet — this phase closes that gap.

### Step 9.1 — Shipping it

`git switch -c step/9.1-shipping-it`

- [ ] **Project structure** — config, seeds, and genuine reproducibility
- [ ] **Experiment tracking** — MLflow or Weights & Biases, and what to log
- [ ] **Versioning data and models** — so a result from March can be reproduced in October
- [ ] **Serialisation** — saving models, and the pickle security problem
- [ ] **Serving with FastAPI** — request validation, batching, sensible errors
- [ ] **Docker** — pinned dependencies and builds that behave the same everywhere
- [ ] **CI for ML** — what runs on every commit when part of the code is a model

### Step 9.2 — Keeping it alive

`git switch -c step/9.2-keeping-it-alive`

- [ ] **Testing ML code** — data tests, model tests, behavioural tests
- [ ] **Monitoring** — data drift, concept drift, and performance decay in the wild
- [ ] **Retraining strategy** — when, on what, and how you'd know it's needed
- [ ] **Cost and latency** — the constraints that decide which model actually ships
- [ ] **Fairness in practice** — subgroup metrics, bias auditing, and what to do about findings
- [ ] **Documentation** — model cards, data statements, and stating limits honestly

### Step 9.3 — 🔨 Capstone: One deployed product, end to end

`git switch -c step/9.3-capstone-one-deployed-product-end-to-end`

Data pipeline, trained model, served API, monitoring, and a README a stranger
could follow to run the whole thing. Pick a problem you'd use yourself; the ones
that get finished are the ones you care about.

*Ships: the deployed thing you point people at.*

---

## Running through every phase

**Version everything, publicly.**
Every phase is a repo on GitHub with a README a stranger could follow. Commit
small and often; the history is evidence of how you work.

**Keep a decisions log.**
One markdown file per project: what you tried, what failed, why you chose what you
chose. It is the single highest-value habit here and takes five minutes a session.

**Read one paper a fortnight.**
From Phase 6 onward. Start with the papers behind the algorithms you just
implemented — they are far more readable once you have written the code.

**Always build the dumb baseline.**
Predict the mean. Predict the majority class. Use logistic regression. If the
sophisticated model can't beat it, the sophisticated model is not the answer.

**Teach it back.**
Write a short explainer for anything that took more than an hour to understand.
If you can't explain broadcasting in a paragraph, you don't have it yet.

**Compete sparingly.**
Kaggle sharpens modelling but skips the parts that matter most — problem framing,
messy data, deployment. Treat it as drills, never as the main work.

---

## Deliberately not in this course

| Topic | When | Why it waits |
|---|---|---|
| R | Probably never | Python covers everything here. Learn R only if a specific job or a statistics-heavy field demands it. |
| Spark / big data | After Phase 9 | Distributed tooling solves a scale problem you don't have yet. A single machine handles more than most people assume. |
| Reinforcement learning | After Phase 7 | Fascinating, and rarely what a first ML job involves. Come back once supervised learning is genuinely comfortable. |
| Bayesian modelling | After Phase 4 | PyMC and hierarchical models are wonderful — and much easier once frequentist statistics and calculus are solid. |
| CUDA / C++ | Much later | Only matters if you end up writing kernels or optimising inference. PyTorch is the abstraction until then. |
| Computer vision depth | Optional, Phase 7+ | Detection, segmentation and diffusion are a specialisation. Phase 7 gives you enough to know whether you want it. |

---

Week counts assume 15 hrs/week and are a rhythm, not a deadline. Phases 4 and 6
are the ones people rush; they are also the ones that separate someone who can run
a model from someone who can be trusted with a decision. Slow down there and take
the time back in Phase 8.
