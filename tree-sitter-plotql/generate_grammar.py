#!/usr/bin/env python3
"""
Generate tree-sitter grammar.js from shared grammar.json.

NOTE: This script is deprecated. The grammar.js file is now maintained
directly as the source of truth. This script is kept for reference only.

To modify the grammar, edit grammar.js directly and run:
    cd tree-sitter-plotql && npx tree-sitter generate
"""
import json
from pathlib import Path


def to_case_insensitive(word: str) -> str:
    """Convert a word to a case-insensitive regex pattern using character classes.

    Tree-sitter doesn't support the /i flag, so we use [Aa][Bb] patterns.
    """
    return "".join(f"[{c.upper()}{c.lower()}]" for c in word)


GRAMMAR_JSON = Path(__file__).parent.parent / "plotql" / "grammar.json"
OUTPUT_FILE = Path(__file__).parent / "grammar.js"


def generate():
    print("WARNING: This script is deprecated. Edit grammar.js directly instead.")
    print("The grammar.js file is the source of truth for the tree-sitter grammar.")
    print()

    with open(GRAMMAR_JSON) as f:
        grammar = json.load(f)

    keywords = grammar["keywords"]
    functions = grammar["functions"]

    # Build keyword rules (case-insensitive using character classes)
    keyword_rules = []
    for kw in keywords:
        pattern = to_case_insensitive(kw)
        keyword_rules.append(f'    {kw.lower()}: _ => token(prec(2, /{pattern}/)),')

    # Build aggregate function pattern
    func_patterns = "|".join(to_case_insensitive(f) for f in functions)

    grammar_js = f'''// Auto-generated from grammar.json - DO NOT EDIT MANUALLY
// Regenerate with: python generate_grammar.py
//
// NOTE: This script is deprecated. Edit this file directly instead.

module.exports = grammar({{
  name: 'plotql',

  extras: _ => [/\\s+/],

  rules: {{
    query: $ => seq(
      $.with_clause,
      repeat1($.series_clause)
    ),

    series_clause: $ => seq(
      $.plot_clause,
      optional($.filter_clause),
      optional($.format_clause)
    ),

    with_clause: $ => seq(
      $.with,
      $.source_call
    ),

    source_call: $ => seq(
      $.source,
      '(',
      $.string,
      repeat(seq(',', $.string)),
      ')'
    ),

    plot_clause: $ => seq(
      $.plot,
      $.column_ref,
      $.against,
      $.column_ref,
      optional(seq($.as, $.string))
    ),

    filter_clause: $ => seq(
      $.filter,
      $.condition,
      repeat(seq(choice($.and, $.or), $.condition))
    ),

    condition: $ => seq(
      $.identifier,
      $.operator,
      choice($.string, $.number, $.identifier)
    ),

    format_clause: $ => seq(
      $.format,
      $.format_option,
      repeat(seq($.and, $.format_option))
    ),

    format_option: $ => seq($.identifier, '=', choice($.string, $.number, $.identifier, $.null)),

    column_ref: $ => choice($.identifier, $.aggregate_call),

    aggregate_call: $ => seq($.aggregate_func, '(', $.identifier, ')'),

    // Keywords (case-insensitive using character classes - tree-sitter doesn't support /i flag)
{chr(10).join(keyword_rules)}

    // Aggregate functions (case-insensitive)
    aggregate_func: _ => token(prec(2, /{func_patterns}/)),

    // Literals
    string: _ => choice(/'[^']*'/, /"[^"]*"/),
    number: _ => /-?\\d+\\.?\\d*/,
    identifier: _ => /[a-zA-Z_][a-zA-Z0-9_]*/,
    operator: _ => choice('<=', '>=', '!=', '<', '>', '='),
  }}
}});
'''

    with open(OUTPUT_FILE, "w") as f:
        f.write(grammar_js)

    print(f"Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    generate()
