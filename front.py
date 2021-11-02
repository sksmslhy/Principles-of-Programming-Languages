charClass = 0
lexeme = []
nextChar = ""
lexLen = 0
token = 0
nextToken = 0

LETTER = 0
DIGIT = 1
UNKNOWN = 99

INT_LIT = 10
IDENT = 11
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP =22
MUL_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
SEMI_COLON = 27

EOF = -1
index = 0

tokenString = ''
symbolTable = {}

cnt_id = 0
cnt_const = 0
cnt_op = 0

order = 0


# lookup
def lookup(char:str):
    global nextToken
    if char == '(':
        addChar()
        nextToken = LEFT_PAREN
    elif char == ')':
        addChar()
        nextToken = RIGHT_PAREN
    elif char == '+':
        addChar()
        nextToken = ADD_OP
    elif char == '-':
        addChar()
        nextToken = SUB_OP
    elif char == '*':
        addChar()
        nextToken = MUL_OP
    elif char == '/':
        addChar()
        nextToken = DIV_OP
    elif char == ';':
        addChar()
        nextToken = SEMI_COLON
    elif char == ':':
        addChar()
        getChar()
        addChar()
        nextToken = ASSIGN_OP
    else:
        addChar()
        nextToken = EOF
    return nextToken


# addChar : nextChar를 lexeme에 추가하는 함수
def addChar():
    global lexLen, lexeme
    if lexLen <= 100:
        lexeme.append(nextChar)
    else:
        print("ERROR : lexeme is too long")


# getChar : 입력으로부터 다음 번째 문자를 가져와서 그 문자 유형을 결정하는 함수
def getChar():
    global nextChar, charClass, index
    nextChar = input[index]
    index += 1

    if nextChar != EOF:
        if nextChar.isalpha():
            charClass = LETTER
        elif nextChar.isdigit():
            charClass = DIGIT
        else:
            charClass = UNKNOWN
    else:
        charClass = EOF


# getNonBlank -
def getNonBlank():
    while nextChar == ' ':
        getChar()


def lexical():
    global lexLen, nextToken, lexeme, tokenString
    lexLen = 0
    getNonBlank()

    if charClass == LETTER:
        addChar()
        getChar()
        while charClass == LETTER or charClass ==DIGIT:
            addChar()
            getChar()
        nextToken = IDENT
        symbolTable[''.join(lexeme)] = 0

    elif charClass == DIGIT:
        addChar()
        getChar()
        while charClass == DIGIT:
            addChar()
            getChar()
        nextToken = INT_LIT
    elif charClass == UNKNOWN:
        lookup(nextChar)
        getChar()
    elif charClass == EOF:
        nextToken = EOF
        lexeme[:3] = 'EOF'
    print("Next token is : %d  Next lexeme is %s" %(nextToken, ''.join(lexeme)))
    tokenString = ''.join(lexeme)
    lexeme = []
    return nextToken, tokenString


def program(string:str):
    global input, cnt_id, cnt_const, cnt_op
    input = string
    input = list(input)
    input.append(EOF)
    lexical()
    print('Enter <program>')
    statements()
    #print(symbolTable)
    #print("Exit <program>")
    print("ID: %d; CONST: %d; OP: %d;" % (cnt_id, cnt_const, cnt_op))


def statements():
    print("Enter <statements>")
    statement()
    temp()
    #print("Exit <statements>")


def temp():
    print("Enter <temp>")
    if nextToken == SEMI_COLON:
        semi_colon()
        statements()


def statement():
    print("Enter <statement>")
    ident()
    assignment_op()
    expression()
    #print("Exit <statement>")


def expression():
    print("Enter <expression>")
    term()
    term_tail()
    #print("Exit <expression>")


def term_tail():
    print("Enter <term_tail>")
    if nextToken == ADD_OP or nextToken == SUB_OP:
        add_op()
        term()
        term_tail()
    #print("Exit <term_tail>")


def term():
    print("Enter <term>")
    factor()
    factor_tail()
    #print("Exit <term>")


def factor_tail():
    print("Enter <factor_tail>")
    if nextToken == MUL_OP or nextToken == DIV_OP:
        mult_op()
        factor()
        factor_tail()
    #print("Exit <factor_tail>")


def factor():
    print("Enter <factor>")
    if nextToken == LEFT_PAREN:
        left_paren()
        expression()
        right_paren()
    elif nextToken == IDENT:
        ident()
    else:
        const()
    #print("Exit <factor>")


def const():
    global cnt_const
    cnt_const += 1
    print('Enter <const>')
    lexical()
    #print("Exit <const>")


def ident():
    global cnt_id
    cnt_id += 1
    print('Enter <ident>')
    lexical()
    #print("Exit <ident>")


def assignment_op():
    print('Enter <assignment_op>')
    lexical()
    #print("Exit <assignment_op>")


def semi_colon():
    global cnt_op, cnt_id, cnt_const
    print("ID: %d; CONST: %d; OP: %d;"%(cnt_id, cnt_const, cnt_op))
    cnt_id = 0
    cnt_const = 0
    cnt_op = 0
    print('Enter <semi_colon>')
    lexical()
    #print("Exit <semi_colon>")


def add_op():
    global cnt_op, order
    cnt_op += 1
    order += 1
    print('Enter <add_operator>')
    lexical()
    #print("Exit <add_operator>")


def mult_op():
    global cnt_op
    cnt_op += 1
    print('Enter <mult_operator>')
    lexical()
    #print("Exit <mult_operator>")


def left_paren():
    print('Enter <left_paren>')
    lexical()
    #print("Exit <left_paren>")


def right_paren():
    print('Enter <right_paren>')
    lexical()
    #print("Exit <right_paren>")


#program('operand1 := 3 ; operand2 := operand1 + 2 ; target := operand1 + operand2 * 3')
program('operand1 := 3 ; operand2 := operand1 + 2 ; target := (operand1 + operand2) / 30 + 2 * 3')
#program("o1 := 3; o2 = o1 + 2 ; target = (o1 + o2) / 3")


#print(tokenString)
#print(symbolTable)

