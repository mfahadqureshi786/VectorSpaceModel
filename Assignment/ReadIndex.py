import ast
from nltk.stem import PorterStemmer
from Main import baseFilePath

#Block by block search for lexeme from inverted index..block size is set to 2000 lexemes
def blockSearch(term):
    stemmer=PorterStemmer()
    term=stemmer.stem(term)

    fileObj=open(baseFilePath+'invertedIndex.txt','r')
    if fileObj.mode == 'r':

        totalLexicons=int(fileObj.readline())
        blockLimit=2000

        for i in range(0,totalLexicons,blockLimit):
            mydictionary={}
            lexeme=''
            posting=[]
            for a in range(blockLimit):
                lexeme=fileObj.readline()
                lexeme=lexeme.rstrip('\n')
                posting=fileObj.readline()
                posting = posting.rstrip('\n')
                mydictionary[lexeme]=posting
                if lexeme==term:
                    return posting
            #print('Printing Block')
            #print(mydictionary)

    return -1
