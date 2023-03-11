# Details

Date : 2023-03-10 18:03:20

Directory /Users/fengming/Documents/GitHub/dsxindexer

Total : 48 files,  1592 codes, 743 comments, 311 blanks, all 2646 lines

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [README.md](/README.md) | Markdown | 41 | 0 | 3 | 44 |
| [pyproject.toml](/pyproject.toml) | toml | 17 | 0 | 1 | 18 |
| [setup.cfg](/setup.cfg) | Properties | 6 | 0 | 3 | 9 |
| [setup.py](/setup.py) | Python | 21 | 3 | 5 | 29 |
| [src/dsxindexer/configer.py](/src/dsxindexer/configer.py) | Python | 62 | 35 | 9 | 106 |
| [src/dsxindexer/factors/base_factor.py](/src/dsxindexer/factors/base_factor.py) | Python | 11 | 1 | 3 | 15 |
| [src/dsxindexer/factors/float_factor.py](/src/dsxindexer/factors/float_factor.py) | Python | 8 | 2 | 5 | 15 |
| [src/dsxindexer/factors/function_factor.py](/src/dsxindexer/factors/function_factor.py) | Python | 105 | 36 | 9 | 150 |
| [src/dsxindexer/factors/int_factor.py](/src/dsxindexer/factors/int_factor.py) | Python | 8 | 2 | 5 | 15 |
| [src/dsxindexer/factors/lparen_factor.py](/src/dsxindexer/factors/lparen_factor.py) | Python | 17 | 11 | 6 | 34 |
| [src/dsxindexer/factors/newline_factor.py](/src/dsxindexer/factors/newline_factor.py) | Python | 9 | 3 | 4 | 16 |
| [src/dsxindexer/factors/string_factor.py](/src/dsxindexer/factors/string_factor.py) | Python | 8 | 2 | 4 | 14 |
| [src/dsxindexer/factors/variable_factor.py](/src/dsxindexer/factors/variable_factor.py) | Python | 25 | 11 | 6 | 42 |
| [src/dsxindexer/functioner.py](/src/dsxindexer/functioner.py) | Python | 86 | 21 | 20 | 127 |
| [src/dsxindexer/operators/andor_operator.py](/src/dsxindexer/operators/andor_operator.py) | Python | 23 | 2 | 3 | 28 |
| [src/dsxindexer/operators/base_operator.py](/src/dsxindexer/operators/base_operator.py) | Python | 12 | 1 | 3 | 16 |
| [src/dsxindexer/operators/equal_operator.py](/src/dsxindexer/operators/equal_operator.py) | Python | 26 | 9 | 4 | 39 |
| [src/dsxindexer/operators/grealess_operator.py](/src/dsxindexer/operators/grealess_operator.py) | Python | 31 | 2 | 3 | 36 |
| [src/dsxindexer/operators/greaterthen_operator.py](/src/dsxindexer/operators/greaterthen_operator.py) | Python | 18 | 4 | 3 | 25 |
| [src/dsxindexer/operators/muldiv_operator.py](/src/dsxindexer/operators/muldiv_operator.py) | Python | 29 | 2 | 4 | 35 |
| [src/dsxindexer/operators/plusminus_operator.py](/src/dsxindexer/operators/plusminus_operator.py) | Python | 30 | 2 | 4 | 36 |
| [src/dsxindexer/parser.py](/src/dsxindexer/parser.py) | Python | 49 | 35 | 11 | 95 |
| [src/dsxindexer/processors/base_processor.py](/src/dsxindexer/processors/base_processor.py) | Python | 26 | 12 | 10 | 48 |
| [src/dsxindexer/processors/factor_processor.py](/src/dsxindexer/processors/factor_processor.py) | Python | 27 | 2 | 5 | 34 |
| [src/dsxindexer/processors/operator_processor.py](/src/dsxindexer/processors/operator_processor.py) | Python | 24 | 6 | 5 | 35 |
| [src/dsxindexer/processors/sindexer_processor.py](/src/dsxindexer/processors/sindexer_processor.py) | Python | 81 | 25 | 14 | 120 |
| [src/dsxindexer/sindexer/BOLL.py](/src/dsxindexer/sindexer/BOLL.py) | Python | 10 | 18 | 3 | 31 |
| [src/dsxindexer/sindexer/CCI.py](/src/dsxindexer/sindexer/CCI.py) | Python | 10 | 17 | 3 | 30 |
| [src/dsxindexer/sindexer/DMI.py](/src/dsxindexer/sindexer/DMI.py) | Python | 10 | 14 | 3 | 27 |
| [src/dsxindexer/sindexer/EMA.py](/src/dsxindexer/sindexer/EMA.py) | Python | 18 | 15 | 4 | 37 |
| [src/dsxindexer/sindexer/KDJ.py](/src/dsxindexer/sindexer/KDJ.py) | Python | 11 | 7 | 3 | 21 |
| [src/dsxindexer/sindexer/MA.py](/src/dsxindexer/sindexer/MA.py) | Python | 17 | 5 | 3 | 25 |
| [src/dsxindexer/sindexer/MACD.py](/src/dsxindexer/sindexer/MACD.py) | Python | 13 | 6 | 4 | 23 |
| [src/dsxindexer/sindexer/RSI.py](/src/dsxindexer/sindexer/RSI.py) | Python | 10 | 10 | 3 | 23 |
| [src/dsxindexer/sindexer/SMA.py](/src/dsxindexer/sindexer/SMA.py) | Python | 14 | 12 | 3 | 29 |
| [src/dsxindexer/sindexer/WR.py](/src/dsxindexer/sindexer/WR.py) | Python | 10 | 7 | 3 | 20 |
| [src/dsxindexer/sindexer/base/cons_funcs.py](/src/dsxindexer/sindexer/base/cons_funcs.py) | Python | 5 | 27 | 3 | 35 |
| [src/dsxindexer/sindexer/base/index_funcs.py](/src/dsxindexer/sindexer/base/index_funcs.py) | Python | 18 | 44 | 4 | 66 |
| [src/dsxindexer/sindexer/base/logical_funcs.py](/src/dsxindexer/sindexer/base/logical_funcs.py) | Python | 9 | 3 | 1 | 13 |
| [src/dsxindexer/sindexer/base/math_funcs.py](/src/dsxindexer/sindexer/base/math_funcs.py) | Python | 65 | 39 | 10 | 114 |
| [src/dsxindexer/sindexer/base/price_funcs.py](/src/dsxindexer/sindexer/base/price_funcs.py) | Python | 43 | 39 | 1 | 83 |
| [src/dsxindexer/sindexer/base/refer_funcs.py](/src/dsxindexer/sindexer/base/refer_funcs.py) | Python | 39 | 62 | 7 | 108 |
| [src/dsxindexer/sindexer/base_sindexer.py](/src/dsxindexer/sindexer/base_sindexer.py) | Python | 161 | 51 | 36 | 248 |
| [src/dsxindexer/sindexer/fomulas.py](/src/dsxindexer/sindexer/fomulas.py) | Python | 27 | 49 | 10 | 86 |
| [src/dsxindexer/sindexer/models/kline_model.py](/src/dsxindexer/sindexer/models/kline_model.py) | Python | 16 | 0 | 1 | 17 |
| [src/dsxindexer/sindexer/sindexer_factory.py](/src/dsxindexer/sindexer/sindexer_factory.py) | Python | 13 | 0 | 4 | 17 |
| [src/dsxindexer/tokenizer.py](/src/dsxindexer/tokenizer.py) | Python | 211 | 57 | 42 | 310 |
| [src/test.py](/src/test.py) | Python | 62 | 32 | 8 | 102 |

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)