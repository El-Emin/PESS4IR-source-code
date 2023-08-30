# PESS4IR-source-code
Source code PESS4IR approach

EL4DT (mention detection and candidate selection methods): 1.1) For Robust collection: Usage: entityLinkingDocumentText.py [path/to/folder/]

[path/to/folder/]: the path to the folder in which the Robust collection is located the where each doc is splited in paragraghs (and is stored as 'DocID' fisrt line of a document and its paragraphs in the folowing lines (each paragraph in a line)). 1.2) For MSMARCO collection Usage: entityLinkingDocumentText.py [path/to/folder/] [-msDv1/-msDv2/msTv2/-msTv1]
[-msDv1/-msDv2/msTv2/-msTv1]: for MSMARCO versions.
The disambiguation method of EL4DT and the indexing method: Usage: entityLinkingIndexing.py [ELinkedCollectionFileName] [path/to/Folder/]

[ELinkedCollectionFileName]: the result of the two first steps of EL4DT method, which is the output of mention detection and candidate selection methods (entityLinkingDocumentText.py).
Retrieval and ranking function: Usage: retrieveRanking.py [indexFileName] [queriesFileName] [path/to/Folder/] [meanScore]

indexFileName : The file name of inverted index file. In this demo, data/robustCollectionIndex.txt is inverted index corresponding to the Standard Collection Robust04, annotated by our entity linking method (EL4DT).

queriesFileName: The file name of annotated entities. In the demo, is the annotated entities of Robust04 query set, which are annotated by two entity linking methods, namely REL and DBpedia Spotlight (bumchQ_REL_Annotations.txt and bumchQ_Spotlight_Annotations.txt, respectively).

meanScore: The mean score of entities annotation score corresponding to the given query. It should be between 0 and 1.

Execution Requirements:

At least python 3.6.8
