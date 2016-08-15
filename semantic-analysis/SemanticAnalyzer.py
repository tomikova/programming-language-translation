class Provjera:

    def prijevodna_jedinica(self, br_cvor): #*
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<vanjska_deklaracija>':
            provjeri=Provjera()
            provjeri.vanjska_deklaracija(produkcija[0])
        elif stablo[produkcija[0]][0]=='<prijevodna_jedinica>':
            provjeri=Provjera()
            provjeri.prijevodna_jedinica(produkcija[0])
            provjeri=Provjera()
            provjeri.vanjska_deklaracija(produkcija[1])

    def vanjska_deklaracija(self, br_cvor): #*
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<definicija_funkcije>':
            provjeri=Provjera()
            provjeri.definicija_funkcije(produkcija[0])
        elif stablo[produkcija[0]][0]=='<deklaracija>':
            provjeri=Provjera()
            provjeri.deklaracija(produkcija[0])

    def definicija_funkcije(self, br_cvor): 
        global stablo, definicije, deklaracije, djelokrug, identifikatori, fun_pov
        produkcija=stablo[br_cvor][2]
        elem=stablo[produkcija[1]][0]
        red1=elem.split(' ')[1]
        jed1=elem.split(' ')[2]
        elem=stablo[produkcija[2]][0]
        red2=elem.split(' ')[1]
        jed2=elem.split(' ')[2]
        if 'KR_VOID' in stablo[produkcija[3]][0]:
            provjeri=Provjera()
            provjeri.ime_tipa(produkcija[0])
            tip=stablo[produkcija[0]][3]
            ime=stablo[produkcija[1]][0].split(' ')[2]
            elem=stablo[produkcija[3]][0]
            red3=elem.split(' ')[1]
            jed3=elem.split(' ')[2]
            elem=stablo[produkcija[4]][0]
            red4=elem.split(' ')[1]
            jed4=elem.split(' ')[2]
            if tip in ('const(int)', 'const(char)') or ime in definicije: 
                print('<definicija_funkcije> ::= <ime_tipa> IDN(%s,%s) L_ZAGRADA(%s,%s) KR_VOID(%s,%s) D_ZAGRADA(%s,%s) <slozena_naredba>'%(red1,jed1,red2,jed2,red3,jed3,red4,jed4))
                exit(0)
            elif ime in deklaracije:
                if deklaracije[ime][0]!='void' or definicije[ime][1]!=tip:
                    print('<definicija_funkcije> ::= <ime_tipa> IDN(%s,%s) L_ZAGRADA(%s,%s) KR_VOID(%s,%s) D_ZAGRADA(%s,%s) <slozena_naredba>'%(red1,jed1,red2,jed2,red3,jed3,red4,jed4))
                    exit(0)
                
            definicije[ime]=['void', tip]
            if ime not in deklaracije:
                deklaracije[ime]=['void', tip]
            idn.append([ime, 'void', tip,1])
            provjeri=Provjera()
            fun_pov.append(tip)
            provjeri.slozena_naredba(produkcija[5])
            fun_pov.pop()
        else:
            provjeri=Provjera()
            provjeri.ime_tipa(produkcija[0])
            tip=stablo[produkcija[0]][3]
            ime=stablo[produkcija[1]][0].split(' ')[2]
            elem=stablo[produkcija[4]][0]
            red3=elem.split(' ')[1]
            jed3=elem.split(' ')[2]
            if tip in ('const(int)', 'const(char)') or ime in definicije: 
                print('<definicija_funkcije> ::= <ime_tipa> IDN(%s,%s) L_ZAGRADA(%s,%s) <lista_parametara> D_ZAGRADA(%s,%s) <slozena_naredba>'%(red1,jed1,red2,jed2,red3,jed3))
                exit(0)
            provjeri=Provjera()
            provjeri.lista_parametara(produkcija[3])
            tipovi=stablo[produkcija[3]][3]
            imena=stablo[produkcija[3]][4]
            if ime in deklaracije:
                if deklaracije[ime][0]!=tipovi or deklaracije[ime][1]!=tip:
                    print('<definicija_funkcije> ::= <ime_tipa> IDN(%s,%s) L_ZAGRADA(%s,%s) <lista_parametara> D_ZAGRADA(%s,%s) <slozena_naredba>'%(red1,jed1,red2,jed2,red3,jed3))
                    exit(0)
            
            definicije[ime]=[tipovi, tip]
            if ime not in deklaracije:
                deklaracije[ime]=[tipovi, tip]
            idn.append([ime, tipovi, tip,1])
            for i in range(len(imena)):
                idn.append([imena[i], tipovi[i], 0, sljedeci_djelokrug])
                
            provjeri=Provjera()
            fun_pov.append(tip)
            provjeri.slozena_naredba(produkcija[5])
            fun_pov.pop()

    def lista_parametara(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<deklaracija_parametra>':
            provjeri=Provjera()
            provjeri.deklaracija_parametra(produkcija[0])
            tip=stablo[produkcija[0]][3]
            ime=stablo[produkcija[0]][4]
            stablo[br_cvor].append([tip])
            stablo[br_cvor].append([ime])
        else:
            provjeri=Provjera()
            provjeri.lista_parametara(produkcija[0])
            tipovi=stablo[produkcija[0]][3]
            imena=stablo[produkcija[0]][4]
            provjeri=Provjera()
            provjeri.deklaracija_parametra(produkcija[2])
            tip=stablo[produkcija[2]][3]
            ime=stablo[produkcija[2]][4]
            if ime in imena:
                elem=stablo[produkcija[1]][0]
                red=elem.split(' ')[1]
                jed=elem.split(' ')[2]
                print('<lista_parametara> ::= <lista_parametara> ZAREZ(%s,%s) <deklaracija_parametra>'%(red, jed))
                exit(0)
            tipovi.append(tip)
            imena.append(ime)
            stablo[br_cvor].append(tipovi)
            stablo[br_cvor].append(imena)
    def deklaracija_parametra(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        elem=stablo[produkcija[1]][0]
        red=elem.split(' ')[1]
        jed=elem.split(' ')[2]
        
        if len(produkcija)<3:
            provjeri=Provjera()
            provjeri.ime_tipa(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if tip=='void':
                print('<deklaracija_parametra> ::= <ime_tipa> IDN(%s,%s)'%(red, jed))
                exit(0)
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(jed)
        else:
            provjeri=Provjera()
            provjeri.ime_tipa(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if tip=='void':
                elem=stablo[produkcija[2]][0]
                red2=elem.split(' ')[1]
                jed2=elem.split(' ')[2]
                elem=stablo[produkcija[3]][0]
                red3=elem.split(' ')[1]
                jed3=elem.split(' ')[2]
                print('<deklaracija_parametra> ::= <ime_tipa> IDN(%s,%s) L_UGL_ZAGRADA(%s,%s) D_UGL_ZAGRADA(%s,%s)'%(red, jed,red2,jed2,red3,jed3))
                exit(0)
            stablo[br_cvor].append('niz(%s)'%tip)
            stablo[br_cvor].append(jed)
            
            
    def ime_tipa(self, br_cvor): ##*
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<specifikator_tipa>':
            provjeri=Provjera()
            provjeri.specifikator_tipa(produkcija[0])
            tip=stablo[produkcija[0]][3]
            stablo[br_cvor].append(tip)
        else:
            provjeri=Provjera()
            provjeri.specifikator_tipa(produkcija[1])
            tip=stablo[produkcija[1]][3]
            if tip=='void':
                elem=stablo[produkcija[0]]
                red=elem.split(' ')[1]
                jed=elem.split(' ')[2]
                print ('<ime_tipa> ::= KR_CONST(%s,%s) <specifikator_tipa>'%(red,jed))
                exit(0)
            tip='const(%s)'%tip
            stablo[br_cvor].append(tip)
            

    def specifikator_tipa(self, br_cvor): ##*
        global stablo
        produkcija=stablo[br_cvor][2]
        if 'KR_VOID' in stablo[produkcija[0]][0]:
            tip='void'
        elif 'KR_INT' in stablo[produkcija[0]][0]:
            tip='int'
        elif 'KR_CHAR' in stablo[produkcija[0]][0]:
            tip='char'
        stablo[br_cvor].append(tip)    
        
            
        
    def slozena_naredba(self, br_cvor): ##*
        global stablo, djelokrug, sljedeci_djelokrug
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[1]][0]=='<lista_naredbi>':
            djelokrug.append(sljedeci_djelokrug)
            sljedeci_djelokrug+=1
            provjeri=Provjera()
            provjeri.lista_naredbi(produkcija[1])
            djelokrug.pop()
        elif stablo[produkcija[1]][0]=='<lista_deklaracija>':
            djelokrug.append(sljedeci_djelokrug)
            sljedeci_djelokrug+=1
            provjeri=Provjera()
            provjeri.lista_deklaracija(produkcija[1])
            provjeri=Provjera()
            provjeri.lista_naredbi(produkcija[2])
            djelokrug.pop()
    def lista_naredbi(self, br_cvor): ##*
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<naredba>':
            provjeri=Provjera()
            provjeri.naredba(produkcija[0])
        elif stablo[produkcija[0]][0]=='<lista_naredbi>':
            provjeri=Provjera()
            provjeri.lista_naredbi(produkcija[0])         
            provjeri=Provjera()
            provjeri.naredba(produkcija[1])            
        
    def naredba(self, br_cvor): ##*
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<slozena_naredba>':
            provjeri=Provjera()
            provjeri.slozena_naredba(produkcija[0])
        elif stablo[produkcija[0]][0]=='<izraz_naredba>':
            provjeri=Provjera()
            provjeri.izraz_naredba(produkcija[0])
        elif stablo[produkcija[0]][0]=='<naredba_grananja>':
            provjeri=Provjera()
            provjeri.naredba_grananja(produkcija[0])
        elif stablo[produkcija[0]][0]=='<naredba_petlje>':
            provjeri=Provjera()
            provjeri.naredba_petlje(produkcija[0])
        elif stablo[produkcija[0]][0]=='<naredba_skoka>':
            provjeri=Provjera()
            provjeri.naredba_skoka(produkcija[0])        

    def izraz_naredba(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<izraz>':
            provjeri=Provjera()
            provjeri.izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            stablo[br_cvor].append(tip)
        else:
            stablo[br_cvor].append('int')

    def naredba_grananja(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        elem=stablo[produkcija[0]][0]
        red1=elem.split(' ')[1]
        jed1=elem.split(' ')[2]
        elem=stablo[produkcija[1]][0]
        red2=elem.split(' ')[1]
        jed2=elem.split(' ')[2]
        elem=stablo[produkcija[3]][0]
        red3=elem.split(' ')[1]
        jed3=elem.split(' ')[2]
        if len(produkcija)<6:
            provjeri=Provjera()
            provjeri.izraz(produkcija[2])            
            tip=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<naredba_grananja> ::= KR_IF(%s,%s) L_ZAGRADA(%s,%s) <izraz> D_ZAGRADA(%s,%s) <naredba>'%(red1, jed1, red2, jed2, red3, jed3))
                exit(0)
            provjeri=Provjera()
            provjeri.naredba(produkcija[4])
        else:
            provjeri=Provjera()
            provjeri.izraz(produkcija[2])            
            tip=stablo[produkcija[2]][3]           
            elem=stablo[produkcija[5]][0]
            red4=elem.split(' ')[1]
            jed4=elem.split(' ')[2]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<naredba_grananja> ::= KR_IF(%s,%s) L_ZAGRADA(%s,%s) <izraz> D_ZAGRADA(%s,%s) <naredba> KR_ELSE(%s,%s) <naredba>'%(red1, jed1, red2, jed2, red3, jed3, red4, jed4))
                exit(0)
            provjeri=Provjera()
            provjeri.naredba(produkcija[4])
            provjeri=Provjera()
            provjeri.naredba(produkcija[6])
            
    def naredba_skoka(self, br_cvor):
        global stablo, petlja, fun_pov
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0].split(' ')[0] in ('KR_CONTINUE', 'KR_BREAK'):
            if petlja==[]:
                elem=stablo[produkcija[0]][0]
                znak1=elem.split(' ')[0]
                red1=elem.split(' ')[1]
                jed1=elem.split(' ')[2]
                elem=stablo[produkcija[1]][0]
                red2=elem.split(' ')[1]
                jed2=elem.split(' ')[2]
                print ('<naredba_skoka> ::= %s(%s,%s) TOCKAZAREZ(%s,%s)'%(znak1, red1, jed1, red2, jed2))
                exit(0)
        elif stablo[produkcija[1]][0]!='<izraz>':
            if fun_pov[-1]!='void':
                elem=stablo[produkcija[0]][0]
                red1=elem.split(' ')[1]
                jed1=elem.split(' ')[2]
                elem=stablo[produkcija[1]][0]
                red2=elem.split(' ')[1]
                jed2=elem.split(' ')[2]               
                print ('<naredba_skoka> ::= KR_RETURN(%s,%s) TOCKAZAREZ(%s,%s)'%(red1, jed1, red2, jed2))
                exit(0)
        elif stablo[produkcija[1]][0]=='<izraz>':
            provjeri=Provjera()
            provjeri.izraz(produkcija[1])
            tip=stablo[produkcija[1]][3]
            if vrijedi_tilda(tip, fun_pov[-1])==0:
                elem=stablo[produkcija[0]][0]
                red1=elem.split(' ')[1]
                jed1=elem.split(' ')[2]
                elem=stablo[produkcija[2]][0]
                red2=elem.split(' ')[1]
                jed2=elem.split(' ')[2]               
                print ('<naredba_skoka> ::= KR_RETURN(%s,%s) <izraz> TOCKAZAREZ(%s,%s)'%(red1, jed1, red2, jed2))
                exit(0)
                
    def naredba_petlje(self, br_cvor):
        global stablo, petlja
        produkcija=stablo[br_cvor][2]
        elem=stablo[produkcija[0]][0]
        red1=elem.split(' ')[1]
        jed1=elem.split(' ')[2]
        elem=stablo[produkcija[1]][0]
        red2=elem.split(' ')[1]
        jed2=elem.split(' ')[2]
        if 'KR_WHILE' in stablo[produkcija[0]][0]:
            provjeri=Provjera()
            provjeri.izraz(produkcija[2])
            tip=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip, 'int')==0:
                elem=stablo[produkcija[3]][0]
                red3=elem.split(' ')[1]
                jed3=elem.split(' ')[2]
                print('<naredba_petlje> ::= KR_WHILE(%s,%s) L_ZAGRADA(%s,%s) <izraz> D_ZAGRADA(%s,%s) <naredba>'%(red1,jed1,red2,jed2,red3,jed3))
                exit(0)
            provjeri=Provjera()
            petlja.append(1)
            provjeri.naredba(produkcija[4])
            petlja.pop()
        elif stablo[produkcija[5]][0]=='<naredba>':
            provjeri=Provjera()
            provjeri.izraz_naredba(produkcija[2])
            provjeri=Provjera()
            provjeri.izraz_naredba(produkcija[3])
            tip=stablo[produkcija[3]][3]
            if vrijedi_tilda(tip, 'int')==0:
                elem=stablo[produkcija[4]][0]
                red3=elem.split(' ')[1]
                jed3=elem.split(' ')[2]
                print('<naredba_petlje> ::= KR_FOR(%s,%s) L_ZAGRADA(%s,%s) <izraz_naredba> <izraz_naredba> D_ZAGRADA(%s,%s) <naredba>'%(red1,jed1,red2,jed2,red3,jed3))
                exit(0)
            provjeri=Provjera()
            petlja.append(1)
            provjeri.naredba(produkcija[5])
            petlja.pop()
        else:
            provjeri=Provjera()
            provjeri.izraz_naredba(produkcija[2])
            provjeri=Provjera()
            provjeri.izraz_naredba(produkcija[3])
            tip=stablo[produkcija[3]][3]
            if vrijedi_tilda(tip, 'int')==0:
                elem=stablo[produkcija[5]][0]
                red3=elem.split(' ')[1]
                jed3=elem.split(' ')[2]
                print('<naredba_petlje> ::= KR_FOR(%s,%s) L_ZAGRADA(%s,%s) <izraz_naredba> <izraz_naredba> <izraz> D_ZAGRADA(%s,%s) <naredba>'%(red1,jed1,red2,jed2,red3,jed3))
                exit(0)
            provjeri=Provjera()
            provjeri.izraz(produkcija[4])
            provjeri=Provjera()
            petlja.append(1)
            provjeri.naredba(produkcija[6])
            petlja.pop()
            
                
    def izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<izraz_pridruzivanja>':
            provjeri=Provjera()
            provjeri.izraz_pridruzivanja(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)

        elif stablo[produkcija[0]][0]=='<izraz>':
            provjeri=Provjera()
            provjeri.izraz(produkcija[0])            
            provjeri=Provjera()
            provjeri.izraz_pridruzivanja(produkcija[2])
            tip=stablo[produkcija[2]][3]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(0)            
            

    def izraz_pridruzivanja(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<log_ili_izraz>':
            provjeri=Provjera()
            provjeri.log_ili_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        elif stablo[produkcija[0]][0]=='<postfiks_izraz>':
            provjeri=Provjera()
            provjeri.postfiks_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            elem=stablo[produkcija[1]][0]
            red=elem.split(' ')[1]
            jed=elem.split(' ')[2]
            if stablo[produkcija[0]][4]!=1:
                print ('<izraz_pridruzivanja> ::= <postfiks_izraz> OP_PRIDRUZI(%s,%s) <izraz_pridruzivanja>'%(red, jed))
                exit(0)
            provjeri=Provjera()
            provjeri.izraz_pridruzivanja(produkcija[2])
            if vrijedi_tilda(stablo[produkcija[2]][3], stablo[produkcija[0]][3])==0:
                print ('<izraz_pridruzivanja> ::= <postfiks_izraz> OP_PRIDRUZI(%s,%s) <izraz_pridruzivanja>'%(red, jed))
                exit(0)
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(0)

    def log_ili_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<log_i_izraz>':
            provjeri=Provjera()
            provjeri.log_i_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        else:
            element=stablo[produkcija[1]][0]
            znak=element.split(' ')[0]
            redak=element.split(' ')[1]
            jedinka=element.split(' ')[2]
            provjeri=Provjera()
            provjeri.log_ili_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<log_ili_izraz> ::= <log_ili_izraz> %s(%s,%s) <log_i_izraz>'%(znak, redak, jedinka))
                exit(0)
            provjeri=Provjera()
            provjeri.log_i_izraz(produkcija[2])
            tip=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<log_ili_izraz> ::= <log_ili_izraz> %s(%s,%s) <log_i_izraz>'%(znak, redak, jedinka))
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)

    def log_i_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<bin_ili_izraz>':
            provjeri=Provjera()
            provjeri.bin_ili_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        else:
            element=stablo[produkcija[1]][0]
            znak=element.split(' ')[0]
            redak=element.split(' ')[1]
            jedinka=element.split(' ')[2]
            provjeri=Provjera()
            provjeri.log_i_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<log_i_izraz> ::= <log_i_izraz> %s(%s,%s) <bin_ili_izraz>'%(znak, redak, jedinka))
                exit(0)
            provjeri=Provjera()
            provjeri.bin_ili_izraz(produkcija[2])
            tip=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<log_i_izraz> ::= <log_i_izraz> %s(%s,%s) <bin_ili_izraz>'%(znak, redak, jedinka))
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)

    def bin_ili_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<bin_xili_izraz>':
            provjeri=Provjera()
            provjeri.bin_xili_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        else:
            element=stablo[produkcija[1]][0]
            znak=element.split(' ')[0]
            redak=element.split(' ')[1]
            jedinka=element.split(' ')[2]
            provjeri=Provjera()
            provjeri.bin_ili_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<bin_ili_izraz> ::= <bin_ili_izraz> %s(%s,%s) <bin_xili_izraz>'%(znak, redak, jedinka))
                exit(0)
            provjeri=Provjera()
            provjeri.bin_xili_izraz(produkcija[2])
            tip=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<bin_ili_izraz> ::= <bin_ili_izraz> %s(%s,%s) <bin_xili_izraz>'%(znak, redak, jedinka))
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)
    def bin_xili_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<bin_i_izraz>':
            provjeri=Provjera()
            provjeri.bin_i_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        else:
            element=stablo[produkcija[1]][0]
            znak=element.split(' ')[0]
            redak=element.split(' ')[1]
            jedinka=element.split(' ')[2]
            provjeri=Provjera()
            provjeri.bin_xili_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<bin_xili_izraz> ::= <bin_xili_izraz> %s(%s,%s) <bin_i_izraz>'%(znak, redak, jedinka))
                exit(0)
            provjeri=Provjera()
            provjeri.bin_i_izraz(produkcija[2])
            tip=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<bin_xili_izraz> ::= <bin_xili_izraz> %s(%s,%s) <bin_i_izraz>'%(znak, redak, jedinka))
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)

    def bin_i_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<jednakosni_izraz>':
            provjeri=Provjera()
            provjeri.jednakosni_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        else:
            element=stablo[produkcija[1]][0]
            znak=element.split(' ')[0]
            redak=element.split(' ')[1]
            jedinka=element.split(' ')[2]
            provjeri=Provjera()
            provjeri.bin_i_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<bin_i_izraz> ::= <bin_i_izraz> %s(%s,%s) <jednakosni_izraz>'%(znak, redak, jedinka))
                exit(0)
            provjeri=Provjera()
            provjeri.jednakosni_izraz(produkcija[2])
            tip=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<bin_i_izraz> ::= <bin_i_izraz> %s(%s,%s) <jednakosni_izraz>'%(znak, redak, jedinka))
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)

    def jednakosni_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<odnosni_izraz>':
            provjeri=Provjera()
            provjeri.odnosni_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        else:
            element=stablo[produkcija[1]][0]
            znak=element.split(' ')[0]
            redak=element.split(' ')[1]
            jedinka=element.split(' ')[2]
            provjeri=Provjera()
            provjeri.jednakosni_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<jednakosni_izraz> ::= <jednakosni_izraz> %s(%s,%s) <odnosni_izraz>'%(znak, redak, jedinka))
                exit(0)
            provjeri=Provjera()
            provjeri.odnosni_izraz(produkcija[2])
            tip=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<jednakosni_izraz> ::= <jednakosni_izraz> %s(%s,%s) <odnosni_izraz>'%(znak, redak, jedinka))
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)

    def odnosni_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<aditivni_izraz>':
            provjeri=Provjera()
            provjeri.aditivni_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        else:
            element=stablo[produkcija[1]][0]
            znak=element.split(' ')[0]
            redak=element.split(' ')[1]
            jedinka=element.split(' ')[2]
            provjeri=Provjera()
            provjeri.odnosni_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<odnosni_izraz> ::= <odnosni_izraz> %s(%s,%s) <aditivni_izraz>'%(znak, redak, jedinka))
                exit(0)
            provjeri=Provjera()
            provjeri.aditivni_izraz(produkcija[2])
            tip=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<odnosni_izraz> ::= <odnosni_izraz> %s(%s,%s) <aditivni_izraz>'%(znak, redak, jedinka))
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)

    def aditivni_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<multiplikativni_izraz>':
            provjeri=Provjera()
            provjeri.multiplikativni_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        else:
            element=stablo[produkcija[1]][0]
            znak=element.split(' ')[0]
            redak=element.split(' ')[1]
            jedinka=element.split(' ')[2]
            provjeri=Provjera()
            provjeri.aditivni_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<aditivni_izraz> ::= <aditivni_izraz> %s(%s,%s) <multiplikativni_izraz>'%(znak, redak, jedinka))
                exit(0)
            provjeri=Provjera()
            provjeri.multiplikativni_izraz(produkcija[2])
            tip=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<aditivni_izraz> ::= <aditivni_izraz> %s(%s,%s) <multiplikativni_izraz>'%(znak, redak, jedinka))
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)
            
            

            

    def multiplikativni_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<cast_izraz>':
            provjeri=Provjera()
            provjeri.cast_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        else:
            element=stablo[produkcija[1]][0]
            znak=element.split(' ')[0]
            redak=element.split(' ')[1]
            jedinka=element.split(' ')[2]
            provjeri=Provjera()
            provjeri.multiplikativni_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<multiplikativni_izraz> ::= <multiplikativni_izraz> %s(%s,%s) <cast_izraz>'%(znak, redak, jedinka))
                exit(0)
            provjeri=Provjera()
            provjeri.cast_izraz(produkcija[2])
            tip=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print ('<multiplikativni_izraz> ::= <multiplikativni_izraz> %s(%s,%s) <cast_izraz>'%(znak, redak, jedinka))
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)

    def cast_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<unarni_izraz>':
            provjeri=Provjera()
            provjeri.unarni_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        else:
            provjeri=Provjera()
            provjeri.ime_tipa(produkcija[1])
            tip=stablo[produkcija[1]][3]
            provjeri=Provjera()
            provjeri.cast_izraz(produkcija[3])
            tip1=stablo[produkcija[3]][3]
            if tip=='void' or tip1 not in('int', 'char', 'const(int)', 'const(char)'):
                element=stablo[produkcija[0]][0]
                red1=element.split(' ')[1]
                jed1=element.split(' ')[2]               
                element=stablo[produkcija[2]][0]
                red2=element.split(' ')[1]
                jed2=element.split(' ')[2]
                print('<cast_izraz> ::= L_ZAGRADA(%s,%s) <ime_tipa> D_ZAGRADA(%s,%s) <cast_izraz>'%(red1,jed1,red2,jed2))
                exit(0)
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(0)            


    def unarni_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<postfiks_izraz>':
            provjeri=Provjera()
            provjeri.postfiks_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        elif stablo[produkcija[1]][0]=='<unarni_izraz>':
            provjeri=Provjera()
            provjeri.unarni_izraz(produkcija[1])
            tip=stablo[produkcija[1]][3]
            l_izraz=stablo[produkcija[1]][4]
            if l_izraz==0 or vrijedi_tilda(tip, 'int')==0:
                elem=stablo[produkcija[0]][0]
                znak=elem.split(' ')[0]
                red=elem.split(' ')[1]
                jed=elem.split(' ')[2]
                print ('<unarni_izraz> ::= %s(%s,%s) <unarni_izraz>'%(znak, red, jed))
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)
        else:
            provjeri=Provjera()
            provjeri.cast_izraz(produkcija[1])
            tip=stablo[produkcija[1]][3]
            if vrijedi_tilda(tip, 'int')==0:
                print('<unarni_izraz> ::= <unarni_operator> <cast_izraz>')
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)            

    def postfiks_izraz(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<primarni_izraz>':
            provjeri=Provjera()
            provjeri.primarni_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        elif 'L_UGL_ZAGRADA' in stablo[produkcija[1]][0]:
            provjeri=Provjera()
            provjeri.postfiks_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            if tip not in ('niz(int)', 'niz(const(int))', 'niz(char)', 'niz(const(char))'):
                element=stablo[produkcija[1]][0]
                redak1=element.split(' ')[1]
                jedinka1=element.split(' ')[2]
                element=stablo[produkcija[3]][0]
                redak2=element.split(' ')[1]
                jedinka2=element.split(' ')[2]
                print ('<postfiks_izraz> ::= <postfiks_izraz> L_UGL_ZAGRADA(%s,%s) <izraz> D_UGL_ZAGRADA(%s,%s)'%(redak1, jedinka1, redak2, jedinka2))
                exit(0)
            provjeri=Provjera()
            provjeri.izraz(produkcija[2])
            tip1=stablo[produkcija[2]][3]
            if vrijedi_tilda(tip1, 'int')==0:
                element=stablo[produkcija[1]][0]
                redak1=element.split(' ')[1]
                jedinka1=element.split(' ')[2]
                element=stablo[produkcija[3]][0]
                redak2=element.split(' ')[1]
                jedinka2=element.split(' ')[2]
                print ('<postfiks_izraz> ::= <postfiks_izraz> L_UGL_ZAGRADA(%s,%s) <izraz> D_UGL_ZAGRADA(%s,%s)'%(redak1, jedinka1, redak2, jedinka2))
                exit(0)
            tip=tip[4:-1]
            if len(tip)>5:
                l_izraz=0
            else:
                l_izraz=1;
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)
        elif len(produkcija)==3:
            provjeri=Provjera()
            provjeri.postfiks_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            pov=stablo[produkcija[0]][4]
            if tip!='void' or type(pov)!=str:
                element=stablo[produkcija[1]][0]
                redak1=element.split(' ')[1]
                jedinka1=element.split(' ')[2]
                element=stablo[produkcija[2]][0]
                redak2=element.split(' ')[1]
                jedinka2=element.split(' ')[2]
                print ('<postfiks_izraz> ::= <postfiks_izraz> L_ZAGRADA(%s,%s) D_ZAGRADA(%s,%s)'%(redak1, jedinka1, redak2, jedinka2))
                exit(0)
            stablo[br_cvor].append(pov)
            stablo[br_cvor].append(0)
        elif 'L_ZAGRADA' in stablo[produkcija[1]][0]:
            provjeri=Provjera()
            provjeri.postfiks_izraz(produkcija[0])
            params=stablo[produkcija[0]][3]
            pov=stablo[produkcija[0]][4]            
            provjeri=Provjera()
            provjeri.lista_argumenata(produkcija[2])
            tipovi=stablo[produkcija[2]][3]
            if type(pov)!=str or len(params)!=len(tipovi):
                element=stablo[produkcija[1]][0]
                redak1=element.split(' ')[1]
                jedinka1=element.split(' ')[2]
                element=stablo[produkcija[3]][0]
                redak2=element.split(' ')[1]
                jedinka2=element.split(' ')[2]
                print ('<postfiks_izraz> ::= <postfiks_izraz> L_ZAGRADA(%s,%s) <lista_argumenata> D_ZAGRADA(%s,%s)'%(redak1, jedinka1, redak2, jedinka2))
                exit(0)
            for i in range(len(params)):
                if vrijedi_tilda(tipovi[i], params[i])==0:
                    element=stablo[produkcija[1]][0]
                    redak1=element.split(' ')[1]
                    jedinka1=element.split(' ')[2]
                    element=stablo[produkcija[3]][0]
                    redak2=element.split(' ')[1]
                    jedinka2=element.split(' ')[2]
                    print ('<postfiks_izraz> ::= <postfiks_izraz> L_ZAGRADA(%s,%s) <lista_argumenata> D_ZAGRADA(%s,%s)'%(redak1, jedinka1, redak2, jedinka2))
                    exit(0)
            stablo[br_cvor].append(pov)
            stablo[br_cvor].append(0)
        else:
            provjeri=Provjera()
            provjeri.postfiks_izraz(produkcija[0])
            tip=stablo[produkcija[0]][3]
            l_izraz=stablo[produkcija[0]][4]
            if l_izraz==0 or vrijedi_tilda(tip, 'int')==0:
                element=stablo[produkcija[1]][0]
                znak=element.split(' ')[0]
                redak=element.split(' ')[1]
                jedinka=element.split(' ')[2]                
                print ('<postfiks_izraz> ::= <postfiks_izraz> %s(%s,%s)'%(znak, redak, jedinka))
                exit(0)
            stablo[br_cvor].append('int')
            stablo[br_cvor].append(0)
    def lista_argumenata(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<izraz_pridruzivanja>':
            provjeri=Provjera()
            provjeri.izraz_pridruzivanja(produkcija[0])
            tip=stablo[produkcija[0]][3]
            stablo[br_cvor].append([tip])
        elif stablo[produkcija[0]][0]=='<lista_argumenata>':
            provjeri=Provjera()
            provjeri.lista_argumenata(produkcija[0])
            tipovi=stablo[produkcija[0]][3]
            provjeri=Provjera()
            provjeri.izraz_pridruzivanja(produkcija[2])
            tip=stablo[produkcija[2]][3]
            tipovi.append(tip)
            stablo[br_cvor].append(tipovi)
            
            
    def primarni_izraz(self, br_cvor):
        global stablo, idn, djelokrug
        produkcija=stablo[br_cvor][2]
        element=stablo[produkcija[0]][0]
        unif_znak=element.split(' ')[0]
        redak=element.split(' ')[1]
        jedinka=element.split(' ')[2]
        if unif_znak=='IDN':
            trazena=[]
            for var in idn:
                if jedinka==var[0]:
                    djelokrug.reverse()
                    for krug in djelokrug:
                        if var[3]==krug:
                            trazena.append(var)
                            break;
                    djelokrug.reverse()
            if trazena==[]: 
                print('<primarni_izraz> ::= IDN(%s,%s)'%(redak, jedinka))
                exit(0)    
            elif len(trazena)>1:
                max_polje=[]
                for var in trazena:
                    max_polje.append(var[3])
                maxi=max(max_polje)
                for var in trazena:
                    if var[3]==maxi:
                        varijabla=var
                        break;
            else:
                varijabla=trazena[0]
            stablo[br_cvor].append(varijabla[1])
            stablo[br_cvor].append(varijabla[2])   

        elif unif_znak=='BROJ':
            broj=long(jedinka)
            if broj<-2147483648 or broj>2147483647:
                print('<primarni_izraz> ::= BROJ(%s,%s)'%(redak, jedinka))
                exit(0)
            tip='int'
            l_izraz=0
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)

        elif unif_znak=='ZNAK':
            if '\\' in jedinka and jedinka not in('\\\\', '\t', '\n', '\0', '\'', '\"'):
                print('<primarni_izraz> ::= ZNAK(%s,%s)'%(redak, jedinka))
                exit(0)
            else:
                tip='char'
                l_izraz=0
                stablo[br_cvor].append(tip)
                stablo[br_cvor].append(l_izraz)

        elif unif_znak=='NIZ_ZNAKOVA':
            i=0
            while i < len(jedinka):
                if jedinka[i]=='\\':
                    if jedinka[i+1] not in ('\\','\t', '\n', '\0', '\'', '\"'):
                        print ('<primarni_izraz> ::= NIZ_ZNAKOVA(%s,%s)'%(redak, jedinka))
                        exit(0)
                    i+=1
                i+=1
            tip='niz(const(char))'
            l_izraz=len(jedinka)
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)

        elif unif_znak=='L_ZAGRADA':
            provjeri=Provjera()
            provjeri.izraz(produkcija[1])
            tip=stablo[produkcija[1]][3]
            l_izraz=stablo[produkcija[1]][4]
            stablo[br_cvor].append(tip)
            stablo[br_cvor].append(l_izraz)


            

    def lista_deklaracija(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if stablo[produkcija[0]][0]=='<deklaracija>':
            provjeri=Provjera()
            provjeri.deklaracija(produkcija[0])
        elif stablo[produkcija[0]][0]=='<lista_deklaracija>':
            provjeri=Provjera()
            provjeri.lista_deklaracija(produkcija[0])            
            provjeri=Provjera()
            provjeri.deklaracija(produkcija[1])

    def deklaracija(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        provjeri=Provjera()
        provjeri.ime_tipa(produkcija[0])
        ntip=stablo[produkcija[0]][3]
        provjeri=Provjera()
        provjeri.lista_init_deklaratora(produkcija[1], ntip)

    def lista_init_deklaratora(self, br_cvor, ntip):
        global stablo
        produkcija=stablo[br_cvor][2]        
        if stablo[produkcija[0]][0]=='<init_deklarator>':
            provjeri=Provjera()
            provjeri.init_deklarator(produkcija[0], ntip)
        elif stablo[produkcija[0]][0]=='<lista_init_deklaratora>':
            provjeri=Provjera()
            provjeri.lista_init_deklaratora(produkcija[0], ntip)            
            provjeri=Provjera()
            provjeri.init_deklarator(produkcija[2], ntip)

    def init_deklarator(self, br_cvor, ntip):
        global stablo
        produkcija=stablo[br_cvor][2]
        if len(produkcija)==1:
            provjeri=Provjera()
            provjeri.izravni_deklarator(produkcija[0], ntip)        
            tip=stablo[produkcija[0]][3]
            if tip in ('const(int)', 'const(char)', 'niz(const(int))', 'niz(const(char))'):
                print ('<init_deklarator> ::= <izravni_deklarator>')
                exit(0)
        else:
            provjeri=Provjera()
            provjeri.izravni_deklarator(produkcija[0], ntip)        
            tip=stablo[produkcija[0]][3]            
            provjeri=Provjera()
            provjeri.inicijalizator(produkcija[2])
            tip1=stablo[produkcija[2]][3]
            element=stablo[produkcija[1]][0]
            znak=element.split(' ')[0]
            redak=element.split(' ')[1]
            jedinka=element.split(' ')[2]
            dalje=0
            if tip in ('int','const(int)'):
                if vrijedi_tilda(tip1, 'int')==0:
                    print ('<init_deklarator> ::= <izravni_deklarator> OP_PRIDRUZI(%s,%s) <inicijalizator>'%(redak, jedinka))
                    exit(0)
                else:
                    dalje=1
            elif tip in ('char', 'const(char)'):
                if vrijedi_tilda(tip1, 'char')==0:
                    print ('<init_deklarator> ::= <izravni_deklarator> OP_PRIDRUZI(%s,%s) <inicijalizator>'%(redak, jedinka))
                    exit(0)
                else:
                    dalje=1
                
            elif tip in ('niz(int)', 'niz(const(int))', 'niz(char)', 'niz(const(char))'):
                if tip in ('niz(int)', 'niz(const(int))'):
                    t='int'
                else:
                    t='char'
                br_elem=stablo[produkcija[0]][4]
                br_elem1=stablo[produkcija[2]][4]
                if br_elem1>br_elem:
                    print ('<init_deklarator> ::= <izravni_deklarator> OP_PRIDRUZI(%s,%s) <inicijalizator>'%(redak, jedinka))
                    exit(0)
                for u in tip1:
                    if vrijedi_tilda(u, t)==0:
                        print ('<init_deklarator> ::= <izravni_deklarator> OP_PRIDRUZI(%s,%s) <inicijalizator>'%(redak, jedinka))
                        exit(0)
                dalje=1
            if dalje==0:
                print ('<init_deklarator> ::= <izravni_deklarator> OP_PRIDRUZI(%s,%s) <inicijalizator>'%(redak, jedinka))
                exit(0)

    def izravni_deklarator(self, br_cvor, ntip):
        global stablo, djelokrug, idn
        produkcija=stablo[br_cvor][2]
        element=stablo[produkcija[0]][0]
        znak=element.split(' ')[0]
        redak1=element.split(' ')[1]
        jedinka1=element.split(' ')[2]        
        if len(produkcija)==1:
            if ntip=='void':
                print ('<izravni_deklarator> ::= IDN(%s,%s)'%(redak1, jedinka1))
                exit(0)
            lokalni=djelokrug[-1]
            for var in idn:
                if var[0]==jedinka1 and var[3]==lokalni:
                    print ('<izravni_deklarator> ::= IDN(%s,%s)'%(redak1, jedinka1))
                    exit(0)
            idn.append([jedinka1, ntip, 1, lokalni])
            stablo[br_cvor].append(ntip)
        else:
            elem=stablo[produkcija[1]][0]
            znak2=elem.split(' ')[0]
            red2=elem.split(' ')[1]
            jed2=elem.split(' ')[2]
            elem=stablo[produkcija[3]][0]
            znak4=elem.split(' ')[0]
            red4=elem.split(' ')[1]
            jed4=elem.split(' ')[2]
            if 'BROJ' in stablo[produkcija[2]][0]:
                elem=stablo[produkcija[2]][0]
                znak3=elem.split(' ')[0]
                red3=elem.split(' ')[1]
                jed3=elem.split(' ')[2]
                if ntip=='void' or int(jed3)<=0 or int(jed3)>1024:
                    print('<izravni_deklarator> ::= IDN(%s,%s) %s(%s,%s) %s(%s,%s) %s(%s,%s)'%(redak1, jedinka1, znak2,red2,jed2,znak3,red3,jed3,znak4,red4,jed4))
                    exit(0)
                for var in idn:
                    if var[0]==jedinka1 and var[3]==djelokrug[-1]:
                        print('<izravni_deklarator> ::= IDN(%s,%s) %s(%s,%s) %s(%s,%s) %s(%s,%s)'%(redak1, jedinka1, znak2,red2,jed2,znak3,red3,jed3,znak4,red4,jed4))
                        exit(0)
                idn.append([jedinka1, 'niz(%s)'%ntip, int(jed3) ,djelokrug[-1]])
                stablo[br_cvor].append('niz(%s)'%ntip)
                stablo[br_cvor].append(int(jed3))
            elif 'KR_VOID' in stablo[produkcija[2]][0]:
                elem=stablo[produkcija[2]][0]
                znak3=elem.split(' ')[0]
                red3=elem.split(' ')[1]
                jed3=elem.split(' ')[2]
                flag=1
                for var in idn:
                    if var[0]==jedinka1 and var[3]==djelokrug[-1]:
                        flag=0
                        if var[1]!='void' or var[2]!=ntip:
                            print('<izravni_deklarator> ::= IDN(%s,%s) %s(%s,%s) %s(%s,%s) %s(%s,%s)'%(redak1, jedinka1, znak2,red2,jed2,znak3,red3,jed3,znak4,red4,jed4))
                            exit(0)
                if flag:
                    idn.append([jedinka1, 'void', ntip, djelokrug[-1]])
                    if jedinka1 not in deklaracije:
                        deklaracije[jedinka1]=['void', ntip]
                stablo[br_cvor].append('funkcija(void -> %s)'%ntip)    
            elif stablo[produkcija[2]][0]=='<lista_parametara>':
                provjeri=Provjera()
                provjeri.lista_parametara(produkcija[2])
                tipovi=stablo[produkcija[2]][3]
                flag=1
                for var in idn:
                    if var[0]==jedinka1 and var[3]==djelokrug[-1]:
                        flag=0
                        if var[1]!=tipovi or var[2]!=ntip:
                            print('<izravni_deklarator> ::= IDN(%s,%s) %s(%s,%s) <lista_parametara> %s(%s,%s)'%(redak1, jednika1, znak2,red2,jed2,znak4,red4,jed4))
                            exit(0)
                if flag:
                    idn.append([jedinka1, tipovi, ntip, djelokrug[-1]])
                    if jedinka1 not in deklaracije:
                        deklaracije[jedinka1]=[tipovi, ntip]
                stablo[br_cvor].append('funkcija(%s -> %s)'%(tipovi, ntip) )                 


    def inicijalizator(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if len(produkcija)==1:
            provjeri=Provjera()
            provjeri.izraz_pridruzivanja(produkcija[0])
            tip=stablo[produkcija[0]][3]
            br_elem=stablo[produkcija[0]][4]
            if type(br_elem)==int and br_elem > 1:
                br_elem-=1
                tipovi=[]
                for i in range(br_elem):
                    tipovi.append('char')
                stablo[br_cvor].append(tipovi)
                stablo[br_cvor].append(br_elem)
            else:
                stablo[br_cvor].append(tip)
        else:
            provjeri=Provjera()
            provjeri.lista_izraza_pridruzivanja(produkcija[1])
            tipovi=stablo[produkcija[1]][3]
            br_elem=stablo[produkcija[1]][4]
            stablo[br_cvor].append(tipovi)
            stablo[br_cvor].append(br_elem)

    def lista_izraza_pridruzivanja(self, br_cvor):
        global stablo
        produkcija=stablo[br_cvor][2]
        if len(produkcija)==1:
            provjeri=Provjera()
            provjeri.izraz_pridruzivanja(produkcija[0])
            tip=stablo[produkcija[0]][3]
            stablo[br_cvor].append([tip])
            stablo[br_cvor].append(1)
        else:
            provjeri=Provjera()
            provjeri.lista_izraza_pridruzivanja(produkcija[0])
            tipovi=stablo[produkcija[0]][3]
            br_elem=stablo[produkcija[0]][4]
            provjeri=Provjera()
            provjeri.izraz_pridruzivanja(produkcija[2])
            tip=stablo[produkcija[2]][3]
            tipovi.append(tip)
            br_elem+=1
            stablo[br_cvor].append(tipovi)
            stablo[br_cvor].append(br_elem)
        
def vrijedi_tilda(prvi, drugi):
    if prvi in ('char', 'const(char)') and drugi in ('char', 'int', 'const(char)' 'const(char)'):
        return 1
    if prvi in ('int', 'const(int)') and drugi in ('int', 'const(int)'):
        return 1
    if prvi in ('niz(int)', 'niz(const(int))') and drugi in ('niz(int)', 'niz(const(int))'):
        return 1
    if prvi in ('niz(char)', 'niz(const(char))') and drugi in ('niz(char)', 'niz(const(char))'):
        return 1
    if prvi == drugi:
        return 1
    return 0
    
dat=open("test.in")
ulaz1=dat.read()
ulaz=ulaz1.splitlines()
global stablo, definicije, deklaracije, djelokrug, trenutni_djelokrug, idn
definicije={}
deklaracije={}
stablo=[]
idn=[]
petlja=[]
fun_pov=[]
djelokrug=[1]
sljedeci_djelokrug=2
br_cvor=0
stablo_temp=[]
i=0
for redak in ulaz:
    razina=len(redak)-len(redak.lstrip())
    cvor=[redak.lstrip(), i, razina, []]
    i+=1
    stablo_temp.append(cvor)
    
for cvor in stablo_temp:
    for j in range(cvor[1]+1, i):
        if stablo_temp[j][2]==cvor[2]+1:
            cvor[3].append(j)
        elif stablo_temp[j][2]<=cvor[2]:
            break
    
for cvor in stablo_temp:
    cvor1=[cvor[0], cvor[1], cvor[3]]
    stablo.append(cvor1)
    

provjeri=Provjera()
provjeri.prijevodna_jedinica(0)
print stablo
if 'main' not in definicije:
    print 'main'
elif definicije['main']!=['void','int']:
    print 'main'
if definicije!=deklaracije:
    print 'funkcija'


