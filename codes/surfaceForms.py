"""
The surfaceForms class provides the surface form for our entity linking method.

Author: Mohamed Lemine Sidi (mlsidi@ogr.eskisehir.edu.tr)
"""
import os
from utils import *
class SurfaceForm(object):
    """
    This class contains a list 

    Attributes:
        E_db_Dict: ...
    """
    def __init__(self):
        self.E_db_Dict={}
        self.cleanedE_db_Dict={}
        self.ED_db_Dict={}
        self.cleanedED_db_Dict={}
        # entities and their subEntities 
        self.subLinkE_db_Dict={}
        # redirects
        self.redirct_ER_db_Dict={}
        self.cRedirct_ER_db_Dict={}
        self.redirects_Dict={}
        self.cRedirects_Dict={}
        # common Entities (by ids): these two set should be considered only when the previous one are not selected.
        self.newComonE_Facc_db_Dict={}
        self.newcComonE_Facc_db_Dict={}
        # similar entities:
        self.similarE_Dict={}
        Upstopwords_list=[]
        self.db_stopWords=[]
        self.termWithPoint_Dict=self.getTermWithPoint() # all of terms in which point.
    
    def getDbEntities(self):
        fn="D:/PESS4IR/data/E_db_Dict1.txt"
        with open(fn,'r', encoding='utf-8') as nf:
            for l in nf:
                k,v=l.strip().split('->')
                self.E_db_Dict[k]=''
    def getCleanedDbE(self):
        filename="D:/PESS4IR/data/cleanedE_db_Dict1.txt"
        with open(filename,'r',encoding='utf-8') as f:
            for l in f:
                k,v=l.strip().split('->')
                self.cleanedE_db_Dict[k]=v
    def getDisambiguations(self):
        fn="D:/PESS4IR/data/ED_db_Dict.txt"
        with open(fn,'r',encoding='utf-8') as f:
            for l in f:
                k,vs=l.strip().split('->')
                v=vs[2:len(vs)-2]
                v=v.strip().split("', '")      
                self.ED_db_Dict[k]=v
    def getCleanedDbED(self):
        filename="D:/PESS4IR/data/cleanedED_db_Dict1.txt"
        with open(filename,'r',encoding='utf-8') as f:
            for l in f:
                k,v=l.strip().split('->')
                self.cleanedED_db_Dict[k]=v
    def getE_subRedirects(self):                     
        with open("D:/PESS4IR/data/redirct_ER_db_Dict1.txt",'r', encoding='utf-8') as nf:
            for l in nf:   
                k,v=l.strip().split('->')
                self.redirct_ER_db_Dict[k]=v.strip().split(" ")
    #cRedirct_ER_db_Dict
    def getCleanedDbER(self):
        filename="D:/PESS4IR/data/cRedirct_ER_db_Dict1.txt"
        with open(filename,'r',encoding='utf-8') as f:
            for l in f:
                k,v=l.strip().split('->')
                self.cRedirct_ER_db_Dict[k]=v
    def getAllRedirects(self):
        filename="D:/PESS4IR/data/allRedirects_Dict1.txt"
        with open(filename,'r',encoding='utf-8') as f:
            for l in f:
                k,v=l.strip().split('->')
                self.redirects_Dict[k]=v
    def getAllcRedirects(self):
        filename="D:/PESS4IR/data/cleanedAllRedirects_Dict1.txt"
        with open(filename,'r',encoding='utf-8') as f:
            for l in f:
                k,v=l.strip().split('->')
                self.cRedirects_Dict[k]=v
    def getComonEntitiesFaccDb(self):
        '''
        by common Freebase Ids, ...
        '''
        filename='D:/PESS4IR/data/comonE_Facc_db_Dict_new.txt'
        with open(filename,'r',encoding='utf-8') as f:
            for l in f:
                if len(l.strip().split('->'))==2: #
                    k,v=l.strip().split('->')
                    self.newComonE_Facc_db_Dict[k]=v
    def getcComonEntitiesFaccDb(self):
        filename="D:/PESS4IR/data/comonE_Facc_db_Dict_cleanedNew.txt"
        with open(filename,'r',encoding='utf-8') as f:
            for l in f:
                if len(l.strip().split('->'))==2:
                    k,v=l.strip().split('->')
                    self.newcComonE_Facc_db_Dict[k]=v
    # additional entities (similar to E_db)
    def getSimilarEntities(self):
        filename="D:/PESS4IR/data/similarE_Dict.txt"
        with open(filename,'r',encoding='utf-8') as f:
            for l in f:
                k,v=l.strip().split('->')
                self.similarE_Dict[k]=v
    def getStopWordEntity(self):
        UpLowerLetters_Dict={}
        LowerUpLetters_Dict={}
        Ul='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        ml='abcdefghijklmnopqrstuvwxyz'
        for i in range(len(ml)):
            UpLowerLetters_Dict[Ul[i]]=ml[i]
            LowerUpLetters_Dict[ml[i]]=Ul[i]
        stopwords_list=[]
        filename='E:/DBpedia/stopwords-list-LemurProject.txt'
        with open(filename, 'r') as file:
            for l in file:
                t=l.strip().split(" ")
                stopwords_list.append(t[0])
        for w in stopwords_list:
            nw=LowerUpLetters_Dict[w[0]]
            nw+=w[1:len(w)] 
            Upstopwords_list.append(nw)
    # all terms in which we have point.
    def getTermWithPoint(self):
        # get them in a dict
        termWithPoint_Dict={}
        filename="D:/PESS4IR/data/allTermIncludingPoint.txt"
        with open(filename,'r', encoding='utf-8') as nf:
            for l in nf:
                t=l.strip().split(" ")
                t=t[0]
                termWithPoint_Dict[t]=''
        return termWithPoint_Dict
    def getDbStopWords(self):
        '''
        To get the set of stop words  
        '''        
        filename='D:/PESS4IR/data/db_stopWords2.txt'
        with open(filename,'r',encoding='utf-8') as f:
            for l in f:
                w=l.strip().split(" ")
                self.db_stopWords.append(w[0])
        return self.db_stopWords
    def size(self):
        return len(self.ED_db_Dict)+len(self.E_db_Dict)+len(self.redirects_Dict)+len(self.newComonE_Facc_db_Dict)


if __name__ == '__main__':
    sform = SurfaceForm()
    #print('Loading ...')
    sform.getDbEntities()


