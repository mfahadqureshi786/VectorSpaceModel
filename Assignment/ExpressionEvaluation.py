#Stack and its methods
MyStack = []
StackSize = 50
def DisplayStack():
 print("Stack currently contains:")
 for Item in MyStack:
  print(Item)
def Push(Value):
 if len(MyStack) < StackSize:
  MyStack.append(Value)
 else:
  print("Stack is full!")
def Pop():
 if len(MyStack) > 0:
  MyStack.pop()
 else:
  print("Stack is empty.")
def isEmpty():
    if len(MyStack) <= 0:
        return True
    return False
def Top():
    if not isEmpty():
        return MyStack[len(MyStack)-1]
    return -1


#Weight count for operators used in infix to postfix conversion
def weightCount(str):
    if str=='(' or str==')':
        return 0
    if str=='NOT':
        return 3
    if str=='AND':
        return 2
    if str=='OR':
        return 1
    if str[0]=='/':
        return 0
    return -1

def isOperator(str):
    if str=='AND' or str=='OR' or str=='NOT' or str=='(' or str==')' or str[0]=='/':
        return True
    return False

#Converts Infix expression to Postfix
def evaluator(str):
    res=[]
    for a in range(len(str)):
        if not isOperator(str[a]):
            res.append(str[a])
        elif isOperator(str[a]):
            if str[a] == ')':
                while not isEmpty() and Top() != '(':
                    res.append(Top())
                    Pop()
                if Top() =='(':
                    Pop()
                    continue
            if str[a] =='(':
                Push(str[a])
                continue
            while not isEmpty() and weightCount(Top())>=weightCount(str[a]):
                res.append(Top())
                Pop()
            Push(str[a])
    while not isEmpty():
        res.append(Top())
        Pop()
    return res


#Checks if given query is Positional Query
def isPositionalQuery(str):
    if len(str)==1 and not isOperator(str):
        return False
    for elem in str:
        if '/' in elem:
            return  True
    for elem in str:
        if isOperator(elem) and elem!='(' and elem!=')':
            return  False

    return True

#Checks if given query is Boolean Query
def isBooleanQuery(str):
    for elem in str:
        if isOperator(elem) and elem!='(' and elem!=')':
            return True
    return False

def parsePositionalQuery(query):
    k=0
    lexemes=[]
    if '/' in query and len(query)<=3:
        for elem in query:
            if not isOperator(elem):
                lexemes.append(elem)
            else:
                k=int(elem[-1])
    return lexemes
