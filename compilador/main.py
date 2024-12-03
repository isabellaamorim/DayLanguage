import re
import sys
from abc import ABC, abstractmethod

class Token:
    def __init__(self, type_, value):
        self.type = type_  # Tipo do token
        self.value = value  # Valor do token

# Análise Léxica - Tokenizer
class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0  
        self.current_char = self.text[self.pos] if self.text else None
        self.keywords = {'day', 'if', 'repeat', 'times'} #Palavras reservadas

    # Adianta o ponteiro de posição e seta o token atual
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None     

    def selectNext(self):
        # Ignora espaços
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
                continue

            # == ou assign
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('EQ', '==')
                else:
                    return Token('ASSIGN', '=')

            # !=
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('NE', '!=')
                else:
                    self.error("Expected '!=' after '!'")

            # > ou >=
            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('GE', '>=')
                else:
                    return Token('GT', '>')

            # < ou <=
            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('LE', '<=')
                else:
                    return Token('LT', '<')

            if self.current_char == '{':
                self.advance()
                return Token('LBRACE', '{')
            if self.current_char == '}':
                self.advance()
                return Token('RBRACE', '}')
            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')
            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')
            if self.current_char == ';':
                self.advance()
                return Token('SEMI', ';')
            if self.current_char == ',':
                self.advance()
                return Token('COMMA', ',')

            #String    
            if self.current_char == '"':
                result = ''
                self.advance()  
                while self.current_char is not None and self.current_char != '"':
                    result += self.current_char
                    self.advance()
                if self.current_char == '"':
                    self.advance() 
                    return Token('STRING', result)
                else:
                    self.error("Unterminated string literal")

            # Keywords e identifiers
            if self.current_char.isalpha():
                result = ''
                if self.current_char.isalpha():
                    result += self.current_char
                    self.advance()
                    while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
                        result += self.current_char
                        self.advance()
                    if result in self.keywords:
                        return Token(result.upper(), result)
                    else:
                        return Token('IDENTIFIER', result)
                else:
                    self.error(f"Invalid character '{self.current_char}' at position {self.pos}")

            # Numbers
            if self.current_char.isdigit():
                result = ''
                while self.current_char is not None and self.current_char.isdigit():
                    result += self.current_char
                    self.advance()
                return Token('NUMBER', int(result))

            self.error(f"Unknown character {self.current_char}")

        return Token('EOF', None)

    def error(self, message):
        raise Exception(f"Lexer error: {message}")

    #Salva todos os tokens do input em uma lista
    def tokenize(self):
        tokens = []
        while True:
            token = self.selectNext()
            if token.type == 'EOF':
                break
            tokens.append(token)
        return tokens

# Análise Sintática - Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # Posição na lista de tokens
        self.current_token = self.tokens[self.pos] if self.tokens else None

    # Função para consumir os tokens 
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            self.error(f"Expected token {token_type}, got {self.current_token.type}")

    # Adianta o ponteiro de posição e seta o token atual
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token('EOF', None)

    def error(self, message):
        raise Exception(f"Parser error: {message}")

    # Recebe a lista de tokens e devolve a AST
    def parse(self):
        """Parse 'day { STATEMENT_LIST }'"""
        self.eat('DAY')
        self.eat('LBRACE')
        statements = self.statement_list()
        self.eat('RBRACE')
        return Day(statements)

    def statement_list(self):
        """Parse STATEMENT_LIST"""
        statements = []
        while self.current_token.type != 'RBRACE' and self.current_token.type != 'EOF':
            stmt = self.statement()
            statements.append(stmt)
        return StatementList(statements)

    def statement(self):
        """Parse STATEMENT"""
        if self.current_token.type == 'IDENTIFIER':
            next_token = self.tokens[self.pos + 1]
            if next_token.type == 'ASSIGN':
                stmt = self.assignment_statement()
                self.eat('SEMI')
                return stmt
            else:
                stmt = self.task_statement()
                self.eat('SEMI')
                return stmt
        elif self.current_token.type == 'IF':
            return self.if_statement()
        elif self.current_token.type == 'REPEAT':
            return self.repeat_statement()
        else:
            self.error(f"Unexpected token {self.current_token.type} in statement")

    def assignment_statement(self):
        """Parse ASSIGNMENT_STATEMENT"""
        identifier = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        expr = self.expression()
        return Assignment(identifier, expr)

    def task_statement(self):
        """Parse TASK_STATEMENT"""
        identifier = self.current_token.value
        self.eat('IDENTIFIER')
        params = None
        if self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            if self.current_token.type != 'RPAREN':
                params = self.parameter_list()
            self.eat('RPAREN')
        return Task(identifier, params)

    def parameter_list(self):
        """Parse PARAMETER_LIST"""
        params = [self.parameter()]
        while self.current_token.type == 'COMMA':
            self.eat('COMMA')
            params.append(self.parameter())
        return params

    def parameter(self):
        """Parse PARAMETER"""
        identifier = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        expr = self.expression()
        return Parameter(identifier, expr)

    def if_statement(self):
        """Parse IF_STATEMENT"""
        self.eat('IF')
        condition = self.condition()
        self.eat('LBRACE')
        statements = self.statement_list()
        self.eat('RBRACE')
        return Flow('if', condition, statements)

    def repeat_statement(self):
        """Parse REPEAT_STATEMENT"""
        self.eat('REPEAT')
        number = self.current_token.value
        self.eat('NUMBER')
        self.eat('TIMES')
        self.eat('LBRACE')
        statements = self.statement_list()
        self.eat('RBRACE')
        return Flow('repeat', number, statements)

    def condition(self):
        """Parse CONDITION"""
        left = self.expression()
        if self.current_token.type in ('GT', 'LT', 'EQ', 'NE', 'GE', 'LE'):
            operator = self.current_token.type
            self.advance()
        else:
            self.error("Expected comparison operator in condition")
        right = self.expression()
        return Condition(left, operator, right)

    def expression(self):
        """Parse EXPRESSION"""
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Number(token.value)
        elif token.type == 'STRING':
            self.eat('STRING')
            return String(token.value)
        elif token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            return Variable(token.value)
        else:
            self.error(f"Expected expression, got {token.type}")

# Definição dos nós da AST
class AST:
    pass

class Day(AST):
    def __init__(self, statements):
        self.statements = statements

class StatementList(AST):
    def __init__(self, statements):
        self.statements = statements

class Assignment(AST):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class Task(AST):
    def __init__(self, identifier, params=None):
        self.identifier = identifier #Nome da task
        self.params = params #Parâmetros da task

class Flow(AST):
    def __init__(self, flow_type, condition_or_number, statements):
        self.flow_type = flow_type  # 'if' ou 'repeat'
        self.condition_or_number = condition_or_number  # Condition caso 'if', number caso 'repeat'
        self.statements = statements

class Condition(AST):
    def __init__(self, left, operator, right):
        self.left = left  # Expression
        self.operator = operator  # 'GT', 'LT', 'EQ', 'NE', 'GE', 'LE'
        self.right = right  # Expression

class Parameter(AST):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class Number(AST):
    def __init__(self, value):
        self.value = value

class String(AST):
    def __init__(self, value):
        self.value = value

class Variable(AST):
    def __init__(self, name):
        self.name = name

#Eval da AST
class Evaluator:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}  # Symble Table

    def evaluate(self):
        self.visit(self.ast)

    #Visita um nó da AST, implementando a ação desejada a partir do tipo do nó
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, Exception(f'No visit_{type(node).__name__} method'))
        return visitor(node)

    #Funções de return para o Visitor
    def visit_Day(self, node):
        self.visit(node.statements)

    def visit_StatementList(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_Assignment(self, node):
        value = self.visit(node.expression)
        self.variables[node.identifier] = value
        print(f"Assigned {node.identifier} = {value}")

    def visit_Number(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Variable(self, node):
        value = self.variables.get(node.name)
        if value is None:
            raise Exception(f"Undefined variable '{node.name}'")
        return value

    def visit_Task(self, node):
        if node.params:
            params = {}
            for param in node.params:
                key, value = self.visit(param)
                params[key] = value
            print(f"Executing task '{node.identifier}' with parameters {params}")
        else:
            print(f"Executing task '{node.identifier}'")

    def visit_Parameter(self, node):
        value = self.visit(node.expression)
        return (node.identifier, value)

    def visit_Flow(self, node):
        if node.flow_type == 'if':
            condition_result = self.evaluate_condition(node.condition_or_number)
            if condition_result:
                self.visit(node.statements)
        elif node.flow_type == 'repeat':
            count = int(node.condition_or_number)
            for _ in range(count):
                self.visit(node.statements)

    def evaluate_condition(self, condition):
        left = self.visit(condition.left)
        right = self.visit(condition.right)
        operator = condition.operator
        if operator == 'GT':
            result = left > right
        elif operator == 'LT':
            result = left < right
        elif operator == 'EQ':
            result = left == right
        elif operator == 'NE':
            result = left != right
        elif operator == 'GE':
            result = left >= right
        elif operator == 'LE':
            result = left <= right
        else:
            result = False
        print(f"Evaluating condition: {left} {operator} {right} => {result}")
        return result

def main():
    filename = 'test1.txt'
    
    with open(filename, "r") as file:
        code = file.read()

    # Tokenize 
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()

    # Parse
    parser = Parser(tokens)
    ast = parser.parse()

    # Evaluate a AST
    evaluator = Evaluator(ast)
    evaluator.evaluate()

if __name__ == '__main__':
    main()
