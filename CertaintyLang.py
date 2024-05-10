from sly import Lexer
from sly import Parser
import sys

class CertaintyLexer(Lexer):
    tokens = {
        NAME, NUMBER, STRING, IF, THEN, ELSE,
        FOR, WHILE, DO, FUN, TO, ARROW, EQEQ,
        BIGGER, BIGGEREQ, SMALLEREQ, SMALLER,
        GAND, GOR, GNAND, GNOR, GXOR, GXNOR,
        GMUX2X1,GMUX4X1,BINVERTER,BINADDER,BINSUBTRACTOR,
        DFLIPFLOP,TFLIPFLOP,SRFLIPFLOP,JKFLIPFLOP,
        GNOT, BIN, PRINT, FILE, EXIT
        }
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '^', '(', ')',
                 ',', ';', '>', '<', '{', '}'
                }

    # Define tokens
    FILE = r'FILEOPEN'
    EXIT = r'EXIT'
    PRINT = r'PRINT'
    GAND = r'AND|&'
    GOR = r'OR|\|'
    GNAND = r'NAND|!&'
    GNOR = r'NOR|!\|'
    GXOR = r'XOR'
    GXNOR = r'XNOR'
    GNOT = r'NOT|!'
    
    GMUX2X1=r'MUX2X1'
    GMUX4X1=r'MUX4X1'
    BINVERTER=r'BINVERTER'
    BINADDER=r'BINADDER'
    BINSUBTRACTOR=r'BINSUBTRACTOR'
    DFLIPFLOP=r'DFLIPFLOP'
    TFLIPFLOP=r'TFLIPFLOP'
    SRFLIPFLOP=r'SRFLIPFLOP'
    JKFLIPFLOP=r'JKFLIPFLOP'
    
    BIN = r'BIN'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    FOR = r'FOR'
    WHILE = r'WHILE'
    DO = r'DO'
    FUN = r'FUN'
    TO = r'TO'
    ARROW = r'->'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    EQEQ = r'=='
    BIGGEREQ = r'>='
    BIGGER = r'>'
    SMALLEREQ = r'<='
    SMALLER = r'<'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

class CertaintyParser(Parser):
    tokens = CertaintyLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.env = { }
    @_('')
    def statement(self, p):
        pass

    @_('FILE STRING') ## Command to open files
    def statement(self, p):
        return ('fileopen', p.STRING)

    @_('PRINT expr') ## Command to print the output of an expression
    def statement(self, p):
        return ('print_expr', p.expr)
    
    @_('PRINT condition') ## Command to print True / False
    def statement(self, p):
        return ('print_cond', p.condition)

    @_('PRINT STRING') ## Command to print a String
    def statement(self, p):
        return ('print_str', p.STRING)

    @_('EXIT') ## Command to kill the program
    def statement(self, p):
        quit()

    @_('statement ";" statement') ## Used to recognise statement seperation in same line
    def statement(self, p):
        return ('statement_set', p.statement0, p.statement1)

    @_('FOR var_assign TO expr "{" statement "}"') ## For-Loop Structure
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    @_('WHILE condition DO "{" statement "}"') ## While-Loop Structure
    def statement(self, p):
        return ('while_loop', p.condition, p.statement)

    @_('IF condition THEN "{" statement "}"') ## If-Then Structure
    def statement(self, p):
        return ('if_stmt_noelse', p.condition, p.statement)

    @_('IF condition THEN "{" statement "}" ELSE "{" statement "}"') ## If-Else structure
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    @_('FUN NAME "(" ")" ARROW "{" statement "}"') ## Function Declaration
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)

    @_('FUN NAME ARROW "{" statement "}"') ## Function Declaration
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)

    @_('NAME "(" ")"') ## Function Call
    def statement(self, p):
        return ('fun_call', p.NAME)
    @_('NAME ";"') ## Function Call
    def statement(self, p):
        return ('fun_call', p.NAME)

     ## Conditions
    @_('expr EQEQ expr')
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)
    @_('expr BIGGEREQ expr')
    def condition(self, p):
        return ('condition_biggereq', p.expr0, p.expr1)
    @_('expr BIGGER expr')
    def condition(self, p):
        return ('condition_bigger', p.expr0, p.expr1)
    @_('expr SMALLEREQ expr')
    def condition(self, p):
        return ('condition_smallereq', p.expr0, p.expr1)
    @_('expr SMALLER expr')
    def condition(self, p):
        return ('condition_smaller', p.expr0, p.expr1)

    ## Variable Assignment statements
    @_('var_assign')
    def statement(self, p):
        return p.var_assign
    @_('NAME "+" "+"')
    def var_assign(self, p):
        return ('pp_assign', p.NAME)
    @_('NAME "+" "=" expr')
    def var_assign(self, p):
        return ('var_assign_plus', p.NAME, p.expr)
    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)
    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)

    ## Logic Gate simulation statements
    @_('logic')
    def statement(self, p):
        return (p.logic)
    @_('expr GAND expr')
    def logic(self, p):
        return ('gand', p.expr0, p.expr1)
    @_('expr GOR expr')
    def logic(self, p):
        return ('gor', p.expr0, p.expr1)
    @_('expr GNAND expr')
    def logic(self, p):
        return ('gnand', p.expr0, p.expr1)
    @_('expr GNOR expr')
    def logic(self, p):
        return ('gnor', p.expr0, p.expr1)
    @_('expr GXOR expr')
    def logic(self, p):
        return ('gxor', p.expr0, p.expr1)
    @_('expr GXNOR expr')
    def logic(self, p):
        return ('gxnor', p.expr0, p.expr1)
    @_('expr GNOT')
    def logic(self, p):
        return ('gnot', p.expr)

    ## IC simulation statements
    @_('expr "," expr GMUX2X1 expr')
    def logic(self,p):
        return ('gmux2x1',p.expr0,p.expr1,p.expr2)
    @_('expr "," expr "," expr "," expr GMUX4X1 expr "," expr')
    def logic(self,p):
        return ('gmux4x1',p.expr0,p.expr1,p.expr2,p.expr3, p.expr4, p.expr5)        
    @_('expr BINVERTER')
    def logic(self, p):
        return ('binverter', p.expr)
    @_('expr BINADDER expr')
    def logic(self, p):
        return ('binadder', p.expr0, p.expr1)
    @_('expr BINSUBTRACTOR expr')
    def logic(self, p):
        return ('binsubtractor', p.expr0, p.expr1)    

    ## Flip-Flop simulation statements
    @_('expr DFLIPFLOP expr')
    def logic(self, p):
        return ('dff', p.expr0, p.expr1)
    @_('expr TFLIPFLOP expr')
    def logic(self, p):
        return ('tff', p.expr0, p.expr1)
    @_('expr "," expr SRFLIPFLOP expr')
    def logic(self,p):
        return ('srff',p.expr0,p.expr1,p.expr2)
    @_('expr "," expr JKFLIPFLOP expr')
    def logic(self,p):
        return ('jkff',p.expr0,p.expr1,p.expr2)

    ## Convert base-10 integer to binary
    @_('BIN expr')
    def statement(self, p):
        return ('bin', p.expr)

    ## Simple operation statements
    @_('expr')
    def statement(self, p):
        return (p.expr)
    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)
    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)
    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)
    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)
    @_('expr "^" expr')
    def expr(self, p):
        return ('pow', p.expr0, p.expr1)
    @_('"(" expr ")"')
    def expr(self, p):
        return (p.expr)
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('uminus', p.expr)

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)
    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)
    @_('STRING')
    def statement(self, p):
        return ('str', p.STRING)

class CertaintyExecute:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result != None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):
        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node
        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            else:
                return self.walkTree(node[2][2])
        if node[0] == 'if_stmt_noelse':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2])

        if node[0] == 'condition_eqeq':
            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == 'condition_biggereq':
            return self.walkTree(node[1]) >= self.walkTree(node[2])

        if node[0] == 'condition_smallereq':
            return self.walkTree(node[1]) <= self.walkTree(node[2])

        if node[0] == 'condition_bigger':
            return (self.walkTree(node[1]) > self.walkTree(node[2]))

        if node[0] == 'condition_smaller':
            return (self.walkTree(node[1]) < self.walkTree(node[2]))

        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]

        if node[0] == 'fun_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print(f"Undefined Function {node[1]}")
                return 0

        if node[0] == 'gand':
            i = 0
            if self.walkTree(node[1]) != 0 and self.walkTree(node[2]) != 0:
                i = 1
            return i
        if node[0] == 'gor':
            i = 0
            if self.walkTree(node[1]) != 0 or self.walkTree(node[2]) != 0:
                i = 1
            return i
        if node[0] == 'gnot':
            i = 0
            if self.walkTree(node[1]) == 0:
                i = 1
            return i
        if node[0] == 'gnand':
            i = 0
            if self.walkTree(node[1]) == 0 or self.walkTree(node[2]) == 0:
                i = 1
            return i
        if node[0] == 'gnor':
            i = 0
            if self.walkTree(node[1]) == 0 and self.walkTree(node[2]) == 0:
                i = 1
            return i
        if node[0] == 'gxor':
            i = 0
            if (self.walkTree(node[1]) == 0 and self.walkTree(node[2]) != 0) or (self.walkTree(node[1]) != 0 and self.walkTree(node[2]) == 0):
                i = 1
            return i
        if node[0] == 'gxnor':
            i = 0
            if (self.walkTree(node[1]) == 0 and self.walkTree(node[2]) == 0) or (self.walkTree(node[1]) != 0 and self.walkTree(node[2]) != 0):
                i = 1
            return i
        
        if node[0]=='gmux2x1':
            if self.walkTree(node[3]) == 0: return self.walkTree(node[1])
            if self.walkTree(node[3])==1: return self.walkTree(node[2])
            return 0
        if node[0]=='gmux4x1':
            if self.walkTree(node[5])==0 and self.walkTree(node[6])==0: return self.walkTree(node[1])
            if self.walkTree(node[5])==0 and self.walkTree(node[6])==1: return self.walkTree(node[2])
            if self.walkTree(node[5])==1 and self.walkTree(node[6])==0: return self.walkTree(node[3])
            if self.walkTree(node[5])==1 and self.walkTree(node[6])==1: return self.walkTree(node[4])
            return 0
        if node[0]=='binverter':#1s compliment of a binary number
            val=self.walkTree(node[1])
            l=len(str(val))
            new=0
            for i in range (l-1,-1,-1):
                temp=1-(val//10**i)%10
                new=new+temp*10**i
            return new
        if node[0]=='binadder' :#adds two binary numbers
            val1=self.walkTree(node[1])
            val2=self.walkTree(node[2])
            summ=0#stores the value of the sum
            car=0#stores the value of the carry
            val=0#stores the total number
            maxlen=max(len(str(val1)),len(str(val2)))
            for i in range (0,maxlen+1,1):
                t1=(val1//(10**i))%2
                t2=(val2//(10**i))%2
                summ=(t1+t2+car)%2
                car=(t1+t2+car)//2
                val+=summ*10**(i)          
            return val
        if node[0]=='binsubtractor' :#subtracts two binary numbers
            val1=self.walkTree(node[1])
            val2=self.walkTree(node[2])
            summ=0
            car=1 
            val=0
            maxlen=max(len(str(val1)),len(str(val2)))
            for i in range (0,maxlen+1,1):
                t1=(val1//(10**i))%2
                t2=1-(val2//(10**i))%2
                summ=(t1+t2+car)%2
                car=(t1+t2+car)//2
                val+=summ*10**i        
            return val%10**i

        if node[0]=='dff':
            return self.walkTree(node[1])
        if node[0]=='tff':
            if self.walkTree(node[1])==0:return self.walkTree(node[2])
            elif self.walkTree(node[1])==1:return 1-self.walkTree(node[2])
        if node[0]=='srff' or node[0]=='jkff':
            print(self.walkTree(node[1]),self.walkTree(node[2]))
            if self.walkTree(node[1])==0 and self.walkTree(node[2])==0:return self.walkTree(node[3])        
            elif self.walkTree(node[1])==0 and self.walkTree(node[2])==1:return 0        
            elif self.walkTree(node[1])==1 and self.walkTree(node[2])==0:return 1
            elif node[0]=='srff': return -352
            else: return 1-self.walkTree(node[3])

        if node[0] == 'bin':
            val = self.walkTree(node[1])
            binary = bin(val)
            print(binary[2:])
            return binary
           
        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        if node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        if node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        if node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])
        if node[0] == 'pow':
            return self.walkTree(node[1]) ** self.walkTree(node[2])
        if node[0] == 'uminus':
            return -1 * self.walkTree(node[1])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]
        if node[0] == 'var_assign_plus':
            self.env[node[1]] += self.walkTree(node[2])
            return node[1]
        if node[0] == 'pp_assign':
            self.env[node[1]] += 1
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return 0

        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'while_loop':
            maxi = 0
            while ((self.walkTree(node[1]) == True) and (maxi < 200)):
                res = self.walkTree(node[2])
                maxi = maxi + 1
            
        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))

        if node[0] == 'statement_set':
            return [self.walkTree(node[1]), self.walkTree(node[2])]

        if node[0] == 'print_expr':
            val = self.walkTree(node[1])
            print(val)
        if node[0] == 'print_cond':
            tf = self.walkTree(node[1])
            if tf == True:
                print (True)
            else:
                print (False)
        if node[0] == 'print_str':
            print(node[1])
        
        
        if node[0] == 'fileopen':
            filename = node[1]
            file = open(filename.strip('"'), "r")
            lexer = CertaintyLexer()
            parser = CertaintyParser()
            env = {}
            count = 0
            for line in file.readlines():
                count += 1
                try:
                    cmd = line
                    tree = parser.parse(lexer.tokenize(cmd))
                    CertaintyExecute(tree, env)
                except:
                    print(f"Error at line {count}")

if __name__ == '__main__':
    
    lexer = CertaintyLexer()
    parser = CertaintyParser()
    env = {}

    ## If executed through terminal with the option of file execution
    if len(sys.argv) > 1:
        try:
            file = open(sys.argv[1], "r")
            count = 0
            print(f"Accessing file {sys.argv[1]}...")
            for line in file.readlines():
                count += 1
                try:
                    cmd = line
                    tree = parser.parse(lexer.tokenize(cmd))
                    CertaintyExecute(tree, env)
                except:
                    print(f"Error at line {count}")
        except:
            print(f"File {sys.argv[1]} was not found")
    else:
        while True:
            try:
                text = input('CeLang > ')
            except EOFError:
                break
            if text:
                tree = parser.parse(lexer.tokenize(text))
                CertaintyExecute(tree, env)
            
