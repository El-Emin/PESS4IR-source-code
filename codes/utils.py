'''
This modul contains the utils functions of PESS4IR.

Author: Mohamed Lemine Sidi (mlsidi@ogr.eskisehir.edu.tr).
'''
import string
def get_db_stopWords(filename):
    db_stopWords={}
    db_stopWords_UpCase={}
    db_stopWords_fullUpCase={}    
    with open(filename,'r',encoding='utf-8') as f:
        for l in f:
            swUp=''
            w=l.strip().split(" ")
            sw=w[0]
            db_stopWords[sw]=''
            UpL=getUp_letter(sw[0])
            if len(sw)==1:
                swUp=UpL
            else:
                swUp=UpL+sw[1:len(sw)]
            db_stopWords_UpCase[swUp]=''
            swFUp=''
            for l in sw:
                swFUp+=getUp_letter(l)
            db_stopWords_fullUpCase[swFUp]=''
    return db_stopWords, db_stopWords_UpCase

def get_db_stopWords_all(filename):
    db_stopWords={}
    db_stopWords_UpCase={}
    db_stopWords_fullUpCase={}    
    with open(filename,'r',encoding='utf-8') as f:
        for l in f:
            swUp=''
            w=l.strip().split(" ")
            sw=w[0]
            db_stopWords[sw]=''
            UpL=getUp_letter(sw[0])
            if len(sw)==1:
                swUp=UpL
            else:
                swUp=UpL+sw[1:len(sw)]
            db_stopWords_UpCase[swUp]=''
            swFUp=''
            for l in sw:
                swFUp+=getUp_letter(l)
            db_stopWords_fullUpCase[swFUp]=''
    return db_stopWords, db_stopWords_UpCase, db_stopWords_fullUpCase


def get_db_stopWords_UpCase_AND_FullUpCase(filename):
    db_stopWords_UpCase_FullUpCase={}
    with open(filename,'r',encoding='utf-8') as f:
        for l in f:
            w=l.strip().split(" ")
            sw=w[0]
            db_stopWords_UpCase_FullUpCase[sw]=''
    return db_stopWords_UpCase_FullUpCase  
def isAscii(s):
    aditionSet='-0123456789.()-,_\''
    for c in s:
        if c not in string.ascii_letters and c not in aditionSet:
            return False
    return True

#
def normalize_title(title):
    '''
        Normalize a title to Wikipedia format. 
        :param title: a title to normalize.
    '''
    title = title.strip().replace(" ", "_")
    return title[0].upper() + title[1:]
#
def cat_res_buildingDict():
    allCatgry= set()
    allResrce= set()
    allCatgryDict={}
    allResrceDict={}
    #
    with open("E:/DBpedia/categories/article_categories_en.nt",'r') as cf:
        s='<http://dbpedia.org/resource/'
        n=0
        nbL=0
        print('*************    Building Dicts of all ressources and categorie:...  *************')
        for l in cf:
            nbL+=1
            wl=l.strip().split(' ')
            r=wl[0]
            if s in r:
                c=wl[2]
                c=c.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(c)-1
                c=c[0:cn]
                allCatgry.add(c)
                r=r.strip().replace("<http://dbpedia.org/resource/", '')
                rn=len(r)-1
                r=r[0:rn]
                allResrce.add(r)
                n+=1
        print(n)
        print(nbL)
        print(len(allResrce))
        print(len(allCatgry))
    #  
    for e in allCatgry:
        allCatgryDict[e]=[] 
    for e in allResrce:
        allResrceDict[e]=[]
    #
    with open("E:/DBpedia/categories/article_categories_en.nt",'r') as articlF:
        s='<http://dbpedia.org/resource/'
        for l in articlF:
            wl=l.strip().split(' ')
            r=wl[0]
            if s in r:
                c=wl[2] 
                c=c.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(c)-1
                c=c[0:cn]
                #ws=wl[0]
                r=r.strip().replace("<http://dbpedia.org/resource/", '')
                rn=len(r)-1
                r=r[0:rn]
                allCatgryDict[c].append(r)
                allResrceDict[r].append(c)
    return allResrceDict, allCatgryDict
# only allResrceDict(which contain the set of categories of a given ressource/article)

def res_buildingDict():
    allResrce= set()
    allResrceDict={}
    #
    with open("E:/DBpedia/categories/article_categories_en.nt",'r') as cf:
        s='<http://dbpedia.org/resource/'
        n=0
        nbL=0
        print('*************    Building Dicts of all/set ressources:...  *************')
        for l in cf:
            nbL+=1
            wl=l.strip().split(' ')
            r=wl[0]
            if s in r:
                r=r.strip().replace("<http://dbpedia.org/resource/", '')
                rn=len(r)-1
                r=r[0:rn]
                allResrce.add(r)
                n+=1
        print(n)
        print(nbL)
        print(len(allResrce))
    #   
    for e in allResrce:
        allResrceDict[e]=[]
    #
    with open("E:/DBpedia/categories/article_categories_en.nt",'r') as articlF:
        s='<http://dbpedia.org/resource/'
        for l in articlF:
            wl=l.strip().split(' ')
            r=wl[0]
            if s in r:
                c=wl[2]
                c=c.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(c)-1
                c=c[0:cn]
                #ws=wl[0]
                r=r.strip().replace("<http://dbpedia.org/resource/", '')
                rn=len(r)-1
                r=r[0:rn]
                allResrceDict[r].append(c)
    return allResrceDict

def res_buildDict():
    allResrceDict={}
    with open("E:/DBpedia/categories/article_categories_en.nt",'r') as articlF:
        s='<http://dbpedia.org/resource/'
        for l in articlF:
            wl=l.strip().split(' ')
            r=wl[0]
            if s in r:
                c=wl[2]
                c=c.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(c)-1
                c=c[0:cn]
                #ws=wl[0]
                r=r.strip().replace("<http://dbpedia.org/resource/", '')
                rn=len(r)-1
                r=r[0:rn]
                if r not in allResrceDict:
                    allResrceDict[r]=[]
                allResrceDict[r].append(c)
    return allResrceDict

def rsE_buildDict():
    allResrceDict={}
    with open("E:/DBpedia/categories/article_categories_en.nt",'r') as articlF:
        s='<http://dbpedia.org/resource/'
        for l in articlF:
            wl=l.strip().split(' ')
            r=wl[0]
            if s in r:
                r=r.strip().replace("<http://dbpedia.org/resource/", '')
                r=r[0:len(r)-1]
                if len(r)>1:
                    if r not in allResrceDict:
                        allResrceDict[r]=''
                    #allResrceDict[r].append(c)
    return allResrceDict

def resources_buildDict(fn):
    allResrceDict={}
    with open(fn,'r', encoding='utf-8') as articlF: # added 'encoding='utf-8''
        s='<http://dbpedia.org/resource/'
        for l in articlF:
            wl=l.strip().split(' ')
            r=wl[0]
            if s in r:
                c=wl[2]
                c=c.strip().replace("<http://dbpedia.org/resource/Category:", '')
                c=c[0:len(c)-1]
                #ws=wl[0]
                r=r.strip().replace("<http://dbpedia.org/resource/", '')
                r=r[0:len(r)-1]
                if r not in allResrceDict:
                    allResrceDict[r]=[]
                allResrceDict[r].append(c)
    return allResrceDict
# skosBroaderGroupDict and skosBroaderDict
def skos_broader_buildingDict():
    broaderCatgry = set() # set (distinct) of categories which have broader
    skosBroaderDict={}
    broaderGroupes = set()
    skosBroaderGroupDict={}
    b='<http://www.w3.org/2004/02/skos/core#broader>'
    with open("E:/DBpedia/categories/skos_categories_en.nt",'r') as skosF:
        n=0
        for l in skosF:
            ws=l.strip().split(' ')
            w=ws[1]
            if b==w:
                n+=1
                w=ws[0]
                w=w.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(w)-1
                w=w[0:cn]
                broaderCatgry.add(w)
                w=ws[2]
                w=w.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(w)-1
                w=w[0:cn]
                broaderGroupes.add(w)
        print(n)
        print(len(broaderCatgry))
        print(len(broaderGroupes))
        #
    for e in broaderCatgry:
        skosBroaderDict[e]=[]
    for e in broaderGroupes:
        skosBroaderGroupDict[e]=[]
    with open("E:/DBpedia/categories/skos_categories_en.nt",'r') as skosF:
        for l in skosF:
            ws=l.strip().split(' ')
            w=ws[1]
            if b==w: # if s in w:
                w=ws[2]
                w=w.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(w)-1
                w=w[0:cn]
                # (cbc):c[0] related_to_cat[2](w)
                cbc=ws[0]
                cbc=cbc.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(cbc)-1
                cbc=cbc[0:cn]
                skosBroaderGroupDict[w].append(cbc)
                skosBroaderDict[cbc].append(w)
    return skosBroaderGroupDict, skosBroaderDict
# skosBroaderDict
def skos_catBroader_buildingDict():
    broaderCatgry = set() # set (distinct) of categories which have broader
    skosBroaderDict={}
    b='<http://www.w3.org/2004/02/skos/core#broader>'
    with open("E:/DBpedia/categories/skos_categories_en.nt",'r') as skosF:
        n=0
        for l in skosF:
            ws=l.strip().split(' ')
            w=ws[1]
            if b==w:
                n+=1
                w=ws[0]
                w=w.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(w)-1
                w=w[0:cn]
                broaderCatgry.add(w)
        print(n)
        print(len(broaderCatgry))
    #
    for e in broaderCatgry:
        skosBroaderDict[e]=[]
    #
    with open("E:/DBpedia/categories/skos_categories_en.nt",'r') as skosF:
        for l in skosF:
            ws=l.strip().split(' ')
            w=ws[1]
            if b==w: # if s in w:
                w=ws[2]
                w=w.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(w)-1
                w=w[0:cn]
                # (cbc):c[0] related_to_cat[2](w)
                cbc=ws[0]
                cbc=cbc.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(cbc)-1
                cbc=cbc[0:cn]
                skosBroaderDict[cbc].append(w)
    return skosBroaderDict
#
def hompages_buildingDict():
    allHomepages= set()
    allHomepagesDict={}
    with open("E:/DBpedia/homepages/homepages_en.nt",'r') as cf:
        s='<http://dbpedia.org/resource/'
        n=0
        nbL=0
        print('*************    Building Dicts of all/set Homepages:...  *************')
        for l in cf:
            nbL+=1
            wl=l.strip().split(' ')
            r=wl[0]
            if s in r:
                r=r.strip().replace("<http://dbpedia.org/resource/", '')
                rn=len(r)-1
                r=r[0:rn]
                allHomepages.add(r)
                n+=1
        print(n)
        print(nbL)
        print(len(allHomepages))
    #   
    for e in allHomepages:
        allHomepagesDict[e]=[]
    #
    with open("E:/DBpedia/homepages/homepages_en.nt",'r') as articlF:
        s='<http://dbpedia.org/resource/'
        for l in articlF:
            wl=l.strip().split(' ')
            r=wl[0]
            if s in r:
                c=wl[2]
                r=r.strip().replace("<http://dbpedia.org/resource/", '')
                rn=len(r)-1
                r=r[0:rn]
                allHomepagesDict[r].append(c)
    return allHomepagesDict 

def skos_related_buildingDict():
    relatedGroupes = set()
    relatedCatrgry = set()
    skosRelatedCatGroupsDict={}
    skosRelatedCatgryDict={}
    s='<http://www.w3.org/2004/02/skos/core#related>'
    with open("E:/DBpedia/categories/skos_categories_en.nt",'r') as skosF:
        tnb=0
        n=0
        for l in skosF:
            ws=l.strip().split(' ')
            w=ws[1]
            n+=1
            if s==w: # if s in w:
                w=ws[2]
                w=w.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(w)-1
                w=w[0:cn]
                relatedGroupes.add(w)
                w=ws[0]
                w=w.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(w)-1
                w=w[0:cn]
                relatedCatrgry.add(w)
                tnb+=1
        print(n)
        print(tnb)
        print(len(relatedCatrgry))
        print(len(relatedGroupes))
    for e in relatedGroupes:
        skosRelatedCatGroupsDict[e]=[]
    for e in relatedCatrgry:
        skosRelatedCatgryDict[e]=[]
    #
    with open("E:/DBpedia/categories/skos_categories_en.nt",'r') as skosF:
        for l in skosF:
            ws=l.strip().split(' ')
            w=ws[1]
            if s==w: # if s in w:
                w=ws[2]
                w=w.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(w)-1
                w=w[0:cn]
                # (rtc):c[0] related_to_cat[2](w)
                rtc=ws[0]
                rtc=rtc.strip().replace("<http://dbpedia.org/resource/Category:", '')
                cn=len(rtc)-1
                rtc=rtc[0:cn]
                skosRelatedCatGroupsDict[w].append(rtc)
                skosRelatedCatgryDict[rtc].append(w)
    return skosRelatedCatGroupsDict, skosRelatedCatgryDict

def graph_buildingDict(n):
    graph_dict={}
    m=n-1
    for i in range(1,n):
        if m>=2:
            k=i+1
            for j in range(k,n+1):
                s=str(i)+'->'+str(j)
                graph_dict[s]=0
            m=m-1
        else:
            s=str(i)+'->'+str(i+1)
            graph_dict[s]=0
    return graph_dict

def graph_Scoring(graph_dict,conceptsIRInumber_dict,allResrceDict):
    for key, value in graph_dict.items():
        l=key.split('->')
        i=conceptsIRInumber_dict[l[0]]
        j=conceptsIRInumber_dict[l[1]]
        if i not in allResrceDict or j not in allResrceDict:
            graph_dict[key]=-1
        elif i==j:
            graph_dict[key]=1
        else:
            cat_i=allResrceDict[i]
            cat_j=allResrceDict[j]
            n_i=len(cat_i)
            n_j=len(cat_j)
            #n_ij=(n_i+n_j)/2
            n_ij=min(n_i,n_j)
            score=0
            for e_i in cat_i:
                for e_j in cat_j:
                    if e_i==e_j:
                        score+=1
                    elif e_i in e_j or e_j in e_i:
                        p='('
                        cIn='_in_'
                        cOf='_of_'
                        if p in e_i and p in e_j:        
                            sp_i=get_btwn_quote(e_i)
                            sp_j=get_btwn_quote(e_j)
                            if sp_i==sp_j:
                                score=score+0.1
                        elif (cIn in e_i and cIn in e_j) or (cOf in e_i and cOf in e_j):
                            lastW_i=last_word(e_i)
                            lastW_j=last_word(e_j)
                            if lastW_i==lastW_j:
                                score=score+0.1
            graph_dict[key]=score/n_ij
            
def last_word(e):
    te=e.strip().split('_')
    wIndice=len(te)-1
    return te[wIndice]

def get_btwn_quote(e):
    btwnQuote=''
    yes=False
    for k in range(len(e)):
        if e[k]==')':
            yes=False
        if yes:
            btwnQuote=btwnQuote+e[k]
        if e[k]=='(':
            yes=True
    return btwnQuote 
    
###################                    New utils:
def dropParantezOther(e):
    e=e.strip().replace(",_", '_') # new added instead of ','
    e=e.strip().replace("(", '')
    e=e.strip().replace(")", '')
    e=e.strip().replace(":_", '_')
    e=e.strip().replace(";_", '_') # new added
    e=e.strip().replace("_-_", '_')
    e=e.strip().replace("_–_", '_')
    e=e.strip().replace("_/_", '_')
    e=e.strip().replace("_+_", '_')
    e=e.strip().replace("__", '_')
    return e
def dropInAtOf(e):
    e=e.strip().replace("_at_", '_')
    e=e.strip().replace("_in_", '_')
    e=e.strip().replace("_of_", '_')
    e=e.strip().replace("_on_", '_')
    e=e.strip().replace("_and_", '_')
    e=e.strip().replace("_or_", '_')
    e=e.strip().replace("_for_", '_')
    e=e.strip().replace("_the_", '_')
    e=e.strip().replace("_to_", '_')
    e=e.strip().replace("_an_", '_')
    e=e.strip().replace("_with_", '_')
    e=e.strip().replace("_by_", '_')
    e=e.strip().replace("_a_", '_')
    e=e.strip().replace("_after_", '_')
    e=e.strip().replace("_about_", '_')
    e=e.strip().replace("_from_", '_')
    e=e.strip().replace("_one_", '_') 
    e=e.strip().replace("_no_", '_')
    e=e.strip().replace("_such_", '_')
    e=e.strip().replace("_as_", '_')
    e=e.strip().replace("__", '_')
    return e
def dropStopWords(e,db_stopWords):
    for w in db_stopWords:
        rw="_"+w+"_"
        e=e.strip().replace(rw, '_')
    e=e.strip().replace("__", '_')
    return e

def dropApostrof(e):
    '''
        We use it when: if "'s" in k:
                            dropApostrof(k)
                            and then match it with the given mention.
    '''
    e=e.strip().replace("'s", '')
    return e

def getEntityTerms(e):
    termsTab=[]
    #delete_db_stopWords_from_Ent(e) # new added
    e=dropParantezOther(e)
    e=dropInAtOf(e) #
    e=e.strip().replace("_", ' ')
    terms=e.strip().split(' ')
    if len(terms)==1:
        termsTab.append(terms[0])
    elif len(terms)>1:
        termsTab=terms
    return termsTab

def getSimpleEntityFromTerms(listE):
    e=''
    for i in range(len(listE)-1):
        e+=listE[i]+'_'
    e+=listE[len(listE)-1]
    oneTerm=0
    et=e.strip().split("_")
    for t in et:
        if len(t)==1:
            oneTerm+=1
    if oneTerm==len(et):
        return listE
    else:
        return e

def getSimpleEntityFromList(listE):
    e=''
    for i in range(len(listE)):
        e+=listE[i]+'_'
    e=e[0:len(e)-1]
    return e

def getTermsTabForEntity(e):
    eTab=[]
    e=e.strip().split("_")
    for i in range(len(e)):
        eTab.append(e[i])
    return eTab
def stopWordList():
    stopwords_list={} # []
    with open('stopwords-list-LemurProject.txt', 'r') as file:
        for l in file:
            t=l.strip().split(" ")
            #stopwords_list.append(t[0])
            stopwords_list[t[0]]=''
    return stopwords_list

def cleanText(text): # 
    Ucase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    Lcase='abcdefghijklmnopqrstuvwxyz'
    Numbers='0123456789'              # string.digits
    nonExistCarater=['"', '#', '<', '>', '?', '[', '\\ ', ']', '^', '`', '{', '|', '}']
    for c in nonExistCarater:
        text=text.strip().replace(c, ' ')
    text=text.strip().replace('_', ' ')
    text=text.strip().replace(")", ' ')
    text=text.strip().replace("(", ' ')
    text=text.strip().replace(' * ', ' ')
    text=text.strip().replace(' + ', ' ')
    text=text.strip().replace(' -- ', ' ')
    text=text.strip().replace(' - ', ' ')
    text=text.strip().replace(' . ', ' ')
    text=text.strip().replace(", ", ' ')
    text=text.strip().replace(" ,", ' ')
    text=text.strip().replace(" ;", ' ')
    text=text.strip().replace(": ", ' ')
    text=text.strip().replace(" :", ' ')
    text=text.strip().replace("; ", ' ')
    text=text.strip().split(' ')
    # stop words clear
    swList=stopWordList()
    cleaned=''
    for w in text:
        if w not in swList:
            nw=w
            if len(w)>0 and w[len(w)-1] == '.':
                if w[0] in Lcase or w[0] in Numbers:
                    nw=w[0:len(w)-1]
                    if nw in swList:
                        nw=''
            if nw!='':
                cleaned+=nw+" "
    cleaned=cleaned[0:len(cleaned)-1] # drop the last empty space.
    return cleaned

def getNonExistCarcter(db):
    caracters=string.punctuation
    nonExistCarater=[]
    for c in caracters:
        i=0
        for k, v in db.items():
            if c in k:
                i+=1
        if i==0:
            nonExistCarater.append(c)
    return nonExistCarater

def cleanText1(text): # for tests
    #nonExistCarater=getNonExistCarcter(db)
    nonExistCarater=['"', '#', '<', '>', '?', '[', '\\ ', ']', '^', '`', '{', '|', '}']
    for c in nonExistCarater:
        text=text.strip().replace(c, ' ')
    text=text.strip().replace('_', ' ')
    text=text.strip().replace(")", ' ')
    text=text.strip().replace("(", ' ')
    text=text.strip().replace(' - ', ' ')
    text=text.strip().replace(' * ', ' ')
    text=text.strip().replace(' + ', ' ')
    text=text.strip().replace(' -- ', ' ')
    text=text.strip().replace(' . ', ' ')
    text=text.strip().replace(", ", ' ')
    text=text.strip().replace(" ,", ' ')
    text=text.strip().replace(" ;", ' ')
    text=text.strip().replace(": ", ' ')
    text=text.strip().replace(" :", ' ')
    text=text.strip().replace('&amp;', '&')
    text=text.strip().replace("; ", ' ')
    return text

def getUp_Low_letter(l):
    #string.ascii_uppercase
    Ucase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    Lcase='abcdefghijklmnopqrstuvwxyz'
    indice=''
    if l in Ucase:
        for i in range(len(Ucase)):
            if Ucase[i]==l:
                indice=Lcase[i]
                #indice=i
    elif l in Lcase:
        for i in range(len(Lcase)):
            if Lcase[i]==l:
                indice=Ucase[i]
    else:
        indice=l
    return indice

def getLow_letter(l):
    Ucase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    Lcase='abcdefghijklmnopqrstuvwxyz'
    indice=l
    if l in Ucase:
        for i in range(len(Ucase)):
            if Ucase[i]==l:
                indice=Lcase[i]
    return indice
def getUp_letter(l):
    Ucase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    Lcase='abcdefghijklmnopqrstuvwxyz'
    indice=l
    if l in Lcase:
        for i in range(len(Lcase)):
            if Lcase[i]==l:
                indice=Ucase[i]
    return indice
def isUpCaseTerm(term):
    Ucase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    Lcase='abcdefghijklmnopqrstuvwxyz'
    nbUpCaseLetters=0
    nbLowCaseLetters=0
    upCaseTerm=False
    for l in term:
        if l in Lcase:
            nbLowCaseLetters+=1
        #elif l in Ucase:
            #nbUpCaseLetters+=1
    if nbLowCaseLetters==0: # or nbUpCaseLetters==len(term):
        upCaseTerm=True
    return upCaseTerm

def getNotFullUpCaseTerm_ExceptStopWord(term,stopWords_UpCase_FullUpCase):
    Ucase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    newTerm=term
    if len(term)>0:
        if isUpCaseTerm(term):
            if term not in stopWords_UpCase_FullUpCase:
                newTerm=term[0]
                for i in range(1,len(term)):
                    if term[i] in Ucase:
                        newTerm+=getLow_letter(term[i])
                    else:
                        newTerm+=term[i]
            else:
                newTerm=''
    else:
        newTerm=''
    return newTerm
def getNotFullUpCaseTerm(term):
    Ucase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    newTerm=term
    if len(term)>0:
        if isUpCaseTerm(term):
            newTerm=term[0]
            for i in range(1,len(term)):
                if term[i] in Ucase:
                    newTerm+=getLow_letter(term[i])
                else:
                    newTerm+=term[i]
    else:
        newTerm=''
    return newTerm

def getAlternatifTitle(line,stopWords_UpCase_FullUpCase):
    ws=line.strip().split(" ")
    alternatifText=''
    for w in ws:
        newT=getNotFullUpCaseTerm_ExceptStopWord(w,stopWords_UpCase_FullUpCase)
        if newT!='':
            alternatifText+=newT+' '
    alternatifText=alternatifText[0:len(alternatifText)-1]
    return alternatifText

def getAlternatifTitleComplete(line):
    ws=line.strip().split(" ")
    alternatifText=''
    for w in ws:
        newT=getNotFullUpCaseTerm(w)
        if newT!='':
            alternatifText+=newT+' '
    alternatifText=alternatifText[0:len(alternatifText)-1]
    return alternatifText
################ without cleaning stopwords
def getFirtLUpCaseTerm(term):
    Ucase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    newTerm=term
    if len(term)>0:
        if isUpCaseTerm(term):
            newTerm=term[0]
            for i in range(1,len(term)):
                if term[i] in Ucase:
                    newTerm+=getLow_letter(term[i])
                else:
                    newTerm+=term[i]
    else:
        newTerm=''
    return newTerm
def getFullLowCaseTerm(term):
    Ucase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    newTerm=term
    if len(term)>0:
        if isUpCaseTerm(term):
            newTerm=''
            for i in range(len(term)):
                if term[i] in Ucase:
                    newTerm+=getLow_letter(term[i])
                else:
                    newTerm+=term[i]
    else:
        newTerm=''
    return newTerm
def getTwoAlternatifTitle(line):
    ws=line.strip().split(" ")
    alternatifText=''
    alternatifText2=''
    for w in ws:
        newT=getFirtLUpCaseTerm(w)
        newT2=getFullLowCaseTerm(w)
        if newT!='':
            alternatifText+=newT+' '
            alternatifText2+=newT2+' '
    alternatifText=alternatifText[0:len(alternatifText)-1]
    alternatifText2=alternatifText2[0:len(alternatifText2)-1]
    return alternatifText,alternatifText2
