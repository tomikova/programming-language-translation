#SYNTAX ANALYZER#

def parser():
    global table, transitions
    for t in table:
        if t[0]=='#':
            state=t[1:]
            transitions[state]={}
        else:
            pair=t.split(' ')
            transitions[state][pair[0]]=pair[1]
            
    
def writeTree(i, level):
    global tree
    space=''
    for node in tree:
        if node[1]==i:
            for lvl in range(level):
                space+=' '
            if len(node)>2:
                print '%s<%s>'%(space, node[0])
                node[2].reverse()
                for next in node[2]:
                    writeTree(next, level+1)
            else: 
                print '%s%s'%(space, node[0])		
            break    
        
    
txt=open('Table.txt')
table=txt.read()
table=table.splitlines()
transitions={}
state=[]
tree=[]
i=0
pointer=[]
_sync=table.pop(0).split(' ')
state.append(table[0][1:])

parser()
d_input=open('test.in')
input=d_input.read()
input=input.splitlines()
input.append('$$')
stack=[]

while input:
    flag=1
    symbol=input[0].split(' ')[0]
    if symbol in transitions[state[-1]]:
        action=transitions[state[-1]][symbol]
        if 'pomakni' in action:
            stack.append([input.pop(0), i])
            i+=1
            state.append(action[8:-1])
        elif 'reduciraj' in action:
            production=action.split('(')[1][:-1]
            leftSide=production.split('->')[0]
            rightSide=production.split('->')[1].split('.')
            while rightSide:
                el=rightSide.pop()
                if stack[-1][0].split(' ')[0]==el:
                    pointer.append(stack[-1][1])
                    tree.append(stack[-1])
                    stack.pop()
                    state.pop()

                elif el=='$':
                    tree.append([el, i])
                    pointer.append(i)
                    i+=1           
    
                ## error   
                else:
                    flag=0
                    print rightSide, stack[-1][0]
                    while input[0].split(' ')[0] not in _sync:
                        input.pop(0)
                    syncSymbol=input[0].split(' ')[0]
                    if syncSymbol not in transitions[state[-1]]:
                        stack.pop()
                        state.pop()
				## error		
            if flag:            
                stack.append([leftSide, i, pointer])
                i+=1
                pointer=[]    
                if leftSide in transitions[state[-1]]:
                    action=transitions[state[-1]][leftSide]
                    state.append(action[6:-1])
        elif 'prihvati' in action:
            tree.append(stack[-1])
            input.pop()
    else:
    
        while input[0].split(' ')[0] not in _sync:
            input.pop(0)
        syncSymbol=input[0].split(' ')[0]
        if syncSymbol not in transitions[state[-1]]:
            stack.pop()
            state.pop()
            
writeTree(i-1, 0)
