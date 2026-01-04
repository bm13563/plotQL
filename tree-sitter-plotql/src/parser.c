#include <tree_sitter/parser.h>

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 52
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 43
#define ALIAS_COUNT 0
#define TOKEN_COUNT 26
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 6
#define PRODUCTION_ID_COUNT 1

enum {
  anon_sym_LPAREN = 1,
  anon_sym_COMMA = 2,
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
  sym_source_call = 29,
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
  aux_sym_source_call_repeat1 = 40,
  aux_sym_filter_clause_repeat1 = 41,
  aux_sym_format_clause_repeat1 = 42,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [anon_sym_LPAREN] = "(",
  [anon_sym_COMMA] = ",",
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
  [sym_source_call] = "source_call",
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
  [aux_sym_source_call_repeat1] = "source_call_repeat1",
  [aux_sym_filter_clause_repeat1] = "filter_clause_repeat1",
  [aux_sym_format_clause_repeat1] = "format_clause_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_COMMA] = anon_sym_COMMA,
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
  [sym_source_call] = sym_source_call,
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
  [aux_sym_source_call_repeat1] = aux_sym_source_call_repeat1,
  [aux_sym_filter_clause_repeat1] = aux_sym_filter_clause_repeat1,
  [aux_sym_format_clause_repeat1] = aux_sym_format_clause_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [anon_sym_LPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMMA] = {
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
  [sym_source_call] = {
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
  [aux_sym_source_call_repeat1] = {
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
  [38] = 38,
  [39] = 39,
  [40] = 40,
  [41] = 41,
  [42] = 42,
  [43] = 43,
  [44] = 44,
  [45] = 45,
  [46] = 46,
  [47] = 47,
  [48] = 48,
  [49] = 49,
  [50] = 50,
  [51] = 51,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(37);
      if (lookahead == '!') ADVANCE(5);
      if (lookahead == '"') ADVANCE(3);
      if (lookahead == '\'') ADVANCE(4);
      if (lookahead == '(') ADVANCE(38);
      if (lookahead == ')') ADVANCE(40);
      if (lookahead == ',') ADVANCE(39);
      if (lookahead == '-') ADVANCE(35);
      if (lookahead == '<') ADVANCE(109);
      if (lookahead == '=') ADVANCE(41);
      if (lookahead == '>') ADVANCE(110);
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(67);
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(83);
      if (lookahead == 'F' ||
          lookahead == 'f') ADVANCE(70);
      if (lookahead == 'M' ||
          lookahead == 'm') ADVANCE(58);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(84);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(87);
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(75);
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(85);
      if (lookahead == 'W' ||
          lookahead == 'w') ADVANCE(71);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(0)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(56);
      if (('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 1:
      if (lookahead == '"') ADVANCE(3);
      if (lookahead == '\'') ADVANCE(4);
      if (lookahead == '-') ADVANCE(35);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(102);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(1)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(56);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 2:
      if (lookahead == '"') ADVANCE(3);
      if (lookahead == '\'') ADVANCE(4);
      if (lookahead == '-') ADVANCE(35);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(2)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(56);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 3:
      if (lookahead == '"') ADVANCE(55);
      if (lookahead != 0) ADVANCE(3);
      END_STATE();
    case 4:
      if (lookahead == '\'') ADVANCE(54);
      if (lookahead != 0) ADVANCE(4);
      END_STATE();
    case 5:
      if (lookahead == '=') ADVANCE(108);
      END_STATE();
    case 6:
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(103);
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(83);
      if (lookahead == 'M' ||
          lookahead == 'm') ADVANCE(58);
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(99);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(6)
      if (('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 7:
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(16);
      END_STATE();
    case 8:
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(30);
      END_STATE();
    case 9:
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(11);
      END_STATE();
    case 10:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(48);
      END_STATE();
    case 11:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(43);
      END_STATE();
    case 12:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(25);
      END_STATE();
    case 13:
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(7);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(10);
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(46);
      END_STATE();
    case 14:
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(42);
      END_STATE();
    case 15:
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(32);
      END_STATE();
    case 16:
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(21);
      END_STATE();
    case 17:
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(19);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(26);
      END_STATE();
    case 18:
      if (lookahead == 'L' ||
          lookahead == 'l') ADVANCE(23);
      END_STATE();
    case 19:
      if (lookahead == 'L' ||
          lookahead == 'l') ADVANCE(33);
      END_STATE();
    case 20:
      if (lookahead == 'M' ||
          lookahead == 'm') ADVANCE(8);
      END_STATE();
    case 21:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(28);
      END_STATE();
    case 22:
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(34);
      END_STATE();
    case 23:
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(29);
      END_STATE();
    case 24:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(49);
      END_STATE();
    case 25:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(47);
      END_STATE();
    case 26:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(20);
      END_STATE();
    case 27:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(9);
      END_STATE();
    case 28:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(31);
      END_STATE();
    case 29:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(44);
      END_STATE();
    case 30:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(50);
      END_STATE();
    case 31:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(45);
      END_STATE();
    case 32:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(14);
      END_STATE();
    case 33:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(12);
      END_STATE();
    case 34:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(27);
      END_STATE();
    case 35:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(56);
      END_STATE();
    case 36:
      if (eof) ADVANCE(37);
      if (lookahead == ')') ADVANCE(40);
      if (lookahead == ',') ADVANCE(39);
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(13);
      if (lookahead == 'F' ||
          lookahead == 'f') ADVANCE(17);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(24);
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(18);
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(22);
      if (lookahead == 'W' ||
          lookahead == 'w') ADVANCE(15);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(36)
      END_STATE();
    case 37:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 38:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 39:
      ACCEPT_TOKEN(anon_sym_COMMA);
      END_STATE();
    case 40:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 41:
      ACCEPT_TOKEN(anon_sym_EQ);
      END_STATE();
    case 42:
      ACCEPT_TOKEN(sym_with);
      END_STATE();
    case 43:
      ACCEPT_TOKEN(sym_source);
      END_STATE();
    case 44:
      ACCEPT_TOKEN(sym_plot);
      END_STATE();
    case 45:
      ACCEPT_TOKEN(sym_against);
      END_STATE();
    case 46:
      ACCEPT_TOKEN(sym_as);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(sym_filter);
      END_STATE();
    case 48:
      ACCEPT_TOKEN(sym_and);
      END_STATE();
    case 49:
      ACCEPT_TOKEN(sym_or);
      END_STATE();
    case 50:
      ACCEPT_TOKEN(sym_format);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(sym_not);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(sym_null);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(sym_aggregate_func);
      END_STATE();
    case 54:
      ACCEPT_TOKEN(aux_sym_string_token1);
      END_STATE();
    case 55:
      ACCEPT_TOKEN(aux_sym_string_token2);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(57);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(56);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(57);
      END_STATE();
    case 58:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(104);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(64);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(80);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 59:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(80);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 60:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(73);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 61:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(97);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 62:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(65);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 63:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(48);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 64:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(72);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 65:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(43);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 66:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(89);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 67:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(60);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(63);
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(46);
      if (lookahead == 'V' ||
          lookahead == 'v') ADVANCE(68);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 68:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(53);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 69:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(42);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 70:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(76);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(90);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 71:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(94);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 72:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(59);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 73:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(81);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 74:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L' ||
          lookahead == 'l') ADVANCE(52);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 75:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L' ||
          lookahead == 'l') ADVANCE(86);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 76:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L' ||
          lookahead == 'l') ADVANCE(95);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 77:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L' ||
          lookahead == 'l') ADVANCE(74);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 78:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'M' ||
          lookahead == 'm') ADVANCE(53);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 79:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'M' ||
          lookahead == 'm') ADVANCE(61);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 80:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(53);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 81:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(91);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 82:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(92);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 83:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(100);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 84:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(93);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(77);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 85:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(101);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(78);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 86:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(96);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 87:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(49);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 88:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(62);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 89:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(47);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 90:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(79);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 91:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(98);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 92:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(53);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 93:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(51);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 94:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(69);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 95:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(66);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 96:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(44);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 97:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(50);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 98:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(45);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 99:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(78);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 100:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(82);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 101:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(88);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 102:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(77);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 103:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'V' ||
          lookahead == 'v') ADVANCE(68);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 104:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'X' ||
          lookahead == 'x') ADVANCE(53);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 105:
      ACCEPT_TOKEN(sym_identifier);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(105);
      END_STATE();
    case 106:
      ACCEPT_TOKEN(anon_sym_LT_EQ);
      END_STATE();
    case 107:
      ACCEPT_TOKEN(anon_sym_GT_EQ);
      END_STATE();
    case 108:
      ACCEPT_TOKEN(anon_sym_BANG_EQ);
      END_STATE();
    case 109:
      ACCEPT_TOKEN(anon_sym_LT);
      if (lookahead == '=') ADVANCE(106);
      END_STATE();
    case 110:
      ACCEPT_TOKEN(anon_sym_GT);
      if (lookahead == '=') ADVANCE(107);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 36},
  [2] = {.lex_state = 36},
  [3] = {.lex_state = 0},
  [4] = {.lex_state = 36},
  [5] = {.lex_state = 36},
  [6] = {.lex_state = 36},
  [7] = {.lex_state = 36},
  [8] = {.lex_state = 36},
  [9] = {.lex_state = 36},
  [10] = {.lex_state = 1},
  [11] = {.lex_state = 2},
  [12] = {.lex_state = 36},
  [13] = {.lex_state = 36},
  [14] = {.lex_state = 36},
  [15] = {.lex_state = 36},
  [16] = {.lex_state = 36},
  [17] = {.lex_state = 36},
  [18] = {.lex_state = 36},
  [19] = {.lex_state = 6},
  [20] = {.lex_state = 36},
  [21] = {.lex_state = 36},
  [22] = {.lex_state = 36},
  [23] = {.lex_state = 36},
  [24] = {.lex_state = 2},
  [25] = {.lex_state = 6},
  [26] = {.lex_state = 36},
  [27] = {.lex_state = 0},
  [28] = {.lex_state = 0},
  [29] = {.lex_state = 36},
  [30] = {.lex_state = 0},
  [31] = {.lex_state = 0},
  [32] = {.lex_state = 0},
  [33] = {.lex_state = 0},
  [34] = {.lex_state = 36},
  [35] = {.lex_state = 2},
  [36] = {.lex_state = 2},
  [37] = {.lex_state = 36},
  [38] = {.lex_state = 0},
  [39] = {.lex_state = 36},
  [40] = {.lex_state = 2},
  [41] = {.lex_state = 2},
  [42] = {.lex_state = 0},
  [43] = {.lex_state = 36},
  [44] = {.lex_state = 36},
  [45] = {.lex_state = 0},
  [46] = {.lex_state = 2},
  [47] = {.lex_state = 36},
  [48] = {.lex_state = 0},
  [49] = {.lex_state = 36},
  [50] = {.lex_state = 0},
  [51] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_COMMA] = ACTIONS(1),
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
    [sym_query] = STATE(51),
    [sym_with_clause] = STATE(20),
    [sym_with] = ACTIONS(3),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 1,
    ACTIONS(5), 8,
      ts_builtin_sym_end,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym_plot,
      sym_filter,
      sym_and,
      sym_or,
      sym_format,
  [11] = 3,
    STATE(11), 1,
      sym_operator,
    ACTIONS(9), 2,
      anon_sym_LT,
      anon_sym_GT,
    ACTIONS(7), 4,
      anon_sym_EQ,
      anon_sym_LT_EQ,
      anon_sym_GT_EQ,
      anon_sym_BANG_EQ,
  [25] = 3,
    STATE(6), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(13), 2,
      sym_and,
      sym_or,
    ACTIONS(11), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_format,
  [38] = 1,
    ACTIONS(15), 6,
      ts_builtin_sym_end,
      sym_plot,
      sym_against,
      sym_as,
      sym_filter,
      sym_format,
  [47] = 3,
    STATE(8), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(13), 2,
      sym_and,
      sym_or,
    ACTIONS(17), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_format,
  [60] = 5,
    ACTIONS(21), 1,
      sym_filter,
    ACTIONS(23), 1,
      sym_format,
    STATE(18), 1,
      sym_filter_clause,
    STATE(39), 1,
      sym_format_clause,
    ACTIONS(19), 2,
      ts_builtin_sym_end,
      sym_plot,
  [77] = 3,
    STATE(8), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(27), 2,
      sym_and,
      sym_or,
    ACTIONS(25), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_format,
  [90] = 1,
    ACTIONS(30), 6,
      ts_builtin_sym_end,
      sym_plot,
      sym_against,
      sym_as,
      sym_filter,
      sym_format,
  [99] = 4,
    ACTIONS(36), 1,
      sym_identifier,
    STATE(29), 1,
      sym_string,
    ACTIONS(32), 2,
      sym_null,
      sym_number,
    ACTIONS(34), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
  [114] = 3,
    STATE(15), 1,
      sym_string,
    ACTIONS(34), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
    ACTIONS(38), 2,
      sym_number,
      sym_identifier,
  [126] = 4,
    ACTIONS(40), 1,
      ts_builtin_sym_end,
    ACTIONS(42), 1,
      sym_plot,
    STATE(7), 1,
      sym_plot_clause,
    STATE(16), 2,
      sym_series_clause,
      aux_sym_query_repeat1,
  [140] = 2,
    ACTIONS(46), 1,
      sym_as,
    ACTIONS(44), 4,
      ts_builtin_sym_end,
      sym_plot,
      sym_filter,
      sym_format,
  [150] = 1,
    ACTIONS(25), 5,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
      sym_or,
      sym_format,
  [158] = 1,
    ACTIONS(48), 5,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
      sym_or,
      sym_format,
  [166] = 4,
    ACTIONS(50), 1,
      ts_builtin_sym_end,
    ACTIONS(52), 1,
      sym_plot,
    STATE(7), 1,
      sym_plot_clause,
    STATE(16), 2,
      sym_series_clause,
      aux_sym_query_repeat1,
  [180] = 1,
    ACTIONS(55), 4,
      ts_builtin_sym_end,
      sym_plot,
      sym_filter,
      sym_format,
  [187] = 3,
    ACTIONS(23), 1,
      sym_format,
    STATE(34), 1,
      sym_format_clause,
    ACTIONS(57), 2,
      ts_builtin_sym_end,
      sym_plot,
  [198] = 4,
    ACTIONS(59), 1,
      sym_aggregate_func,
    ACTIONS(61), 1,
      sym_identifier,
    STATE(9), 1,
      sym_aggregate_call,
    STATE(13), 1,
      sym_column_ref,
  [211] = 3,
    ACTIONS(42), 1,
      sym_plot,
    STATE(7), 1,
      sym_plot_clause,
    STATE(12), 2,
      sym_series_clause,
      aux_sym_query_repeat1,
  [222] = 3,
    ACTIONS(65), 1,
      sym_and,
    STATE(23), 1,
      aux_sym_format_clause_repeat1,
    ACTIONS(63), 2,
      ts_builtin_sym_end,
      sym_plot,
  [233] = 3,
    ACTIONS(65), 1,
      sym_and,
    STATE(21), 1,
      aux_sym_format_clause_repeat1,
    ACTIONS(67), 2,
      ts_builtin_sym_end,
      sym_plot,
  [244] = 3,
    ACTIONS(71), 1,
      sym_and,
    STATE(23), 1,
      aux_sym_format_clause_repeat1,
    ACTIONS(69), 2,
      ts_builtin_sym_end,
      sym_plot,
  [255] = 1,
    ACTIONS(74), 4,
      aux_sym_string_token1,
      aux_sym_string_token2,
      sym_number,
      sym_identifier,
  [262] = 4,
    ACTIONS(59), 1,
      sym_aggregate_func,
    ACTIONS(61), 1,
      sym_identifier,
    STATE(9), 1,
      sym_aggregate_call,
    STATE(47), 1,
      sym_column_ref,
  [275] = 1,
    ACTIONS(69), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
  [281] = 3,
    ACTIONS(76), 1,
      anon_sym_COMMA,
    ACTIONS(78), 1,
      anon_sym_RPAREN,
    STATE(31), 1,
      aux_sym_source_call_repeat1,
  [291] = 3,
    ACTIONS(80), 1,
      anon_sym_COMMA,
    ACTIONS(83), 1,
      anon_sym_RPAREN,
    STATE(28), 1,
      aux_sym_source_call_repeat1,
  [301] = 1,
    ACTIONS(85), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
  [307] = 2,
    STATE(38), 1,
      sym_string,
    ACTIONS(34), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
  [315] = 3,
    ACTIONS(76), 1,
      anon_sym_COMMA,
    ACTIONS(87), 1,
      anon_sym_RPAREN,
    STATE(28), 1,
      aux_sym_source_call_repeat1,
  [325] = 2,
    STATE(17), 1,
      sym_string,
    ACTIONS(34), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
  [333] = 2,
    STATE(27), 1,
      sym_string,
    ACTIONS(34), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
  [341] = 1,
    ACTIONS(89), 2,
      ts_builtin_sym_end,
      sym_plot,
  [346] = 2,
    ACTIONS(91), 1,
      sym_identifier,
    STATE(14), 1,
      sym_condition,
  [353] = 2,
    ACTIONS(93), 1,
      sym_identifier,
    STATE(26), 1,
      sym_format_option,
  [360] = 2,
    ACTIONS(95), 1,
      sym_source,
    STATE(49), 1,
      sym_source_call,
  [367] = 1,
    ACTIONS(83), 2,
      anon_sym_COMMA,
      anon_sym_RPAREN,
  [372] = 1,
    ACTIONS(57), 2,
      ts_builtin_sym_end,
      sym_plot,
  [377] = 2,
    ACTIONS(93), 1,
      sym_identifier,
    STATE(22), 1,
      sym_format_option,
  [384] = 2,
    ACTIONS(91), 1,
      sym_identifier,
    STATE(4), 1,
      sym_condition,
  [391] = 1,
    ACTIONS(97), 1,
      anon_sym_RPAREN,
  [395] = 1,
    ACTIONS(99), 1,
      sym_plot,
  [399] = 1,
    ACTIONS(101), 1,
      sym_plot,
  [403] = 1,
    ACTIONS(103), 1,
      anon_sym_EQ,
  [407] = 1,
    ACTIONS(105), 1,
      sym_identifier,
  [411] = 1,
    ACTIONS(107), 1,
      sym_against,
  [415] = 1,
    ACTIONS(109), 1,
      anon_sym_LPAREN,
  [419] = 1,
    ACTIONS(111), 1,
      sym_plot,
  [423] = 1,
    ACTIONS(113), 1,
      anon_sym_LPAREN,
  [427] = 1,
    ACTIONS(115), 1,
      ts_builtin_sym_end,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 11,
  [SMALL_STATE(4)] = 25,
  [SMALL_STATE(5)] = 38,
  [SMALL_STATE(6)] = 47,
  [SMALL_STATE(7)] = 60,
  [SMALL_STATE(8)] = 77,
  [SMALL_STATE(9)] = 90,
  [SMALL_STATE(10)] = 99,
  [SMALL_STATE(11)] = 114,
  [SMALL_STATE(12)] = 126,
  [SMALL_STATE(13)] = 140,
  [SMALL_STATE(14)] = 150,
  [SMALL_STATE(15)] = 158,
  [SMALL_STATE(16)] = 166,
  [SMALL_STATE(17)] = 180,
  [SMALL_STATE(18)] = 187,
  [SMALL_STATE(19)] = 198,
  [SMALL_STATE(20)] = 211,
  [SMALL_STATE(21)] = 222,
  [SMALL_STATE(22)] = 233,
  [SMALL_STATE(23)] = 244,
  [SMALL_STATE(24)] = 255,
  [SMALL_STATE(25)] = 262,
  [SMALL_STATE(26)] = 275,
  [SMALL_STATE(27)] = 281,
  [SMALL_STATE(28)] = 291,
  [SMALL_STATE(29)] = 301,
  [SMALL_STATE(30)] = 307,
  [SMALL_STATE(31)] = 315,
  [SMALL_STATE(32)] = 325,
  [SMALL_STATE(33)] = 333,
  [SMALL_STATE(34)] = 341,
  [SMALL_STATE(35)] = 346,
  [SMALL_STATE(36)] = 353,
  [SMALL_STATE(37)] = 360,
  [SMALL_STATE(38)] = 367,
  [SMALL_STATE(39)] = 372,
  [SMALL_STATE(40)] = 377,
  [SMALL_STATE(41)] = 384,
  [SMALL_STATE(42)] = 391,
  [SMALL_STATE(43)] = 395,
  [SMALL_STATE(44)] = 399,
  [SMALL_STATE(45)] = 403,
  [SMALL_STATE(46)] = 407,
  [SMALL_STATE(47)] = 411,
  [SMALL_STATE(48)] = 415,
  [SMALL_STATE(49)] = 419,
  [SMALL_STATE(50)] = 423,
  [SMALL_STATE(51)] = 427,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT(37),
  [5] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_string, 1),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(24),
  [9] = {.entry = {.count = 1, .reusable = false}}, SHIFT(24),
  [11] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_filter_clause, 2),
  [13] = {.entry = {.count = 1, .reusable = true}}, SHIFT(35),
  [15] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_aggregate_call, 4),
  [17] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_filter_clause, 3),
  [19] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_series_clause, 1),
  [21] = {.entry = {.count = 1, .reusable = true}}, SHIFT(41),
  [23] = {.entry = {.count = 1, .reusable = true}}, SHIFT(40),
  [25] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_filter_clause_repeat1, 2),
  [27] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_filter_clause_repeat1, 2), SHIFT_REPEAT(35),
  [30] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_column_ref, 1),
  [32] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [34] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [36] = {.entry = {.count = 1, .reusable = false}}, SHIFT(29),
  [38] = {.entry = {.count = 1, .reusable = true}}, SHIFT(15),
  [40] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_query, 2),
  [42] = {.entry = {.count = 1, .reusable = true}}, SHIFT(25),
  [44] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_plot_clause, 4),
  [46] = {.entry = {.count = 1, .reusable = true}}, SHIFT(32),
  [48] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_condition, 3),
  [50] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_query_repeat1, 2),
  [52] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_query_repeat1, 2), SHIFT_REPEAT(25),
  [55] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_plot_clause, 6),
  [57] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_series_clause, 2),
  [59] = {.entry = {.count = 1, .reusable = true}}, SHIFT(48),
  [61] = {.entry = {.count = 1, .reusable = false}}, SHIFT(9),
  [63] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_clause, 3),
  [65] = {.entry = {.count = 1, .reusable = true}}, SHIFT(36),
  [67] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_clause, 2),
  [69] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_format_clause_repeat1, 2),
  [71] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_format_clause_repeat1, 2), SHIFT_REPEAT(36),
  [74] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_operator, 1),
  [76] = {.entry = {.count = 1, .reusable = true}}, SHIFT(30),
  [78] = {.entry = {.count = 1, .reusable = true}}, SHIFT(43),
  [80] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_call_repeat1, 2), SHIFT_REPEAT(30),
  [83] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_source_call_repeat1, 2),
  [85] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_option, 3),
  [87] = {.entry = {.count = 1, .reusable = true}}, SHIFT(44),
  [89] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_series_clause, 3),
  [91] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [93] = {.entry = {.count = 1, .reusable = true}}, SHIFT(45),
  [95] = {.entry = {.count = 1, .reusable = true}}, SHIFT(50),
  [97] = {.entry = {.count = 1, .reusable = true}}, SHIFT(5),
  [99] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_call, 4),
  [101] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_call, 5),
  [103] = {.entry = {.count = 1, .reusable = true}}, SHIFT(10),
  [105] = {.entry = {.count = 1, .reusable = true}}, SHIFT(42),
  [107] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [109] = {.entry = {.count = 1, .reusable = true}}, SHIFT(46),
  [111] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_with_clause, 2),
  [113] = {.entry = {.count = 1, .reusable = true}}, SHIFT(33),
  [115] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
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
