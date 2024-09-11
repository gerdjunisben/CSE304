print("Hi")
print("Donato's first edit")
print("Ben's second edit")

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