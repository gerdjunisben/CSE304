#ideas
#data structures
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

symbols = {}
store = {}

stack = []
commands = []
token = ""
i = 0
valid = True

sampleInput1 = "ildc 10\nildc 20\niadd\n"
input = sampleInput1

while(i<len(input)):
    token += (input[i])
    i+=1
    if token=="ildc ":
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

        while input[i]!='\n':
            if input[i]<='9' or input[i]>='0':
                num*=10
                num += ord(input[i]) - ord('0')
                i+=1
            else:
                valid = False
                break
        
        commands.append((0,num*sign))
        token=""
    elif token=='iadd\n':
        commands.append((1,))
        token=""
    elif token=='isub\n':
        commands.append((2,))
        token=""
    elif token=='idiv\n':
        commands.append((3,))
        token=""
    elif token=='imod\n':
        commands.append((4,))
        token=""
    elif token=='pop\n':
        commands.append((5,))
        token=""
    elif token=='dup\n':
        commands.append((6,))
        token=""
    elif token=='swap\n':
        commands.append((7,))
        token=""
    elif token=='\n':
        token=""
        continue



if len(token) >0:
    valid = False

if(valid):
    for i in commands:
        if i[0] == 0:
            stack.append(i[1])
        elif i[0] == 1:
            a = stack.pop()
            b = stack.pop()
            stack.append(a+b)
        elif i[0] == 2:
            a = stack.pop()
            b = stack.pop()
            stack.append(b-a)
        elif i[0] == 3:
            a = stack.pop()
            b = stack.pop()
            stack.append(b/a)
        elif i[0] == 4:
            a = stack.pop()
            b = stack.pop()
            stack.append(b%a)
        elif i[0] == 5:
            stack.pop()
        elif i[0] == 6:
            a = stack.pop()
            stack.append(a)
            stack.append(a)
        elif i[0] == 7:
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)
    print(stack.pop())
else:
    print("Invalid program")

