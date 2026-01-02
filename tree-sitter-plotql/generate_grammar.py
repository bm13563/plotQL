#!/usr/bin/env python3
"""Generate tree-sitter grammar.js from shared grammar.json."""
import json
from pathlib import Path

GRAMMAR_JSON = Path(__file__).parent.parent / "plotql" / "grammar.json"
OUTPUT_FILE = Path(__file__).parent / "grammar.js"


def generate():
    with open(GRAMMAR_JSON) as f:
        grammar = json.load(f)

    keywords = grammar["keywords"]
    functions = grammar["functions"]

    # Build keyword rules (case-insensitive)
    keyword_rules = []
    for kw in keywords:
        keyword_rules.append(f'    {kw.lower()}: _ => token(prec(2, /{kw}/i)),')

    func_names = "|".join(functions)

    grammar_js = f'''// Auto-generated from grammar.json - DO NOT EDIT MANUALLY
// Regenerate with: python generate_grammar.py

module.exports = grammar({{
  name: 'plotql',

  extras: _ => [/\\s+/],

  rules: {{
    query: $ => seq(
      $.with_clause,
      $.plot_clause,
      optional($.filter_clause),
      optional($.format_clause)
    ),

    with_clause: $ => seq($.with, $.string),

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

    format_option: $ => seq($.identifier, '=', choice($.string, $.number, $.identifier)),

    column_ref: $ => choice($.identifier, $.aggregate_call),

    aggregate_call: $ => seq($.aggregate_func, '(', $.identifier, ')'),

    // Keywords (case-insensitive)
{chr(10).join(keyword_rules)}

    // Aggregate functions
    aggregate_func: _ => token(prec(2, /{func_names}/i)),

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
