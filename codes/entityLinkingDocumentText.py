"""
The EntityLinkingDocumentText class performs the first two steps of our entity linking method (EL4DT) which are mention detection and candidate selection.

Author: Mohamed Lemine Sidi (mlsidi@ogr.eskisehir.edu.tr)
"""
import os
import re
import math
import sys
import ir_datasets
from surfaceForms import SurfaceForm
from paragEntityExtraction import ParagEntityExtraction
from utils import *

class EntityLinkingDocumentText(object):
    """
    This class contains 
    Attributes:
        db_: ...
    """
    def __init__(self):
        self.db_stopWords,self.db_stopWords_UpCase=self.get_db_stopWords()
        self.db_stopWords_UpCase_FUpCase=self.get_db_stopWords_UpCase_FullUpCase()
        self.annotationsE_Dict={}       # The output
        self.allFoundEntities_Dict={} 
        self.foundEntities=[]           # all found entities
        self.subEntities={}             # subEntities set
        self.sureEntities={}            # sure entities set
        self.nonSureEs={}               # non sure entities set
        self.someSubEntities={}         # addictional nonSureEntities
        self.resultEntities=[]
        self.resultScores=[]
        self.nonUsefullEntities=self.getnonUsefullEntities() 
        self.mentionsTerms=() 
    def matchingNgram2(self, surfaceF_Dicts,p,n):
        paragEEs=[] 
        terms=p.strip().split(' ')
        for i in range(0,len(terms)-n+1): 
            e=[]
            for j in range(i,i+n): 
                e.append(terms[j])
            if (n==1 and len(e)==1) and ((e[0].isnumeric()==True and len(e[0])<5) or (e[0] in self.nonUsefullEntities or e[0] in self.db_stopWords_UpCase)):
                e='#######'
                #paragEE=ParagEntityExtraction()
                #paragEE.m=e
            else:
                termsE=e
                i=0
                for t in termsE:
                    if '.' in t: # len(t)>0
                        if t[len(t)-1]=='.' and t not in surfaceF_Dicts.termWithPoint_Dict:
                            newTerm=t[0:len(t)-1]
                            e[i]=newTerm
                    i+=1
                paragEE=self.matchingNgram(surfaceF_Dicts,e)
                if paragEE.isEmpty() and paragEE.SE_db==[] and len(e)==1 and '-' in e[0]:
                    termsU=e[0].strip().split("-")
                    for tU in termsU:
                        tTab=[]
                        tTab.append(tU)
                        paragEE=self.matchingNgram(surfaceF_Dicts,tTab)
                        if paragEE.isEmpty()==False or paragEE.SE_db!=[]:
                            paragEEs.append(paragEE)
                else:
                    paragEEs.append(paragEE)
        return paragEEs
    #
    def matchingNgram(self, surfaceF_Dicts,e):
        e=getSimpleEntityFromList(e)
        paragEE=ParagEntityExtraction() # creating the object
        paragEE.m=e
        if e in surfaceF_Dicts.E_db_Dict:
            paragEE.E_db.append(e)
        elif e in surfaceF_Dicts.cleanedE_db_Dict:
            paragEE.cE_db.append(surfaceF_Dicts.cleanedE_db_Dict[e])
        if e in surfaceF_Dicts.ED_db_Dict:
            paragEE.D_db=surfaceF_Dicts.ED_db_Dict[e]
        elif e in surfaceF_Dicts.cleanedED_db_Dict:
            ent=surfaceF_Dicts.cleanedED_db_Dict[e]
            paragEE.cD_db=surfaceF_Dicts.ED_db_Dict[ent]
        if e in surfaceF_Dicts.redirects_Dict:
            if '(disambiguation)' not in surfaceF_Dicts.redirects_Dict[e]: # this could be solved in Categories!
                paragEE.R_db.append(surfaceF_Dicts.redirects_Dict[e])
        elif e in surfaceF_Dicts.cRedirects_Dict:
            paragEE.cR_db.append(surfaceF_Dicts.cRedirects_Dict[e])
        if e in surfaceF_Dicts.newComonE_Facc_db_Dict:
            paragEE.Fb_FaccDB.append(surfaceF_Dicts.newComonE_Facc_db_Dict[e])
        elif e in surfaceF_Dicts.newcComonE_Facc_db_Dict:
            ent=surfaceF_Dicts.newcComonE_Facc_db_Dict[e]
            paragEE.Fb_FaccDB.append(surfaceF_Dicts.newComonE_Facc_db_Dict[ent])
        if e in surfaceF_Dicts.similarE_Dict:
            paragEE.SE_db.append(surfaceF_Dicts.similarE_Dict[e])
        return paragEE
        
    def sureDisambiguiation(self,surfaceF_Dicts,p):
        paragEEss=[]
        ngram=8 # 
        if len(p.strip().split(' '))<ngram:
            ngram=len(p.strip().split(' '))
            if ngram==1:
                ngram=2
        for n in range(1,ngram):
            paragEEs=self.matchingNgram2(surfaceF_Dicts,p,n)
            for pe in paragEEs:
                if  pe.D_db!=[]: # E_db and D_db exist:
                    need=True
                    if pe.E_db!=[]:
                        need=False
                    pd=self.preDesambiguition2(pe.D_db,pe.m,p)
                    pd=self.selectRelevantOnes(pd,pe.m,need)
                    if len(pd)==1: 
                        pe.D_db=pd
                    else:
                        pe.D_db=[]
                if pe.cD_db!=[]:
                    need=True
                    if pe.E_db==[] and pe.R_db==[]:
                        need=False
                    pd=self.preDesambiguition2(pe.cD_db,pe.m,p)
                    pd=self.selectRelevantOnes(pd,pe.m,need)
                    if len(pd)==1:
                        pe.cD_db=pd
                    else:
                        pe.cD_db=[]
            paragEEss.append(paragEEs) 
        return paragEEss
    def preDesambiguition2(self, surfaceF_Dict,m,p):
        candidate_ED=[]
        paragraph=p.strip().split(' ')
        relpaeTab=[]
        for e in surfaceF_Dict:
            subTab=[]
            if '", "' in e or "', '" in e or "', \"" in e or '", \'' in e:
                subTab=re.split('\"\, \"|\'\, \'|\'\, \"|\"\, \'',e, flags=re.IGNORECASE)
                for el in subTab:
                    relpaeTab.append(el)
            else:
                relpaeTab.append(e)
        for e in relpaeTab:
            ent=self.delete_db_stopWords_from_Ent(e)
            ent=ent.strip().split('_')
            m_lenghth=len(m.strip().split('_'))
            men=m.strip().split('_')
            n=0
            i=0
            j=0 # j represents the similarity between entity and mention.
            score=0
            CE=''
            SCE=0
            for t in ent:
                if CE=='':
                    CE=t
                else:
                    CE+=' '+t
                if t not in men:
                    n+=1
                    if t in paragraph:
                        i+=1
                        if CE in p:
                            SCE+=0.05
                        else:
                            SCE-=0.05
                else:
                    j+=1
            if i==0:
                if len(ent)==j: # mention term(s) are the equal to those of the candidate_entity. 
                    score=0.51 #
            else: # means: i and n > 0
                score=0.51+SCE
            if score>0:
                candidate_ED.append(e)
                candidate_ED.append(score)
        return candidate_ED
    def contextScore(self, e,m,p):
        candidate_ED=[]
        paragraph=p.strip().split(' ')
        lp=len(paragraph)
        lg=math.log10(lp)
        e=self.delete_db_stopWords_from_Ent(e)
        ent=e.strip().split('_')
        mention=m.strip().split('_')
        n=0
        i=0
        for t in ent:
            n+=1
            if len(t)>0:
                alternatif_t=getUp_Low_letter(t[0])
            if len(t)>1:
                alternatif_t+=t[1:len(t)-1]
            if len(t)>0 and (t in paragraph or alternatif_t in paragraph): 
                i+=1
        coherence=True
        if i>0: #
            candidate_ED.append(e)
            candidate_ED.append(i/(n+lg))
            return candidate_ED[1]
        else:
            return 0
    # selecting one entity according to its piriority:
    def entitySelectionPiriority(self,pe):
        if pe.m not in self.someSubEntities:
            self.someSubEntities[pe.m]=[]
        entitySelected=''
        if pe.E_db!=[]:
            if len(pe.D_db)==1:
                EnbT=len(pe.E_db[0].strip().split("_"))
                DnbT=len(pe.D_db[0].strip().split("_"))
                if DnbT-EnbT>=1: # and score>0.5: 
                    entitySelected=pe.D_db[0]
                else:
                    if pe.D_db[0]!=pe.E_db[0]:
                        self.someSubEntities[pe.m].append(pe.D_db[0])# 
                    entitySelected=pe.E_db[0]
            else:
                entitySelected=pe.E_db[0]
        else: # pe.ER_db[0]=[] so ER_db.
            if pe.D_db!=[] or pe.R_db!=[]:
                if len(pe.D_db)==1:
                    entitySelected=pe.D_db[0]
                    if pe.R_db!=[]: #
                        self.someSubEntities[pe.m].append(pe.R_db[0])
                else: # 
                    entitySelected=pe.R_db[0]
            else: #
                if pe.cE_db!=[]:
                    if len(pe.cD_db)==1:
                        entitySelected=pe.cD_db[0]
                        self.someSubEntities[pe.m]=pe.cE_db[0]
                    else:
                        entitySelected=pe.cE_db[0]
                else:
                    if pe.Fb_FaccDB!=[]:
                        entitySelected=pe.Fb_FaccDB[0]
                    elif pe.cR_db!=[]:
                        entitySelected=pe.cR_db[0]
                    elif len(pe.cD_db)==1:
                        entitySelected=pe.cD_db[0]
                    elif pe.cFb_FaccDB!=[]:
                        entitySelected=pe.Fb_cFaccDB[0]
                    elif pe.SE_db!=[]:
                        entitySelected=pe.SE_db[0]
        return entitySelected
    # selecting significant ones:
    def selectRelevantOnes(self,tabEs,m,need):
        indice=1
        indiceE=0
        scoreOnes=[]
        maxScore=0
        maxScoreE=[]
        E=''
        for i in range(int(len(tabEs)/2)):
            if tabEs[indice]>0.5: # >=0.5
                if maxScore<tabEs[indice]:
                    maxScore=tabEs[indice]
                    E=tabEs[indiceE]
                scoreOnes.append(tabEs[indiceE])
            indice+=2
            indiceE+=2
        if scoreOnes!=[] or need==False:
            if E!='':
                maxScoreE=[E]
                scoreOnes=maxScoreE
        return scoreOnes  
    def groupingMentions(self,p):
        linkedEntities=[] #
        pTab = p.strip().split(' ')
        i=0
        while i<len(pTab):
            t_eTab=[]
            maxK=0
            for e in self.foundEntities:
                te=e.strip().split('_')
                if '_' in e and pTab[i]==te[0]: 
                    t_eTab.append(e)
            for e in t_eTab:
                te=e.strip().split('_')
                if len(te)>1 and e!=pTab[i]: #.
                    k=0
                    for j in range(len(te)):
                        if pTab[j]==te[j]:
                            k+=1
                    if k==len(te):
                        if self.preELinking(self.allFoundEntities_Dict[e],self.allFoundEntities_Dict[pTab[i]],p)==True and k>maxK:
                            maxK=k
                            entity=e
            if maxK==0:
                if pTab[i] in self.foundEntities:
                    linkedEntities.append(pTab[i])
                i+=1
            else:
                linkedEntities.append(entity)
                i=i+maxK          
        return linkedEntities

    def preELinking(self,grandE,smallE,p):
        result=False
        score=0
        if grandE.E_db!=[] or len(grandE.D_db)==1 or grandE.R_db!=[]:
            result=True
        elif grandE.cE_db!=[]:
            result=True
        else:
            if grandE.cR_db!=[]:
                score=self.contextScore(grandE.cR_db[0],grandE.m,p)
            elif len(grandE.Fb_FaccDB)==1:
                if smallE.D_db!=[]: #
                    if grandE.Fb_FaccDB[0]!=smallE.D_db[0]:
                        score=-1
                if score!=-1: # 
                    e=grandE.Fb_FaccDB[0]
                    m=grandE.m
                    score=self.contextScore(e,m,p)
            elif grandE.cFb_FaccDB!=[]:
                if smallE.D_db!=[]:
                    if grandE.Fb_FaccDB[0]!=smallE.D_db[0]:
                        score=-1
                if score!=-1:
                    score=self.contextScore(grandE.cFb_FaccDB[0],grandE.m,p)
            if score>0.5:
                result=True 
        return result

    def groupingMentions2(self,p):
        linkedEntities={} 
        i=0
        for x in range(len(self.foundEntities)-1):
            t_eTab=[]
            maxK=0
            sm=self.foundEntities[x].strip().split('_')
            for y in range(x+1,len(self.foundEntities)):
                gd=self.foundEntities[y].strip().split('_')
                if len(sm)<len(gd):
                    k=0
                    for t in sm:
                        if t in gd:
                            k+=1
                    if k==len(sm):
                        t_eTab.append(self.foundEntities[y])
            for e in t_eTab:
                gd=e.strip().split('_')
                k=len(gd)
                if k>maxK and self.preELinking(self.allFoundEntities_Dict[e],self.allFoundEntities_Dict[self.foundEntities[x]],p)==True:
                    maxK=k
                    entity=e
            if maxK==0:
                entity=self.foundEntities[x]
            if entity not in linkedEntities:
                linkedEntities[entity]=[]
            if entity!=self.foundEntities[x]:
                linkedEntities[entity].append(self.foundEntities[x])       
        return linkedEntities
    def nonSureEntities(self,p):
        nonSureEs={}
        maxE=''
        for k, v in self.allFoundEntities_Dict.items():
            score=0 # 
            if v.E_db!=[] or (v.E_db!=[] and len(v.D_db)==1):
                if len(v.D_db)==1:
                    score=self.contextScore(v.D_db[0],v.m,p)
                    if score<=0.5:
                        v.D_db=[]
                score=1
            elif len(v.D_db)==1 and v.R_db==[] and v.cD_db==[] and v.SE_db==[] and v.Fb_FaccDB==[]:
                score=self.contextScore(v.D_db[0],v.m,p)
                maxE=v.D_db[0]
            elif v.cE_db!=[] and v.R_db==[] and v.cD_db==[] and v.SE_db==[] and v.Fb_FaccDB==[]:
                score=1
            elif v.R_db!=[] and v.cE_db==[]:
                if len(v.R_db[0])<=4 and v.R_db[0].isnumeric():
                    score=0
                else:
                    score=self.contextScore(v.R_db[0],v.m,p)
                maxE=v.R_db[0]
            else:
                maxE=''
                maxES=-1
                if v.cE_db!=[]:
                    score=self.contextScore(v.cE_db[0],v.m,p)
                    if maxES<score:
                        maxES=score
                        maxE=v.cE_db[0]
                if v.R_db!=[]:
                    score=self.contextScore(v.R_db[0],v.m,p)
                    if maxES<score:
                        maxES=score
                        maxE=v.R_db[0]
                if v.D_db!=[]:
                    score=self.contextScore(v.D_db[0],v.m,p)
                    if maxES<score:
                        maxES=score
                        maxE=v.D_db[0]
                if len(v.cD_db)==1 and score<0.5:
                    score=self.contextScore(v.cD_db[0],v.m,p)
                    if maxES<score:
                        maxES=score
                        maxE=v.cD_db[0]
                if len(v.cR_db)==1 and score<0.5:
                    score=self.contextScore(v.cR_db[0],v.m,p)
                    if maxES<score:
                        maxES=score
                        maxE=v.cR_db[0]
                if len(v.Fb_FaccDB)==1 and score<0.5:
                    score=self.contextScore(v.Fb_FaccDB[0],v.m,p)
                    if maxES<score:
                        maxES=score
                        maxE=v.Fb_FaccDB[0]
                if len(v.cFb_FaccDB)==1 and score<0.5:
                    score=self.contextScore(v.cFb_FaccDB[0],v.m,p)
                    if maxES<score:
                        maxES=score
                        maxE=v.cFb_FaccDB[0]
                if len(v.SE_db)==1 and score<0.5:
                    score=self.contextScore(v.m,v.m,p)
                    if maxES<score:
                        maxES=score
                        maxE=v.SE_db[0]
            if score<0.5:
                nonSureEs[k]=maxE
        return nonSureEs
    ###
    def getEntity(self, v):
        e=''
        if len(v.E_db)>=1:
            e=v.E_db[0]
        elif len(v.cE_db)>=1:
            e=v.cE_db[0]
        elif len(v.D_db)==1: ##
            e=v.D_db[0]
        elif len(v.cD_db)>=1:
            e=v.cD_db[0]
        elif len(v.R_db)>=1:
            e=v.R_db[0]
        elif len(v.cR_db)>=1:
            e=v.cR_db[0]
        elif len(v.Fb_FaccDB)>=1:
            e=v.Fb_FaccDB[0]
        elif len(v.cFb_FaccDB)>=1:
            e=v.cFb_FaccDB[0]
        elif len(v.SE_db)>=1:
            e=v.SE_db[0]
        return e
    # non sure subEntities
    def nonSureSubEntities(self,p):
        score=0
        for k, v in self.allFoundEntities_Dict.items():
            if v.E_db!=[] or len(v.D_db)==1:
                if v.R_db!=[]:
                    if k not in self.someSubEntities:
                        self.someSubEntities[k]=[]
                    self.someSubEntities[k].append(v.R_db[0])
                    v.R_db=[] # and then delete it
            if len(v.cD_db)==1:
                score=self.contextScore(v.cD_db[0],v.m,p)
                if score<0.5:
                    v.cD_db=[]
            elif len(v.cD_db)>1:
                v.cD_db=[]
            if len(v.cR_db)==1:
                score=self.contextScore(v.cR_db[0],v.m,p)
                if score<0.5:
                    v.cR_db=[]
            if len(v.Fb_FaccDB)==1:
                score=self.contextScore(v.Fb_FaccDB[0],v.m,p)
                if score<0.5:
                    v.Fb_FaccDB=[]
            elif len(v.cFb_FaccDB)==1:
                score=self.contextScore(v.cFb_FaccDB[0],v.m,p)
                if score<0.5:
                    v.cFb_FaccDB=[]
            if len(v.SE_db)==1:
                score=self.contextScore(v.m,v.m,p)
                if score<0.5:
                    v.SE_db=[]

    def getSureEntitie(self,p):  
        self.subEntities=self.groupingMentions2(p)
        for k, v in self.subEntities.items():
            if v!=[]:
                for e in v:
                    if e in self.allFoundEntities_Dict:
                        del self.allFoundEntities_Dict[e]
        # deleting non sure entities
        self.nonSureEs=self.nonSureEntities(p)
        for k, v in self.nonSureEs.items():
            del self.allFoundEntities_Dict[k]
        # deleting non sure subEntities
        sureEntities_Dict=self.nonSureSubEntities(p)
        toDelete=[]
        for k, v in self.allFoundEntities_Dict.items():
            if v.isEmpty()==True and v.SE_db==[]:
                toDelete.append(k)
        for e in toDelete:
            del self.allFoundEntities_Dict[e]
        # feed sureE
        for k, v in self.allFoundEntities_Dict.items():
            ek=self.entitySelectionPiriority(v)
            #ek=self.getEntity(v)
            self.sureEntities[k]=ek # 
    
    def delete_db_stopWords_from_Ent(self, e):
        originE=e
        e=dropParantezOther(e)
        e=e.strip().split('_')
        newE=''
        for t in e:
            if len(t)>0 and t not in self.db_stopWords:
                newE+=t+'_'
        if newE!='':
            newE=newE[0:len(newE)-1]
            return newE
        else:
            return originE    
    def get_db_stopWords(self):
        db_stopWords={}
        db_stopWords_UpCase={}
        db_stopWords_fullUpCase={}
        filename='D:/PESS4IR/data/db_stopWords2.txt'
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
    def get_db_stopWords_UpCase_FullUpCase(self):
        db_stopWords_UpCase_FullUpCase={}
        filename='D:/PESS4IR/data/db_stopWords_UpCase_FullUpCase.txt'
        with open(filename,'r',encoding='utf-8') as f:
            for l in f:
                w=l.strip().split(" ")
                sw=w[0]
                db_stopWords_UpCase_FullUpCase[sw]=''
        return db_stopWords_UpCase_FullUpCase
    def setEProperties(self,paragEEss):
        for paragEEs in paragEEss:
            for pe in paragEEs:
                if pe.E_db!=[] or pe.cE_db!=[] or pe.D_db!=[] or pe.cD_db!=[] or pe.ER_db!=[] or pe.cER_db!=[] or pe.R_db!=[] or pe.cR_db!=[] or pe.Fb_FaccDB!=[] or pe.cFb_FaccDB!=[] or pe.SE_db!=[]:
                    self.foundEntities.append(pe.m)
                    if pe.m not in self.allFoundEntities_Dict:
                        self.allFoundEntities_Dict[pe.m]=pe
        self.mentionsTerms=self.getMentionedTerms()
    def getMentionedTerms(self):
        ##### the rest : start
        mentionsTerms=set()
        #mentions=() # non annotated text.
        for m, v in self.allFoundEntities_Dict.items():
            terms=m.strip().split("_")
            for t in terms:
                mentionsTerms.add(t)
        return mentionsTerms
            
    def showEntities(self):
        for k, v in self.allFoundEntities_Dict.items():
            print(k,v.E_db,v.cE_db,v.D_db,v.cD_db,v.ER_db,v.cER_db,v.R_db,v.cR_db,v.Fb_FaccDB,v.cFb_FaccDB,v.SE_db)

    def isCompletlyLinked(self,qTerms):
        '''
            input: qTerms: tab of terms, within the given text.
            output: True/False
        '''
        foundTerms=set()
        for m, v in self.allFoundEntities_Dict.items():
            if '_' in m:
                mTerms=m.strip().split("_")
                for t in mTerms:
                    foundTerms.add(t)
            else:
                foundTerms.add(m)
        n=0
        for t in qTerms:
            if t in foundTerms or t in self.db_stopWords_UpCase_FUpCase:
                n+=1
        return n==len(qTerms)
            
    def getnonUsefullEntities(self):
        nonUsefullEntities=[]
        filename="D:/PESS4IR/data/nonUsefullE_db.txt"
        with open(filename,'r',encoding='utf-8') as f:
            for l in f:
                w=l.strip().split(" ")
                e=w[0]
                nonUsefullEntities.append(e)    
        return nonUsefullEntities

    def entitiesScoring(self):
        '''
            This method give/compute scores for each found entity as following:
                -> for sureEntities: 0.5+len(nbTermsInE)/10*0.5       #threshold=0.5
                                     +len(nbSubEntities)/10*0.5
                                     if score(e)>1: score(e)=1
                   NB: here we note that except the similarEntities: we treat them as a
                       spetial case as following:
                -> for nonSureEntities: thereshold=0.25
                                        EScore=thereshold/i
                                        EScore+=nbof_/10*0.5
            Input : foundEntities, subEntities,sureEntities, nonSureEs
            Output: {ent1->score, ent2->score, ..... entn->score}
        '''
        # sure Entities scoring:
        threshold=0.5    # threshold for incrementing or threshold=0.05
        SEThreshold=0.5  # the base threshold for sureEntities
        SimEThreshold=0.25
        nSEThreshold=0.25 
        nbMultiTermE=0   #nb of Multi Term entity (sureEntities).
        selectedEntities={}
        for k, v in self.allFoundEntities_Dict.items():
            if '_' in k and v.SE_db==[]:
                nbMultiTermE+=1
        for k, v in self.sureEntities.items():
            score=0
            termNb=len(k.strip().split("_"))
            if self.allFoundEntities_Dict[k].isEmpty()==False: # not empty
                score=SEThreshold+((termNb/10)*threshold)
                # nbSubEntities weighting:
                nbSubEntities=0
                if k in self.subEntities:
                    nbSubEntities=len(self.subEntities[k])
                if nbSubEntities>0:
                    score+=(nbSubEntities/10*threshold)
            else: # similarEntity case
                if nbMultiTermE>0:
                    SimEThreshold=SimEThreshold/nbMultiTermE # here we change the threshold.
                score=SimEThreshold+((termNb/10)*threshold)
            # store the entity and its score.
            if v in self.annotationsE_Dict: # v could be occured!!!
                if self.allFoundEntities_Dict[k].E_db!=[] or self.allFoundEntities_Dict[k].D_db!=[]:
                    score+= termNb*0.1 # *0.05 
            if score>1:
                score=1
            if score>=0.1:
                self.annotationsE_Dict[v]=score
                if k not in selectedEntities:   # for entityOccurances
                    selectedEntities[k]=v # from sureE
        # at the end we check there is some repeated entites (from self.foundEntities)
        # non-sure entities scoring:
        for k, v in self.nonSureEs.items():
            score=0
            termNb=len(k.strip().split("_"))
            if nbMultiTermE>0:
                nSEThreshold=nSEThreshold/nbMultiTermE # here we change the threshold.
            score=nSEThreshold+((termNb/10)*threshold)
            if score>0.45: # 0.6 is the max score for non entities. we can set threshold=0.3. as alternatif.
                score=0.45
            if score>=0.1:
                self.annotationsE_Dict[v]=score
                if k not in selectedEntities:
                    selectedEntities[k]=v
        # scoring the additional entities:
        for m, a in self.someSubEntities.items():
            if a!=[]:
                e=a[0]
                if e not in self.annotationsE_Dict: # normaly it is the case
                    score=0
                    termNb=len(m.strip().split("_"))
                    if nbMultiTermE>0:
                        nSEThreshold=nSEThreshold/nbMultiTermE # here we change the threshold.
                    score=nSEThreshold+((termNb/10)*threshold)
                    if score>1:
                        score=0.84 # we don't want it be strong entity. 
                    if score>=0.1:
                        if e not in self.annotationsE_Dict: # to not give cange to chance.
                            self.annotationsE_Dict[e]=score
                            if m not in selectedEntities: # for entityOccurances
                                selectedEntities[m]=e
        # repeated entities:
        entityOccurances={}
        for e in self.foundEntities:
            if e in selectedEntities: # means E was selected
                if e not in entityOccurances:
                    entityOccurances[e]=0
                entityOccurances[e]+=1    # icrementing
        # feeding/storing
        for m, v in entityOccurances.items():
            for i in range(0,v):
                e=selectedEntities[m]
                self.resultEntities.append(e) # to get the E.
                self.resultScores.append(self.annotationsE_Dict[e])
    #
    def howAnnotation(self,q):
        fullAnnation=False
        maxScore=0
        #for e in self.resultEntities:
        for m in self.mentionsTerms:
            q=q.strip().replace(m, '')
        if q=='':
            fullAnnation=True
        else:
            rest=q.strip().split(' ')
            for t in rest:
                if t in self.db_stopWords_UpCase:
                    q=q.strip().replace(t, '')
            if q=='':
                fullAnnation=True
        somme=0
        moyenn=0.3
        for s in self.resultScores:
            somme+=s
            if maxScore<s:
                maxScore=s
        if len(self.resultScores)>0:
            moyenn=somme/len(self.resultScores)
        return fullAnnation,maxScore,moyenn
        
def parageraphAdditionalClean(p):
    while " . " in p:
        p=p.strip().replace(" . ", " ")
    # at the end
    if ' .' == p[len(p)-2:len(p)]: 
        p=p[0:len(p)-2]
    if '. ' == p[0:2]: 
        p=p[2:len(p)]
    if '--' == p[0:2]:
        p=p[2:len(p)]
    if '-' == p[0:1]: #
        p=p[1:len(p)]
    return p

def getTabCleanEntity(e):
    e=e.strip().replace("(", '')
    e=e.strip().replace(")", '')
    e=e.strip().split("_")
    return e

      
def annotate_Robust04(preparedfolder):
    surfaceF_Dicts= SurfaceForm()
    surfaceF_Dicts.getDbEntities()
    db_stopWords=[]
    db_stopWords=surfaceF_Dicts.getDbStopWords()
    surfaceF_Dicts.getCleanedDbE()
    surfaceF_Dicts.getDisambiguations()
    surfaceF_Dicts.getCleanedDbED()
    surfaceF_Dicts.getAllRedirects()
    surfaceF_Dicts.getAllcRedirects()
    surfaceF_Dicts.getComonEntitiesFaccDb()
    surfaceF_Dicts.getcComonEntitiesFaccDb()
    surfaceF_Dicts.getSimilarEntities()
    dID='<DOCNO>'
    writing=False
    outPutFN="E:/DBpedia/DBpedia_2016.10/RobustCollection/annotated_FR94_SubCollection.txt"
    InputFN="E:/DBpedia/DBpedia_2016.10/RobustCollection/preparedSplitedText_FR94.txt"
    with open(outPutFN, 'w', encoding='utf-8') as outPutF:
        with open(InputFN, 'r', encoding='utf-8', errors='ignore') as f:
            i=0
            for l in f:
                t=l.strip().split("\n")
                p=t[0]
                if dID in p:
                    #line=l.strip().split("\n")
                    docNO=p
                    docNO=docNO.strip().replace('<DOCNO>', '')
                    outPutF.write('<DOCNO>'+docNO+'\n')
                else:
                    p=parageraphAdditionalClean(p)
                    condP=p.strip().split(" ")
                    if len(condP)>=1 and condP[0]!='':
                        myEL=EntityLinkingDocumentText()
                        paragEEss=myEL.sureDisambiguiation(surfaceF_Dicts,p)
                        #myEL.get_db_stopWords()
                        myEL.setEProperties(paragEEss)
                        myEL.getSureEntitie(p)
                        myEL.entitiesScoring()
                        pText=''
                        if len(myEL.resultEntities)>=1:
                            for i in range(len(myEL.resultEntities)):
                                pText+=myEL.resultEntities[i]+'->'+str(myEL.resultScores[i])+'+>'
                            pText=pText[0:len(pText)-2]
                            outPutF.write(pText+'\n')

def annotate_msMarco_docTitle(path,datasetName):
    surfaceF_Dicts= SurfaceForm()
    surfaceF_Dicts.getDbEntities()
    db_stopWords=[]
    db_stopWords=surfaceF_Dicts.getDbStopWords()
    surfaceF_Dicts.getCleanedDbE()
    # here we desactivated return in all methods in the class
    surfaceF_Dicts.getDisambiguations()
    surfaceF_Dicts.getCleanedDbED()
    surfaceF_Dicts.getAllRedirects()
    surfaceF_Dicts.getAllcRedirects()
    surfaceF_Dicts.getComonEntitiesFaccDb()
    surfaceF_Dicts.getcComonEntitiesFaccDb()
    surfaceF_Dicts.getSimilarEntities()  
    v="V2" 
    if datasetName=="msmarco-document":
        v="V1"
    A_fn='msMarco'+v+'DocTitle_EL4DT_Annotations01.txt'
    outputFolder='D:/PESS4IR/annotations/'
    dataset = ir_datasets.load(datasetName)
    with open(outputFolder+A_fn, 'w', encoding='utf-8') as annfile:
        for d in dataset.docs_iter():
            tText=parageraphAdditionalClean(d[2])
            condT=tText.strip().split(" ")
            if len(condT)>=1 and condT[0]!='':
                myEL=EntityLinkingDocumentText()
                paragEEss=myEL.sureDisambiguiation(surfaceF_Dicts,tText)
                myEL.setEProperties(paragEEss)
                myEL.getSureEntitie(tText)
                myEL.entitiesScoring()
                aText=''
                if len(myEL.resultEntities)>=1:
                    for i in range(len(myEL.resultEntities)):
                        score=str(myEL.resultScores[i])
                        if len(score)>4:
                            score=score[0:4]
                        aText+=myEL.resultEntities[i]+'->'+score+'+>'
                    if len(aText)>0: 
                        aText=aText[0:len(aText)-2]
                        annfile.write("<DOCNO>"+d[0]+'\n')  
                        annfile.write(aText+'\n')

# For tests: inputs: are "text lines"
def annotate_smallText_EL4DT(path,fileName):
    surfaceF_Dicts= SurfaceForm()
    surfaceF_Dicts.getDbEntities()
    db_stopWords=[]
    db_stopWords=surfaceF_Dicts.getDbStopWords()
    surfaceF_Dicts.getCleanedDbE()
    # here we desactivated return in all methods in the class
    surfaceF_Dicts.getDisambiguations()
    surfaceF_Dicts.getCleanedDbED()
    surfaceF_Dicts.getAllRedirects()
    surfaceF_Dicts.getAllcRedirects()
    surfaceF_Dicts.getComonEntitiesFaccDb()
    surfaceF_Dicts.getcComonEntitiesFaccDb()
    surfaceF_Dicts.getSimilarEntities()  
    A_fn='test_EL4DT_textAnnotations.txt'
    outputFolder='D:/PESS4IR/annotations/'
    with open(outputFolder+A_fn, 'w', encoding='utf-8') as annfile:
        with open(outputFolder+fileName, 'r', encoding='utf-8') as f:
            for l in f:
                tText=parageraphAdditionalClean(l)
                condT=tText.strip().split(" ")
                if len(condT)>=1 and condT[0]!='':
                    myEL=EntityLinkingDocumentText()
                    paragEEss=myEL.sureDisambiguiation(surfaceF_Dicts,tText)
                    myEL.setEProperties(paragEEss)
                    myEL.getSureEntitie(tText)
                    myEL.entitiesScoring()
                    aText=''
                    if len(myEL.resultEntities)>=1:
                        for i in range(len(myEL.resultEntities)):
                            score=str(myEL.resultScores[i])
                            if len(score)>4:
                                score=score[0:4]
                            aText+=myEL.resultEntities[i]+'->'+score+'+>'
                        if len(aText)>0: 
                            aText=aText[0:len(aText)-2]
                            annfile.write("<Text>"+l)  
                            annfile.write(aText+'\n')

def annotate_msMarco_allDocTitle(path):
    surfaceF_Dicts= SurfaceForm()
    surfaceF_Dicts.getDbEntities()
    db_stopWords=[]
    db_stopWords=surfaceF_Dicts.getDbStopWords()
    surfaceF_Dicts.getCleanedDbE()
    # here we desactivated return in all methods in the class
    surfaceF_Dicts.getDisambiguations()
    surfaceF_Dicts.getCleanedDbED()
    surfaceF_Dicts.getAllRedirects()
    surfaceF_Dicts.getAllcRedirects()
    surfaceF_Dicts.getComonEntitiesFaccDb()
    surfaceF_Dicts.getcComonEntitiesFaccDb()
    surfaceF_Dicts.getSimilarEntities()   
    #
    A_fn='msMarcoDocTitle_EL4DT_Annotations.txt'
    outputFolder='D:/PESS4IR/annotations/'
    dataset = ir_datasets.load("msmarco-document-v2")
    with open(outputFolder+A_fn, 'w',  ) as annfile:
        for d in dataset.docs_iter():
            tText=parageraphAdditionalClean(d[2])
            condT=tText.strip().split(" ")
            if len(condT)>=1 and condT[0]!='':
                myEL=EntityLinkingDocumentText()
                paragEEss=myEL.sureDisambiguiation(surfaceF_Dicts,tText)
                myEL.setEProperties(paragEEss)
                myEL.getSureEntitie(tText)
                myEL.entitiesScoring()
                aText=''
                if len(myEL.resultEntities)>=1:
                    for i in range(len(myEL.resultEntities)):
                        if myEL.resultScores[i]>=0.5:
                            aText+=myEL.resultEntities[i]+'->'
                    if len(aText)>0: 
                        aText=aText[0:len(aText)-2]
                        annfile.write("<DOCNO>"+d[0]+'\n')  
                        annfile.write(aText+'\n')
def annotate_msMarco_allDocs(path):
    surfaceF_Dicts= SurfaceForm()
    surfaceF_Dicts.getDbEntities()
    db_stopWords=[]
    db_stopWords=surfaceF_Dicts.getDbStopWords()
    surfaceF_Dicts.getCleanedDbE()
    # here we desactivated return in all methods in the class
    surfaceF_Dicts.getDisambiguations()
    surfaceF_Dicts.getCleanedDbED()
    surfaceF_Dicts.getAllRedirects()
    surfaceF_Dicts.getAllcRedirects()
    surfaceF_Dicts.getComonEntitiesFaccDb()
    surfaceF_Dicts.getcComonEntitiesFaccDb()
    surfaceF_Dicts.getSimilarEntities()   
    A_fn='msMarcoDocsAnnotations.txt'
    outputFolder='D:/PESS4IR/annotations/'
    dataset = ir_datasets.load("msmarco-document-v2")
    with open(outputFolder+A_fn, 'w',  encoding='utf-8') as annfile:
        for d in dataset.docs_iter():
            annfile.write('<DOCNO>'+d[0]+'\n')
            paragraphs=re.split('\n\n|\.\s\n|\.\n',d[4], flags=re.IGNORECASE)
            for p in paragraphs: 
                tText=parageraphAdditionalClean(p)
                condT=tText.strip().split(" ")
                if len(condT)>=1 and condT[0]!='':
                    myEL=EntityLinkingDocumentText()
                    paragEEss=myEL.sureDisambiguiation(surfaceF_Dicts,tText)
                    myEL.setEProperties(paragEEss)
                    myEL.getSureEntitie(tText)
                    myEL.entitiesScoring()
                    aText=''
                    if len(myEL.resultEntities)>=1:
                        for i in range(len(myEL.resultEntities)):
                            scoree=str(myEL.resultScores[i])
                            if len(scoree)>4:
                                scoree=scoree[0:4]
                            aText+=myEL.resultEntities[i]+'->'+scoree+'+>'
                        if len(aText)>0: 
                            aText=aText[0:len(aText)-2]
                            annfile.write(aText+'\n')

# from a specific doc:
def annotate_msMarco_allDocs2(path,datasetName):
    surfaceF_Dicts= SurfaceForm()
    surfaceF_Dicts.getDbEntities()
    db_stopWords=[]
    db_stopWords=surfaceF_Dicts.getDbStopWords()
    surfaceF_Dicts.getCleanedDbE()
    surfaceF_Dicts.getDisambiguations()
    surfaceF_Dicts.getCleanedDbED()
    surfaceF_Dicts.getAllRedirects()
    surfaceF_Dicts.getAllcRedirects()
    surfaceF_Dicts.getComonEntitiesFaccDb()
    surfaceF_Dicts.getcComonEntitiesFaccDb()
    surfaceF_Dicts.getSimilarEntities()   
    A_fn='msMarcoDocsAnnotations9_3.txt'
    outputFolder='D:/PESS4IR/annotations/msmV1_annot2.5M/'
    did=''
    listFolder=os.listdir(outputFolder)
    if len(listFolder)>0:
        fn='msMarcoV1_DocsAnnotations'+str(len(listFolder))+'.txt'
        with open(outputFolder+fn, 'r', encoding='utf-8') as annf:
            for l in annf:
                if "<DOCNO>" in l:
                    did=l.strip().split("\n")
                    did=did[0].strip().replace("<DOCNO>",'')
    dataset = ir_datasets.load(datasetName)
    tnb=4
    if datasetName=="msmarco-document":
        tnb=3
        #A_fn='msMarcoV1_DocsAnnotations1.txt'
        A_fn='msMarcoV1_DocsAnnotations'+str(len(listFolder)+1)+'.txt'
    passed=False
    with open(outputFolder+A_fn, 'w', encoding='utf-8') as annfile:
        for d in dataset.docs_iter():
            if passed==False:
                if d[0]==did: 
                    print("Started ...")
                    passed=True
            if passed==True:
                annfile.write('<DOCNO>'+d[0]+'\n')
                paragraphs=re.split('\n\n|\.\s\n|\.\n',d[tnb], flags=re.IGNORECASE)
                for p in paragraphs: 
                    tText=parageraphAdditionalClean(p)
                    condT=tText.strip().split(" ")
                    if len(condT)>=1 and condT[0]!='':
                        myEL=EntityLinkingDocumentText()
                        paragEEss=myEL.sureDisambiguiation(surfaceF_Dicts,tText)
                        myEL.setEProperties(paragEEss)
                        myEL.getSureEntitie(tText)
                        myEL.entitiesScoring()
                        aText=''
                        if len(myEL.resultEntities)>=1:
                            for i in range(len(myEL.resultEntities)):
                                scoree=str(myEL.resultScores[i])
                                if len(scoree)>4:
                                    scoree=scoree[0:4]
                                aText+=myEL.resultEntities[i]+'->'+scoree+'+>'
                            if len(aText)>0: 
                                aText=aText[0:len(aText)-2]
                                annfile.write(aText+'\n')
#
if __name__ == '__main__':
    if len(sys.argv)<2 or len(sys.argv)>3:
        print("Usage: entityLinkingDocumentText.py [path/to/folder/] [-msDv1/-msDv1/msTv2/-msTv1]")
        exit(0)
    else:
        if len(sys.argv)==2:
            print("Annotate Robust Collections' folders ...")
            annotate_Robust04()
        else:
            path=sys.argv[1]
            msMacro=sys.argv[2]
            if msMacro=='-msDv2':
                print("msMarcoV2 Annotation by EL4DT .....")
                datasetName="msmarco-document-v2"
                annotate_msMarco_allDocs2(path,datasetName)
            elif msMacro=='-msDv1':
                print("msMarcoV1 Annotation by EL4DT .....")
                datasetName="msmarco-document"
                annotate_msMarco_allDocs2(path,datasetName)
            else:
                if msMacro=='-msTv2':
                    print(path+': '+" Annotation by EL4DT ...")
                    datasetName="msmarco-document-v2"
                    annotate_msMarco_docTitle(path,datasetName)
                elif msMacro=='-msTv1':
                    print("msMarcoV1: Titles Annotation by EL4DT ...")
                    print("Started ...")
                    datasetName="msmarco-document"
                    annotate_msMarco_docTitle(path,datasetName)
