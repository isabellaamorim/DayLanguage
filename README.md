# DayLanguage
Linguagem para programar tarefas diárias.

Vídeo: https://youtu.be/pE6zjqpH7S0

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

## Compilador 

O compilador da DayLanguage foi feito em Python, baseado no compilador desenvolvido na disciplina. Para rodá-lo, execute o código 'main.py' na pasta 'compilador'. Nessa pasta, há 5 arquivos .txt para serem usados como testes. Altere a variável 'filename' na main para testar esses múltiplos programas. 

## Conjunto de Testes

test1.txt - programa funcional com 2 variáveis, 4 tasks (uma com parâmetros), condicionais e repeat   
```
day {
    tasksPending = 1;
    time = 17;

    checkEmails();

    if tasksPending > 0 {
        completeTasks(priority="high");
    }

    repeat 3 times {
        attendMeeting();
    }
    
    if time < 18 {
        scheduleNextDay();
    }
}
```

test2.txt - programa funcional com 3 tasks

```
day {
    startDay();
    checkCalendar();
    endDay();
}
```

test3.txt - programa com erro de sintaxe (sem aspas fechando string)

```
day {
    message = "Incomplete string;
    notifyUser(message=message);
}
```

test4.txt - programa com erro de semântica (não declarou as variáveis)

```
day {

    if tasksCompleted != totalTasks {
        notifyUser(message="Tasks remaining");
    }
    if timeSpent <= totalTime {
        takeBreak();
    }
}
```

test5.txt - programa funcional com repeat alinhado (executará a tarefa 6 vezes)

```
day {
    repeat 2 times {
        repeat 3 times {
            logActivity();
        }
    }
}
```

## Autoria

Por Isabella Amorim e Ana Laiz 


