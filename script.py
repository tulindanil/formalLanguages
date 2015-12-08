# coding=UTF-8
import sys

letters = ['a', 'b', 'c', '1']
unary = ['*']
binary = ['+', '.']

ans = 0

class term:

    prefix = 0 #длина префикса вида a^*
    suffix = 0 #длина суффикса вида a^*
    length = 0 #длина слова (имеет слова при ispattern = true)
    ispattern = False #true, если слово вида a^*. Иначе - false

# Геттеры, чтобы удобно описать объект класса при вызове print term

    def getPattern(self):
        return self.ispattern

    def getPrefix(self):
        return self.prefix

    def getLength(self):
        return self.length

    def getSuffix(self):
        return self.suffix

    ch = '' #Регулярное выражение, которое соответствует объекту класса

    def __init__(self):
        self.items = [('prefix', self.getPrefix), ('length', self.getLength), ('suffix', self.getSuffix), ('ispattern', self.getPattern)]

    def __repr__(self):
        return self.__str__() 

    def __str__(self):
        
        string = self.ch + ': '

        for index, item in self.items:
            string += index + ' - ' + str(item()) 
            if not self.items.index((index, item)) == len(self.items) - 1:
                string += ', '

        return string

def compile(item): # преобразует символ в объект класса term

    t = term()

    if item == '1':
        t.ispattern = True
    elif item not in letters:
        t.prefix = 1
        t.length = 1
        t.suffix = 1
        t.ispattern = True

    t.ch = item

    return t

def mergeStar(item):

    global ans

    t = term()

    t.ch = '(' + item.ch + ')'  + '*'

    if item.ispattern == True and item.length > 0: #если к слову вида a^+ применить * то значит будет бесконечность 
        ans = sys.maxint

    t.ispattern = True #Слово может иметь вид a^0 
    t.length = 0

    t.prefix = item.prefix
    t.suffix = item.suffix

    ans = max(ans, t.suffix + t.prefix) #нас интересует длина подслова из a на стыке если мы размножаем звуздочку больше
                                        #одного раза

    return t

def mergePlus(item1, item2):

    t = term()

#мы можем взять любой из двух термов, на которые действует
#оператор

    t.prefix = max(item1.prefix, item2.prefix)
    t.suffix = max(item1.suffix, item2.suffix)
    t.ispattern = item1.ispattern or item2.ispattern  
    
    if item1.ispattern == True:
        t.length = item1.length

    if item2.ispattern == True:
        t.length = max(t.length, item2.length)

    t.ch = '(' + item1.ch + '+' + item2.ch + ')'

    return t

def mergeConcat(l, r):

    global ans

    t = term()
    t.ch = l.ch + r.ch

    t.prefix = l.prefix
    t.suffix = r.suffix
    t.length = l.length + r.length
    t.ispattern = l.ispattern and r.ispattern

#разбор случая вида (b+c)*a* . a*
    if r.ispattern == True:
        t.suffix = max(t.suffix, l.suffix + r.length)

#разбор случая вида a* . a*(b+c)*
    if l.ispattern == True:
        t.prefix = max(t.prefix, l.length + r.prefix)

    ans = max(ans, l.suffix + r.prefix)

    if t.ispattern == True:
        ans = max(ans, t.length)

    return t

def proceedLiteral(s, sym):
    s.append(compile(sym))

binaryFunc = [mergePlus, mergeConcat]

def proceedBinary(s, sym):
    item2 = s.pop()
    item1 = s.pop()
    s.append(binaryFunc[binary.index(sym)](item1, item2))

def proceedUnary(s, sym):
    s.append(mergeStar(s.pop()))

def proceed(stack, symbol):
    if symbol in binary:
        proceedBinary(stack, symbol)
    elif symbol in unary:
        proceedUnary(stack, symbol)
    else:
        proceedLiteral(stack, symbol)

if __name__ == '__main__':

    output = False
    if len(sys.argv) > 1 and sys.argv[1] == '-o':
        output = True

    string = raw_input()
    pattern, symbol = string.split()

    letters = [x for x in letters if not x == symbol]
    stack = []

    try:
        for sym in pattern:
            if not sym in letters + [symbol] + binary + unary:
                raise Exception()
            if output == True:
                print stack
            proceed(stack, sym)
    except Exception as e:
        print 'Error'
        sys.exit(1)

    if output == True:
        print stack

    if len(stack) == 1:
        if ans == sys.maxint:
            print 'INF'
            sys.exit(0)
        item = stack[0]
        ans = max(ans, item.prefix, item.suffix)
        if item.ispattern == True:
            ans = max(ans, item.length)
        print ans
    else:
        print 'Error'
        

