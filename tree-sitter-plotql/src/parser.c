#include <tree_sitter/parser.h>

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 53
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 42
#define ALIAS_COUNT 0
#define TOKEN_COUNT 26
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 6
#define PRODUCTION_ID_COUNT 1

enum {
  anon_sym_ = 1,
  anon_sym_LPAREN = 2,
  anon_sym_RPAREN = 3,
  anon_sym_EQ = 4,
  sym_with = 5,
  sym_source = 6,
  sym_plot = 7,
  sym_against = 8,
  sym_as = 9,
  sym_filter = 10,
  sym_and = 11,
  sym_or = 12,
  sym_format = 13,
  sym_not = 14,
  sym_null = 15,
  sym_aggregate_func = 16,
  aux_sym_string_token1 = 17,
  aux_sym_string_token2 = 18,
  sym_number = 19,
  sym_identifier = 20,
  anon_sym_LT_EQ = 21,
  anon_sym_GT_EQ = 22,
  anon_sym_BANG_EQ = 23,
  anon_sym_LT = 24,
  anon_sym_GT = 25,
  sym_query = 26,
  sym_series_clause = 27,
  sym_with_clause = 28,
  sym_connector_call = 29,
  sym_plot_clause = 30,
  sym_filter_clause = 31,
  sym_condition = 32,
  sym_format_clause = 33,
  sym_format_option = 34,
  sym_column_ref = 35,
  sym_aggregate_call = 36,
  sym_string = 37,
  sym_operator = 38,
  aux_sym_query_repeat1 = 39,
  aux_sym_filter_clause_repeat1 = 40,
  aux_sym_format_clause_repeat1 = 41,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [anon_sym_] = "",
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [anon_sym_EQ] = "=",
  [sym_with] = "with",
  [sym_source] = "source",
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
  [sym_series_clause] = "series_clause",
  [sym_with_clause] = "with_clause",
  [sym_connector_call] = "connector_call",
  [sym_plot_clause] = "plot_clause",
  [sym_filter_clause] = "filter_clause",
  [sym_condition] = "condition",
  [sym_format_clause] = "format_clause",
  [sym_format_option] = "format_option",
  [sym_column_ref] = "column_ref",
  [sym_aggregate_call] = "aggregate_call",
  [sym_string] = "string",
  [sym_operator] = "operator",
  [aux_sym_query_repeat1] = "query_repeat1",
  [aux_sym_filter_clause_repeat1] = "filter_clause_repeat1",
  [aux_sym_format_clause_repeat1] = "format_clause_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [anon_sym_] = anon_sym_,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [anon_sym_EQ] = anon_sym_EQ,
  [sym_with] = sym_with,
  [sym_source] = sym_source,
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
  [sym_series_clause] = sym_series_clause,
  [sym_with_clause] = sym_with_clause,
  [sym_connector_call] = sym_connector_call,
  [sym_plot_clause] = sym_plot_clause,
  [sym_filter_clause] = sym_filter_clause,
  [sym_condition] = sym_condition,
  [sym_format_clause] = sym_format_clause,
  [sym_format_option] = sym_format_option,
  [sym_column_ref] = sym_column_ref,
  [sym_aggregate_call] = sym_aggregate_call,
  [sym_string] = sym_string,
  [sym_operator] = sym_operator,
  [aux_sym_query_repeat1] = aux_sym_query_repeat1,
  [aux_sym_filter_clause_repeat1] = aux_sym_filter_clause_repeat1,
  [aux_sym_format_clause_repeat1] = aux_sym_format_clause_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [anon_sym_] = {
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
  [anon_sym_EQ] = {
    .visible = true,
    .named = false,
  },
  [sym_with] = {
    .visible = true,
    .named = true,
  },
  [sym_source] = {
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
  [sym_series_clause] = {
    .visible = true,
    .named = true,
  },
  [sym_with_clause] = {
    .visible = true,
    .named = true,
  },
  [sym_connector_call] = {
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
  [aux_sym_query_repeat1] = {
    .visible = false,
    .named = false,
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
  [38] = 16,
  [39] = 39,
  [40] = 40,
  [41] = 41,
  [42] = 42,
  [43] = 43,
  [44] = 15,
  [45] = 45,
  [46] = 46,
  [47] = 47,
  [48] = 6,
  [49] = 49,
  [50] = 41,
  [51] = 37,
  [52] = 45,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(32);
      if (lookahead == '!') ADVANCE(5);
      if (lookahead == '"') ADVANCE(3);
      if (lookahead == '\'') ADVANCE(4);
      if (lookahead == '(') ADVANCE(34);
      if (lookahead == ')') ADVANCE(35);
      if (lookahead == '-') ADVANCE(30);
      if (lookahead == '<') ADVANCE(104);
      if (lookahead == '=') ADVANCE(36);
      if (lookahead == '>') ADVANCE(105);
      if (lookahead == 'A') ADVANCE(59);
      if (lookahead == 'F') ADVANCE(62);
      if (lookahead == 'N') ADVANCE(70);
      if (lookahead == 'O') ADVANCE(73);
      if (lookahead == 'P') ADVANCE(65);
      if (lookahead == 'S') ADVANCE(71);
      if (lookahead == 'W') ADVANCE(63);
      if (lookahead == 'a') ADVANCE(98);
      if (lookahead == 'c') ADVANCE(94);
      if (lookahead == 'm') ADVANCE(86);
      if (lookahead == 's') ADVANCE(96);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(0)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(51);
      if (('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 1:
      if (lookahead == '"') ADVANCE(3);
      if (lookahead == '\'') ADVANCE(4);
      if (lookahead == '-') ADVANCE(30);
      if (lookahead == 'N') ADVANCE(85);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(1)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(51);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 2:
      if (lookahead == '"') ADVANCE(3);
      if (lookahead == '\'') ADVANCE(4);
      if (lookahead == '-') ADVANCE(30);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(2)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(51);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 3:
      if (lookahead == '"') ADVANCE(50);
      if (lookahead != 0) ADVANCE(3);
      END_STATE();
    case 4:
      if (lookahead == '\'') ADVANCE(49);
      if (lookahead != 0) ADVANCE(4);
      END_STATE();
    case 5:
      if (lookahead == '=') ADVANCE(103);
      END_STATE();
    case 6:
      if (lookahead == 'A') ADVANCE(13);
      END_STATE();
    case 7:
      if (lookahead == 'A') ADVANCE(25);
      END_STATE();
    case 8:
      if (lookahead == 'D') ADVANCE(43);
      END_STATE();
    case 9:
      if (lookahead == 'E') ADVANCE(21);
      END_STATE();
    case 10:
      if (lookahead == 'G') ADVANCE(6);
      if (lookahead == 'N') ADVANCE(8);
      if (lookahead == 'S') ADVANCE(41);
      END_STATE();
    case 11:
      if (lookahead == 'H') ADVANCE(37);
      END_STATE();
    case 12:
      if (lookahead == 'I') ADVANCE(27);
      END_STATE();
    case 13:
      if (lookahead == 'I') ADVANCE(18);
      END_STATE();
    case 14:
      if (lookahead == 'I') ADVANCE(16);
      if (lookahead == 'O') ADVANCE(22);
      END_STATE();
    case 15:
      if (lookahead == 'L') ADVANCE(19);
      END_STATE();
    case 16:
      if (lookahead == 'L') ADVANCE(28);
      END_STATE();
    case 17:
      if (lookahead == 'M') ADVANCE(7);
      END_STATE();
    case 18:
      if (lookahead == 'N') ADVANCE(23);
      END_STATE();
    case 19:
      if (lookahead == 'O') ADVANCE(24);
      END_STATE();
    case 20:
      if (lookahead == 'R') ADVANCE(44);
      END_STATE();
    case 21:
      if (lookahead == 'R') ADVANCE(42);
      END_STATE();
    case 22:
      if (lookahead == 'R') ADVANCE(17);
      END_STATE();
    case 23:
      if (lookahead == 'S') ADVANCE(26);
      END_STATE();
    case 24:
      if (lookahead == 'T') ADVANCE(39);
      END_STATE();
    case 25:
      if (lookahead == 'T') ADVANCE(45);
      END_STATE();
    case 26:
      if (lookahead == 'T') ADVANCE(40);
      END_STATE();
    case 27:
      if (lookahead == 'T') ADVANCE(11);
      END_STATE();
    case 28:
      if (lookahead == 'T') ADVANCE(9);
      END_STATE();
    case 29:
      if (lookahead == 'a') ADVANCE(98);
      if (lookahead == 'c') ADVANCE(94);
      if (lookahead == 'm') ADVANCE(86);
      if (lookahead == 's') ADVANCE(96);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(29)
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 30:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(51);
      END_STATE();
    case 31:
      if (eof) ADVANCE(32);
      if (lookahead == 'A') ADVANCE(10);
      if (lookahead == 'F') ADVANCE(14);
      if (lookahead == 'O') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(15);
      if (lookahead == 'W') ADVANCE(12);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(31)
      END_STATE();
    case 32:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 33:
      ACCEPT_TOKEN(anon_sym_);
      END_STATE();
    case 34:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 35:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 36:
      ACCEPT_TOKEN(anon_sym_EQ);
      END_STATE();
    case 37:
      ACCEPT_TOKEN(sym_with);
      END_STATE();
    case 38:
      ACCEPT_TOKEN(sym_source);
      END_STATE();
    case 39:
      ACCEPT_TOKEN(sym_plot);
      END_STATE();
    case 40:
      ACCEPT_TOKEN(sym_against);
      END_STATE();
    case 41:
      ACCEPT_TOKEN(sym_as);
      END_STATE();
    case 42:
      ACCEPT_TOKEN(sym_filter);
      END_STATE();
    case 43:
      ACCEPT_TOKEN(sym_and);
      END_STATE();
    case 44:
      ACCEPT_TOKEN(sym_or);
      END_STATE();
    case 45:
      ACCEPT_TOKEN(sym_format);
      END_STATE();
    case 46:
      ACCEPT_TOKEN(sym_not);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(sym_null);
      END_STATE();
    case 48:
      ACCEPT_TOKEN(sym_aggregate_func);
      END_STATE();
    case 49:
      ACCEPT_TOKEN(aux_sym_string_token1);
      END_STATE();
    case 50:
      ACCEPT_TOKEN(aux_sym_string_token2);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(52);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(51);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(52);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'A') ADVANCE(61);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 54:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'A') ADVANCE(82);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 55:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'C') ADVANCE(57);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'D') ADVANCE(43);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'E') ADVANCE(38);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 58:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'E') ADVANCE(76);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 59:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'G') ADVANCE(53);
      if (lookahead == 'N') ADVANCE(56);
      if (lookahead == 'S') ADVANCE(41);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 60:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'H') ADVANCE(37);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 61:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I') ADVANCE(69);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 62:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I') ADVANCE(66);
      if (lookahead == 'O') ADVANCE(74);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 63:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I') ADVANCE(79);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 64:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(47);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 65:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(72);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 66:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(80);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 67:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(64);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 68:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'M') ADVANCE(54);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 69:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'N') ADVANCE(77);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 70:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O') ADVANCE(78);
      if (lookahead == 'U') ADVANCE(67);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 71:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O') ADVANCE(84);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 72:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O') ADVANCE(81);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 73:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R') ADVANCE(44);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 74:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R') ADVANCE(68);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 75:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R') ADVANCE(55);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 76:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R') ADVANCE(42);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 77:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'S') ADVANCE(83);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 78:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(46);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 79:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(60);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 80:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(58);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 81:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(39);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 82:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(45);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 83:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(40);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 84:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'U') ADVANCE(75);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 85:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'U') ADVANCE(67);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 86:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'a') ADVANCE(99);
      if (lookahead == 'e') ADVANCE(88);
      if (lookahead == 'i') ADVANCE(92);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 87:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'a') ADVANCE(92);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 88:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'd') ADVANCE(90);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 89:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'g') ADVANCE(48);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 90:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'i') ADVANCE(87);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 91:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'm') ADVANCE(48);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 92:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(48);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 93:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(95);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 94:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(97);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 95:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(48);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 96:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'u') ADVANCE(91);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 97:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'u') ADVANCE(93);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 98:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'v') ADVANCE(89);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 99:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'x') ADVANCE(48);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 100:
      ACCEPT_TOKEN(sym_identifier);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(100);
      END_STATE();
    case 101:
      ACCEPT_TOKEN(anon_sym_LT_EQ);
      END_STATE();
    case 102:
      ACCEPT_TOKEN(anon_sym_GT_EQ);
      END_STATE();
    case 103:
      ACCEPT_TOKEN(anon_sym_BANG_EQ);
      END_STATE();
    case 104:
      ACCEPT_TOKEN(anon_sym_LT);
      if (lookahead == '=') ADVANCE(101);
      END_STATE();
    case 105:
      ACCEPT_TOKEN(anon_sym_GT);
      if (lookahead == '=') ADVANCE(102);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 31},
  [2] = {.lex_state = 0},
  [3] = {.lex_state = 1},
  [4] = {.lex_state = 31},
  [5] = {.lex_state = 31},
  [6] = {.lex_state = 31},
  [7] = {.lex_state = 31},
  [8] = {.lex_state = 31},
  [9] = {.lex_state = 31},
  [10] = {.lex_state = 31},
  [11] = {.lex_state = 31},
  [12] = {.lex_state = 31},
  [13] = {.lex_state = 2},
  [14] = {.lex_state = 33},
  [15] = {.lex_state = 31},
  [16] = {.lex_state = 31},
  [17] = {.lex_state = 31},
  [18] = {.lex_state = 29},
  [19] = {.lex_state = 31},
  [20] = {.lex_state = 31},
  [21] = {.lex_state = 31},
  [22] = {.lex_state = 31},
  [23] = {.lex_state = 29},
  [24] = {.lex_state = 31},
  [25] = {.lex_state = 31},
  [26] = {.lex_state = 2},
  [27] = {.lex_state = 31},
  [28] = {.lex_state = 31},
  [29] = {.lex_state = 0},
  [30] = {.lex_state = 31},
  [31] = {.lex_state = 2},
  [32] = {.lex_state = 2},
  [33] = {.lex_state = 2},
  [34] = {.lex_state = 31},
  [35] = {.lex_state = 2},
  [36] = {.lex_state = 0},
  [37] = {.lex_state = 2},
  [38] = {.lex_state = 31},
  [39] = {.lex_state = 0},
  [40] = {.lex_state = 0},
  [41] = {.lex_state = 0},
  [42] = {.lex_state = 31},
  [43] = {.lex_state = 31},
  [44] = {.lex_state = 31},
  [45] = {.lex_state = 0},
  [46] = {.lex_state = 2},
  [47] = {.lex_state = 31},
  [48] = {.lex_state = 31},
  [49] = {.lex_state = 0},
  [50] = {.lex_state = 0},
  [51] = {.lex_state = 2},
  [52] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [anon_sym_EQ] = ACTIONS(1),
    [sym_with] = ACTIONS(1),
    [sym_source] = ACTIONS(1),
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
    [sym_query] = STATE(40),
    [sym_with_clause] = STATE(20),
    [sym_with] = ACTIONS(3),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 3,
    STATE(13), 1,
      sym_operator,
    ACTIONS(7), 2,
      anon_sym_LT,
      anon_sym_GT,
    ACTIONS(5), 4,
      anon_sym_EQ,
      anon_sym_LT_EQ,
      anon_sym_GT_EQ,
      anon_sym_BANG_EQ,
  [14] = 4,
    ACTIONS(13), 1,
      sym_identifier,
    STATE(28), 1,
      sym_string,
    ACTIONS(9), 2,
      sym_null,
      sym_number,
    ACTIONS(11), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
  [29] = 5,
    ACTIONS(17), 1,
      sym_filter,
    ACTIONS(19), 1,
      sym_format,
    STATE(21), 1,
      sym_filter_clause,
    STATE(34), 1,
      sym_format_clause,
    ACTIONS(15), 2,
      ts_builtin_sym_end,
      sym_plot,
  [46] = 3,
    STATE(8), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(23), 2,
      sym_and,
      sym_or,
    ACTIONS(21), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_format,
  [59] = 1,
    ACTIONS(25), 6,
      ts_builtin_sym_end,
      sym_plot,
      sym_filter,
      sym_and,
      sym_or,
      sym_format,
  [68] = 3,
    STATE(5), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(23), 2,
      sym_and,
      sym_or,
    ACTIONS(27), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_format,
  [81] = 3,
    STATE(8), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(31), 2,
      sym_and,
      sym_or,
    ACTIONS(29), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_format,
  [94] = 1,
    ACTIONS(34), 5,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
      sym_or,
      sym_format,
  [102] = 4,
    ACTIONS(36), 1,
      ts_builtin_sym_end,
    ACTIONS(38), 1,
      sym_plot,
    STATE(4), 1,
      sym_plot_clause,
    STATE(12), 2,
      sym_series_clause,
      aux_sym_query_repeat1,
  [116] = 1,
    ACTIONS(29), 5,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
      sym_or,
      sym_format,
  [124] = 4,
    ACTIONS(40), 1,
      ts_builtin_sym_end,
    ACTIONS(42), 1,
      sym_plot,
    STATE(4), 1,
      sym_plot_clause,
    STATE(12), 2,
      sym_series_clause,
      aux_sym_query_repeat1,
  [138] = 3,
    STATE(9), 1,
      sym_string,
    ACTIONS(11), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
    ACTIONS(45), 2,
      sym_number,
      sym_identifier,
  [150] = 3,
    ACTIONS(47), 1,
      anon_sym_,
    ACTIONS(49), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
    STATE(47), 2,
      sym_connector_call,
      sym_string,
  [162] = 1,
    ACTIONS(51), 5,
      ts_builtin_sym_end,
      sym_plot,
      sym_as,
      sym_filter,
      sym_format,
  [170] = 1,
    ACTIONS(53), 5,
      ts_builtin_sym_end,
      sym_plot,
      sym_as,
      sym_filter,
      sym_format,
  [178] = 2,
    ACTIONS(57), 1,
      sym_as,
    ACTIONS(55), 4,
      ts_builtin_sym_end,
      sym_plot,
      sym_filter,
      sym_format,
  [188] = 4,
    ACTIONS(59), 1,
      sym_aggregate_func,
    ACTIONS(61), 1,
      sym_identifier,
    STATE(43), 1,
      sym_column_ref,
    STATE(44), 1,
      sym_aggregate_call,
  [201] = 3,
    ACTIONS(65), 1,
      sym_and,
    STATE(19), 1,
      aux_sym_format_clause_repeat1,
    ACTIONS(63), 2,
      ts_builtin_sym_end,
      sym_plot,
  [212] = 3,
    ACTIONS(38), 1,
      sym_plot,
    STATE(4), 1,
      sym_plot_clause,
    STATE(10), 2,
      sym_series_clause,
      aux_sym_query_repeat1,
  [223] = 3,
    ACTIONS(19), 1,
      sym_format,
    STATE(30), 1,
      sym_format_clause,
    ACTIONS(68), 2,
      ts_builtin_sym_end,
      sym_plot,
  [234] = 3,
    ACTIONS(72), 1,
      sym_and,
    STATE(19), 1,
      aux_sym_format_clause_repeat1,
    ACTIONS(70), 2,
      ts_builtin_sym_end,
      sym_plot,
  [245] = 4,
    ACTIONS(74), 1,
      sym_aggregate_func,
    ACTIONS(76), 1,
      sym_identifier,
    STATE(15), 1,
      sym_aggregate_call,
    STATE(17), 1,
      sym_column_ref,
  [258] = 1,
    ACTIONS(78), 4,
      ts_builtin_sym_end,
      sym_plot,
      sym_filter,
      sym_format,
  [265] = 3,
    ACTIONS(72), 1,
      sym_and,
    STATE(22), 1,
      aux_sym_format_clause_repeat1,
    ACTIONS(80), 2,
      ts_builtin_sym_end,
      sym_plot,
  [276] = 1,
    ACTIONS(82), 4,
      aux_sym_string_token1,
      aux_sym_string_token2,
      sym_number,
      sym_identifier,
  [283] = 1,
    ACTIONS(63), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
  [289] = 1,
    ACTIONS(84), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
  [295] = 2,
    STATE(24), 1,
      sym_string,
    ACTIONS(11), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
  [303] = 1,
    ACTIONS(86), 2,
      ts_builtin_sym_end,
      sym_plot,
  [308] = 2,
    ACTIONS(88), 1,
      sym_identifier,
    STATE(25), 1,
      sym_format_option,
  [315] = 2,
    ACTIONS(90), 1,
      sym_identifier,
    STATE(7), 1,
      sym_condition,
  [322] = 2,
    ACTIONS(90), 1,
      sym_identifier,
    STATE(11), 1,
      sym_condition,
  [329] = 1,
    ACTIONS(68), 2,
      ts_builtin_sym_end,
      sym_plot,
  [334] = 2,
    ACTIONS(88), 1,
      sym_identifier,
    STATE(27), 1,
      sym_format_option,
  [341] = 1,
    ACTIONS(92), 1,
      anon_sym_EQ,
  [345] = 1,
    ACTIONS(94), 1,
      sym_identifier,
  [349] = 1,
    ACTIONS(53), 1,
      sym_against,
  [353] = 1,
    ACTIONS(96), 1,
      anon_sym_RPAREN,
  [357] = 1,
    ACTIONS(98), 1,
      ts_builtin_sym_end,
  [361] = 1,
    ACTIONS(100), 1,
      anon_sym_RPAREN,
  [365] = 1,
    ACTIONS(102), 1,
      sym_plot,
  [369] = 1,
    ACTIONS(104), 1,
      sym_against,
  [373] = 1,
    ACTIONS(51), 1,
      sym_against,
  [377] = 1,
    ACTIONS(106), 1,
      anon_sym_LPAREN,
  [381] = 1,
    ACTIONS(108), 1,
      sym_identifier,
  [385] = 1,
    ACTIONS(110), 1,
      sym_plot,
  [389] = 1,
    ACTIONS(25), 1,
      sym_plot,
  [393] = 1,
    ACTIONS(112), 1,
      anon_sym_LPAREN,
  [397] = 1,
    ACTIONS(114), 1,
      anon_sym_RPAREN,
  [401] = 1,
    ACTIONS(116), 1,
      sym_identifier,
  [405] = 1,
    ACTIONS(118), 1,
      anon_sym_LPAREN,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 14,
  [SMALL_STATE(4)] = 29,
  [SMALL_STATE(5)] = 46,
  [SMALL_STATE(6)] = 59,
  [SMALL_STATE(7)] = 68,
  [SMALL_STATE(8)] = 81,
  [SMALL_STATE(9)] = 94,
  [SMALL_STATE(10)] = 102,
  [SMALL_STATE(11)] = 116,
  [SMALL_STATE(12)] = 124,
  [SMALL_STATE(13)] = 138,
  [SMALL_STATE(14)] = 150,
  [SMALL_STATE(15)] = 162,
  [SMALL_STATE(16)] = 170,
  [SMALL_STATE(17)] = 178,
  [SMALL_STATE(18)] = 188,
  [SMALL_STATE(19)] = 201,
  [SMALL_STATE(20)] = 212,
  [SMALL_STATE(21)] = 223,
  [SMALL_STATE(22)] = 234,
  [SMALL_STATE(23)] = 245,
  [SMALL_STATE(24)] = 258,
  [SMALL_STATE(25)] = 265,
  [SMALL_STATE(26)] = 276,
  [SMALL_STATE(27)] = 283,
  [SMALL_STATE(28)] = 289,
  [SMALL_STATE(29)] = 295,
  [SMALL_STATE(30)] = 303,
  [SMALL_STATE(31)] = 308,
  [SMALL_STATE(32)] = 315,
  [SMALL_STATE(33)] = 322,
  [SMALL_STATE(34)] = 329,
  [SMALL_STATE(35)] = 334,
  [SMALL_STATE(36)] = 341,
  [SMALL_STATE(37)] = 345,
  [SMALL_STATE(38)] = 349,
  [SMALL_STATE(39)] = 353,
  [SMALL_STATE(40)] = 357,
  [SMALL_STATE(41)] = 361,
  [SMALL_STATE(42)] = 365,
  [SMALL_STATE(43)] = 369,
  [SMALL_STATE(44)] = 373,
  [SMALL_STATE(45)] = 377,
  [SMALL_STATE(46)] = 381,
  [SMALL_STATE(47)] = 385,
  [SMALL_STATE(48)] = 389,
  [SMALL_STATE(49)] = 393,
  [SMALL_STATE(50)] = 397,
  [SMALL_STATE(51)] = 401,
  [SMALL_STATE(52)] = 405,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(26),
  [7] = {.entry = {.count = 1, .reusable = false}}, SHIFT(26),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [11] = {.entry = {.count = 1, .reusable = true}}, SHIFT(6),
  [13] = {.entry = {.count = 1, .reusable = false}}, SHIFT(28),
  [15] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_series_clause, 1),
  [17] = {.entry = {.count = 1, .reusable = true}}, SHIFT(32),
  [19] = {.entry = {.count = 1, .reusable = true}}, SHIFT(31),
  [21] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_filter_clause, 3),
  [23] = {.entry = {.count = 1, .reusable = true}}, SHIFT(33),
  [25] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_string, 1),
  [27] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_filter_clause, 2),
  [29] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_filter_clause_repeat1, 2),
  [31] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_filter_clause_repeat1, 2), SHIFT_REPEAT(33),
  [34] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_condition, 3),
  [36] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_query, 2),
  [38] = {.entry = {.count = 1, .reusable = true}}, SHIFT(18),
  [40] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_query_repeat1, 2),
  [42] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_query_repeat1, 2), SHIFT_REPEAT(18),
  [45] = {.entry = {.count = 1, .reusable = true}}, SHIFT(9),
  [47] = {.entry = {.count = 1, .reusable = true}}, SHIFT(49),
  [49] = {.entry = {.count = 1, .reusable = false}}, SHIFT(48),
  [51] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_column_ref, 1),
  [53] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_aggregate_call, 4),
  [55] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_plot_clause, 4),
  [57] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [59] = {.entry = {.count = 1, .reusable = true}}, SHIFT(45),
  [61] = {.entry = {.count = 1, .reusable = false}}, SHIFT(44),
  [63] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_format_clause_repeat1, 2),
  [65] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_format_clause_repeat1, 2), SHIFT_REPEAT(35),
  [68] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_series_clause, 2),
  [70] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_clause, 3),
  [72] = {.entry = {.count = 1, .reusable = true}}, SHIFT(35),
  [74] = {.entry = {.count = 1, .reusable = true}}, SHIFT(52),
  [76] = {.entry = {.count = 1, .reusable = false}}, SHIFT(15),
  [78] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_plot_clause, 6),
  [80] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_clause, 2),
  [82] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_operator, 1),
  [84] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_option, 3),
  [86] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_series_clause, 3),
  [88] = {.entry = {.count = 1, .reusable = true}}, SHIFT(36),
  [90] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [92] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [94] = {.entry = {.count = 1, .reusable = true}}, SHIFT(41),
  [96] = {.entry = {.count = 1, .reusable = true}}, SHIFT(42),
  [98] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [100] = {.entry = {.count = 1, .reusable = true}}, SHIFT(38),
  [102] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_connector_call, 4),
  [104] = {.entry = {.count = 1, .reusable = true}}, SHIFT(23),
  [106] = {.entry = {.count = 1, .reusable = true}}, SHIFT(37),
  [108] = {.entry = {.count = 1, .reusable = true}}, SHIFT(39),
  [110] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_with_clause, 2),
  [112] = {.entry = {.count = 1, .reusable = true}}, SHIFT(46),
  [114] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [116] = {.entry = {.count = 1, .reusable = true}}, SHIFT(50),
  [118] = {.entry = {.count = 1, .reusable = true}}, SHIFT(51),
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
