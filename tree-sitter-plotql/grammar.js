// PlotQL tree-sitter grammar
// Note: Do not regenerate from generate_grammar.py - this is the source of truth

module.exports = grammar({
  name: 'plotql',

  extras: _ => [/\s+/],

  rules: {
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
    with: _ => token(prec(2, /[Ww][Ii][Tt][Hh]/)),
    source: _ => token(prec(2, /[Ss][Oo][Uu][Rr][Cc][Ee]/)),
    plot: _ => token(prec(2, /[Pp][Ll][Oo][Tt]/)),
    against: _ => token(prec(2, /[Aa][Gg][Aa][Ii][Nn][Ss][Tt]/)),
    as: _ => token(prec(2, /[Aa][Ss]/)),
    filter: _ => token(prec(2, /[Ff][Ii][Ll][Tt][Ee][Rr]/)),
    and: _ => token(prec(2, /[Aa][Nn][Dd]/)),
    or: _ => token(prec(2, /[Oo][Rr]/)),
    format: _ => token(prec(2, /[Ff][Oo][Rr][Mm][Aa][Tt]/)),
    not: _ => token(prec(2, /[Nn][Oo][Tt]/)),
    null: _ => token(prec(2, /[Nn][Uu][Ll][Ll]/)),

    // Aggregate functions (case-insensitive)
    aggregate_func: _ => token(prec(2, /[Cc][Oo][Uu][Nn][Tt]|[Ss][Uu][Mm]|[Aa][Vv][Gg]|[Mm][Ii][Nn]|[Mm][Aa][Xx]|[Mm][Ee][Dd][Ii][Aa][Nn]/)),

    // Literals
    string: _ => choice(/'[^']*'/, /"[^"]*"/),
    number: _ => /-?\d+\.?\d*/,
    identifier: _ => /[a-zA-Z_][a-zA-Z0-9_]*/,
    operator: _ => choice('<=', '>=', '!=', '<', '>', '='),
  }
});
