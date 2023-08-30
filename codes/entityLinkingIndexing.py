"""
This modul achieves the disambiguation task of our entity linking method and indexing tasks.

Authors: Mohamed Lemine Sidi (mlsidi@ogr.eskisehir.edu.tr)
"""
import re
import os
import sys
import math
        
class EntityLinkingIndexing(object):
    """
    This class performs the disambiguation and the indexing tasks. 
    Attributes:
        db_: ...
    """
    def __init__(self,Folder,FN):
        self.Folder=Folder
        self.InputFN=Folder+FN
        self.E_db_Catg_Dict={}
        self.RobLE_db_CatgToE_Dict={} # grouping entities by catg.
        self.E_db_Catg_Dict, self.RobLE_db_CatgToE_Dict= self.getCategoriesEntities()
        self.skosBroader_Dict={}
        self.skosRelatedDict={}
        self.skosBroader_Dict, self.skosRelatedDict= self.skos_catBroader_buildingDict()
        # strong entities in docs
        self.strongEntitiesInDoc_Dict=self.getStrongEntitiesInDoc()
        strongLE_Dict={}
        # titles entities in docs
        self.titleEntities_Dict={}
        self.titleEntities_Dict=self.getTitleEntitiesInDoc()
        # features:
        self.strongest=0.85 # s >= strongest # strong
        self.strong=0.7     # strong <= s < strongest # litle strong
        self.normal=0.5     # normal <= s < strong
        self.weak=0.49      # s <= weak
        self.smallestGraphScore=0.0000001 # with this score the Graph is considered as not_relevant.

    def getCategoriesEntities(self):
        dID='<DOCNO>'
        FN=self.InputFN
        nbOfLinkedEntity=0
        nbOfDocs=0
        multiE_nb=0
        emptyDocs=0
        isEmptyDoc=False
        linkedE_Dict={}
        with open(FN, 'r', encoding='utf-8') as f:
            for l in f:
                t=l.strip().split("\n")
                if dID in t[0]:
                    nbOfDocs+=1
                    if isEmptyDoc==True:
                        emptyDocs+=1
                    isEmptyDoc=True
                else:
                    isEmptyDoc=False
                    ES_list=l.strip().split("+>")
                    for es in ES_list:
                        e,s=es.strip().split("->")
                        nbOfLinkedEntity+=1
                        if e not in linkedE_Dict:
                            linkedE_Dict[e]=0
                        linkedE_Dict[e]+=1
        fn=self.Folder+"allResourceDict.txt"
        E_db_Catg_Dict={}
        with open(fn,'r', encoding='utf-8') as nf:
            for l in nf:
                k,v=l.strip().split('->')
                if k in linkedE_Dict: # 
                    E_db_Catg_Dict[k]=re.split('\"\, \"|\'\, \'|\'\, \"|\"\, \'',v[2:len(v)-2], flags=re.IGNORECASE)
        RobLE_db_CatgToE_Dict={}
        for e, cs in E_db_Catg_Dict.items():
            for c in cs:
                if c not in RobLE_db_CatgToE_Dict:
                    RobLE_db_CatgToE_Dict[c]=[]
                RobLE_db_CatgToE_Dict[c].append(e)
        return E_db_Catg_Dict,RobLE_db_CatgToE_Dict
    #
    def skos_catBroader_buildingDict(self):
        skosBroaderDict={}
        skosRelatedDict={}
        fn=self.Folder+"skos_categories_en.ttl"
        b='<http://www.w3.org/2004/02/skos/core#broader>'
        r='<http://www.w3.org/2004/02/skos/core#related>'
        with open(fn,'r', encoding='utf-8') as skosF:
            for l in skosF:
                ws=l.strip().split(' ')
                w=ws[1]
                if b==w: #
                    wb=ws[2]
                    wb=wb.strip().replace("<http://dbpedia.org/resource/Category:", '')
                    wb=wb[0:len(wb)-1]
                    w=ws[0]
                    w=w.strip().replace("<http://dbpedia.org/resource/Category:", '')
                    w=w[0:len(w)-1]
                    if w in self.RobLE_db_CatgToE_Dict:
                        if w not in skosBroaderDict:
                            skosBroaderDict[w]=[]    
                        skosBroaderDict[w].append(wb)
                elif r==w: # if s in w:
                    wr=ws[2]
                    wr=wr.strip().replace("<http://dbpedia.org/resource/Category:", '')
                    wr=wr[0:len(wr)-1]
                    w=ws[0]
                    w=w.strip().replace("<http://dbpedia.org/resource/Category:", '')
                    w=w[0:len(w)-1]
                    if w in self.RobLE_db_CatgToE_Dict:
                        if w not in skosRelatedDict:
                            skosRelatedDict[w]=[]    
                        skosRelatedDict[w].append(wr)
        return skosBroaderDict, skosRelatedDict
    def getStrongEntitiesInDoc(self):
        '''
            returns: strongEntitiesInDoc_Dict
        '''
        strongEntitiesInDoc_Dict={}
        dID='<DOCNO>'
        FN=self.Folder+"msmarcoDocStrongEntities.txt"
        FN=self.Folder+"msmarcoV1DocStrongEntities.txt"
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
    def getTitleEntitiesInDoc(self):
        '''
        returns: titleEntities_Dict
        '''
        titleEntities_Dict={}
        dID='<DOCNO>'
        FN=self.Folder+"msMarcoV1DocTitle_EL4DT_Annotations.txt"
        FN=self.Folder+"msMarcoV1QDocTitle_EL4DT_allAnnotation.txt"
        FN=self.Folder+"minCommon_EL4DT_tgm_msV1QDocTitle_annots.txt"
        FN=self.Folder+"maxCommon_EL4DT_tgm_msV1QDocTitle_annots.txt"
        with open(FN, 'r', encoding='utf-8') as f: 
            for l in f:
                t=l.strip().split("\n")
                p=t[0]
                if dID in p:
                    docNO=p
                    docNO=docNO.strip().replace('<DOCNO>', '')
                    titleEntities_Dict[docNO]=[]
                else:
                    Es=l.strip().split("->")
                    for e in Es:
                        titleEntities_Dict[docNO].append(e)      
        return titleEntities_Dict
    def paraScoredGraph2(self,NEp,conceptsIRInumber_dict,entitieScores_Dict, docStrongLE_Catgs):
        '''
        This function achieves the disambiguation process.
        inputs:
            entitieScores_Dict : {e1: score, ...} in the given paragraph
            conceptsIRInumber_dict : {No1:e1,... NoN:eN}, dict of numarated entities in the given paragraph.
            docStrongLE_Catgs: commun entities betwn strong entities in the correcponding doct and title enetites.
        outputs:
            graph_dict: {}
        '''
        graph_dict={}
        n=NEp
        N=len(docStrongLE_Catgs)
        graph_dict=graph_buildingDict(len(conceptsIRInumber_dict))
        for key, value in graph_dict.items():
            docStrongLEs_score=0
            l=key.split('->')
            i=conceptsIRInumber_dict[l[0]]
            j=conceptsIRInumber_dict[l[1]]
            if i!=j: # 
                if i not in self.E_db_Catg_Dict or j not in self.E_db_Catg_Dict:
                    if i in docStrongLE_Catgs and j in docStrongLE_Catgs:
                        graph_dict[key]=(entitieScores_Dict[i]+entitieScores_Dict[j])/n
                else: #
                    cats_i=self.E_db_Catg_Dict[i]
                    cats_j=self.E_db_Catg_Dict[j]
                    n_i=len(cats_i)
                    score=0
                    for cat_i in cats_i:
                        if cat_i in cats_j: 
                            score+=1
                    if score==0 and (i in cats_j or j in cats_i):
                        score+=1
                    if i in docStrongLE_Catgs:
                        score+=1
                    if j in docStrongLE_Catgs:
                        score+=1
                    if n>0 and score>0:
                        graph_dict[key]=(score*(entitieScores_Dict[i]+entitieScores_Dict[j]))/n
        # add broaders to categories of ressources to the graph-scoring :
        for key, value in graph_dict.items():
            l=key.split('->')
            i=conceptsIRInumber_dict[l[0]] # e_i
            j=conceptsIRInumber_dict[l[1]] # e_j
            if i!=j:
                if i in self.skosBroader_Dict and j in self.skosBroader_Dict:
                    broaders_i=self.skosBroader_Dict[i]
                    broaders_j=self.skosBroader_Dict[j]
                    score=0
                    if i in broaders_j or j in broaders_i:
                        score+=1
                        graph_dict[key]+=(entitieScores_Dict[i]+entitieScores_Dict[j])/n
                if i in self.skosRelatedDict and j in self.skosRelatedDict:# and (entitieScores_Dict[i]>=self.strong or entitieScores_Dict[j]>=self.strong):
                    relateds_i=self.skosRelatedDict[i]
                    relateds_j=self.skosRelatedDict[j]
                    score=0
                    if i in relateds_j or j in relateds_i:
                        graph_dict[key]+=(entitieScores_Dict[i]+entitieScores_Dict[j])/n
        return graph_dict
    #
    def getRelationshipScore(self,e,docStrongLE_Catgs):
        relationshipScore=0
        if len(docStrongLE_Catgs)==0:
            relationshipScore=0
        elif e in docStrongLE_Catgs:
            relationshipScore+=1
        elif e in self.E_db_Catg_Dict:
            for e_cat in self.E_db_Catg_Dict[e]:
                if e_cat in docStrongLE_Catgs:
                    relationshipScore+=1
        return relationshipScore
# end of the class.             
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

def getAllEntitiesForIndexing(Disam,InputFN): # 
    '''
    Inputs:
        Disam: A EntityLinkingIndexing object.
        InputFN: File name of the annotated Collection.
    Outputs:
        allSelectedEntity_dict : disambiguated Entities for all document.
        docParagNb_dict : Number of paragraphs per document.
    '''
    dID='<DOCNO>'
    nbAlldocs=0
    allSelectedEntity_dict={}
    docParagNb_dict={}
    pNo=0
    docNO=''
    shaine=''
    with open(InputFN, 'r', encoding='utf-8') as f:
        for l in f:
            t=l.strip().split("\n")
            p=t[0]
            if dID in p:
                if docNO!='':
                    docParagNb_dict[docNO]=pNo # NB: the last doc is not treated here.
                docNO=p
                docNO=docNO.strip().replace('<DOCNO>', '')
                nbAlldocs+=1
                pNo=0  
                docStrongLE=[] # set of strong LEs in the doc.
                docStrongLE_Catgs=set()
                # adding commun E (in both docTitle and docStrongEL)
                if docNO in Disam.titleEntities_Dict:
                    for e in Disam.titleEntities_Dict[docNO]:
                        docStrongLE_Catgs.add(e)
                    if docNO in Disam.strongEntitiesInDoc_Dict:
                        for e in Disam.titleEntities_Dict[docNO]:
                            if e in Disam.strongEntitiesInDoc_Dict[docNO] and e in Disam.E_db_Catg_Dict:
                                catgs=Disam.E_db_Catg_Dict[e]
                                for c in catgs: # adding catgs:
                                    docStrongLE_Catgs.add(c)
            else:
                relatedEntities_Dict={}
                entitieScores_Dict={}
                entitieIDScores_Dict={}
                conceptsIRI=[]
                finalCluster_dict={}
                f_scores_cluster_dict={}
                f_keys_cluster_dict={}
                ES_list=l.strip().split("+>")
                i=0
                EOccurencesDict={}
                NEp=0
                for es in ES_list:
                    NEp+=1
                    e,s=es.strip().split("->")
                    if e not in EOccurencesDict:
                        i+=1
                        EOccurencesDict[e]=0
                        conceptsIRI.append(e)
                        eId=str(i)
                        entitieIDScores_Dict[eId]=s
                        entitieScores_Dict[e]=float(s)
                    EOccurencesDict[e]+=1 # 
                n=len(conceptsIRI)
                conceptsIRInumber_dict={}
                for i in range(n):
                    c=conceptsIRI[i]
                    cId=str(i+1)
                    conceptsIRInumber_dict[cId]=c
                graph_dict=Disam.paraScoredGraph2(NEp,conceptsIRInumber_dict,entitieScores_Dict, docStrongLE_Catgs)
                finalCluster_dict, f_scores_cluster_dict, f_keys_cluster_dict=get_buildGraph2(graph_dict, Disam.smallestGraphScore)
                selected_entities=[]
                if finalCluster_dict=={}:
                    # here we perform the case of "non related entities". 
                    for e, s in  entitieScores_Dict.items():
                        relationshipScore=Disam.getRelationshipScore(e,docStrongLE_Catgs) # coherence
                        if float(s)>=0.35 or relationshipScore>0: # 
                            selected_entities.append(e)
                else:
                    selected_entities,relatedEntities_Dict=conceptSelection3(entitieIDScores_Dict, docStrongLE_Catgs, f_scores_cluster_dict, finalCluster_dict,conceptsIRInumber_dict)
                    for i in range(len(selected_entities)):
                        eId=selected_entities[i]
                        selected_entities[i]=conceptsIRInumber_dict[eId]
                #  for indexing : allSelectedEntity_dict
                if len(selected_entities)>0:
                    pNo+=1
                    nbSEP=0
                    for e in selected_entities:
                        if entitieScores_Dict[e]>=0.85: # e in entitieScores_Dict and 
                            nbSEP+=1
                    for e in selected_entities:       
                        if e not in allSelectedEntity_dict:
                            allSelectedEntity_dict[e]=[]
                        relatedE_nb=1
                        if e in relatedEntities_Dict:
                            relatedE_nb=relatedEntities_Dict[e]
                            #if score(e)>=0.5 sure. # 
                            if entitieScores_Dict[e]>=0.7 and EOccurencesDict[e]>1:
                                if EOccurencesDict[e]<=5:
                                    relatedE_nb+=EOccurencesDict[e]
                                else: #
                                    relatedE_nb+=5
                        IsStrong=0 # entity is strong or not.
                        if entitieScores_Dict[e]>=0.85: 
                            IsStrong=1    
                        shaine=docNO+'>>'+str(pNo)+'/'+str(len(selected_entities))+'/'+str(IsStrong)+'/'+str(nbSEP)+'/'+str(relatedE_nb)
                        allSelectedEntity_dict[e].append(shaine)       
        if docNO!='': #
            docParagNb_dict[docNO]=pNo
    return allSelectedEntity_dict,docParagNb_dict
#
def store_docParagNb(Folder,docParagNb_dict):
    FN=Folder+"docParagNb_dict.txt"
    FN=Folder+"docParagNb_dict_aTE.txt"
    FN=Folder+"docParagNb_dict_minCTE.txt"
    FN=Folder+"docParagNb_dict_maxCTE.txt"
    with open(FN, 'w', encoding='utf-8') as f:
        for d, paragNb in docParagNb_dict.items():
            s=d+'->'+str(paragNb)
            f.write(s+'\n')
#
def get_buildGraph2(graph_dict, min_graphScore):
    cluster_dict={}
    scores_cluster_dict={}
    keys_cluster_dict={}
    k=0
    insered=False
    for key, value in graph_dict.items():
        l=key.split('->')
        i=l[0]
        j=l[1]
        if value>min_graphScore:
            if insered==True:
                insered=False
                for c, v in cluster_dict.items():
                    if insered==False:
                        if (i in cluster_dict[c]) or (j in cluster_dict[c]):    
                            cluster_dict[c].add(i)
                            cluster_dict[c].add(j)
                            insered=True
                            scores_cluster_dict[c]+=value
                            keys_cluster_dict[c].add(key)
            if insered==False:                          
                k+=1
                cluster='cluster_'+str(k)
                cluster_dict[cluster]=set()
                cluster_dict[cluster].add(i)
                cluster_dict[cluster].add(j)
                scores_cluster_dict[cluster]=value
                keys_cluster_dict[cluster]=set()
                keys_cluster_dict[cluster].add(key)
                insered=True
    # identify the commun clusters:
    added=[]
    removed=[]
    for c, v in cluster_dict.items():
        arrived=False
        for c1, v1 in cluster_dict.items():
            if arrived==True:
                inter=set()
                inter= v & v1
                if inter!=set(): # commun clusters
                    if c not in removed:
                        added.append(c)
                        removed.append(c1)
                    else: # transitivity
                        for indice in range(len(removed)):
                            if c==removed[indice]:
                                found=indice
                        added.append(added[found])
                        removed.append(c1)               
            if c==c1:
                arrived=True
    # define the nonModifyed set
    nonModified=[]
    for c, v in cluster_dict.items():
        if c not in added and c not in removed:
            nonModified.append(c)
    # 
    finalCluster_dict={}
    f_scores_cluster_dict={}
    f_keys_cluster_dict={} 
    j=0
    for k in nonModified:
        j+=1
        s='cluster_'+str(j)
        finalCluster_dict[s]=set()
        finalCluster_dict[s]=cluster_dict[k]
        f_keys_cluster_dict[s]=set()
        f_keys_cluster_dict[s]=keys_cluster_dict[k]
        f_scores_cluster_dict[s]=scores_cluster_dict[k]
    # insertion of modified ones:
    toAdd=set()
    ex=''
    for i in range(len(added)):
        if ex!=added[i] or ex=='':
            ex=added[i]
            j+=1
            s='cluster_'+str(j)
            finalCluster_dict[s]=set()
            f_keys_cluster_dict[s]=set()
            f_scores_cluster_dict[s]=0
        toAdd=finalCluster_dict[s] | cluster_dict[added[i]] | cluster_dict[removed[i]]
        finalCluster_dict[s]=toAdd
        f_scores_cluster_dict[s]+=scores_cluster_dict[added[i]]+scores_cluster_dict[removed[i]]
        toAdd=f_keys_cluster_dict[s] |  keys_cluster_dict[added[i]] | keys_cluster_dict[removed[i]]
        f_keys_cluster_dict[s]=toAdd
        ex=added[i]
    return finalCluster_dict, f_scores_cluster_dict, f_keys_cluster_dict  
#
def conceptSelection3(entitieIDScores_Dict,docStrongLE_Catgs, f_scores_cluster_dict, finalCluster_dict,conceptsIRInumber_dict):
    smallestGraphScore=0.0001 # 
    conceptCluster_OurELScore_dict={}
    selectedCluster=''
    maxGraphScore=smallestGraphScore
    for key, value in finalCluster_dict.items():
        if f_scores_cluster_dict[key]>maxGraphScore:
            maxGraphScore=f_scores_cluster_dict[key]
            selectedCluster=key
    selected_concepts=[]
    relatedE_nb_Dict={} # {e/c: rE_nb}
    if selectedCluster!='':
        rE_nb=len(finalCluster_dict[selectedCluster])
        for c in finalCluster_dict[selectedCluster]:
            #if c!=idEcoh:
            selected_concepts.append(c)
            relatedE_nb_Dict[conceptsIRInumber_dict[c]]=rE_nb
    # add sure entities:
    for c, e in conceptsIRInumber_dict.items():
        if c not in selected_concepts:
            s=float(entitieIDScores_Dict[c])
            if s>=0.5 or e in docStrongLE_Catgs: # s>=0.35 or e in docStrongLE_Catgs:    
                selected_concepts.append(c)
    return selected_concepts,relatedE_nb_Dict
#
def indexing(Folder,allSelectedEntity_dict,docParagNb_dict):
    outPutFN=Folder+"msmarcoV1CollectionIndex.txt"
    outPutFN=Folder+"msmarcoV1_allED4DTE_CollectionIndex.txt" # TE: title entities.
    outPutFN=Folder+"msmarcoV1_minCTE_CollectionIndex.txt"
    outPutFN=Folder+"msmarcoV1_maxCTE_CollectionIndex.txt"
    with open(outPutFN, 'w', encoding='utf-8') as indexfile:
        for i in sorted (allSelectedEntity_dict.keys()):
            strg=i
            entity_doc_dict={}
            for DocParg in sorted (allSelectedEntity_dict[i]):
                doc, parag=DocParg.strip().split(">>") # 
                if doc not in entity_doc_dict:
                    entity_doc_dict[doc]=[]
                entity_doc_dict[doc].append(parag)
            for dkey, v in entity_doc_dict.items():
                parg_set=[]
                for p in v:
                    parg_set.append(p)
                pList=''
                for p in parg_set:
                    if pList=='':
                        pList=p
                    else:
                        pList=pList+','+p
                strg+='+>'+dkey+'->'+str(len(v))+'/'+pList
            indexfile.write(strg+'\n')
#
def main(Folder,FN):
    InputFN=Folder+FN
    print('DBpedia Loading ...')
    Disam=EntityLinkingIndexing(Folder,FN)
    allSelectedEntity_dict={}
    docParagNb_dict={}
    print('Disambiguation ...')
    allSelectedEntity_dict,docParagNb_dict=getAllEntitiesForIndexing(Disam,InputFN)
    print('Doc ParagNb saving ...')
    store_docParagNb(Folder,docParagNb_dict)
    print('Indexing ...')
    indexing(Folder,allSelectedEntity_dict,docParagNb_dict)

if __name__ == '__main__':
    if len(sys.argv)!=3:
        print("Usage: entityLinkingIndexing.py [ELinkedCollectionFileName] [path/to/Folder/]")
        exit(0)
    else:
        FN=sys.argv[1]
        Folder=sys.argv[2]
        main(Folder,FN)
