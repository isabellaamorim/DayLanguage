%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);
%}

%union {
    char* str;
    int num;
}

%token <str> IDENTIFIER STRING
%token <num> NUMBER
%token DAY IF REPEAT TIMES
%token LBRACE RBRACE LPAREN RPAREN SEMICOLON COMMA
%token ASSIGN EQ NEQ GTE LTE GT LT

%type <str> expression comparison_operator condition

%%

program:
    DAY LBRACE statement_list RBRACE
    ;

statement_list:
    statement_list statement
    | /* vazio */
    ;

statement:
    assignment_statement
    | task_statement
    | flow_statement
    ;

assignment_statement:
    IDENTIFIER ASSIGN expression SEMICOLON
        {
            printf("Atribuição: %s = %s\n", $1, $3);
            free($1);
            free($3);
        }
    ;

task_statement:
    IDENTIFIER LPAREN parameter_list RPAREN SEMICOLON
        {
            printf("Tarefa: %s com parâmetros\n", $1);
            free($1);
        }
    | IDENTIFIER LPAREN RPAREN SEMICOLON
        {
            printf("Tarefa: %s sem parâmetros\n", $1);
            free($1);
        }
    | IDENTIFIER SEMICOLON
        {
            printf("Tarefa: %s\n", $1);
            free($1);
        }
    ;

parameter_list:
    parameter_list COMMA parameter
    | parameter
    ;

parameter:
    IDENTIFIER ASSIGN expression
        {
            printf("Parâmetro: %s = %s\n", $1, $3);
            free($1);
            free($3);
        }
    ;

flow_statement:
    if_statement
    | repeat_statement
    ;

if_statement:
    IF condition LBRACE statement_list RBRACE
        {
            printf("Estrutura condicional \n");
        }
    ;

repeat_statement:
    REPEAT NUMBER TIMES LBRACE statement_list RBRACE
        {
            printf("Estrutura de repetição \n");
        }
    ;

condition:
    expression comparison_operator expression
        {
            printf("Condição: %s %s %s\n", $1, $2, $3);
            free($1);
            free($2);
            free($3);
        }
    ;

comparison_operator:
    EQ   { $$ = strdup("=="); }
    | NEQ { $$ = strdup("!="); }
    | GTE { $$ = strdup(">="); }
    | LTE { $$ = strdup("<="); }
    | GT  { $$ = strdup(">"); }
    | LT  { $$ = strdup("<"); }
    ;

expression:
    NUMBER
        {
            char buffer[20];
            sprintf(buffer, "%d", $1);
            $$ = strdup(buffer);
        }
    | STRING
        {
            $$ = strdup($1);
            free($1);
        }
    | IDENTIFIER
        {
            $$ = strdup($1);
            free($1);
        }
    ;

%%

int main(void) {
    return yyparse();
}

void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s\n", s);
}
