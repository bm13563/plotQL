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
    connectors = grammar.get("connectors", [])

    # Build keyword rules (case-insensitive)
    keyword_rules = []
    for kw in keywords:
        keyword_rules.append(f'    {kw.lower()}: _ => token(prec(2, /{kw}/i)),')

    func_names = "|".join(functions)

    # Build connector rules (case-insensitive)
    connector_rules = []
    connector_choices = []
    for conn in connectors:
        connector_rules.append(f'    {conn}_connector: _ => token(prec(2, /{conn}/i)),')
        connector_choices.append(f'$.{conn}_connector')

    connector_choice_str = ", ".join(connector_choices) if connector_choices else None

    # Build with_clause with source() function
    with_clause = """with_clause: $ => seq(
      $.with,
      $.source_call
    ),

    source_call: $ => seq(
      $.source,
      '(',
      $.string,
      repeat(seq(',', $.string)),
      ')'
    ),"""

    grammar_js = f'''// Auto-generated from grammar.json - DO NOT EDIT MANUALLY
// Regenerate with: python generate_grammar.py

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

    {with_clause}

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

    // Keywords (case-insensitive)
{chr(10).join(keyword_rules)}

    // Aggregate functions
    aggregate_func: _ => token(prec(2, /{func_names}/i)),

    // Connector functions
{chr(10).join(connector_rules)}

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
