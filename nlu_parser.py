"""
ReasonSynth — Where intent becomes provable code.
Natural language parser (grammar-based intent extraction).
"""

from lark import Lark, Transformer

grammar = r"""
start: instruction
instruction: "write" "a" "function" "that" action condition?
action: /[a-zA-Z0-9 ]+/
condition: /(if|when|where|for) [a-zA-Z0-9 <> =]+/
%ignore " "
"""

class SpecTransformer(Transformer):
    def start(self, items): return items
