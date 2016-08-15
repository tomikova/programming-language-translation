#LEXICAL ANALYZER#

def epsilon(state):
    global fun
    global _list
    f1=[]
    for f in fun:
        if f.count('%s,$->'%state):
            f=f.split('>')
            f=f[1]
            f=f.split(',')
            f1.extend(f)
            for st in f[:]:
                if _list.count(st)==0:
                    _list.append(st)
                    f_next=epsilon(st)
                    if f_next:
                        f1.extend(f_next)
            _list=[]
    if f1:
        return f1    
    return 0 
	
def epsilon1(state):
    global fun
    global _list,transitions
    f1=[]
    if '$' in transitions[state]:
        f=transitions[state]['$']

        f1.extend(f)
        for st in f[:]:
            if _list.count(st)==0:
                _list.append(st)
                f_next=epsilon(st)
                if f_next:
                    f1.extend(f_next)
        _list=[]
    if f1:
        return f1    
    return 0    
	
def minimize(automata):
    states=automata[0].split(',')
    fun=automata[4:]
    _list=[]
    hlpList=[]
    
    for f in fun[:]:

        par=f.split('->')
        par1=par[0].split(',')
        if par1[1]=='$':
            fun.remove(f)
            _list.append(par1[0])
            hlpList.append(par[1])
    for s in states:
        if _list.count(s)>1:
            i=_list.index(s)
            el=hlpList[i]
            del _list[i]
            del hlpList[i]
            i=_list.index(s)
            hlpList[i]+=(',%s'%el)
    
    for i in range(len(_list)):
        fun.append(('%s,$->%s')%(_list[i],hlpList[i]))

    automata[4:]=fun

def enka(automata):
    global sequence
    hlpSequence=sequence[:]
    fi=automata
    entry=fi.splitlines()

    states=entry.pop(0).split(',')
    state=entry.pop(0).split(',')
    okStates=entry.pop(0).split(',')
    startState=entry.pop(0)
    global fun
    global _list, transitions
    fun=entry
    transitions={}

    for s in states:
        transitions[s]={}
    total=[]
    _list=[]
    
    for f in fun:
        name=f.split(',')[0]
        input=f.split('->')[0].split(',')[1]
        if input=='':
            input=','
        aggregate=f.split('->')[1].split(',')
        transitions[name][input]=aggregate
    total.append(state)
    word=[]
    while state and hlpSequence:
        symbol=hlpSequence.pop(0)
        nextState=[]
        for st in state[:]:
            if symbol in transitions[st]:
                st_next=transitions[st][symbol]

            else:
                st_next='#'
            for s in st_next:
                if nextState.count(s)==0 and s!='#':
                    nextState.append(s)
                    environment=epsilon1(s)
                    if environment:
                        for o in environment:
                            if nextState.count(o)==0:
                                nextState.append(o)
            
        prevState=state
        state=nextState
        if state:
            if symbol=='#$':
                word.append('$')
            else:    
                word.append(symbol)
        if state==[]:
            for s in prevState:
                if s in okStates:
                    return ''.join(word)   
    return 0
	
def enka1(automata):
    global sequence
    hlpSequence=sequence[:]
    fi=automata
    entry=fi.splitlines()

    okStates=entry.pop(0).split(',')
    startState=entry.pop(0)
    states.append(okStates)
    global fun
    global _list
    fun=entry
	
    state=[]
    total=[]
    _list=[]
    
    state.append(startState)
    environment=epsilon(startState)
    if environment:
        for o in environment:
            if state.count(o)==0:
                    state.append(o)
    state.sort()
    return ','.join(state)
	
def getStates(automata):
    fi=automata
    entry=fi.splitlines()
    states=[]
    okStates=entry.pop(0).split(',')
    startState=entry.pop(0)
    states.append(okStates[0])
    global fun
    global _list
    fun=entry
    for f in fun:
        s=f.split(',')[0]
        if s not in states:
            states.append(s)
    return ','.join(states)
    
def parser(_list):
    global tables
    automata=[]
    actions=[tables.pop(0)[1:],tables.pop(0),tables.pop(0),tables.pop(0)]
    for line in tables[:]:
        if line[0] in ('p', '#', '%'):
            if line[0]=='%':
                break
            if line[0]=='#':
                a1='\n'.join(automata)
                poc=enka1(a1)
                automata.insert(0, poc)
                s=getStates(a1)
                automata.insert(0, s)
                minimize(automata)
                _list.append([actions,'\n'.join(automata)])
                automata=[]
                actions=[tables.pop(0)[1:],tables.pop(0),tables.pop(0),tables.pop(0)]
            else:
                automata.append(line)       
                tables.pop(0)
    a1='\n'.join(automata)
    poc=enka1(a1)
    automata.insert(0, poc)
    s=getStates(a1)
    automata.insert(0, s)
    minimize(automata)
    _list.append([actions,'\n'.join(automata)])
    
                    
def resolveAmbiguity(_exit):

    maxi=len(_exit[0])
    for i in range(len(_exit)/2):
        if len(_exit[2*i])>maxi:
            maxi=len(_exit[2*i])       
    for i in range(len(_exit)/2):
        if len(_exit[2*i])==maxi and len(_exit[0])!=maxi:
            _exit[0]=_exit[2*i]
            _exit[1]=_exit[2*i+1]


d_input=open('test.in')
sequence=list(d_input.read())
d_output=open('output.txt','w')
for n,i in enumerate(sequence):
    if i=='\n':
        sequence[n]='#n'
    if i=='$':
        sequence[n]='#$'
sequence.append('#end')
txt=open('definition.txt')
tab=txt.read()
tables=tab.splitlines()
_exit=[]
rowNum=1
out=[]
states=[]
mainList=[]
i=0
while tables:
    state=tables.pop(0)[1:]
    mainList.append([state,[]])
    parser(mainList[i][1])
    i+=1
states.append(mainList[0][0])
while sequence and sequence[0]!='#end':
        _exit=[]
        for l in mainList:
            if l[0]==states[-1]:
                _list=l[1]

        for par in _list:
            automataOutput=enka(par[1])
            if automataOutput:
                    _exit.append(automataOutput)
                    _exit.append(par[0])
        print _exit
        if _exit:
            if len(_exit)>2:
                resolveAmbiguity(_exit)
            actions=_exit[1]
            expression=_exit[0]
            if actions[3]!='-':
                br=int(actions[3][9:])
                expression=expression[:br]
            if actions[0]!='-':
                out.append(actions[0])
                out.append(rowNum)
                out.append(expression)
            if actions[1]!='-':
                rowNum+=1
            if actions[2]!='-':
                states.append(actions[2][14:])
            if expression=='#n':
                sequence.pop(0)
            else:
                for i in range(len(expression)):
                    sequence.pop(0)
        else:
            print sequence.pop(0)

while out:
    d_output.write('%s %d %s\n'%(out.pop(0),out.pop(0),out.pop(0)))
    
d_output.close()
