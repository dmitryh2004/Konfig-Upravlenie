import json
from sly import Lexer, Parser

"""
files ::= file files | empty
file ::  group student lesson 
group :: "(" "^" name names  ")"
lesson ::= "(" title ")"
student ::= "(" "@" charac characs ")"
title ::= name
"""


class CalcLexer(Lexer):
    tokens = {BEGIN, END, NAME, STRING, DIGIT, GROUP_IND, STUDENT_IND}

    # Tokens
    BEGIN = r'\('
    END = r'\)'
    ignore = r' \t'
    ignore_newline = r'\n+'
    ignore_comment = r'\#.*'
    NAME = r'[^ \t\#();\'\@\^]+'
    STRING = r"'[^\:\)\()\t\']*'"
    DIGIT = r'[0-9]+'
    GROUP_IND = r'\^'
    STUDENT_IND = r'\@'


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    @_('empty')
    def files(self, p):
        return []

    @_('file files')
    def files(self, p):
        return [p.file] + p.files

    @_('group student lesson')
    def file(self, p):
        return dict(groups=p.group, students=p.student, subject=p.lesson)

    @_("BEGIN title END")
    def lesson(self, p):
        return (p.title[1:-1])

    @_("BEGIN STUDENT_IND charac characs  END")
    def student(self, p):
        return [
            dict(age=int((p.charac[:-1])[0:2]), group=((p.charac[1:-1])[2:12]),
                 name=((p.charac[1:])[12:]))] + p.characs

    @_("BEGIN GROUP_IND name names  END")
    def group(self, p):
        return [p.name] + p.names

    @_('charac characs')
    def characs(self, p):
        return [dict(age=int((p.charac[0:-1])[0:2]), group=((p.charac[1:])[2:12]),
                     name=((p.charac[1:])[12:]))] + p.characs

    @_('STRING')
    def charac(self, p):
        return p[0][1:-1]

    @_('name')
    def title(self, p):
        return '"' + p.name + "'"

    @_('name names')
    def names(self, p):
        return [p.name] + p.names

    @_('empty')
    def characs(self, p):
        return []

    @_('empty')
    def names(self, p):
        return []

    @_('DIGIT')
    def name(self, p):
        return int(p[0])

    @_('NAME')
    def name(self, p):
        return p[0]

    @_('STRING')
    def name(self, p):
        return p[0][1:-1]

    @_('')
    def empty(self, p):
        pass


if __name__ == '__main__':
    data = ""
    with open("input.txt", "r", encoding="utf-8") as inputfile:
        for line in inputfile:
            data += line

    lexer = CalcLexer()
    parser = CalcParser()
    parser_output = parser.parse(lexer.tokenize(data))

    with open("output.json", "w", encoding="utf-8") as jsonfile:
        jsonfile.write(json.dumps(parser_output, indent=4, ensure_ascii=False))

    with open("output.json", "r", encoding="utf-8") as f:
        for line in f:
            print(line.rstrip())


