# 🧠 ReasonSynth — Where intent becomes provable code.

A symbolic program synthesis assistant that transforms natural language into verified, executable code using SMT reasoning and formal proof.

## 🔍 Why
Modern LLMs produce plausible but unverifiable code. ReasonSynth ensures **deterministic correctness** by synthesizing from formal specifications, not guesses.

## ⚙️ Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

Open → [http://localhost:8501](http://localhost:8501)

## 🧠 Example

**Input:**

> Write a Python function that returns the square of a number greater than 0.

**Output:**

```python
def f(x):
    assert x > 0
    result = x**2
    assert result == x**2
    return result
```

**Proof:** ✅ Proven: specification logically consistent.

## 🌐 Deploy

**Hugging Face Spaces:** Upload this folder → select *Streamlit* → deploy.
**Azure App Service:**

```bash
az webapp up --sku B1 --name ReasonSynth --runtime "PYTHON:3.10"
```

## 🤝 Collaboration

Developed for Microsoft PROSE–style research collaboration.
Every function ReasonSynth writes **comes with a proof certificate**.

© 2025 Anurag1. Licensed under Apache 2.0.
