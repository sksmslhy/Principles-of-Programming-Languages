import copy
import sys

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
cnt_op_list = []
cnt_const_list = []
cnt_id_list = []

order = 0 # 파스트리 깊이 구해서 연산자끼리 우선 순위 구하기 위해
order_list = [] # 연산자들의 order 저장 용도
line_cnt = 0 # 현재가 몇번째 라인인지
arithmatic_list = []

token_list = ""
lexemes=[]

option = True
state = 0


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
    global lexLen, nextToken, lexeme, tokenString, token_list, lexemes
    lexLen = 0
    getNonBlank()

    if charClass == LETTER:
        addChar()
        getChar()
        while charClass == LETTER or charClass ==DIGIT:
            addChar()
            getChar()
        nextToken = IDENT
        symbolTable[''.join(lexeme)] = "unknown"  # 심볼테이블에 ident 저장

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
    if option == True:  # 옵션으로 텍스트 파일이 주어지지 않을 때 토큰 출력을 위해
        print("Next token is : %d  Next lexeme is %s" % (nextToken, ''.join(lexeme)))
    tokenString = ''.join(lexeme)
    token_list += ''.join(lexeme)
    lexeme = []
    lexemes.append(tokenString)
    return nextToken, tokenString


def program(string:str):
    global input, cnt_id, cnt_const, cnt_op, order, cnt_op_list, cnt_const_list, cnt_id_list
    input = string
    input = list(input)
    input.append(EOF)
    lexical()
    order += 1
    statements()
    order -= 1
    cnt_op_list.append(cnt_op)
    cnt_const_list.append(cnt_const)
    cnt_id_list.append(cnt_id)


def statements():
    global order
    order += 1
    statement()
    order -= 1
    order += 1
    temp()
    order -= 1


def temp():
    global order
    if nextToken == SEMI_COLON:
        order += 1
        semi_colon()
        order -= 1
        order += 1
        statements()
        order -= 1


def statement():
    global order
    order += 1
    ident()
    order -= 1
    order += 1
    assignment_op(':=')
    order -= 1
    order += 1
    expression()
    order -= 1


def expression():
    global order
    order += 1
    term()
    order -= 1
    order += 1
    term_tail()
    order -= 1


def term_tail():
    global order
    if nextToken == ADD_OP:
        order += 1
        add_op('+')
        order -= 1
        term()
        term_tail()
    if nextToken == SUB_OP:
        order += 1
        add_op('-')
        order -= 1
        term()
        term_tail()


def term():
    global order
    order += 1
    factor()
    order -= 1
    order += 1
    factor_tail()
    order -= 1


def factor_tail():
    global order
    if nextToken == MUL_OP:
        order += 1
        mult_op('*')
        order -= 1
        order += 1
        factor()
        order -= 1
        order += 1
        factor_tail()
        order -= 1
    if nextToken == DIV_OP:
        order += 1
        mult_op('/')
        order -= 1
        order += 1
        factor()
        order -= 1
        order += 1
        factor_tail()
        order -= 1


def factor():
    global order
    if nextToken == LEFT_PAREN:
        order += 1
        left_paren()
        order -= 1
        order += 1
        expression()
        order -= 1
        order += 1
        right_paren()
        order -= 1
    elif nextToken == IDENT:
        order += 1
        ident()
        order -= 1
    else:
        order += 1
        const()
        order -= 1


def const():
    global cnt_const
    cnt_const += 1
    lexical()


def ident():
    global cnt_id
    cnt_id += 1
    lexical()


def assignment_op(arithmatic:str):
    global arithmatic_list, order_list, cnt_op
    order_list.append(order)
    arithmatic_list.append(arithmatic)
    cnt_op += 1
    lexical()


def semi_colon():
    global cnt_op, cnt_id, cnt_const, order_list, line_cnt, cnt_op_list, cnt_const_list, cnt_id_list
    cnt_op_list.append(cnt_op)
    cnt_const_list.append(cnt_const)
    cnt_id_list.append(cnt_id)
    cnt_id = 0
    cnt_const = 0
    cnt_op = 0
    lexical()


def add_op(arithmatic:str):
    global cnt_op, order, order_list, arithmatic_list
    order_list.append(order)
    arithmatic_list.append(arithmatic)
    cnt_op += 1
    lexical()


def mult_op(arithmatic:str):
    global cnt_op, order, arithmatic_list, order_list
    order_list.append(order)
    arithmatic_list.append(arithmatic)
    cnt_op += 1
    lexical()


def left_paren():
    lexical()


def right_paren():
    lexical()


def isDigit(arg:str):
    try:
        int(arg)
        return True
    except:
        return False


# 사용자 정의 함수
def add(a, b):
    global state # error가 출력되었는지 안되었는지 판단
    if isDigit(a):
        a = int(a)
    else:
        if symbolTable[a] == 'unknown':
            print('(Error) : 정의되지 않은 변수 %s가 참조됨' % a)
            state += 1
            return
        else : a = int(symbolTable[a])
    if isDigit(b):
        b = int(b)
    else:
        if symbolTable[b] == 'unknown':
            state += 1
            print('(Error) : 정의되지 않은 변수 %s가 참조됨' % b)
            return
        else : b = int(symbolTable[b])
    result = a + b
    return str(result)



def sub(a, b):
    global state  # error가 출력되었는지 안되었는지 판단
    if isDigit(a):
        a = int(a)
    else:
        if symbolTable[a] == 'unknown':
            print('(Error) : 정의되지 않은 변수 %s가 참조됨' % a)
            state += 1
            return
        else:
            a = int(symbolTable[a])
    if isDigit(b):
        b = int(b)
    else:
        if symbolTable[b] == 'unknown':
            print('(Error) : 정의되지 않은 변수 %s가 참조됨' % b)
            state += 1
            return
        else:
            b = int(symbolTable[b])
    result = a - b
    return str(result)



def div(a, b):
    global state  # error가 출력되었는지 안되었는지 판단
    if isDigit(a):
        a = int(a)
    else:
        if symbolTable[a] == 'unknown':
            print('(Error) : 정의되지 않은 변수 %s가 참조됨' % a)
            state += 1
            return
        else:
            a = int(symbolTable[a])
    if isDigit(b):
        b = int(b)
    else:
        if symbolTable[b] == 'unknown':
            print('(Error) : 정의되지 않은 변수 %s가 참조됨' % b)
            state += 1
            return
        else:
            b = int(symbolTable[b])
    result = a // b
    return str(result)


def mul(a, b):
    global state  # error가 출력되었는지 안되었는지 판단
    if isDigit(a):
        a = int(a)
    else:
        if symbolTable[a] == 'unknown':
            print('(Error) : 정의되지 않은 변수 %s가 참조됨' % a)
            state += 1
            return
        else:
            a = int(symbolTable[a])
    if isDigit(b):
        b = int(b)
    else:
        if symbolTable[b] == 'unknown':
            print('(Error) : 정의되지 않은 변수 %s가 참조됨' % b)
            state += 1
            return
        else:
            b = int(symbolTable[b])
    result = a * b
    return str(result)


def assign(a, b):
    global symbolTable
    if b == None:
        symbolTable[a] = 'unknown'
    else : symbolTable[a] = b



def cal():
    global symbolTable, token_list, arithmatic_list, order_list, cnt_op_list, lexemes, state
    # 라인별로 자르기
    lexemes.remove('EOF')
    copylexemes = copy.deepcopy(lexemes)
    if '(' in lexemes:
        lexemes.remove('(')
    if ')' in lexemes:
        lexemes.remove(')')


    semi = list(filter(lambda x: copylexemes[x] == ';', range(len(copylexemes))))
    semi.insert(0, -1)
    semi.append(len(copylexemes))

    lineprint = []
    for i in range(len(semi) - 1):
        lineprint.append(copy.deepcopy(copylexemes[semi[i]+1:semi[i + 1]+1]))


    semi = list(filter(lambda x: lexemes[x] == ';', range(len(lexemes))))
    semi.insert(0, -1)
    semi.append(len(lexemes))

    lex_list = []
    for i in range(len(semi) - 1):
        lex_list.append(copy.deepcopy(lexemes[semi[i]+1:semi[i + 1]]))

    arithmatic_list_copy = copy.deepcopy(arithmatic_list)
    order_list_copy = copy.deepcopy(order_list)
    now_arithmatics = []
    now_orders = []
    for num in range(len(lex_list)):
        now_arithmatics.append(copy.deepcopy(arithmatic_list_copy[:cnt_op_list[num]]))
        now_orders.append(copy.deepcopy(order_list_copy[:cnt_op_list[num]]))
        for i in range(cnt_op_list[num]):
            arithmatic_list_copy.pop(0)
            order_list_copy.pop(0)

    for num, line in enumerate(lex_list):
        try:
            print(' '.join(lineprint[num]))
            now_arithmatic = now_arithmatics[num]
            now_order = now_orders[num]

            en = 0
            while len(now_arithmatic) != 0:
                if now_order[en] == max(now_order) and len(now_arithmatic) != 1:
                    temp = line.index(now_arithmatic[en])
                    if now_arithmatic[en] == '+':
                        result = add(line[temp - 1], line[temp + 1])
                        del line[temp - 1]
                        del line[temp - 1]
                        del line[temp - 1]
                        line.insert(temp - 1, result)
                        now_arithmatic.pop(en)
                        now_order.pop(en)
                    elif now_arithmatic[en] == '-':
                        result = sub(line[temp - 1], line[temp + 1])
                        del line[temp - 1]
                        del line[temp - 1]
                        del line[temp - 1]
                        line.insert(temp - 1, result)
                        now_arithmatic.pop(en)
                        now_order.pop(en)
                    elif now_arithmatic[en] == '/':
                        result = div(line[temp - 1], line[temp + 1])
                        del line[temp - 1]
                        del line[temp - 1]
                        del line[temp - 1]
                        line.insert(temp - 1, result)
                        now_arithmatic.pop(en)
                        now_order.pop(en)
                    elif now_arithmatic[en] == '*':
                        result = mul(line[temp - 1], line[temp + 1])
                        del line[temp - 1]
                        del line[temp - 1]
                        del line[temp - 1]
                        line.insert(temp - 1, result)
                        now_arithmatic.pop(en)
                        now_order.pop(en)
                    en = 0
                elif now_arithmatic[0] == ':=' and len(now_arithmatic) == 1:
                    assign(line[0], line[2])
                    del line[0]
                    del line[0]
                    del line[0]
                    now_arithmatic.pop(en)
                    now_order.pop(en)

                else:
                    en += 1
                    continue

            if state == 0:
                print("(OK)")
                state = 0
            print("ID: %d; CONST: %d; OP: %d;\n" % (cnt_id_list[num], cnt_const_list[num], cnt_op_list[num]))
            state = 0
        except:
            print("Something Went Wrong!")


    print("Result ==> ", symbolTable)






# Command 내 인자 개수 확인
if len(sys.argv) != 2:
    option = True
    input_string = input()
    program(input_string)
    sys.exit()
else:
    option = False
    # input File 열기
    file_path = sys.argv[1]
    f = open(file_path, 'r')
    with f as file:
        lines = f.read().splitlines()
    f.close()

    input_string = ''.join(lines)
    print(input_string)

    f.close()
    program(input_string)
    #program('operand1 := 3 ; operand2 := operand1 + 5 ; target := operand1 + operand2 * 3')
    #program('operand1 := 3 + 1 ; operand2 := operand1 + 2 ; target := (operand1 + operand2) / 30 + 2 * 3')
    cal()


