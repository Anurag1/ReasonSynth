# ReasonSynth — Where intent becomes provable code.

## 1️⃣ Problem
AI code generation lacks provable correctness.  
LLMs produce plausible syntax but not logical guarantees.

## 2️⃣ Solution
ReasonSynth converts natural language into **symbolically proven programs**, enforcing correctness with Z3 before execution.

## 3️⃣ Technology
- Symbolic math (SymPy)
- Theorem proving (Z3)
- Grammar parsing (Lark)
- Web UI (Streamlit)

## 4️⃣ Example
**Input:** Write a function that doubles a number greater than 0  
**Output:** ✅ Verified function  
`f(x): return 2*x`

## 5️⃣ Vision
A unified framework for **intent-driven verified synthesis** — perfect for integration into **Microsoft PROSE** or **Copilot validation layers**.

## 6️⃣ Collaboration Ask
Pilot ReasonSynth inside Microsoft Research to develop:
- *NL → Spec → Verified Code* pipelines
- *Hybrid symbolic + neural synthesis modules*
