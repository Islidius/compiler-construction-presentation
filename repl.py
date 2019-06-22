from interpreter import *

# init the enviroment for the variables
# so that the single lines all access the same
env = Environment()

while(True):
    # read a single line
    line = input("-> ")

    # lex the line
    l = Lexer(line)
    tokens = l.lexTokens()

    # break if the line is empty
    if(len(tokens) == 1):
        break

    try:
        # parse the tokens
        p = Parser(tokens)
        ast = p.parse()
        
        # interpret the AST
        i = Interpreter(ast, env)
        result = i.eval()
        if(result):
            print(result)

    except Error as err:
        print(err)