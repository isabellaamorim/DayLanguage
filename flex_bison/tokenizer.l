%{
#include "parser.tab.h"
#include <string.h>
#include <stdlib.h>
%}

%%

"day"           { return DAY; }
"if"            { return IF; }
"repeat"        { return REPEAT; }
"times"         { return TIMES; }

"=="            { return EQ; }
"!="            { return NEQ; }
">="            { return GTE; }
"<="            { return LTE; }
">"             { return GT; }
"<"             { return LT; }
"="             { return ASSIGN; }

"{"             { return LBRACE; }
"}"             { return RBRACE; }
"("             { return LPAREN; }
")"             { return RPAREN; }
";"             { return SEMICOLON; }
","             { return COMMA; }

\"(\\.|[^\\"])*\"      { yylval.str = strdup(yytext); return STRING; }

[0-9]+                 { yylval.num = atoi(yytext); return NUMBER; }
[a-zA-Z_][a-zA-Z0-9_]* { yylval.str = strdup(yytext); return IDENTIFIER; }

[ \t\r\n]+             { /* Ignorar espaços em branco */ }

.                      { printf("Caractere inesperado: %c\n", yytext[0]); }

%%
