'''
Retrieve and Ranking modul like its name this module performs the retrieving and ranking tasks.

Author: Mohamed Lemine Sidi (mlsidi@ogr.eskisehir.edu.tr).
'''
import sys
import math
import time
import os

class Entity(object):
    """
    Entity class: represent the structure of entities extracted from the index.
    Attributes:
        nbOfDocs      : nb of documents in which the entity is occured.
        docParags_dict: dictionary which contains for each document the correponding paragraphs' information {docNo: {pNo: Parag()}}
    """
    def __init__(self):
        self.nbOfDocs=0             
        self.docParags_dict={}      
#
class Parag(object):
    '''
    ParagsEntity class: represent the paragraph structure.
    Attributes:
       NbEp       : number of entities in the paragraph.
       isStrong   : (0/1) 0 if the the entity is strong, 1 otherwise.
       NbStrongEp : number of strong entities in the paragraph.
       pOccNb     : occurence number of a given entity in the paragraph
       relatedE_Nb: number of entities related to a given entity (1 by default).
    '''
    def __init__(self):
        self.NbEp=0
        self.isStrong=0 
        self.NbStrongEp=0
        self.pOccNb=0
        self.relatedE_Nb=1
   
def get_docParagNb(InputFN):
    """
        Provides the number of paragraphs for each document. 
        Args:
            InputFN (string): path and the name of the file which contains paragraph number in the document.
        Returns:
            docParagNb_dict : a list of documents and their number of paragraphs.
    """
    docParagNb_dict={}
    with open(InputFN, 'r', encoding='utf-8') as f:
        for l in f:
            d,NbParag=l.strip().split("->")
            docParagNb_dict[d]=int(NbParag)
    return docParagNb_dict
def loadingSubIndex(EqRows):
    entity_index_dict={}
    for l in EqRows:
        allElemt=l.strip().split("+>")
        ent=allElemt[0]
        entity_index_dict[ent]=Entity()
        docIndice=-1
        for doc in range(1,len(allElemt)):
            d,paragsInfo=allElemt[doc].strip().split("->")
            docParag=paragsInfo.strip().split(",")
            docIndice+=1 #
            paragsIndices_dict={}   
            for p in docParag:
                parag=Parag()
                infos=p.strip().split("/")
                infoIndice=0
                if len(infos)==6:
                    infoIndice+=1
                pNo=int(infos[infoIndice])
                if pNo not in paragsIndices_dict:
                    paragsIndices_dict[pNo]=0
                paragsIndices_dict[pNo]+=1 # 
                parag.NbEp=int(infos[infoIndice+1])
                parag.isStrong=int(infos[infoIndice+2])    # new added
                parag.NbStrongEp=int(infos[infoIndice+3])
                parag.relatedE_Nb=int(infos[infoIndice+4]) #
                parag.pOccNb=paragsIndices_dict[pNo] 
                if d not in entity_index_dict[ent].docParags_dict: 
                    entity_index_dict[ent].docParags_dict[d]={} # 
                if paragsIndices_dict[pNo]==1: # new parag
                    if pNo not in entity_index_dict[ent].docParags_dict[d]:
                        entity_index_dict[ent].docParags_dict[d][pNo]=parag
                else: # 
                    entity_index_dict[ent].docParags_dict[d][pNo].pOccNb=paragsIndices_dict[pNo]
        entity_index_dict[ent].nbOfDocs=len(entity_index_dict[ent].docParags_dict)
    return entity_index_dict
#
def loadingIndexAsRows(InputFN): 
    loadingIndexAsRows={}
    with open(InputFN, 'r', encoding='utf-8') as indexF:
        for l in indexF:
            t=l.strip().split("\n")
            allElemt=t[0].strip().split("+>")
            ent=allElemt[0]
            loadingIndexAsRows[ent]=t[0]
    return loadingIndexAsRows
def getTitleEntitiesInDoc(Folder):
    titleEntities_Dict={}
    dID='<DOCNO>'
    FN=Folder+"docTitleAnnotations.txt"
    with open(FN, 'r', encoding='utf-8') as f:
        for l in f:
            t=l.strip().split("\n")
            if dID in t[0]:
                docNO=t[0].strip().replace('<DOCNO>', '')
            else:
                titleEntities_Dict[docNO]=t[0]      
    return titleEntities_Dict
def getStrongEntitiesInDoc(Folder):
    strongEntitiesInDoc_Dict={}
    dID='<DOCNO>'
    FN=Folder+"docStrongEntities.txt"
    with open(FN, 'r', encoding='utf-8') as f:
        for l in f:
            t=l.strip().split("\n")
            p=t[0]
            if dID in p:
                docNO=p
                docNO=docNO.strip().replace('<DOCNO>', '')
                strongEntitiesInDoc_Dict[docNO]=[]
            else:
                stgEs=l.strip().split("->")
                for e in stgEs:
                    strongEntitiesInDoc_Dict[docNO].append(e)
    return strongEntitiesInDoc_Dict 
#
def getAllFoundDocsIDs(entity_index_dict):
    allFoundDocs_Dict={}
    for e, docs in entity_index_dict.items():
        for d, parags in docs.docParags_dict.items():
            if d not in allFoundDocs_Dict:
                allFoundDocs_Dict[d]=''
    return allFoundDocs_Dict
def docsScoring(entity_index_dict,docParagNb_dict,titleEntities_Dict,strongEntitiesInDoc_Dict,EntityQ):
    scoringQ_docs_Dict={} # {DocNo: score}
    allFoundDocs_Dict={}
    allFoundDocs_Dict=getAllFoundDocsIDs(entity_index_dict)
    for docNo, bos in allFoundDocs_Dict.items():
        scoringQ_docs_Dict[docNo]=0
        Nb_SE_d=0
        if docNo in strongEntitiesInDoc_Dict:
            Nb_SE_d=len(strongEntitiesInDoc_Dict[docNo])
        Eqp=[]
        EqpTermNb=0
        for e in EntityQ:
            if docNo in entity_index_dict[e].docParags_dict: # this e is occuring in doc.
                Eqp.append(e)
                EqpTermNb+=len(e.strip().split("_"))
        if len(Eqp)>0: # termNbWeight
            EqpTermNb=EqpTermNb/len(Eqp)
        #score computing:
        score=0
        for e in Eqp:
            Nb_SEqp=0
            relatedEs_Nb=0
            paragNb=len(entity_index_dict[e].docParags_dict[docNo])
            for pargN in entity_index_dict[e].docParags_dict[docNo]:
                relatedEs_Nb=entity_index_dict[e].docParags_dict[docNo][pargN].relatedE_Nb
                Nb_SEqp=entity_index_dict[e].docParags_dict[docNo][pargN].isStrong
                Nb_SEp=entity_index_dict[e].docParags_dict[docNo][pargN].NbStrongEp
                Nb_Ep=entity_index_dict[e].docParags_dict[docNo][pargN].NbEp
                score+=(relatedEs_Nb*EqpTermNb*len(Eqp)*math.exp(Nb_SEqp)*len(Eqp))/(Nb_Ep+(math.exp(Nb_SEp-Nb_SEqp))) #*len(Eqp)
        scoringQ_docs_Dict[docNo]+=score 
        TEQ_weigth=0
        TirleEs=[]
        if docNo in titleEntities_Dict: 
            TirleEs=titleEntities_Dict[docNo].strip().split("->")
        nbTEq=0  # nb e existing in doc title
        for e in EntityQ:
            if e in TirleEs:
                nbTEq+=1
                if '_' in e:
                    nbTEq+=1
        if len(TirleEs)>0:
            TEQ_weigth=nbTEq*score*0.01 
            scoringQ_docs_Dict[docNo]+=TEQ_weigth
    return scoringQ_docs_Dict

# Gesting Eq:
# fullAnnation,maxScore,meanScore,myEL.resultEntities
class QueryDocsScore(object):
    def __init__(self):
        self.Entities=[]   
        self.fullAnnation='N' # by default
        self.meanScore=0
        self.maxScore=0       
def getOurAnnotatedQuerySets(EqFN):
    Q1_ourEL_Dict={}
    with open(EqFN,'r', encoding='utf-8') as f:
        for l in f:
            line=l.strip().split('<++>')
            qID=line[0]
            Q1_ourEL_Dict[qID]=QueryDocsScore()
            Q1_ourEL_Dict[qID].fullAnnation=line[1]
            Q1_ourEL_Dict[qID].meanScore=float(line[3])
            Q1_ourEL_Dict[qID].maxScore=float(line[2])
            Q1_ourEL_Dict[qID].Entities=line[4].strip().split('->')
    return Q1_ourEL_Dict
#
def bumchQueryRanking(queryEL_Dict,docParagNb_dict,titleEntities_Dict,strongEntitiesInDoc_Dict,entity_indexRow_dict,Folder,ms,k=100):
    rF=Folder+'results/'
    listFiles=os.listdir(rF)
    fnb=len(listFiles)
    resultFN=Folder+'results/PESS4IRresultsM'+str(k)+'_'+str(fnb)+'.txt'
    nbQ=0
    with open(resultFN,'w', encoding='utf-8') as outputF:
        for qID, ObEq in queryEL_Dict.items():
            Eq=ObEq.Entities
            if ObEq.fullAnnation=='Y' and ObEq.meanScore>=ms: 
                nbEqF=0
                EqRows=[]
                for e in Eq:
                    if e in entity_indexRow_dict:
                        nbEqF+=1
                        EqRows.append(entity_indexRow_dict[e])
                if len(Eq)==nbEqF:
                    nbQ+=1
                    entity_index_dict={}
                    entity_index_dict=loadingSubIndex(EqRows)
                    scoringQ_docs_Dict={}
                    scoringQ_docs_Dict=docsScoring(entity_index_dict,docParagNb_dict,titleEntities_Dict,strongEntitiesInDoc_Dict,Eq)
                    scoringQ_d=sorted (scoringQ_docs_Dict.items(), key=lambda item: item[1])
                    indice=len(scoringQ_d)-1
                    rank=0
                    while indice >=0 and rank<100:
                        rank+=1
                        line=qID+' Q0 '+scoringQ_d[indice][0]+' '+str(rank)+' '+str(scoringQ_d[indice][1])+' '+'PESS4IR'
                        outputF.write(line+'\n')
                        indice-=1
# 
def main(Folder,FN,qFN,ms):
    InputFN=Folder+FN
    print('Index loading ...')
    entity_indexRow_dict=loadingIndexAsRows(InputFN)
    print('The index is loaded')
    docPFN="docParagNb_dict.txt"
    docParagNb_dict=get_docParagNb(Folder+docPFN)
    titleEntities_Dict=getTitleEntitiesInDoc(Folder)
    strongEntitiesInDoc_Dict=getStrongEntitiesInDoc(Folder)
    annotatedEqFile=Folder+qFN
    Eq_Dict=getOurAnnotatedQuerySets(annotatedEqFile)
    print('Ranking ....')
    bumchQueryRanking(Eq_Dict,docParagNb_dict,titleEntities_Dict,strongEntitiesInDoc_Dict,entity_indexRow_dict,Folder,ms,100)
#    
if __name__ == '__main__':
    if len(sys.argv)!=5:
        print("Usage: retrieveRanking.py [indexFileName] [queriesFileName] [path/to/Folder/] [meanScore]")
        exit(0)
    else:
        FN=sys.argv[1]
        qFN=sys.argv[2]
        Folder=sys.argv[3]
        ms=float(sys.argv[4])
        if ms<0 or ms>1:
            print("Usage: retrieveRanking.py [indexFileName] [queriesFileName] [path/to/Folder/] [meanScore]")
            print("The [meanScore] should be between 0 and 1.")
            exit(0)
        listFiles=os.listdir(Folder)
        if FN not in listFiles or qFN not in listFiles:
            print("The files or one of them do not exist in Folder")
            exit(0)
        main(Folder,FN,qFN,ms)

