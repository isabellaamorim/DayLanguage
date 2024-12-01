# DayLanguage

## EBNF 
DAY = 'day' '{' STATEMENT_LIST '}';

STATEMENT_LIST = { STATEMENT };

STATEMENT = ASSIGNMENT_STATEMENT | TASK_STATEMENT | FLOW_STATEMENT;

ASSIGNMENT_STATEMENT = IDENTIFIER '=' EXPRESSION ';';

TASK_STATEMENT = IDENTIFIER [ '(' PARAMETER_LIST ')' ] ';';

FLOW_STATEMENT = IF_STATEMENT | REPEAT_STATEMENT;

IF_STATEMENT = 'if' CONDITION '{' STATEMENT_LIST '}';

REPEAT_STATEMENT = 'repeat' NUMBER 'times' '{' STATEMENT_LIST '}';

CONDITION = EXPRESSION COMPARISON_OPERATOR EXPRESSION;

COMPARISON_OPERATOR = '>' | '<' | '==' | '!=' | '>=' | '<=';

EXPRESSION = NUMBER | STRING | IDENTIFIER;

PARAMETER_LIST = PARAMETER { ',' PARAMETER };

PARAMETER = IDENTIFIER '=' EXPRESSION;

IDENTIFIER = LETTER { LETTER | DIGIT | '_' };

NUMBER = DIGIT { DIGIT };

STRING = '"' { ANY_CHARACTER - '"' } '"';

LETTER = 'a' | ... | 'z' | 'A' | ... | 'Z';

DIGIT = '0' | ... | '9';

ANY_CHARACTER = qualquer caractere;

## Flex e Bison 

Este projeto utiliza as ferramentas Flex e Bison para implementar um analisador léxico e sintático conforme especificado pela gramática EBNF da linguagem. 

O arquivo tokenizer.l contém as definições léxicas utilizadas pelo Flex.

O arquivo parser.y contém as definições sintáticas utilizadas pelo Bison. 

Para executar o analisador, utilize ./parser < *Arquivo de teste* em um ambiente Linux. 

Na pasta, há 5 arquivos .txt para serem usados como testes. 
