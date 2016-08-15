#GENERATOR OF SYNTAX ANALYZER#

import sys
from copy import deepcopy

def writeTable(dfaTranitions,endingSymbols,notEndingSymbols,smax,syncSymbols):
    dat=open('Table.txt','w')
    syncSymbols[0:]=[' '.join(syncSymbols[0:])]
    dat.write(syncSymbols[0]+'\n')
    for m in range(0,smax,1):
        dat.write('#'+str(m)+'\n')
        for i in range(1,len(dfaTranitions),1):
            if(dfaTranitions[i][0][0]==str(m)):
                if(dfaTranitions[i][1] in endingSymbols):
                    dat.write(dfaTranitions[i][1]+' pomakni('+dfaTranitions[i][2][0]+')\n')
                elif(dfaTranitions[i][1] in notEndingSymbols):
                    dat.write(dfaTranitions[i][1][1]+' stavi('+dfaTranitions[i][2][0]+')\n')
        for d in range(1,len(dfaTranitions),1):
            if(dfaTranitions[d][0][0]==str(m)):
                for j in range(1,len(dfaTranitions[d][0])):
                    index=dfaTranitions[d][0][j].find('{')
                    if(dfaTranitions[d][0][j][index-1]=='.'):
                        t=dfaTranitions[d][0][j].find('->')
                        if(dfaTranitions[d][0][j][0:t] in notEndingSymbols[0] and dfaTranitions[d][0][j][t+2:index-1] in notEndingSymbols[1] and dfaTranitions[d][0][j][index+1]=='#'):
                            dat.write('$$ prihvati\n')    
                        elif(dfaTranitions[d][0][j][0:t]!=notEndingSymbols[0]):
                            for k in range(index+1,len(dfaTranitions[d][0][j])-1,1):
                                if(dfaTranitions[d][0][j][k]=='#'):
                                    dat.write('$$')
                                else:
                                    dat.write(dfaTranitions[d][0][j][k])
                                dat.write(' reduciraj(')
                                t=dfaTranitions[d][0][j].find('.')
                                if(dfaTranitions[d][0][j][t-2]=='-' and dfaTranitions[d][0][j][t-1]=='>' and dfaTranitions[d][0][j][t+1]=='{'):
                                    for r in range(0,t,1):
                                        if(dfaTranitions[d][0][j][r]=='<' or (dfaTranitions[d][0][j][r]=='>' and dfaTranitions[d][0][j][r-1]!='-')):
                                            continue
                                        else:
                                            dat.write(dfaTranitions[d][0][j][r])
                                    dat.write('$')
                                else:
                                    for r in range(0,t,1):
                                        if(dfaTranitions[d][0][j][r]=='<' or (dfaTranitions[d][0][j][r]=='>' and dfaTranitions[d][0][j][r-1]!='-')):
                                            if(dfaTranitions[d][0][j].find('->')+2<r and r<dfaTranitions[d][0][j].find('{')-2 and dfaTranitions[d][0][j][r-1]!='>'):
                                                dat.write('.')
                                            continue
                                        else:
                                            dat.write(dfaTranitions[d][0][j][r])
                                            if(dfaTranitions[d][0][j][r].islower() and dfaTranitions[d][0][j][r+1]!='<' and dfaTranitions[d][0][j][r+1]!='.'):
                                                dat.write('.')
                                dat.write(')\n')
                break
            
    dat.close()
    return
	
def enfaToDfa(endingSymbols,notEndingSymbols,enfaTransitions,syncSymbols):
    sequence=''
    temp=[]
    temp1=[]
    temp2=[]
    temp3=[]
    transitions=[] 
    dfaTranitions=[]
    for i in range(0,len(enfaTransitions),1):
        temp.append(enfaTransitions[i][:enfaTransitions[i].find(',')])
        temp.append(enfaTransitions[i][enfaTransitions[i].find(',')+1:enfaTransitions[i].find('-> ')+3].strip())
        temp.append(enfaTransitions[i][enfaTransitions[i].find('-> ')+3:])
        transitions.append(temp)
        temp=[]
    temp=[]
    temp.append(transitions[0][0])
    t=0
    while(1):
        prevLength=len(temp)
        for i in range(0,len(transitions),1):
            if(transitions[i][0]==temp[t] and transitions[i][1]=='$->'):
                if(transitions[i][2] not in temp):
                    temp.append(transitions[i][2])
        if(prevLength==len(temp) and t==len(temp)-1):
            break
        t=t+1
    symbols=notEndingSymbols+endingSymbols
    temp1.append('')
    temp1.append('')
    temp1.append(temp)
    dfaTranitions.append(temp1)
    temp1=[]
    u=0
    while(1):
        lenDfa=len(dfaTranitions)
        for i in range(1,len(symbols),1):
            for j in range(0,len(dfaTranitions[u][2]),1):
                for k in range(0,len(transitions),1):
                    if(transitions[k][0]==dfaTranitions[u][2][j] and (symbols[i]+'->')==transitions[k][1]):
                        if(transitions[k][2] not in temp1):
                            temp1.append(transitions[k][2])
                        t=0
                        while(1):
                            prevLength=len(temp1)
                            for m in range(0,len(transitions),1):
                                if(transitions[m][0]==temp1[t] and transitions[m][1]=='$->'):
                                    if(transitions[m][2] not in temp1):
                                        temp1.append(transitions[m][2])
                            if(prevLength==len(temp1)):
                                break
                            t=t+1
                        break
            if(len(temp1)):
                temp2.append(dfaTranitions[u][2])
                temp2.append(symbols[i])
                temp2.append(temp1)
                if(temp2 not in dfaTranitions):
                    dfaTranitions.append(temp2)
                temp2=[]
                temp1=[]
            elif(dfaTranitions[u][2]!='!'):
                temp2.append(dfaTranitions[u][2])
                temp2.append('!')
                temp2.append('!')
                if(temp2 not in dfaTranitions):
                    dfaTranitions.append(temp2)
                temp2=[]
                temp1=[]
        if(u==len(dfaTranitions)-1 and lenDfa==len(dfaTranitions)):
            break
        u=u+1
    s=0
    for i in range(0,len(dfaTranitions),1):
        if(not dfaTranitions[i][2][0].isdigit() and dfaTranitions[i][2][0]!='!'):
            for j in range(1,len(dfaTranitions),1):
                if(dfaTranitions[j][0][0].isdigit() and dfaTranitions[j][0][1:]==dfaTranitions[i][2]):
                    dfaTranitions[i][2].insert(0,dfaTranitions[j][0][0])
                elif(dfaTranitions[j][2][0].isdigit() and dfaTranitions[j][2][1:]==dfaTranitions[i][2]):
                    dfaTranitions[i][2].insert(0,dfaTranitions[j][2][0])
            if(not dfaTranitions[i][2][0].isdigit()):
                dfaTranitions[i][2].insert(0,str(s))
                s+=1
    writeTable(dfaTranitions,endingSymbols,notEndingSymbols,s,syncSymbols)

def getEmptySymbols(empty,notEndingSymbols,productions):
    mainList=empty[:]
    mainList.sort()
    for i in range(len(notEndingSymbols)):
        for j in range(len(productions[i])):
            pom=len(productions[i][j])
            br=0
            for k in range(len(productions[i][j])):
                if productions[i][j][k] in empty or productions[i][j][k]=='$':
                    br=br+1
            if pom==br:
                mainList.append(notEndingSymbols[i])
                break
    hlpList=[]
    for i in range(len(mainList)):
        if mainList[i] not in hlpList:
            hlpList.append(mainList[i])
    hlpList.sort()
    if hlpList!=empty:
        return(getEmptySymbols(hlpList,notEndingSymbols,productions))
    else:
        return hlpList

def startWithSymbol(symbol,notEndingSymbols,endingSymbols,productions,empty,mainList,processed):
    if symbol in endingSymbols and symbol not in mainList:
        mainList.append(symbol)
        mainList.sort()
        return mainList
    else:
        for i in range(len(notEndingSymbols)):
            if symbol==notEndingSymbols[i]:
                for j in range(len(productions[i])):
                    if productions[i][j][0] in endingSymbols and productions[i][j][0] not in mainList:
                        mainList.append(productions[i][j][0])
                    elif productions[i][j][0] in notEndingSymbols and productions[i][j][0] not in processed:
                        processed.append(productions[i][j][0])
                        mainList=startWithSymbol(productions[i][j][0],notEndingSymbols,endingSymbols,productions,empty,mainList,processed)
                    if productions[i][j][0] in notEndingSymbols and productions[i][j][0] in empty:
                        if len(productions[i][j])>1:
                            mainList=startWithSymbol(productions[i][j][1],notEndingSymbols,endingSymbols,productions,empty,mainList,processed)
        mainList.sort()
        return mainList

    
def startProduction(sequence,notEndingSymbols,endingSymbols,productions,empty,mainList,processed):
    mainList=[]
    tmp=''
    if len(sequence)==0:
        mainList.append('#')
    for i in range(len(sequence)):
        hlpList=[]
        if sequence[i] in empty:
            hlpList=startWithSymbol(sequence[i],notEndingSymbols,endingSymbols,productions,empty,mainList,processed)
            for j in range(len(hlpList)):
                if hlpList[j] not in mainList:
                    mainList.append(hlpList[j])
        else:
            tmp=sequence[i]
            break
    if tmp!='':
        hlpList=startWithSymbol(tmp,notEndingSymbols,endingSymbols,productions,empty,mainList,processed)
        for j in range(len(hlpList)):
                if hlpList[j] not in mainList:
                    mainList.append(hlpList[j])
    mainList.sort()
    return mainList
            

class Transition:
    enfaTransition=[]
    def doAdd(self,symb1,symb2,first,next,symbol):
        output=str(symb1)+'->'
        for i in range(len(first[1])-1):
            output=output+str(first[1][i])
        output=output+'{'
        for i in range(len(first[2])):
            output=output+str(first[2][i])
        output=output+'}'  
        output=output+', '+str(symbol)+'-> '+str(symb2)+'->'
        for i in range(len(next[1])-1):
            output=output+str(next[1][i])          
        output=output+'{'
        for i in range(len(next[2])):
            output=output+str(next[2][i])
        output=output+'}'
        
        if output not in self.enfaTransition:
            self.enfaTransition.append(output)

def doSwitch(index,original):
    tmp=original[1][index+1]
    original[1][index+1]=original[1][index]
    original[1][index]=tmp
    return original[1]

def ENFA(item,stack,automata,startItems,productions,notEndingSymbols,endingSymbols,empty,processedItems):
    index=0
    newItem=[]
    processedItems.append(item)
    for i in range(len(item[1])-1):
        if item[1][i]=='.':
            index=i
            if item[1][i+1]!='#':
                tmp=deepcopy(item)
                hlp=[]
                hlp.append()
                hlp.append(doSwitch(index,tmp))
                hlp.append(item[2])
                automata.doAdd(item[0][0],item[0][0],item,hlp,item[1][i+1])
                if hlp not in processedItems and hlp not in stack:
                    stack.append(hlp)
            if item[1][i+1] in notEndingSymbols:
                pom=len(item[1][i+2:-1])
                br=0
                for j in range(pom):
                    if item[1][i+2+j] in empty:
                        br=br+1
                    else:
                        break
                        
                for j in range(len(notEndingSymbols)):
                    if item[1][i+1]==notEndingSymbols[j]:
                        for k in range(len(startItems[j])):
                            tmp2=deepcopy(startItems[j][k])
                            tmpl=[]
                            tmpl=startProduction(item[1][i+2:-1],notEndingSymbols,endingSymbols,productions,empty,[],[])
                            if br==pom:
                                copyList=[]
                                for z in range(len(item[2])):
                                    if item[2][z] not in copyList:
                                        copyList.append(item[2][z])
                                for z in range(len(tmpl)):
                                    if tmpl[z] not in copyList:
                                        copyList.append(tmpl[z])
                                copyList.sort()
                                newItem=[]
                                newItem.append([item[1][i+1]])
                                newItem.append(tmp2[1])
                                newItem.append(copyList)
                                automata.doAdd(item[0][0],item[1][i+1],item,newItem,'$')
                                if newItem not in processedItems and newItem not in stack:
                                    stack.append(newItem)
                            else:
                                newItem=[]
                                newItem.append([item[1][i+1]])
                                newItem.append(tmp2[1])
                                newItem.append(tmpl)
                                automata.doAdd(item[0][0],item[1][i+1],item,newItem,'$')
                                if newItem not in processedItems and newItem not in stack:
                                    stack.append(newItem)
    return [stack,processedItems]

                                
                   
def main():
    inputFile=file('test.san')
    n=len(inputFile.readlines())
    inputFile.seek(0)
    for i in range(n):
        row=inputFile.readline()
        if (row.count('%V')):
            output=row[row.find('%V')+3:row.find('\n')]
            notEndingSymbols=output.split(' ')
        if (row.count('%T')):
            output=row[row.find('%T')+3:row.find('\n')]
            endingSymbols=output.split(' ')
        if (row.count('%Syn')):
            output=row[row.find('%Syn')+5:row.find('\n')]
            syncSymbols=output.split(' ')
    inputFile.seek(0)
    productions=[]
    startItems=[]
    empty=[]
    tmp=0
    startingNESymbol='<pocNZ>'
    for i in range(len(notEndingSymbols)):
        productions.append([])
        startItems.append([])
    for i in range(n):
        row=inputFile.readline()
        row=row[:row.find('\n')]
        if row in notEndingSymbols:
            tmp=row
        else:
            for j in range(len(notEndingSymbols)):
                if tmp==notEndingSymbols[j]:
                    prod=row[1:].split(' ')
                    productions[j].append(prod)
                    if row.count('$'):
                        empty.append(tmp)
                        startItems[j].append([[notEndingSymbols[j]],['.','#']])
                    else:
                        prod2=[]
                        prod2.append('.')
                        for k in range(len(prod)):
                            prod2.append(prod[k])
                        prod2.append('#')    
                        startItems[j].append([[notEndingSymbols[j]],prod2])
    automata=Transition()
    empty=getEmptySymbols([],notEndingSymbols,productions)

    for i in range(len(productions)):
        for j in range(len(productions[i])):
            startItems[i][j].append(['#'])
            
    stack=[]
    startItem=[]
    startItem.append([startingNESymbol])
    startItem.append(['.',notEndingSymbols[0],'#'])
    startItem.append(['#'])
    solution=ENFA(startItem,stack,automata,startItems,productions,notEndingSymbols,endingSymbols,empty,[])
    while(len(solution[0]))>0:
        startItem=solution[0].pop()
        solution=ENFA(startItem,solution[0],automata,startItems,productions,notEndingSymbols,endingSymbols,empty,solution[1])
    notEndingSymbols.insert(0,'<pocNZ>')
    enfaToDfa(endingSymbols,notEndingSymbols,automata.enfaTransition,syncSymbols)
 
main()

