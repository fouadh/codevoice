# Introduction

This project explores a Git repository’s history by building a **bipartite graph of authors and files**, using Python libraries like `pandas`, `networkx`, and `matplotlib`.

The goal is to visualize **who modifies what, and how often**, and to gain insights into the collaborative structure of the codebase.

# Requirements

- Python **≥ 3.10**
- [uv](https://github.com/astral-sh/uv) — a fast Python package manager compatible with `pyproject.toml`

To install `uv` (if you don’t have it yet):

```bash
curl -Ls https://astral.sh/uv/install.sh | bash
```

or via pipx:

```bash
pipx install uv
```

# Installation

```bash
git clone https://github.com/fouadh/codevoice.git
cd code-analysis
uv venv
source .venv/bin/activate
uv pip install --requirements pyproject.toml
```

# Running the Notebook

```bash
uv pip install notebook
uv run --with jupyter jupyter notebook
```

Then, select the notebook you are interested in.

## Available notebooks

- L'envers du décode ([related blog article](todo))