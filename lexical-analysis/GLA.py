#GENERATOR OF LEXICAL ANALYZER#

import sys

def isOperator(expression,i):
    br=0
    while ((i-1)>=0 and expression[i-1]=='\\'):
        br=br+1
        i=i-1
    return br%2==0
        
def convert(expression,automata):
    choices=[]
    bracketNum=0
    var=0
    for i in range(len(expression)):
        if expression[i]=='(' and isOperator(expression,i):
            bracketNum=bracketNum+1
        elif expression[i]==')' and isOperator(expression,i):
            bracketNum=bracketNum-1
        elif bracketNum==0 and expression[i]=='|' and isOperator(expression,i):
            if var==0:
                choices.append(expression[var:i])
                var=i
            else:
                choices.append(expression[(var+1):i])
                var=i
    if len(choices)!=0:
        choices.append(expression[(var+1):])
    leftState=automata.newState()
    rightState=automata.newState()
    if len(choices)!=0:
        for i in range(len(choices)):
            temporary=convert(choices[i],automata)
            automata.addEpsilonTransition(leftState,temporary[0])
            automata.addEpsilonTransition(temporary[1],rightState)
    else:
        prefixed=False
        lastState=leftState
        i=0
        while i<len(expression):
            if prefixed:
                prefixed=False   ####CASE 1
                if expression[i]=='t':
                    transSign='\t'
                elif expression[i]=='n':
                    transSign='#n'
                elif expression[i]=='_':
                    transSign=' '
                elif expression[i]=='$':
                    transSign='#$'
                else:
                    transSign=expression[i]
                a=automata.newState()
                b=automata.newState()
                automata.addTransition(a,b,transSign)
            else:              ####CASE 2
                if expression[i]=='\\': 
                    prefixed=True
                    i=i+1
                    continue
                if expression[i]!='(':
                    a=automata.newState()
                    b=automata.newState()
                    if expression[i]=='$':
                        automata.addEpsilonTransition(a,b)
                    else:             
                            automata.addTransition(a,b,expression[i])   
                else:
                    brackets=1
                    for j in range(len(expression)):
                        if j>i:
                            if expression[j]=='(' and isOperator(expression,j):
                                brackets=brackets+1
                            elif expression[j]==')' and isOperator(expression,j):
                                if brackets>0:
                                    brackets=brackets-1
                                if brackets==0:
                                    index=j
                                    break
                    temporary=convert(expression[(i+1):(index)],automata)
                    a=temporary[0]
                    b=temporary[1]
                    i=index
            if (i+1)<len(expression) and expression[i+1]=='*':
                x=a
                y=b
                a=automata.newState()
                b=automata.newState()
                automata.addEpsilonTransition(a,x)
                automata.addEpsilonTransition(y,b)
                automata.addEpsilonTransition(a,b)
                automata.addEpsilonTransition(y,x)
                i=i+1
            automata.addEpsilonTransition(lastState,a)
            lastState=b
            i=i+1
        automata.addEpsilonTransition(lastState,rightState)
    return [leftState,rightState]

class Automata:
    
    stateNum=0
    startState=0
    acceptableState=0

    def newState(self):
        self.stateNum=self.stateNum+1
        return self.stateNum-1

    def addEpsilonTransition(self,state,next):
        dat=open('./definition.txt','a')
        dat.write('p'+str(state)+',$->'+'p'+str(next)+'\n')
        dat.close()

    def addTransition(self,state,next,transSign):
        dat=open('./definition.txt','a')
        dat.write('p'+str(state)+','+str(transSign)+'->'+'p'+str(next)+'\n')
        dat.close()

def doWrite(name,regExpression,newLine,enter,goBack):
    dat=open('./definition.txt','a')
    dat.write('#'+str(name)+'\n')
    dat.write(str(newLine)+'\n')
    dat.write(str(enter)+'\n')
    dat.write(str(goBack)+'\n')
    dat.write('p1\n')
    dat.write('p0\n')
    dat.close()
    aut=vars()[name]=Automata()
    lista=convert(regExpression,aut)
    aut.startState=lista[0]
    aut.acceptableState=lista[1]

def main():
    rows = [i[:] for i in sys.stdin.readlines()]
    n=len(rows)
    lkey=[]
    lvalue=[]
    counter=0
    for i in range(n):
        row=rows[i]
        counter=counter+1
        if (row.count('%X')):
            states=row[row.find('%X')+3:row.find('\n')].split(' ')
            break;
        else:
            key=row[row.find('{')+1:row.find('}')]
            value=row[row.find('}')+2:row.find('\n')]
            for k in range(len(lkey)):
                value=value.replace('{'+str(lkey[k])+'}','('+str(lvalue[k])+')')
            lkey.append(key)
            lvalue.append(value)
            
    for k in range(len(states)):
        vars()[states[k]]=[[],[],[],[],[]]
    i=0
    num=0
    symbol=0
    while i<len(rows):
        if i>counter:
            red=rows[i]
            for j in range(len(states)):
                doFind='<'+str(states[j])+'>'
                if red.count(doFind):
                    regExpression=red[red.find(doFind)+len(doFind):red.find('\n')]
                    for k in range(len(lkey)):
                        regExpression=regExpression.replace('{'+str(lkey[k])+'}','('+str(lvalue[k])+')')
                    name=rows[i+2]
                    name=name[:name.find('\n')]
                    z=1
                    newLine='-'
                    enter='-'
                    goBack='-'
                    while rows[i+2+z]!='}\n':
                        if rows[i+2+z].count('NOVI_REDAK'):
                            newLine=rows[i+2+z]
                            newLine=newLine[:newLine.find('\n')]
                        elif rows[i+2+z].count('UDJI_U_STANJE'):
                            enter=rows[i+2+z]
                            enter=enter[:enter.find('\n')]
                        elif rows[i+2+z].count('VRATI_SE'):
                            goBack=rows[i+2+z]
                            goBack=goBack[:goBack.find('\n')]
                        z=z+1

                    vars()[states[j]][0].append(name)
                    vars()[states[j]][1].append(regExpression)
                    vars()[states[j]][2].append(newLine)
                    vars()[states[j]][3].append(enter)
                    vars()[states[j]][4].append(goBack)
        i=i+1
    for i in range(len(states)):
        dat=open('./definition.txt','a')
        dat.write('%'+str(states[i])+'\n')
        dat.close()
        for j in range(len(vars()[states[i]][0])):
            doWrite(vars()[states[i]][0][j],vars()[states[i]][1][j],vars()[states[i]][2][j],vars()[states[i]][3][j],vars()[states[i]][4][j]) 
main()

