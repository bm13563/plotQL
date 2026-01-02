#include <tree_sitter/parser.h>

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 47
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 42
#define ALIAS_COUNT 0
#define TOKEN_COUNT 26
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 6
#define PRODUCTION_ID_COUNT 1

enum {
  anon_sym_LPAREN = 1,
  anon_sym_RPAREN = 2,
  anon_sym_EQ = 3,
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
  sym_file_connector = 15,
  sym_clickhouse_connector = 16,
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
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [anon_sym_EQ] = "=",
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
  [sym_file_connector] = "file_connector",
  [sym_clickhouse_connector] = "clickhouse_connector",
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
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [anon_sym_EQ] = anon_sym_EQ,
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
  [sym_file_connector] = sym_file_connector,
  [sym_clickhouse_connector] = sym_clickhouse_connector,
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
  [sym_file_connector] = {
    .visible = true,
    .named = true,
  },
  [sym_clickhouse_connector] = {
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
  [38] = 38,
  [39] = 39,
  [40] = 40,
  [41] = 41,
  [42] = 42,
  [43] = 43,
  [44] = 44,
  [45] = 45,
  [46] = 46,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(44);
      if (lookahead == '!') ADVANCE(5);
      if (lookahead == '"') ADVANCE(3);
      if (lookahead == '\'') ADVANCE(4);
      if (lookahead == '(') ADVANCE(45);
      if (lookahead == ')') ADVANCE(46);
      if (lookahead == '-') ADVANCE(42);
      if (lookahead == '<') ADVANCE(123);
      if (lookahead == '=') ADVANCE(47);
      if (lookahead == '>') ADVANCE(124);
      if (lookahead == 'A') ADVANCE(69);
      if (lookahead == 'F') ADVANCE(72);
      if (lookahead == 'N') ADVANCE(80);
      if (lookahead == 'O') ADVANCE(82);
      if (lookahead == 'P') ADVANCE(74);
      if (lookahead == 'W') ADVANCE(73);
      if (lookahead == 'a') ADVANCE(117);
      if (lookahead == 'c') ADVANCE(106);
      if (lookahead == 'f') ADVANCE(101);
      if (lookahead == 'm') ADVANCE(93);
      if (lookahead == 's') ADVANCE(114);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(0)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(63);
      if (('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 1:
      if (lookahead == '"') ADVANCE(3);
      if (lookahead == '\'') ADVANCE(4);
      if (lookahead == '-') ADVANCE(42);
      if (lookahead == 'N') ADVANCE(92);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(1)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(63);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 2:
      if (lookahead == '"') ADVANCE(3);
      if (lookahead == '\'') ADVANCE(4);
      if (lookahead == '-') ADVANCE(42);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(2)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(63);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 3:
      if (lookahead == '"') ADVANCE(62);
      if (lookahead != 0) ADVANCE(3);
      END_STATE();
    case 4:
      if (lookahead == '\'') ADVANCE(61);
      if (lookahead != 0) ADVANCE(4);
      END_STATE();
    case 5:
      if (lookahead == '=') ADVANCE(122);
      END_STATE();
    case 6:
      if (lookahead == 'A') ADVANCE(13);
      END_STATE();
    case 7:
      if (lookahead == 'A') ADVANCE(25);
      END_STATE();
    case 8:
      if (lookahead == 'D') ADVANCE(53);
      END_STATE();
    case 9:
      if (lookahead == 'E') ADVANCE(21);
      END_STATE();
    case 10:
      if (lookahead == 'G') ADVANCE(6);
      if (lookahead == 'N') ADVANCE(8);
      if (lookahead == 'S') ADVANCE(51);
      END_STATE();
    case 11:
      if (lookahead == 'H') ADVANCE(48);
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
      if (lookahead == 'R') ADVANCE(54);
      END_STATE();
    case 21:
      if (lookahead == 'R') ADVANCE(52);
      END_STATE();
    case 22:
      if (lookahead == 'R') ADVANCE(17);
      END_STATE();
    case 23:
      if (lookahead == 'S') ADVANCE(26);
      END_STATE();
    case 24:
      if (lookahead == 'T') ADVANCE(49);
      END_STATE();
    case 25:
      if (lookahead == 'T') ADVANCE(55);
      END_STATE();
    case 26:
      if (lookahead == 'T') ADVANCE(50);
      END_STATE();
    case 27:
      if (lookahead == 'T') ADVANCE(11);
      END_STATE();
    case 28:
      if (lookahead == 'T') ADVANCE(9);
      END_STATE();
    case 29:
      if (lookahead == 'a') ADVANCE(117);
      if (lookahead == 'c') ADVANCE(110);
      if (lookahead == 'm') ADVANCE(93);
      if (lookahead == 's') ADVANCE(114);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(29)
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 30:
      if (lookahead == 'c') ADVANCE(36);
      END_STATE();
    case 31:
      if (lookahead == 'e') ADVANCE(59);
      END_STATE();
    case 32:
      if (lookahead == 'e') ADVANCE(60);
      END_STATE();
    case 33:
      if (lookahead == 'h') ADVANCE(39);
      END_STATE();
    case 34:
      if (lookahead == 'i') ADVANCE(30);
      END_STATE();
    case 35:
      if (lookahead == 'i') ADVANCE(37);
      END_STATE();
    case 36:
      if (lookahead == 'k') ADVANCE(33);
      END_STATE();
    case 37:
      if (lookahead == 'l') ADVANCE(31);
      END_STATE();
    case 38:
      if (lookahead == 'l') ADVANCE(34);
      END_STATE();
    case 39:
      if (lookahead == 'o') ADVANCE(41);
      END_STATE();
    case 40:
      if (lookahead == 's') ADVANCE(32);
      END_STATE();
    case 41:
      if (lookahead == 'u') ADVANCE(40);
      END_STATE();
    case 42:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(63);
      END_STATE();
    case 43:
      if (eof) ADVANCE(44);
      if (lookahead == '"') ADVANCE(3);
      if (lookahead == '\'') ADVANCE(4);
      if (lookahead == 'A') ADVANCE(10);
      if (lookahead == 'F') ADVANCE(14);
      if (lookahead == 'O') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(15);
      if (lookahead == 'W') ADVANCE(12);
      if (lookahead == 'c') ADVANCE(38);
      if (lookahead == 'f') ADVANCE(35);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(43)
      END_STATE();
    case 44:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 45:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 46:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(anon_sym_EQ);
      END_STATE();
    case 48:
      ACCEPT_TOKEN(sym_with);
      END_STATE();
    case 49:
      ACCEPT_TOKEN(sym_plot);
      END_STATE();
    case 50:
      ACCEPT_TOKEN(sym_against);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(sym_as);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(sym_filter);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(sym_and);
      END_STATE();
    case 54:
      ACCEPT_TOKEN(sym_or);
      END_STATE();
    case 55:
      ACCEPT_TOKEN(sym_format);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(sym_not);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(sym_null);
      END_STATE();
    case 58:
      ACCEPT_TOKEN(sym_aggregate_func);
      END_STATE();
    case 59:
      ACCEPT_TOKEN(sym_file_connector);
      END_STATE();
    case 60:
      ACCEPT_TOKEN(sym_clickhouse_connector);
      END_STATE();
    case 61:
      ACCEPT_TOKEN(aux_sym_string_token1);
      END_STATE();
    case 62:
      ACCEPT_TOKEN(aux_sym_string_token2);
      END_STATE();
    case 63:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(64);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(63);
      END_STATE();
    case 64:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(64);
      END_STATE();
    case 65:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'A') ADVANCE(71);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 66:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'A') ADVANCE(90);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 67:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'D') ADVANCE(53);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 68:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'E') ADVANCE(84);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 69:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'G') ADVANCE(65);
      if (lookahead == 'N') ADVANCE(67);
      if (lookahead == 'S') ADVANCE(51);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 70:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'H') ADVANCE(48);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 71:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I') ADVANCE(79);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 72:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I') ADVANCE(76);
      if (lookahead == 'O') ADVANCE(83);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 73:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'I') ADVANCE(87);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 74:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(81);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 75:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(57);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 76:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(88);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 77:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'L') ADVANCE(75);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 78:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'M') ADVANCE(66);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 79:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'N') ADVANCE(85);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 80:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O') ADVANCE(86);
      if (lookahead == 'U') ADVANCE(77);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 81:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'O') ADVANCE(89);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 82:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R') ADVANCE(54);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 83:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R') ADVANCE(78);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 84:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'R') ADVANCE(52);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 85:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'S') ADVANCE(91);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 86:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(56);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 87:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(70);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 88:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(68);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 89:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(49);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 90:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(55);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 91:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'T') ADVANCE(50);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 92:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'U') ADVANCE(77);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 93:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'a') ADVANCE(118);
      if (lookahead == 'e') ADVANCE(96);
      if (lookahead == 'i') ADVANCE(108);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 94:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'a') ADVANCE(108);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 95:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'c') ADVANCE(104);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 96:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'd') ADVANCE(103);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 97:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(59);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 98:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'e') ADVANCE(60);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 99:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'g') ADVANCE(58);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 100:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'h') ADVANCE(111);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 101:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'i') ADVANCE(105);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 102:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'i') ADVANCE(95);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 103:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'i') ADVANCE(94);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 104:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'k') ADVANCE(100);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 105:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'l') ADVANCE(97);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 106:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'l') ADVANCE(102);
      if (lookahead == 'o') ADVANCE(116);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 107:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'm') ADVANCE(58);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 108:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(58);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 109:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'n') ADVANCE(113);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 110:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(116);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 111:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'o') ADVANCE(115);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 112:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 's') ADVANCE(98);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 113:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 't') ADVANCE(58);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 114:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'u') ADVANCE(107);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 115:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'u') ADVANCE(112);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 116:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'u') ADVANCE(109);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 117:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'v') ADVANCE(99);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 118:
      ACCEPT_TOKEN(sym_identifier);
      if (lookahead == 'x') ADVANCE(58);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 119:
      ACCEPT_TOKEN(sym_identifier);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(119);
      END_STATE();
    case 120:
      ACCEPT_TOKEN(anon_sym_LT_EQ);
      END_STATE();
    case 121:
      ACCEPT_TOKEN(anon_sym_GT_EQ);
      END_STATE();
    case 122:
      ACCEPT_TOKEN(anon_sym_BANG_EQ);
      END_STATE();
    case 123:
      ACCEPT_TOKEN(anon_sym_LT);
      if (lookahead == '=') ADVANCE(120);
      END_STATE();
    case 124:
      ACCEPT_TOKEN(anon_sym_GT);
      if (lookahead == '=') ADVANCE(121);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 43},
  [2] = {.lex_state = 0},
  [3] = {.lex_state = 43},
  [4] = {.lex_state = 43},
  [5] = {.lex_state = 43},
  [6] = {.lex_state = 43},
  [7] = {.lex_state = 1},
  [8] = {.lex_state = 43},
  [9] = {.lex_state = 43},
  [10] = {.lex_state = 43},
  [11] = {.lex_state = 43},
  [12] = {.lex_state = 43},
  [13] = {.lex_state = 43},
  [14] = {.lex_state = 43},
  [15] = {.lex_state = 43},
  [16] = {.lex_state = 43},
  [17] = {.lex_state = 2},
  [18] = {.lex_state = 43},
  [19] = {.lex_state = 43},
  [20] = {.lex_state = 43},
  [21] = {.lex_state = 29},
  [22] = {.lex_state = 29},
  [23] = {.lex_state = 43},
  [24] = {.lex_state = 43},
  [25] = {.lex_state = 2},
  [26] = {.lex_state = 43},
  [27] = {.lex_state = 43},
  [28] = {.lex_state = 0},
  [29] = {.lex_state = 43},
  [30] = {.lex_state = 2},
  [31] = {.lex_state = 43},
  [32] = {.lex_state = 2},
  [33] = {.lex_state = 43},
  [34] = {.lex_state = 2},
  [35] = {.lex_state = 2},
  [36] = {.lex_state = 43},
  [37] = {.lex_state = 0},
  [38] = {.lex_state = 0},
  [39] = {.lex_state = 0},
  [40] = {.lex_state = 2},
  [41] = {.lex_state = 0},
  [42] = {.lex_state = 43},
  [43] = {.lex_state = 0},
  [44] = {.lex_state = 2},
  [45] = {.lex_state = 43},
  [46] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [anon_sym_EQ] = ACTIONS(1),
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
    [sym_file_connector] = ACTIONS(1),
    [sym_clickhouse_connector] = ACTIONS(1),
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
    [sym_query] = STATE(39),
    [sym_with_clause] = STATE(26),
    [sym_with] = ACTIONS(3),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 3,
    STATE(17), 1,
      sym_operator,
    ACTIONS(7), 2,
      anon_sym_LT,
      anon_sym_GT,
    ACTIONS(5), 4,
      anon_sym_EQ,
      anon_sym_LT_EQ,
      anon_sym_GT_EQ,
      anon_sym_BANG_EQ,
  [14] = 3,
    STATE(3), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(11), 2,
      sym_and,
      sym_or,
    ACTIONS(9), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_format,
  [27] = 3,
    ACTIONS(14), 2,
      sym_file_connector,
      sym_clickhouse_connector,
    ACTIONS(16), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
    STATE(45), 2,
      sym_connector_call,
      sym_string,
  [40] = 3,
    STATE(11), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(20), 2,
      sym_and,
      sym_or,
    ACTIONS(18), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_format,
  [53] = 1,
    ACTIONS(22), 6,
      ts_builtin_sym_end,
      sym_plot,
      sym_filter,
      sym_and,
      sym_or,
      sym_format,
  [62] = 4,
    ACTIONS(26), 1,
      sym_identifier,
    STATE(27), 1,
      sym_string,
    ACTIONS(16), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
    ACTIONS(24), 2,
      sym_null,
      sym_number,
  [77] = 1,
    ACTIONS(28), 6,
      ts_builtin_sym_end,
      sym_plot,
      sym_against,
      sym_as,
      sym_filter,
      sym_format,
  [86] = 5,
    ACTIONS(32), 1,
      sym_filter,
    ACTIONS(34), 1,
      sym_format,
    STATE(18), 1,
      sym_filter_clause,
    STATE(33), 1,
      sym_format_clause,
    ACTIONS(30), 2,
      ts_builtin_sym_end,
      sym_plot,
  [103] = 1,
    ACTIONS(36), 6,
      ts_builtin_sym_end,
      sym_plot,
      sym_against,
      sym_as,
      sym_filter,
      sym_format,
  [112] = 3,
    STATE(3), 1,
      aux_sym_filter_clause_repeat1,
    ACTIONS(20), 2,
      sym_and,
      sym_or,
    ACTIONS(38), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_format,
  [125] = 1,
    ACTIONS(9), 5,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
      sym_or,
      sym_format,
  [133] = 4,
    ACTIONS(40), 1,
      ts_builtin_sym_end,
    ACTIONS(42), 1,
      sym_plot,
    STATE(9), 1,
      sym_plot_clause,
    STATE(15), 2,
      sym_series_clause,
      aux_sym_query_repeat1,
  [147] = 1,
    ACTIONS(44), 5,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
      sym_or,
      sym_format,
  [155] = 4,
    ACTIONS(46), 1,
      ts_builtin_sym_end,
    ACTIONS(48), 1,
      sym_plot,
    STATE(9), 1,
      sym_plot_clause,
    STATE(15), 2,
      sym_series_clause,
      aux_sym_query_repeat1,
  [169] = 2,
    ACTIONS(53), 1,
      sym_as,
    ACTIONS(51), 4,
      ts_builtin_sym_end,
      sym_plot,
      sym_filter,
      sym_format,
  [179] = 3,
    STATE(14), 1,
      sym_string,
    ACTIONS(16), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
    ACTIONS(55), 2,
      sym_number,
      sym_identifier,
  [191] = 3,
    ACTIONS(34), 1,
      sym_format,
    STATE(31), 1,
      sym_format_clause,
    ACTIONS(57), 2,
      ts_builtin_sym_end,
      sym_plot,
  [202] = 1,
    ACTIONS(59), 4,
      ts_builtin_sym_end,
      sym_plot,
      sym_filter,
      sym_format,
  [209] = 3,
    ACTIONS(63), 1,
      sym_and,
    STATE(23), 1,
      aux_sym_format_clause_repeat1,
    ACTIONS(61), 2,
      ts_builtin_sym_end,
      sym_plot,
  [220] = 4,
    ACTIONS(65), 1,
      sym_aggregate_func,
    ACTIONS(67), 1,
      sym_identifier,
    STATE(10), 1,
      sym_aggregate_call,
    STATE(42), 1,
      sym_column_ref,
  [233] = 4,
    ACTIONS(65), 1,
      sym_aggregate_func,
    ACTIONS(67), 1,
      sym_identifier,
    STATE(10), 1,
      sym_aggregate_call,
    STATE(16), 1,
      sym_column_ref,
  [246] = 3,
    ACTIONS(71), 1,
      sym_and,
    STATE(23), 1,
      aux_sym_format_clause_repeat1,
    ACTIONS(69), 2,
      ts_builtin_sym_end,
      sym_plot,
  [257] = 3,
    ACTIONS(63), 1,
      sym_and,
    STATE(20), 1,
      aux_sym_format_clause_repeat1,
    ACTIONS(74), 2,
      ts_builtin_sym_end,
      sym_plot,
  [268] = 1,
    ACTIONS(76), 4,
      aux_sym_string_token1,
      aux_sym_string_token2,
      sym_number,
      sym_identifier,
  [275] = 3,
    ACTIONS(42), 1,
      sym_plot,
    STATE(9), 1,
      sym_plot_clause,
    STATE(13), 2,
      sym_series_clause,
      aux_sym_query_repeat1,
  [286] = 1,
    ACTIONS(78), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
  [292] = 2,
    STATE(19), 1,
      sym_string,
    ACTIONS(16), 2,
      aux_sym_string_token1,
      aux_sym_string_token2,
  [300] = 1,
    ACTIONS(69), 3,
      ts_builtin_sym_end,
      sym_plot,
      sym_and,
  [306] = 2,
    ACTIONS(80), 1,
      sym_identifier,
    STATE(12), 1,
      sym_condition,
  [313] = 1,
    ACTIONS(82), 2,
      ts_builtin_sym_end,
      sym_plot,
  [318] = 2,
    ACTIONS(84), 1,
      sym_identifier,
    STATE(29), 1,
      sym_format_option,
  [325] = 1,
    ACTIONS(57), 2,
      ts_builtin_sym_end,
      sym_plot,
  [330] = 2,
    ACTIONS(84), 1,
      sym_identifier,
    STATE(24), 1,
      sym_format_option,
  [337] = 2,
    ACTIONS(80), 1,
      sym_identifier,
    STATE(5), 1,
      sym_condition,
  [344] = 1,
    ACTIONS(86), 1,
      sym_plot,
  [348] = 1,
    ACTIONS(88), 1,
      anon_sym_RPAREN,
  [352] = 1,
    ACTIONS(90), 1,
      anon_sym_EQ,
  [356] = 1,
    ACTIONS(92), 1,
      ts_builtin_sym_end,
  [360] = 1,
    ACTIONS(94), 1,
      sym_identifier,
  [364] = 1,
    ACTIONS(96), 1,
      anon_sym_RPAREN,
  [368] = 1,
    ACTIONS(98), 1,
      sym_against,
  [372] = 1,
    ACTIONS(100), 1,
      anon_sym_LPAREN,
  [376] = 1,
    ACTIONS(102), 1,
      sym_identifier,
  [380] = 1,
    ACTIONS(104), 1,
      sym_plot,
  [384] = 1,
    ACTIONS(106), 1,
      anon_sym_LPAREN,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 14,
  [SMALL_STATE(4)] = 27,
  [SMALL_STATE(5)] = 40,
  [SMALL_STATE(6)] = 53,
  [SMALL_STATE(7)] = 62,
  [SMALL_STATE(8)] = 77,
  [SMALL_STATE(9)] = 86,
  [SMALL_STATE(10)] = 103,
  [SMALL_STATE(11)] = 112,
  [SMALL_STATE(12)] = 125,
  [SMALL_STATE(13)] = 133,
  [SMALL_STATE(14)] = 147,
  [SMALL_STATE(15)] = 155,
  [SMALL_STATE(16)] = 169,
  [SMALL_STATE(17)] = 179,
  [SMALL_STATE(18)] = 191,
  [SMALL_STATE(19)] = 202,
  [SMALL_STATE(20)] = 209,
  [SMALL_STATE(21)] = 220,
  [SMALL_STATE(22)] = 233,
  [SMALL_STATE(23)] = 246,
  [SMALL_STATE(24)] = 257,
  [SMALL_STATE(25)] = 268,
  [SMALL_STATE(26)] = 275,
  [SMALL_STATE(27)] = 286,
  [SMALL_STATE(28)] = 292,
  [SMALL_STATE(29)] = 300,
  [SMALL_STATE(30)] = 306,
  [SMALL_STATE(31)] = 313,
  [SMALL_STATE(32)] = 318,
  [SMALL_STATE(33)] = 325,
  [SMALL_STATE(34)] = 330,
  [SMALL_STATE(35)] = 337,
  [SMALL_STATE(36)] = 344,
  [SMALL_STATE(37)] = 348,
  [SMALL_STATE(38)] = 352,
  [SMALL_STATE(39)] = 356,
  [SMALL_STATE(40)] = 360,
  [SMALL_STATE(41)] = 364,
  [SMALL_STATE(42)] = 368,
  [SMALL_STATE(43)] = 372,
  [SMALL_STATE(44)] = 376,
  [SMALL_STATE(45)] = 380,
  [SMALL_STATE(46)] = 384,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT(4),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(25),
  [7] = {.entry = {.count = 1, .reusable = false}}, SHIFT(25),
  [9] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_filter_clause_repeat1, 2),
  [11] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_filter_clause_repeat1, 2), SHIFT_REPEAT(30),
  [14] = {.entry = {.count = 1, .reusable = true}}, SHIFT(46),
  [16] = {.entry = {.count = 1, .reusable = true}}, SHIFT(6),
  [18] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_filter_clause, 2),
  [20] = {.entry = {.count = 1, .reusable = true}}, SHIFT(30),
  [22] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_string, 1),
  [24] = {.entry = {.count = 1, .reusable = true}}, SHIFT(27),
  [26] = {.entry = {.count = 1, .reusable = false}}, SHIFT(27),
  [28] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_aggregate_call, 4),
  [30] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_series_clause, 1),
  [32] = {.entry = {.count = 1, .reusable = true}}, SHIFT(35),
  [34] = {.entry = {.count = 1, .reusable = true}}, SHIFT(34),
  [36] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_column_ref, 1),
  [38] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_filter_clause, 3),
  [40] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_query, 2),
  [42] = {.entry = {.count = 1, .reusable = true}}, SHIFT(21),
  [44] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_condition, 3),
  [46] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_query_repeat1, 2),
  [48] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_query_repeat1, 2), SHIFT_REPEAT(21),
  [51] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_plot_clause, 4),
  [53] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [55] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [57] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_series_clause, 2),
  [59] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_plot_clause, 6),
  [61] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_clause, 3),
  [63] = {.entry = {.count = 1, .reusable = true}}, SHIFT(32),
  [65] = {.entry = {.count = 1, .reusable = true}}, SHIFT(43),
  [67] = {.entry = {.count = 1, .reusable = false}}, SHIFT(10),
  [69] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_format_clause_repeat1, 2),
  [71] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_format_clause_repeat1, 2), SHIFT_REPEAT(32),
  [74] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_clause, 2),
  [76] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_operator, 1),
  [78] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_format_option, 3),
  [80] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [82] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_series_clause, 3),
  [84] = {.entry = {.count = 1, .reusable = true}}, SHIFT(38),
  [86] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_connector_call, 4),
  [88] = {.entry = {.count = 1, .reusable = true}}, SHIFT(8),
  [90] = {.entry = {.count = 1, .reusable = true}}, SHIFT(7),
  [92] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [94] = {.entry = {.count = 1, .reusable = true}}, SHIFT(37),
  [96] = {.entry = {.count = 1, .reusable = true}}, SHIFT(36),
  [98] = {.entry = {.count = 1, .reusable = true}}, SHIFT(22),
  [100] = {.entry = {.count = 1, .reusable = true}}, SHIFT(40),
  [102] = {.entry = {.count = 1, .reusable = true}}, SHIFT(41),
  [104] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_with_clause, 2),
  [106] = {.entry = {.count = 1, .reusable = true}}, SHIFT(44),
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
