# 🧱 ReasonSynth Architecture

## Overview
A hybrid symbolic reasoning system combining natural language parsing, program synthesis, and formal verification.

## Flow
```

User Input (NL)
↓
Spec Parser (Lark)
↓
ReasonSynth Core
├─ Spec Extractor
├─ Synthesizer
├─ Z3 Proof Engine
↓
Outputs → Code + Proof + Explanation

```

## Components
| Module | Role |
|--------|------|
| `app.py` | User interface |
| `synthesizer.py` | Symbolic synthesis and proof |
| `nlu_parser.py` | Grammar-based parsing |
| `Z3` | SMT theorem prover |
| `SymPy` | Symbolic algebra simplifier |

ReasonSynth proves that **AI can be deterministic, explainable, and correct.**
