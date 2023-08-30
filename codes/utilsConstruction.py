"""
The utilsConstruction module provides functions which prepare the construction of surface form, for our entity linking method.

Author: Mohamed Lemine Sidi (mlsidi@ogr.eskisehir.edu.tr)
"""
import gzip
import os

def get_E_facc_dict():
    E_FACC_Dict={}
    filenames=os.listdir("path/to/data/FACC1/")
    for fn in filenames:
        it=0
        with gzip.open('path/to/data/FACC1/'+fn,'rt', encoding='utf-8') as f:
            s='clueweb12'
            for l in f:
                wl=l.strip().split('\t')
                if s in wl[0]:
                    it+=1
                    e = wl[2].strip().replace(" ", "_")
                    if e not in E_FACC_Dict: 
                        E_FACC_Dict[e]=wl[7]
    return E_FACC_Dict
def construct_E_facc_dict():
    E_FACC_Dict=get_E_facc_dict()
    filename='path/to/data/FACC1/E_Facc_Dict.txt'
    with open(filename,'w',encoding='utf-8') as f:
        for k, v in E_FACC_Dict.items():
            l=k+'<+>'+v
            f.write(l+'\n')
#
################################################################################## Freebase
def fbIDs_db_Dict_Build(): #(E_db_Dict):
    fbIDs_db_Dict={}
    filename='path/to/data/freebase_links_en.ttl'
    with open(filename,'r',encoding='utf-8') as f:
        s='<http://dbpedia.org/resource/'
        for l in f:
            wl=l.strip().split(" ")
            if s in wl[0]:
                fId=wl[2].strip().replace("<http://rdf.freebase.com/ns/", '')
                fId=fId[0:len(fId)-1]
                fId=fId.strip().replace("m.", "/m/")
                e=wl[0].strip().replace("<http://dbpedia.org/resource/", '')
                e=e[0:len(e)-1]
                if e in E_db_Dict:
                    if fId not in fbIDs_db_Dict:
                        fbIDs_db_Dict[fId]=e
    return fbIDs_db_Dict
#fbIDs_db_Dict=fbIDs_db_Dict_Build()
def comonE_Facc_db_Build(FbIDs_FACC_Dict,fbIDs_db_Dict,E_db_Dict, redirects_Dict):
    comonE_Facc_db_Dict={}
    for k, v in FbIDs_FACC_Dict.items():
        if k in fbIDs_db_Dict:
            for e in v: #
                if e not in comonE_Facc_db_Dict and e not in redirects_Dict and e not in E_db_Dict: 
                    comonE_Facc_db_Dict[e]=fbIDs_db_Dict[k]
    filename='path/to/data/comonE_Facc_db_Dict.txt'
    with open(filename,'w',encoding='utf-8') as f:
        s=''
        for k, v in comonE_Facc_db_Dict.items():
            s=k+'->'+str(v)
            f.write(s+'\n')
    return comonE_Facc_db_Dict # 
#
def get_ComonE_Facc_db_Dict():
    comonE_Facc_db_Dict={}
    filename="path/to/data/comonE_Facc_db_Dict.txt"
    with open(filename,'r',encoding='utf-8') as f:
        for l in f:
            if len(l.strip().split('->'))==2:
                k,v=l.strip().split('->')
                comonE_Facc_db_Dict[k]=v
    return comonE_Facc_db_Dict
#
def stopWordList():
    fn='path/to/data/stopwords-list-LemurProject.txt'
    stopwords_list={} # []
    with open(fn, 'r') as file:
        for l in file:
            t=l.strip().split(" ")
            stopwords_list[t[0]]=''
    return stopwords_list

def construct_DbStopWords(surfaceF_Dicts,stopWords):
    db_StopWords=set()
    for k, v in surfaceF_Dicts.E_db_Dict.items():
        terms=k.strip().split('_')
        for t in terms:
            if t in stopWords:
                db_StopWords.add(t)
    db_StopWords=sorted(db_StopWords)
    filename='path/to/data/db_stopWords2.txt'
    with open(filename,'w',encoding='utf-8') as f:
        for w in db_StopWords:
            f.write(w+'\n')

########################################################  allTermIncludingPoint.txt
def getTermWPoint():
    termIncludingPoint=set()
    for k, v in surfaceF_Dicts.E_db_Dict.items():
        if '.' in k:
            terms=k.strip().split("_")
            for t in terms:
                if len(t)>0:
                    c=t[len(t)-1]
                    if c=='.':
                        termIncludingPoint.add(t)
    return termIncludingPoint

def findPossibleEntities():
    mayBe_entity_set=set()
    for e, v in mayBe_entity_Dict.items():
        if e in surfaceF_Dicts.E_db_Dict:
            mayBe_entity_set.add(e)
    for e, v in mayBe_entity_Dict.items():
        if e in surfaceF_Dicts.cleanedE_db_Dict:
            mayBe_entity_set.add(e)
    for e, v in mayBe_entity_Dict.items():
        if e in surfaceF_Dicts.ED_db_Dict:
            mayBe_entity_set.add(e)
    for e, v in mayBe_entity_Dict.items():
        if e in surfaceF_Dicts.redirects_Dict:
            mayBe_entity_set.add(e)
    for t in mayBe_entity_set:
        del mayBe_entity_Dict[t]
    return mayBe_entity_Dict
def construct_allTermIncludingPoint()
    mayBe_entity_Dict=findPossibleEntities()
    mayBe_entity_set=set()
    for e, v in mayBe_entity_Dict.items():
        mayBe_entity_set.add(v)
    filename="path/to/data/allTermIncludingPoint.txt"
    with open(filename,'w',encoding='utf-8') as f:
        for t in mayBe_entity_set:
            f.write(t+'\n')

############################################################################## FACC1
def get_E_facc_dict():
    E_FACC_Dict={}
    filename='path/to/data/FACC1/E_Facc_Dict.txt'
    with open(filename,'r',encoding='utf-8') as f:
        for l in f:
            k,v=l.strip().split('<+>')
            E_FACC_Dict[k]=v
    return E_FACC_Dict
def get_FbIDs_FACC_Dict():
    FbIDs_FACC_Dict={}
    for k,v in E_FACC_Dict.items():
        if v not in FbIDs_FACC_Dict:
            FbIDs_FACC_Dict[v]=[]
        FbIDs_FACC_Dict[v].append(k)
    return FbIDs_FACC_Dict
def construct_FbR_db_not_IN_FACC():
    filename='path/to/data/FbR_db_not_IN_FACC.txt'
    with open(filename,'w',encoding='utf-8') as f:
        s=''
        for k, v in redirects_Dict.items():
            if redirct_ER_db_Dict[v]!='' and k not in commonFbR_Facc_db_Dict:
                s=k+'->'+str(redirct_ER_db_Dict[v])
                f.write(s+'\n')
def constr_restR_db():
    filename='path/to/data/restR_db.txt'
    with open(filename,'w',encoding='utf-8') as f:
        s=''
        for k, v in redirects_Dict.items():
            if redirct_ER_db_Dict[v]=='':
                s=k+'->'+str(redirct_ER_db_Dict[v])
                f.write(s+'\n')
def get_restR_db():
    restR_db_Dict={}
    filename='path/to/data/restR_db.txt'
    with open(filename,'r',encoding='utf-8') as f:
        for l in f:
            k,v=l.strip().split("->")
            restR_db_Dict[k]=v
    return restR_db_Dict
restR_db_Dict=get_restR_db()

def construct_commonFbR_Facc_db():
    filename='path/to/data/commonFbR_Facc_db.txt'
    with open(filename,'w',encoding='utf-8') as f:
        s=''
        for k, v in redirects_Dict.items():
            if redirct_ER_db_Dict[v]!='':
                s=k+'->'+str(redirct_ER_db_Dict[v])
                f.write(s+'\n')
def get_commonFbR_Facc_db_Dict():
    commonFbR_Facc_db_Dict={}
    filename='path/to/data/commonFbR_Facc_db.txt'
    with open(filename,'r',encoding='utf-8') as f:
        for l in f:
            k,v=l.strip().split("->")
            commonFbR_Facc_db_Dict[k]=v
    return commonFbR_Facc_db_Dict
#commonFbR_Facc_db_Dict=get_commonFbR_Facc_db_Dict()
newComonE_Facc_db_Dict={}
for k, v in comonE_Facc_db_Dict.items():
    if k not in ED_db_Dict:
        newComonE_Facc_db_Dict[k]=v
def construct_commonFbR_Facc_db_new():
    filename='path/to/data/comonE_Facc_db_Dict_new.txt'
    with open(filename,'w',encoding='utf-8') as f:
        s=''
        for k, v in newComonE_Facc_db_Dict.items():
            s=k+'->'+str(v)
            f.write(s+'\n')
#db_stopWords=surfaceF_Dicts.getDbStopWords()
def construct_cCommonFbR_Facc_db_new():
    newcComonE_Facc_db_Dict={}
    for k, v in newComonE_Facc_db_Dict.items():
        nk=dropParantezOther(k)
        nk=dropStopWords(nk,db_stopWords)
        if nk not in newComonE_Facc_db_Dict:
            newcComonE_Facc_db_Dict[nk]=k
        # store it
    filename="path/to/data/comonE_Facc_db_Dict_cleanedNew.txt"
    with open(filename,'w',encoding='utf-8') as f:
        s=''
        for k, v in newcComonE_Facc_db_Dict.items():
            s=k+'->'+str(v)
            f.write(s+'\n')
#construct_cCommonFbR_Facc_db_new()
def construct_cED_db():
    cleanED_db_Dict={}
    for k, v in surfaceF_Dicts.ED_db_Dict.items():
        if '_' in k:
            nk=dropParantezOther(k)
            nk=dropInAtOf(nk)
            nk=nk.strip().split('_')
            newE=''
            for t in nk:
                if t not in surfaceF_Dicts.db_stopWords:
                    newE+=t+'_'
            if newE!='':
                newE=newE[0:len(newE)-1]
                if newE not in surfaceF_Dicts.ED_db_Dict:
                    if newE not in cleanED_db_Dict:
                        cleanED_db_Dict[newE]=k
        # storeIt
        filename="D:/PESS4IR/data/cleanedED_db_Dict1.txt"
        with open(filename,'w',encoding='utf-8') as f:
            s=''
            for k, v in cleanED_db_Dict.items():
                s=k+'->'+str(v)
                f.write(s+'\n')
#
def construct_db_stopWords_UpCase_FullUpCase():
    db_stopWords_UpCase=[]
    db_stopWords_fullUpCase=[]
    filename='D:/PESS4IR/data/db_stopWords2.txt'
    with open(filename,'r',encoding='utf-8') as f:
        for l in f:
            swUp=''
            w=l.strip().split(" ")
            sw=w[0]
            UpL=getUp_letter(sw[0])
            if len(sw)==1:
                swUp=UpL
            else:
                swUp=UpL+sw[1:len(sw)]
            db_stopWords_UpCase.append(swUp)
            swFUp=''
            for l in sw:
                swFUp+=getUp_letter(l)
            db_stopWords_fullUpCase.append(swFUp)
    # store
    filename='D:/PESS4IR/data/db_stopWords_UpCase_FullUpCase.txt'
    with open(filename,'w',encoding='utf-8') as f:
        for w in db_stopWords_UpCase:
            f.write(w+'\n')
        for w in db_stopWords_fullUpCase:
            if len(w)>1:
                f.write(w+'\n')
#
def get_EtoC_db():
    EtoC_db_Dict={}
    categories_Dict={}
    fn="D:/PESS4IR/data/allResourceDict.txt"
    with open(fn,'r', encoding='utf-8') as nf:
        for l in nf:
            k,w=l.strip().split('->')
            if len(k)>1: 
                v=w.strip().split("', '")
                if len(v)>1:
                    v0=v[0]
                    vn=v[len(v)-1]
                    v[0]=v0[2:len(v0)]
                    v[len(v)-1]=vn[0:len(vn)-2]
                else:
                    v0=v[0]
                    v[0]=v0[2:len(v0)-2]
                EtoC_db_Dict[k]=v
    return EtoC_db_Dict
#EtoC_db_Dict=get_EtoC_db()
def construct_nonUsefullE_db():
    nonUsefullEntities=[]
    # Days
    catg='Days_of_the_week'
    for k, v in EtoC_db_Dict.items():
        if catg in v and '_' not in k: #
            nonUsefullEntities.append(k)
    # Months
    catg='Months'
    for k, v in EtoC_db_Dict.items():
        if catg in v and '_' not in k and len(v)==2: # len(v)==2: for Months
            nonUsefullEntities.append(k)
    # add stopWords_as_E_db:
    #for t in stopWords_as_E_db:
    #    nonUsefullEntities.append(t)
    # store the nonUsefullEntities:      
    filename="D:/PESS4IR/data/nonUsefullE_db.txt"
    with open(filename,'w',encoding='utf-8') as f:
        for e in nonUsefullEntities:
            f.write(e+'\n')
