"""
The ParagEntityExtraction class extract entities for a given corpus.

Authors: M. Lemine Sidi (mlsidi@ogr.eskisehir.edu.tr)
"""
import os
class ParagEntityExtraction(object):
    """
    This class contains  
    Attributes:
        E_db: ...
    """
    def __init__(self):
        self.m=''
        self.E_db=[]
        self.cE_db=[]
        self.D_db=[]
        self.cD_db=[]
        # redirects
        self.ER_db=[]
        self.cER_db=[]
        self.R_db=[]
        self.cR_db=[]
        # common Entities (by ids)
        self.Fb_FaccDB=[]
        self.cFb_FaccDB=[]
        # similar entities
        self.SE_db=[]
    def isEmpty(self):
        if self.E_db==self.cE_db==self.D_db==self.cD_db==self.cD_db==self.ER_db==self.cER_db==self.R_db==self.cR_db==self.Fb_FaccDB==self.cFb_FaccDB==[]: # self.SE_db==[]:
            return True
        else:
            return False
    def getProperties():
        propertiesNames=['E_db','cE_db','D_db','cD_db','cD_db','ER_db','cER_db','R_db','cR_db','Fb_FaccDB','cFb_FaccDB','SE_db']
        return propertiesNames
'''
if __name__ == '__main__':
    surfaceF_Dicts= SurfaceForm()
    surfaceF_Dicts.getDbEntities()
    db_stopWords=[]
    db_stopWords=surfaceF_Dicts.getDbStopWords()
    surfaceF_Dicts.getCleanedDbE()
    # here we desactivated return in all methods in the class
    surfaceF_Dicts.getDisambiguations()
    surfaceF_Dicts.getCleanedDbED()
    surfaceF_Dicts.getE_subRedirects()
    surfaceF_Dicts.getCleanedDbER()
    surfaceF_Dicts.getAllRedirects()
    surfaceF_Dicts.getAllcRedirects()
    surfaceF_Dicts.getComonEntitiesFaccDb()
    surfaceF_Dicts.getcComonEntitiesFaccDb()
    # testing with a given paragraph
    p=cleanText(p)
    # building
    paragEEss=sureDisambiguiation(surfaceF_Dicts,p)
    print('Loading ...')
    sform.getDbEntities()
    print('E_db_Dict loaded')
    

   '''
