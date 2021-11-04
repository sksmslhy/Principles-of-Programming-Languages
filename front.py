import copy

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
        symbolTable[''.join(lexeme)] = "unknown"

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
    #print("Next token is : %d  Next lexeme is %s" %(nextToken, ''.join(lexeme)))
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
    #print('Enter <program>')
    order += 1
    statements()
    order -= 1
    #print(symbolTable)
    #print("Exit <program>")
    #print("ID: %d; CONST: %d; OP: %d;" % (cnt_id, cnt_const, cnt_op))
    cnt_op_list.append(cnt_op)
    cnt_const_list.append(cnt_const)
    cnt_id_list.append(cnt_id)


def statements():
    global order
    #print("Enter <statements>")
    order += 1
    statement()
    order -= 1
    order += 1
    temp()
    order -= 1
    #print("Exit <statements>")


def temp():
    global order
    #print("Enter <temp>")
    if nextToken == SEMI_COLON:
        order += 1
        semi_colon()
        order -= 1
        order += 1
        statements()
        order -= 1


def statement():
    global order
    #print("Enter <statement>")
    order += 1
    ident()
    order -= 1
    order += 1
    assignment_op(':=')
    order -= 1
    order += 1
    expression()
    order -= 1
    #print("Exit <statement>")


def expression():
    global order
    #print("Enter <expression>")
    order += 1
    term()
    order -= 1
    order += 1
    term_tail()
    order -= 1
    #print("Exit <expression>")


def term_tail():
    global order
    #print("Enter <term_tail>")
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
    #print("Exit <term_tail>")


def term():
    global order
    #print("Enter <term>")
    order += 1
    factor()
    order -= 1
    order += 1
    factor_tail()
    order -= 1
    #print("Exit <term>")


def factor_tail():
    global order
    #print("Enter <factor_tail>")
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
    #print("Exit <factor_tail>")


def factor():
    global order
    #print("Enter <factor>")
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
    #print("Exit <factor>")


def const():
    global cnt_const
    cnt_const += 1
    #print('Enter <const>')
    lexical()
    #print("Exit <const>")


def ident():
    global cnt_id
    cnt_id += 1
    #print('Enter <ident>')
    lexical()
    #print("Exit <ident>")


def assignment_op(arithmatic:str):
    global arithmatic_list, order_list, cnt_op
    #print('Enter <assignment_op>', order)
    order_list.append(order)
    arithmatic_list.append(arithmatic)
    cnt_op += 1
    lexical()
    #print("Exit <assignment_op>")


def semi_colon():
    global cnt_op, cnt_id, cnt_const, order_list, line_cnt, cnt_op_list, cnt_const_list, cnt_id_list

#    print("ID: %d; CONST: %d; OP: %d;"%(cnt_id, cnt_const, cnt_op))
    cnt_op_list.append(cnt_op)
    cnt_const_list.append(cnt_const)
    cnt_id_list.append(cnt_id)
    cnt_id = 0
    cnt_const = 0
    cnt_op = 0
    #print('Enter <semi_colon>')
    lexical()
    #print("Exit <semi_colon>")


def add_op(arithmatic:str):
    global cnt_op, order, order_list, arithmatic_list
    order_list.append(order)
    arithmatic_list.append(arithmatic)
    cnt_op += 1
    #print('Enter <add_operator>, order : ', order)
    lexical()
    #print("Exit <add_operator>")


def mult_op(arithmatic:str):
    global cnt_op, order, arithmatic_list, order_list
    order_list.append(order)
    arithmatic_list.append(arithmatic)
    cnt_op += 1
    #print('Enter <mult_operator>, order : ', order)
    lexical()
    #print("Exit <mult_operator>")


def left_paren():
    #print('Enter <left_paren>')
    lexical()
    #print("Exit <left_paren>")


def right_paren():
    #print('Enter <right_paren>')
    lexical()
    #print("Exit <right_paren>")


def isDigit(arg:str):
    try:
        int(arg)
        return True
    except:
        return False


def add(a, b):
    if isDigit(a):
        a = int(a)
    else:
        a = int(symbolTable[a])
    if isDigit(b):
        b = int(b)
    else:
        b = int(symbolTable[b])
    result = a + b
    return str(result)


def sub(a, b):
    if isDigit(a):
        a = int(a)
    else:
        a = int(symbolTable[a])
    if isDigit(b):
        b = int(b)
    else:
        b = int(symbolTable[b])
    result = a - b
    return str(result)


def div(a, b):
    if isDigit(a):
        a = int(a)
    else:
        a = int(symbolTable[a])
    if isDigit(b):
        b = int(b)
    else:
        b = int(symbolTable[b])
    result = a // b
    return str(result)


def mul(a, b):
    if isDigit(a):
        a = int(a)
    else:
        a = int(symbolTable[a])
    if isDigit(b):
        b = int(b)
    else:
        b = int(symbolTable[b])
    result = a * b
    return str(result)


def assign(a, b):
    global symbolTable
    symbolTable[a] = b



def cal():
    global symbolTable, token_list, arithmatic_list, order_list, cnt_op_list, lexemes
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
    #print(lex_list)

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

    #print("now_arithmatics : ", now_arithmatics)
    #print('now_orders : ', now_orders)

    for num, line in enumerate(lex_list):
        try:
            print(' '.join(lineprint[num]))
            now_arithmatic = now_arithmatics[num]
            now_order = now_orders[num]

            #print("-"*20,num,"-"*20)
            #print(' '.join(line))
            #print('now_arithmatic = ', now_arithmatic)
            #print('now_order = ', now_order)

            en = 0
            while len(now_arithmatic) != 0:
                #print(line)
                #print(now_arithmatic[en])
                #print(len(now_arithmatic))
                #temp = line.index(now_arithmatic[en])
                #print("now en : ", en)
                if now_order[en] == max(now_order) and len(now_arithmatic) != 1:
                    temp = line.index(now_arithmatic[en])
                    if now_arithmatic[en] == '+':
                        #print("DO +")
                        result = add(line[temp - 1], line[temp + 1])
                        del line[temp - 1]
                        del line[temp - 1]
                        del line[temp - 1]
                        line.insert(temp - 1, result)
                        now_arithmatic.pop(en)
                        now_order.pop(en)
                        #print("now arithmatic : ", now_arithmatic)
                    elif now_arithmatic[en] == '-':
                        #print("DO -")
                        result = sub(line[temp - 1], line[temp + 1])
                        del line[temp - 1]
                        del line[temp - 1]
                        del line[temp - 1]
                        line.insert(temp - 1, result)
                        now_arithmatic.pop(en)
                        now_order.pop(en)
                        #print("now arithmatic : ", now_arithmatic)
                    elif now_arithmatic[en] == '/':
                        #print("DO /")
                        result = div(line[temp - 1], line[temp + 1])
                        del line[temp - 1]
                        del line[temp - 1]
                        del line[temp - 1]
                        line.insert(temp - 1, result)
                        now_arithmatic.pop(en)
                        now_order.pop(en)
                        #print("now arithmatic : ", now_arithmatic)
                    elif now_arithmatic[en] == '*':
                        #print("DO *")
                        result = mul(line[temp - 1], line[temp + 1])
                        del line[temp - 1]
                        del line[temp - 1]
                        del line[temp - 1]
                        line.insert(temp - 1, result)
                        now_arithmatic.pop(en)
                        now_order.pop(en)
                        #print("now arithmatic : ", now_arithmatic)
                    en = 0
                elif now_arithmatic[0] == ':=' and len(now_arithmatic) == 1:
                    #print("DO :=")
                    result = assign(line[0], line[2])
                    del line[0]
                    del line[0]
                    del line[0]
                    line.insert(temp - 1, result)
                    now_arithmatic.pop(en)
                    now_order.pop(en)

                else:
                    en += 1
                    continue
            print('(OK)')
            print("ID: %d; CONST: %d; OP: %d;\n" % (cnt_id_list[num], cnt_const_list[num], cnt_op_list[num]))
        except:
            print('(Error)')
            print("ID: %d; CONST: %d; OP: %d;\n" % (cnt_id_list[num], cnt_const_list[num], cnt_op_list[num]))


    print("Result ==> ", symbolTable)



program('operand1 := 3 ; operand2 := operand1 + 2 ; target := operand1 + operand2 * 3')
#program('operand1 := 3 + 1 ; operand2 := operand1 + 2 ; target := (operand1 + operand2) / 30 + 2 * 3')


#program("o1 := 3; o2 = o1 + 2 ; target = (o1 + o2) / 3")
# 7 / 12 10 9  10

#print(symbolTable)
#print(token_list)
#print("cnt_op_list : ", cnt_op_list)
#print('lexemes = ', lexemes)
print()
print()
cal()



