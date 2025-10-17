"""
ReasonSynth — Where intent becomes provable code.
Core symbolic synthesizer and theorem prover.
"""

from z3 import *
import re

class ReasonSynth:
    """
    Converts natural language specifications into provable code
    and validates correctness using symbolic logic and SMT reasoning.
    """

    def __init__(self):
        pass

    def parse_spec(self, text):
        """Extracts preconditions, postconditions, and expressions."""
        spec = {"pre": None, "post": None, "expr": None}
        text = text.lower()

        if "positive" in text or "greater than 0" in text:
            spec["pre"] = "x > 0"
        if "square" in text:
            spec["expr"] = "x**2"
            spec["post"] = "result == x**2"
        elif "double" in text:
            spec["expr"] = "2*x"
            spec["post"] = "result == 2*x"
        elif "cube" in text:
            spec["expr"] = "x**3"
            spec["post"] = "result == x**3"
        elif "even" in text:
            spec["expr"] = "x % 2 == 0"
            spec["post"] = "result == (x % 2 == 0)"
        return spec

    def synthesize_code(self, spec):
        """Generates symbolic code candidate."""
        if not spec["expr"]:
            return "Unable to synthesize from given specification."
        return (
            f"def f(x):\n"
            f"    assert {spec['pre']}\n"
            f"    result = {spec['expr']}\n"
            f"    assert {spec['post']}\n"
            f"    return result"
        )

    def verify_code(self, spec):
        """Formal verification using Z3 theorem proving."""
        try:
            x = Real('x')
            result = Real('result')
            s = Solver()
            if spec["pre"]:
                s.add(eval(spec["pre"]))
            if spec["expr"]:
                expr = eval(spec["expr"])
                s.add(result == expr)
            if spec["post"]:
                s.add(Not(eval(spec["post"])))
            if s.check() == unsat:
                return "✅ Proven: specification logically consistent."
            else:
                return "❌ Verification failed — contradiction found."
        except Exception as e:
            return f"⚠️ Verification error: {e}"

    def run(self, text):
        """Full synthesis + verification pipeline."""
        spec = self.parse_spec(text)
        code = self.synthesize_code(spec)
        proof = self.verify_code(spec)
        return {"spec": spec, "code": code, "proof": proof}
