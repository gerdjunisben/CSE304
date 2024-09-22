# CSE 304 Homework 2
#
# Benjamin Gerdjunis, bgerdjunis, 115962358
# Donato Zampini, dzampini, 114849209
#
#ideas
#hashes:
#   symbols:for holding the labels and their jump location
#   store:for storing vars used in store and load (done at runtime)
#array:
#   stack:for runtime
#   commands:list of commands in order
#   token:use like a stack, take a char from text, if you reach an accept add to commands
#Finding accept states for commands:
#   >>NOTE: all commands on accept except whitespace and ":label" should add to the commands
#   array so we don't gotta reread the parsed copies. We will try to keep line number best we
#   can
#   >white space:accept iff only this
#   >":label":when a colon is scanned as the first char, read until '\n' or ' ' or tab I guess
#   then put in symbols with the line number of the command
#   Also note that labels can only be alpha numeric and underscore. Implement at end.
#   >"ildc": check for white space then optional '-' then (1-9) then some number of (0-9)
#   and finally a '\n'
#   >"iadd":next few ar ejust the command and a '\n'
#   >"isub"
#   >"idiv"
#   >"imod"
#   >"pop"
#   >"dup":push whatever is on top of the stack on top
#   >"swap":swap top 2 elems
#   >"jz": First scan "jz " then empty token and scan until you hit "\n" then add the 
#   label to symbols. Note this only jumps if the top is zero also it pops the value.
#   >"jnz":Exactly like jz but if the top isn't zero
#   >"jmp":Exactly like jz but always jump
#   >"load":Similar to jz but instead add the thing you read after "load " to store.
#   this only copies the value placed by store. When store is called consider placing a 
#   dumby value to make sure you are actually loading something (checkable at end)
#   >"store":Same parsing deal as load read load for my ideas on this
#Once we scan through:
#   run the commands in commands array in order, do jumps when needed, pretty straight forward
#   I think
#>NOTE:this clearly wasn't our final implementation these were the initial ideas

import sys

symbols = {}
store = {}

stack = []
commands = []
commandCounter = 0
token = ""
i = 0
valid = True


rawInput = sys.argv #Get file path and open it for reading
filePath = str(rawInput[1])
# filePath = 'HW2/test.txt'
file = open(filePath, "r")
input = file.read() #Return input as one string
input += ' '

def isWhiteSpace(char):
    return char=='\n' or char==' ' or char=='\t'


while(i<len(input)):
    token += (input[i])
    i+=1
    if len(token) == 1 and token[0] == '#':
        while input[i]!='\n':
            i+=1
        token=""
    elif token[-1] == ':':
        token = token[0:-1]
        for j in token:
            if not j.isalnum() and j!='_':
                valid = False
                break
        symbols[token] = commandCounter
        token = ""
    elif token=="ildc":
        i+=1
        while(isWhiteSpace(input[i])):
            i+=1
        sign = 1
        num = 0
        if(input[i]=='-'):
            sign = -1
            i+=1

        if input[i]<='9' or input[i]>='1':
            num = ord(input[i]) - ord('0')
            i+=1
        else:
            valid = False
            break

        while not isWhiteSpace(input[i]):
            if input[i]<='9' or input[i]>='0':
                num*=10
                num += ord(input[i]) - ord('0')
                i+=1
            else:
                valid = False
                break
        
        commands.append((0,num*sign))
        commandCounter+=1
        token=""
    elif token=='iadd':
        if isWhiteSpace(input[i]):
            commandCounter+=1
            commands.append((1,))
            token=""
        else:
            valid=False
            break
        i+=1
    elif token=='isub':
        if isWhiteSpace(input[i]):
            commandCounter+=1
            commands.append((2,))
            token=""
        else:
            valid=False
            break
        i+=1
    elif token=='idiv':
        if isWhiteSpace(input[i]):
            commandCounter+=1
            commands.append((3,))
            token=""
        else:
            valid=False
            break
        i+=1
    elif token=='imod':
        if isWhiteSpace(input[i]):
            commandCounter+=1
            commands.append((4,))
            token=""
        else:
            valid=False
            break
        i+=1
    elif token=='pop':
        if isWhiteSpace(input[i]):
            commandCounter+=1
            commands.append((5,))
            token=""
        else:
            valid=False
            break
        i+=1
    elif token=='dup':
        if isWhiteSpace(input[i]):
            commandCounter+=1
            commands.append((6,))
            token=""
        else:
            valid=False
            break
        i+=1
    elif token=='swap':
        if isWhiteSpace(input[i]):
            commandCounter+=1
            commands.append((7,))
            token=""
        else:
            valid=False
            break
        i+=1
    elif token=='load':
        if isWhiteSpace(input[i]):
            commandCounter+=1
            commands.append((8,))
            token=""
        else:
            valid=False
            break
        i+=1
    elif token=='store':
        if isWhiteSpace(input[i]):
            commandCounter+=1
            commands.append((9,))
            token=""
        else:
            valid=False
            break
        i+=1
    elif token=='jz':
        i+=1
        while(isWhiteSpace(input[i])):
            i+=1
        
        token=""
        while not isWhiteSpace(input[i]):
            token += input[i]
            i+=1
        if not token in symbols:
            symbols[token] = -1
        commands.append((10,token))
        token=""
        commandCounter += 1
    elif token=='jnz':
        i+=1
        while(isWhiteSpace(input[i])):
            i+=1
        
        token=""
        while not isWhiteSpace(input[i]):
            token += input[i]
            i+=1
        if not token in symbols:
            symbols[token] = -1
        commands.append((11,token))
        token=""
        commandCounter += 1
    elif token=='jmp':
        i+=1
        while(isWhiteSpace(input[i])):
            i+=1
        
        token=""
        while not isWhiteSpace(input[i]):
            token += input[i]
            i+=1
        if not token in symbols:
            symbols[token] = -1
        commands.append((12,token))
        token=""
        commandCounter += 1
    elif len(token) ==1 and isWhiteSpace(token):
        token=""
        continue



if len(token) >0:
    valid = False

for i in symbols.values():
    if i == -1:
        valid = False
        break

runtime = False
if(valid):
    j = 0
    while j < commandCounter:
        if commands[j][0] == 0:
            stack.append(commands[j][1])
        elif commands[j][0] == 1:
            if len(stack)>=2:
                a = stack.pop()
                b = stack.pop()
                stack.append(a+b)
            else:
                runtime = True
                break
        elif commands[j][0] == 2:
            if len(stack)>=2:
                a = stack.pop()
                b = stack.pop()
                stack.append(b-a)
            else:
                runtime = True
                break
        elif commands[j][0] == 3:
            if len(stack)>=2:
                a = stack.pop()
                b = stack.pop()
                stack.append(b/a)
            else:
                runtime = True
                break
        elif commands[j][0] == 4:
            if len(stack)>=2:
                a = stack.pop()
                b = stack.pop()
                stack.append(b%a)
            else:
                runtime = True
                break
        elif commands[j][0] == 5:
            if len(stack)>=1:
                stack.pop()
            else:
                runtime = True
                break
        elif commands[j][0] == 6:
            if len(stack)>=1:
                a = stack.pop()
                stack.append(a)
                stack.append(a)
            else:
                runtime = True
                break
        elif commands[j][0] == 7:
            if len(stack)>=2:
                a = stack.pop()
                b = stack.pop()
                stack.append(a)
                stack.append(b)
            else:
                runtime = True
                break
        elif commands[j][0] == 8:
            if len(stack)>=1:
                a = stack.pop()
                if not a in store:
                    runtime=True 
                    break
                val = store[a] 
                stack.append(a)
                stack.append(val)
            else:
                runtime = True
                break
        elif commands[j][0] ==9:
            if len(stack)>=2:
                b = stack.pop()
                a = stack.pop()
                store[a] = b
            else:
                runtime = True
                break
        elif commands[j][0] == 10: #jz
            if len(stack)>=1:
                a = stack.pop()
                if a == 0:
                    j = symbols[commands[j][1]] -1
            else:
                runtime = True
                break
        elif commands[j][0] == 11: #jnz
            if len(stack)>=1:
                a = stack.pop()
                if a != 0:
                    j = symbols[commands[j][1]] -1 
            else:
                runtime = True
                break
        elif commands[j][0] == 12: #jump
            j = symbols[commands[j][1]] -1
        j+=1
    if runtime:
        print("Runtime error around line %d",j)
    else:
        print(stack.pop())
else:
    print("Invalid program")

