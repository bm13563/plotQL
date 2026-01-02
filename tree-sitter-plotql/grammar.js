// Auto-generated from grammar.json - DO NOT EDIT MANUALLY
// Regenerate with: python generate_grammar.py

module.exports = grammar({
  name: 'plotql',

  extras: _ => [/\s+/],

  rules: {
    query: $ => seq(
      $.with_clause,
      repeat1($.series_clause)
    ),

    with_clause: $ => seq($.with, $.string),

    // A series is a PLOT clause followed by optional FILTER and FORMAT
    series_clause: $ => seq(
      $.plot_clause,
      optional($.filter_clause),
      optional($.format_clause)
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

    format_option: $ => seq($.identifier, '=', choice($.string, $.number, $.identifier)),

    column_ref: $ => choice($.identifier, $.aggregate_call),

    aggregate_call: $ => seq($.aggregate_func, '(', $.identifier, ')'),

    // Keywords (case-insensitive)
    with: _ => token(prec(2, /WITH/i)),
    plot: _ => token(prec(2, /PLOT/i)),
    against: _ => token(prec(2, /AGAINST/i)),
    as: _ => token(prec(2, /AS/i)),
    filter: _ => token(prec(2, /FILTER/i)),
    and: _ => token(prec(2, /AND/i)),
    or: _ => token(prec(2, /OR/i)),
    format: _ => token(prec(2, /FORMAT/i)),
    not: _ => token(prec(2, /NOT/i)),
    null: _ => token(prec(2, /NULL/i)),

    // Aggregate functions
    aggregate_func: _ => token(prec(2, /count|sum|avg|min|max|median/i)),

    // Literals
    string: _ => choice(/'[^']*'/, /"[^"]*"/),
    number: _ => /-?\d+\.?\d*/,
    identifier: _ => /[a-zA-Z_][a-zA-Z0-9_]*/,
    operator: _ => choice('<=', '>=', '!=', '<', '>', '='),
  }
});
