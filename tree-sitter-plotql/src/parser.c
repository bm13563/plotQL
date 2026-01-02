#include <tree_sitter/parser.h>

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 41
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 37
#define ALIAS_COUNT 0
#define TOKEN_COUNT 24
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 6
#define PRODUCTION_ID_COUNT 1

enum {
  anon_sym_EQ = 1,
  anon_sym_LPAREN = 2,
  anon_sym_RPAREN = 3,
  sym_with = 4,
  sym_plot = 5,
  sym_against = 6,
  sym_as = 7,
  sym_filter = 8,
  sym_and = 9,
  sym_or = 10,
  sym_format = 11,
  sym_not = 12,
  sym_null = 13,
  sym_aggregate_func = 14,
  aux_sym_string_token1 = 15,
  aux_sym_string_token2 = 16,
  sym_number = 17,
  sym_identifier = 18,
  anon_sym_LT_EQ = 19,
  anon_sym_GT_EQ = 20,
  anon_sym_BANG_EQ = 21,
  anon_sym_LT = 22,
  anon_sym_GT = 23,
  sym_query = 24,
  sym_with_clause = 25,
  sym_plot_clause = 26,
  sym_filter_clause = 27,
  sym_condition = 28,
  sym_format_clause = 29,
  sym_format_option = 30,
  sym_column_ref = 31,
  sym_aggregate_call = 32,
  sym_string = 33,
  sym_operator = 34,
  aux_sym_filter_clause_repeat1 = 35,
  aux_sym_format_clause_repeat1 = 36,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [anon_sym_EQ] = "=",
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [sym_with] = "with",
  [sym_plot] = "plot",
  [sym_against] = "against",
  [sym_as] = "as",
  [sym_filter] = "filter",
  [sym_and] = "and",
  [sym_or] = "or",
  [sym_format] = "format",
  [sym_not] = "not",
  [sym_null] = "null",
  [sym_aggregate_func] = "aggregate_func",
  [aux_sym_string_token1] = "string_token1",
  [aux_sym_string_token2] = "string_token2",
  [sym_number] = "number",
  [sym_identifier] = "identifier",
  [anon_sym_LT_EQ] = "<=",
  [anon_sym_GT_EQ] = ">=",
  [anon_sym_BANG_EQ] = "!=",
  [anon_sym_LT] = "<",
  [anon_sym_GT] = ">",
  [sym_query] = "query",
  [sym_with_clause] = "with_clause",
  [sym_plot_clause] = "plot_clause",
  [sym_filter_clause] = "filter_clause",
  [sym_condition] = "condition",
  [sym_format_clause] = "format_clause",
  [sym_format_option] = "format_option",
  [sym_column_ref] = "column_ref",
  [sym_aggregate_call] = "aggregate_call",
  [sym_string] = "string",
  [sym_operator] = "operator",
  [aux_sym_filter_clause_repeat1] = "filter_clause_repeat1",
  [aux_sym_format_clause_repeat1] = "format_clause_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [anon_sym_EQ] = anon_sym_EQ,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [sym_with] = sym_with,
  [sym_plot] = sym_plot,
  [sym_against] = sym_against,
  [sym_as] = sym_as,
  [sym_filter] = sym_filter,
  [sym_and] = sym_and,
  [sym_or] = sym_or,
  [sym_format] = sym_format,
  [sym_not] = sym_not,
  [sym_null] = sym_null,
  [sym_aggregate_func] = sym_aggregate_func,
  [aux_sym_string_token1] = aux_sym_string_token1,
  [aux_sym_string_token2] = aux_sym_string_token2,
  [sym_number] = sym_number,
  [sym_identifier] = sym_identifier,
  [anon_sym_LT_EQ] = anon_sym_LT_EQ,
  [anon_sym_GT_EQ] = anon_sym_GT_EQ,
  [anon_sym_BANG_EQ] = anon_sym_BANG_EQ,
  [anon_sym_LT] = anon_sym_LT,
  [anon_sym_GT] = anon_sym_GT,
  [sym_query] = sym_query,
  [sym_with_clause] = sym_with_clause,
  [sym_plot_clause] = sym_plot_clause,
  [sym_filter_clause] = sym_filter_clause,
  [sym_condition] = sym_condition,
  [sym_format_clause] = sym_format_clause,
  [sym_format_option] = sym_format_option,
  [sym_column_ref] = sym_column_ref,
  [sym_aggregate_call] = sym_aggregate_call,
  [sym_string] = sym_string,
  [sym_operator] = sym_operator,
  [aux_sym_filter_clause_repeat1] = aux_sym_filter_clause_repeat1,
  [aux_sym_format_clause_repeat1] = aux_sym_format_clause_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [anon_sym_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RPAREN] = {
    .visible = true,
    .named = false,
  },
  [sym_with] = {
    .visible = true,
    .named = true,
  },
  [sym_plot] = {
    .visible = true,
    .named = true,
  },
  [sym_against] = {
    .visible = true,
    .named = true,
  },
  [sym_as] = {
    .visible = true,
    .named = true,
  },
  [sym_filter] = {
    .visible = true,
    .named = true,
  },
  [sym_and] = {
    .visible = true,
    .named = true,
  },
  [sym_or] = {
    .visible = true,
    .named = true,
  },
  [sym_format] = {
    .visible = true,
    .named = true,
  },
  [sym_not] = {
    .visible = true,
    .named = true,
  },
  [sym_null] = {
    .visible = true,
    .named = true,
  },
  [sym_aggregate_func] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_string_token1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_string_token2] = {
    .visible = false,
    .named = false,
  },
  [sym_number] = {
    .visible = true,
    .named = true,
  },
  [sym_identifier] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_LT_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GT_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_BANG_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GT] = {
    .visible = true,
    .named = false,
  },
  [sym_query] = {
    .visible = true,
    .named = true,
  },
  [sym_with_clause] = {
    .visible = true,
    .named = true,
  },
  [sym_plot_clause] = {
    .visible = true,
    .named = true,
  },
  [sym_filter_clause] = {
    .visible = true,
    .named = true,
  },
  [sym_condition] = {
    .visible = true,
    .named = true,
  },
  [sym_format_clause] = {
    .visible = true,
    .named = true,
  },
  [sym_format_option] = {
    .visible = true,
    .named = true,
  },
  [sym_column_ref] = {
    .visible = true,
    .named = true,
  },
  [sym_aggregate_call] = {
    .visible = true,
    .named = true,
  },
  [sym_string] = {
    .visible = true,
    .named = true,
  },
  [sym_operator] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_filter_clause_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_format_clause_repeat1] = {
    .visible = false,
    .named = false,
  },
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static const uint16_t ts_non_terminal_alias_map[] = {
  0,
};

static const TSStateId ts_primary_state_ids[STATE_COUNT] = {
  [0] = 0,
  [1] = 1,
  [2] = 2,
  [3] = 3,
  [4] = 4,
  [5] = 5,
  [6] = 6,
  [7] = 7,
  [8] = 8,
  [9] = 9,
  [10] = 10,
  [11] = 11,
  [12] = 12,
  [13] = 13,
  [14] = 14,
  [15] = 15,
  [16] = 16,
  [17] = 17,
  [18] = 18,
  [19] = 19,
  [20] = 20,
  [21] = 21,
  [22] = 22,
  [23] = 23,
  [24] = 24,
  [25] = 25,
  [26] = 26,
  [27] = 27,
  [28] = 28,
  [29] = 29,
  [30] = 30,
  [31] = 31,
  [32] = 32,
  [33] = 33,
  [34] = 34,
  [35] = 35,
  [36] = 36,
  [37] = 37,
  [38] = 38,
  [39] = 39,
  [40] = 40,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(31);
      if (lookahead == '!') ADVANCE(4);
      if (lookahead == '"') ADVANCE(2);
      if (lookahead == '\'') ADVANCE(3);
      if (lookahead == '(') ADVANCE(33);
      if (lookahead == ')') ADVANCE(34);
      if (lookahead == '-') ADVANCE(29);
      if (lookahead == '<') ADVANCE(95);
      if (lookahead == '=') ADVANCE(32);
      if (lookahead == '>') ADVANCE(96);
      if (lookahead == 'A') ADVANCE(54);
      if (lookahead == 'F') ADVANCE(57);
      if (lookahead == 'N') ADVANCE(65);
      if (lookahead == 'O') ADVANCE(67);
      if (lookahead == 'P') ADVANCE(59);
      if (lookahead == 'W') ADVANCE(58);
      if (lookahead == 'a') ADVANCE(89);
      if (lookahead == 'c') ADVANCE(85);
      if (lookahead == 'm') ADVANCE(77);
      if (lookahead == 's') ADVANCE(87);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(0)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(48);
      if (('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 1:
      if (lookahead == '"') ADVANCE(2);
      if (lookahead == '\'') ADVANCE(3);
      if (lookahead == '-') ADVANCE(29);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(1)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(48);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 2:
      if (lookahead == '"') ADVANCE(47);
      if (lookahead != 0) ADVANCE(2);
      END_STATE();
    case 3:
      if (lookahead == '\'') ADVANCE(46);
      if (lookahead != 0) ADVANCE(3);
      END_STATE();
    case 4:
      if (lookahead == '=') ADVANCE(94);
      END_STATE();
    case 5:
      if (lookahead == 'A') ADVANCE(12);
      END_STATE();
    case 6:
      if (lookahead == 'A') ADVANCE(24);
      END_STATE();
    case 7:
      if (lookahead == 'D') ADVANCE(40);
      END_STATE();
    case 8:
      if (lookahead == 'E') ADVANCE(20);
      END_STATE();
    case 9:
      if (lookahead == 'G') ADVANCE(5);
      if (lookahead == 'N') ADVANCE(7);
      if (lookahead == 'S') ADVANCE(38);
      END_STATE();
    case 10:
      if (lookahead == 'H') ADVANCE(35);
      END_STATE();
    case 11:
      if (lookahead == 'I') ADVANCE(26);
      END_STATE();
    case 12:
      if (lookahead == 'I') ADVANCE(17);
      END_STATE();
    case 13:
      if (lookahead == 'I') ADVANCE(15);
      if (lookahead == 'O') ADVANCE(21);
      END_STATE();
    case 14:
      if (lookahead == 'L') ADVANCE(18);
      END_STATE();
    case 15:
      if (lookahead == 'L') ADVANCE(27);
      END_STATE();
    case 16:
      if (lookahead == 'M') ADVANCE(6);
      END_STATE();
    case 17:
      if (lookahead == 'N') ADVANCE(22);
      END_STATE();
    case 18:
      if (lookahead == 'O') ADVANCE(23);
      END_STATE();
    case 19:
      if (lookahead == 'R') ADVANCE(41);
      END_STATE();
    case 20:
      if (lookahead == 'R') ADVANCE(39);
      END_STATE();
    case 21:
      if (lookahead == 'R') ADVANCE(16);
      END_STATE();
    case 22:
      if (lookahead == 'S') ADVANCE(25);
      END_STATE();
    case 23:
      if (lookahead == 'T') ADVANCE(36);
      END_STATE();
    case 24:
      if (lookahead == 'T') ADVANCE(42);
      END_STATE();
    case 25:
      if (lookahead == 'T') ADVANCE(37);
      END_STATE();
    case 26:
      if (lookahead == 'T') ADVANCE(10);
      END_STATE();
    case 27:
      if (lookahead == 'T') ADVANCE(8);
      END_STATE();
    case 28:
      if (lookahead == 'a') ADVANCE(89);
      if (lookahead == 'c') ADVANCE(85);
      if (lookahead == 'm') ADVANCE(77);
      if (lookahead == 's') ADVANCE(87);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(28)
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 29:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(48);
      END_STATE();
    case 30:
      if (eof) ADVANCE(31);
      if (lookahead == 'A') ADVANCE(9);
      if (lookahead == 'F') ADVANCE(13);
      if (lookahead == 'O') ADVANCE(19);
      if (lookahead == 'P') ADVANCE(14);
      if (lookahead == 'W') ADVANCE(11);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(30)
      END_STATE();
    case 31:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 32:
      ACCEPT_TOKEN(anon_sym_EQ);
      END_STATE();
    case 33:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 34:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 35:
      ACCEPT_TOKEN(sym_with);
      END_STATE();
    case 36:
      ACCEPT_TOKEN(sym_plot);
      END_STATE();
    case 37:
      ACCEPT_TOKEN(sym_against);
      END_STATE();
    case 38:
      ACCEPT_TOKEN(sym_as);
      END_STATE();
    case 39:
      ACCEPT_TOKEN(sym_filter);
      END_STATE();
    case 40:
      ACCEPT_TOKEN(sym_and);
      END_STATE();
    case 41:
      ACCEPT_TOKEN(sym_or);
      END_STATE();
    case 42:
      ACCEPT_TOKEN(sym_format);
      END_STATE();
    case 43:
      ACCEPT_TOKEN(sym_not);
      END_STATE();
    case 44:
      ACCEPT_TOKEN(sym_null);
      END_STATE();
    case 45:
      ACCEPT_TOKEN(sym_aggregate_func);
      END_STATE();
    case 46:
      ACCEPT_TOKEN(aux_sym_string_token1);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(aux_sym_string_token2);
      END_STATE();
    case 48:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(49);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(48);
      END_STATE();
    case 49:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(49);
      END_STATE();
    case 50:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'A') ADVANCE(56);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'A') ADVANCE(75);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'D') ADVANCE(40);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'E') ADVANCE(69);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 54:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'G') ADVANCE(50);
      if (lookahead == 'N') ADVANCE(52);
      if (lookahead == 'S') ADVANCE(38);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 55:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'H') ADVANCE(35);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I') ADVANCE(64);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I') ADVANCE(61);
      if (lookahead == 'O') ADVANCE(68);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 58:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I') ADVANCE(72);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 59:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(66);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 60:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(44);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 61:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(73);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 62:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(60);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 63:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'M') ADVANCE(51);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 64:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'N') ADVANCE(70);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 65:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O') ADVANCE(71);
      if (lookahead == 'U') ADVANCE(62);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 66:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O') ADVANCE(74);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 67:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R') ADVANCE(41);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 68:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R') ADVANCE(63);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 69:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R') ADVANCE(39);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 70:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'S') ADVANCE(76);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 71:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(43);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 72:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(55);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 73:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(53);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 74:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(36);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 75:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(42);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 76:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(37);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 77:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'a') ADVANCE(90);
      if (lookahead == 'e') ADVANCE(79);
      if (lookahead == 'i') ADVANCE(83);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 78:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'a') ADVANCE(83);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 79:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'd') ADVANCE(81);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 80:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'g') ADVANCE(45);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 81:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'i') ADVANCE(78);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 82:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'm') ADVANCE(45);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 83:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(45);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 84:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(86);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 85:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(88);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 86:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(45);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 87:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'u') ADVANCE(82);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 88:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'u') ADVANCE(84);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 89:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'v') ADVANCE(80);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 90:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'x') ADVANCE(45);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 91:
      ACCEPT_TOKEN(sym_identifier);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(91);
      END_STATE();
    case 92:
      ACCEPT_TOKEN(anon_sym_LT_EQ);
      END_STATE();
    case 93:
      ACCEPT_TOKEN(anon_sym_GT_EQ);
      END_STATE();
    case 94:
      ACCEPT_TOKEN(anon_sym_BANG_EQ);
      END_STATE();
    case 95:
      ACCEPT_TOKEN(anon_sym_LT);
      if (lookahead == '=') ADVANCE(92);
      END_STATE();
    case 96:
      ACCEPT_TOKEN(anon_sym_GT);
      if (lookahead == '=') ADVANCE(93);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 30},
  [2] = {.lex_state = 0},
  [3] = {.lex_state = 30},
  [4] = {.lex_state = 30},
  [5] = {.lex_state = 30},
  [6] = {.lex_state = 30},
  [7] = {.lex_state = 30},
  [8] = {.lex_state = 30},
  [9] = {.lex_state = 30},
  [10] = {.lex_state = 1},
  [11] = {.lex_state = 1},
  [12] = {.lex_state = 28},
  [13] = {.lex_state = 30},
  [14] = {.lex_state = 30},
  [15] = {.lex_state = 28},
  [16] = {.lex_state = 30},
  [17] = {.lex_state = 1},
  [18] = {.lex_state = 30},
  [19] = {.lex_state = 0},
  [20] = {.lex_state = 30},
  [21] = {.lex_state = 30},
  [22] = {.lex_state = 0},
  [23] = {.lex_state = 30},
  [24] = {.lex_state = 30},
  [25] = {.lex_state = 1},
  [26] = {.lex_state = 1},
  [27] = {.lex_state = 1},
  [28] = {.lex_state = 1},
  [29] = {.lex_state = 30},
  [30] = {.lex_state = 30},
  [31] = {.lex_state = 30},
  [32] = {.lex_state = 0},
  [33] = {.lex_state = 0},
  [34] = {.lex_state = 0},
  [35] = {.lex_state = 0},
  [36] = {.lex_state = 1},
  [37] = {.lex_state = 0},
  [38] = {.lex_state = 30},
  [39] = {.lex_state = 0},
  [40] = {.lex_state = 30},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [anon_sym_EQ] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [sym_with] = ACTIONS(1),
    [sym_plot] = ACTIONS(1),
    [sym_against] = ACTIONS(1),
    [sym_as] = ACTIONS(1),
    [sym_filter] = ACTIONS(1),
    [sym_and] = ACTIONS(1),
    [sym_or] = ACTIONS(1),
    [sym_format] = ACTIONS(1),
    [sym_not] = ACTIONS(1),
    [sym_null] = ACTIONS(1),
    [sym_aggregate_func] = ACTIONS(1),
    [aux_sym_string_token1] = ACTIONS(1),
    [aux_sym_string_token2] = ACTIONS(1),
    [sym_number] = ACTIONS(1),
    [sym_identifier] = ACTIONS(1),
    [anon_sym_LT_EQ] = ACTIONS(1),
    [anon_sym_GT_EQ] = ACTIONS(1),
    [anon_sym_BANG_EQ] = ACTIONS(1),
    [anon_sym_LT] = ACTIONS(1),
    [anon_sym_GT] = ACTIONS(1),
  },
  [1] = {
    [sym_query] = STATE(34),
    [sym_with_clause] = STATE(31),
    [sym_with] = ACTIONS(3),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 3,
    STATE(11), 1,
      sym_operator,
    ACTIONS(7), 2,
      anon_sym_LT,
      anon_sym_GT,
    ACTIONS(5), 4,
      anon_sym_EQ,
      anon_sym_LT_EQ,
      anon_sym_GT_EQ,
      anon_sym_BANG_EQ,
  [14] = 1,
    ACTIONS(9), 6,
      ts_builtin_sym_end,
      sym_plot,
      sym_filter,
      sym_and,
      sym_or,
      sym_format,
  [23] = 3,
    STATE(4), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(11), 2,
      ts_builtin_sym_end,
      sym_format,
    ACTIONS(13), 2,
      sym_and,
      sym_or,
  [35] = 3,
    STATE(4), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(16), 2,
      ts_builtin_sym_end,
      sym_format,
    ACTIONS(18), 2,
      sym_and,
      sym_or,
  [47] = 5,
    ACTIONS(20), 1,
      ts_builtin_sym_end,
    ACTIONS(22), 1,
      sym_filter,
    ACTIONS(24), 1,
      sym_format,
    STATE(20), 1,
      sym_filter_clause,
    STATE(37), 1,
      sym_format_clause,
  [63] = 1,
    ACTIONS(26), 5,
      ts_builtin_sym_end,
      sym_against,
      sym_as,
      sym_filter,
      sym_format,
  [71] = 1,
    ACTIONS(28), 5,
      ts_builtin_sym_end,
      sym_against,
      sym_as,
      sym_filter,
      sym_format,
  [79] = 3,
    STATE(5), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(18), 2,
      sym_and,
      sym_or,
    ACTIONS(30), 2,
      ts_builtin_sym_end,
      sym_format,
  [91] = 3,
    STATE(29), 1,
      sym_string,
    ACTIONS(32), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
    ACTIONS(34), 2,
      sym_number,
      sym_identifier,
  [103] = 3,
    STATE(14), 1,
      sym_string,
    ACTIONS(32), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
    ACTIONS(36), 2,
      sym_number,
      sym_identifier,
  [115] = 4,
    ACTIONS(38), 1,
      sym_aggregate_func,
    ACTIONS(40), 1,
      sym_identifier,
    STATE(7), 1,
      sym_aggregate_call,
    STATE(38), 1,
      sym_column_ref,
  [128] = 1,
    ACTIONS(11), 4,
      ts_builtin_sym_end,
      sym_and,
      sym_or,
      sym_format,
  [135] = 1,
    ACTIONS(42), 4,
      ts_builtin_sym_end,
      sym_and,
      sym_or,
      sym_format,
  [142] = 4,
    ACTIONS(38), 1,
      sym_aggregate_func,
    ACTIONS(40), 1,
      sym_identifier,
    STATE(7), 1,
      sym_aggregate_call,
    STATE(16), 1,
      sym_column_ref,
  [155] = 2,
    ACTIONS(46), 1,
      sym_as,
    ACTIONS(44), 3,
      ts_builtin_sym_end,
      sym_filter,
      sym_format,
  [164] = 1,
    ACTIONS(48), 4,
      aux_sym_string_token1,
      aux_sym_string_token2,
      sym_number,
      sym_identifier,
  [171] = 3,
    ACTIONS(50), 1,
      ts_builtin_sym_end,
    ACTIONS(52), 1,
      sym_and,
    STATE(18), 1,
      aux_sym_format_clause_repeat1,
  [181] = 2,
    STATE(23), 1,
      sym_string,
    ACTIONS(32), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
  [189] = 3,
    ACTIONS(24), 1,
      sym_format,
    ACTIONS(55), 1,
      ts_builtin_sym_end,
    STATE(32), 1,
      sym_format_clause,
  [199] = 3,
    ACTIONS(57), 1,
      ts_builtin_sym_end,
    ACTIONS(59), 1,
      sym_and,
    STATE(18), 1,
      aux_sym_format_clause_repeat1,
  [209] = 2,
    STATE(40), 1,
      sym_string,
    ACTIONS(32), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
  [217] = 1,
    ACTIONS(61), 3,
      ts_builtin_sym_end,
      sym_filter,
      sym_format,
  [223] = 3,
    ACTIONS(59), 1,
      sym_and,
    ACTIONS(63), 1,
      ts_builtin_sym_end,
    STATE(21), 1,
      aux_sym_format_clause_repeat1,
  [233] = 2,
    ACTIONS(65), 1,
      sym_identifier,
    STATE(30), 1,
      sym_format_option,
  [240] = 2,
    ACTIONS(67), 1,
      sym_identifier,
    STATE(13), 1,
      sym_condition,
  [247] = 2,
    ACTIONS(65), 1,
      sym_identifier,
    STATE(24), 1,
      sym_format_option,
  [254] = 2,
    ACTIONS(67), 1,
      sym_identifier,
    STATE(9), 1,
      sym_condition,
  [261] = 1,
    ACTIONS(69), 2,
      ts_builtin_sym_end,
      sym_and,
  [266] = 1,
    ACTIONS(50), 2,
      ts_builtin_sym_end,
      sym_and,
  [271] = 2,
    ACTIONS(71), 1,
      sym_plot,
    STATE(6), 1,
      sym_plot_clause,
  [278] = 1,
    ACTIONS(73), 1,
      ts_builtin_sym_end,
  [282] = 1,
    ACTIONS(75), 1,
      anon_sym_RPAREN,
  [286] = 1,
    ACTIONS(77), 1,
      ts_builtin_sym_end,
  [290] = 1,
    ACTIONS(79), 1,
      anon_sym_EQ,
  [294] = 1,
    ACTIONS(81), 1,
      sym_identifier,
  [298] = 1,
    ACTIONS(55), 1,
      ts_builtin_sym_end,
  [302] = 1,
    ACTIONS(83), 1,
      sym_against,
  [306] = 1,
    ACTIONS(85), 1,
      anon_sym_LPAREN,
  [310] = 1,
    ACTIONS(87), 1,
      sym_plot,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 14,
  [SMALL_STATE(4)] = 23,
  [SMALL_STATE(5)] = 35,
  [SMALL_STATE(6)] = 47,
  [SMALL_STATE(7)] = 63,
  [SMALL_STATE(8)] = 71,
  [SMALL_STATE(9)] = 79,
  [SMALL_STATE(10)] = 91,
  [SMALL_STATE(11)] = 103,
  [SMALL_STATE(12)] = 115,
  [SMALL_STATE(13)] = 128,
  [SMALL_STATE(14)] = 135,
  [SMALL_STATE(15)] = 142,
  [SMALL_STATE(16)] = 155,
  [SMALL_STATE(17)] = 164,
  [SMALL_STATE(18)] = 171,
  [SMALL_STATE(19)] = 181,
  [SMALL_STATE(20)] = 189,
  [SMALL_STATE(21)] = 199,
  [SMALL_STATE(22)] = 209,
  [SMALL_STATE(23)] = 217,
  [SMALL_STATE(24)] = 223,
  [SMALL_STATE(25)] = 233,
  [SMALL_STATE(26)] = 240,
  [SMALL_STATE(27)] = 247,
  [SMALL_STATE(28)] = 254,
  [SMALL_STATE(29)] = 261,
  [SMALL_STATE(30)] = 266,
  [SMALL_STATE(31)] = 271,
  [SMALL_STATE(32)] = 278,
  [SMALL_STATE(33)] = 282,
  [SMALL_STATE(34)] = 286,
  [SMALL_STATE(35)] = 290,
  [SMALL_STATE(36)] = 294,
  [SMALL_STATE(37)] = 298,
  [SMALL_STATE(38)] = 302,
  [SMALL_STATE(39)] = 306,
  [SMALL_STATE(40)] = 310,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT(22),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [7] = {.entry = {.count = 1, .reusable = false}}, SHIFT(17),
  [9] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_string, 1),
  [11] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_filter_clause_repeat1, 2),
  [13] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_filter_clause_repeat1, 2), SHIFT_REPEAT(26),
  [16] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_filter_clause, 3),
  [18] = {.entry = {.count = 1, .reusable = true}}, SHIFT(26),
  [20] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_query, 2),
  [22] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [24] = {.entry = {.count = 1, .reusable = true}}, SHIFT(27),
  [26] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_column_ref, 1),
  [28] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_aggregate_call, 4),
  [30] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_filter_clause, 2),
  [32] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [34] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [36] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [38] = {.entry = {.count = 1, .reusable = true}}, SHIFT(39),
  [40] = {.entry = {.count = 1, .reusable = false}}, SHIFT(7),
  [42] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_condition, 3),
  [44] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_plot_clause, 4),
  [46] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [48] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_operator, 1),
  [50] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_format_clause_repeat1, 2),
  [52] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_format_clause_repeat1, 2), SHIFT_REPEAT(25),
  [55] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_query, 3),
  [57] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_clause, 3),
  [59] = {.entry = {.count = 1, .reusable = true}}, SHIFT(25),
  [61] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_plot_clause, 6),
  [63] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_clause, 2),
  [65] = {.entry = {.count = 1, .reusable = true}}, SHIFT(35),
  [67] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [69] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_option, 3),
  [71] = {.entry = {.count = 1, .reusable = true}}, SHIFT(12),
  [73] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_query, 4),
  [75] = {.entry = {.count = 1, .reusable = true}}, SHIFT(8),
  [77] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [79] = {.entry = {.count = 1, .reusable = true}}, SHIFT(10),
  [81] = {.entry = {.count = 1, .reusable = true}}, SHIFT(33),
  [83] = {.entry = {.count = 1, .reusable = true}}, SHIFT(15),
  [85] = {.entry = {.count = 1, .reusable = true}}, SHIFT(36),
  [87] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_with_clause, 2),
};

#ifdef __cplusplus
extern "C" {
#endif
#ifdef _WIN32
#define extern __declspec(dllexport)
#endif

extern const TSLanguage *tree_sitter_plotql(void) {
  static const TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .state_count = STATE_COUNT,
    .large_state_count = LARGE_STATE_COUNT,
    .production_id_count = PRODUCTION_ID_COUNT,
    .field_count = FIELD_COUNT,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .parse_table = &ts_parse_table[0][0],
    .small_parse_table = ts_small_parse_table,
    .small_parse_table_map = ts_small_parse_table_map,
    .parse_actions = ts_parse_actions,
    .symbol_names = ts_symbol_names,
    .symbol_metadata = ts_symbol_metadata,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .alias_sequences = &ts_alias_sequences[0][0],
    .lex_modes = ts_lex_modes,
    .lex_fn = ts_lex,
    .primary_state_ids = ts_primary_state_ids,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
