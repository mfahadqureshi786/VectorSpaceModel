import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re
import ast
import os
from pathlib import Path
from Main import baseFilePath,buildInvertedIndex

def stemmedDocumentExist(DocID):
    dir = os.path.join(baseFilePath,"Stemmed")
    if not os.path.exists(dir):
        os.mkdir(dir)
    my_file = Path(baseFilePath+"Stemmed/speech_"+str(DocID)+".txt")
    if my_file.is_file():
        return True
    return False

#Checks first if stemmed document exist otherwise returns stemmed version of document
def processDocument(DocId):
    if not stemmedDocumentExist(DocId):
        trumpFileObj = open(baseFilePath+'Trump Speechs/speech_' + str(DocId) + '.txt', 'r')
        document = trumpFileObj.read()
        Lexicon = []
        stopWords = nltk.word_tokenize(open(baseFilePath+"Stopword-List.txt", 'r').read())
        processedDocument = ''
        sentences = nltk.sent_tokenize(document)
        Stemmer = PorterStemmer()
        "Sentences Preprocessing"
        for j in range(len(sentences)):
            processedSentence = re.sub('[^a-zA-Z]', ' ', sentences[j])
            processedSentence = processedSentence.lower()
            wordList = processedSentence.split()
            processedSentence = ''
            newSentence = ''
            for word in wordList:
                if word not in stopWords:
                    newSentence = newSentence + ' ' + Stemmer.stem(word)
                    if Stemmer.stem(word) not in Lexicon:
                        if len(Stemmer.stem(word)) > 1:
                            Lexicon.append(Stemmer.stem(word))
            #print(sentences[j])
            sentences[j] = newSentence
            #print(sentences[j])
            processedDocument = ''.join(sentences)
            #print(processedDocument)
        fileObj = open(baseFilePath+'Stemmed/speech_'+str(DocId)+'.txt', 'w')
        fileObj.write(processedDocument)
        return processedDocument
    else:
        fileObj = open(baseFilePath+'Stemmed/speech_'+ str(DocId) + ".txt","r")
        return fileObj.read()
    return None

#Builds the positional Index based on inverted Index
def buildPositionalIndex(event):
    print('Building Positional Index..')
    try:
        if not os.path.exists(baseFilePath+'positionalIndex.txt') and not os.path.getsize(baseFilePath + 'positionalIndex.txt') > 0:
            raise FileNotFoundError
    except FileNotFoundError:
        print('catched exception')
        buildInvertedIndex(event)
    fileObj = open(baseFilePath + 'invertedIndex.txt', 'r')
    if fileObj.mode == 'r':
        totalLexicons = int(fileObj.readline())
        posIndexObj = open(baseFilePath + 'positionalIndex.txt', 'w')
        posIndexObj.write(str(totalLexicons))
        mydictionary = {}
        lexeme = ""
        posting = []
        positionList = []
    for i in range(0, totalLexicons):
        # print('Current word index:'+str(i)+',Totallexicons:'+str(totalLexicons))
        lexeme = fileObj.readline()
        lexeme = lexeme.rstrip('\n')

        posting = fileObj.readline()
        posting = posting.rstrip('\n')
        posting = list(ast.literal_eval(posting))
        # mydictionary[lexeme] = positions
        posIndexObj.write('\n')
        posIndexObj.write(lexeme)
        posIndexObj.write('\n')
        posIndexObj.write(str(posting))
        posIndexObj.write('\n')

        for post in posting:
            # trumpFileObj = open('C:/MyFiles/Trump Speechs/speech_'+str(post)+'.txt', 'r')
            # document=trumpFileObj.read()
            ##Edit starts here
            document = processDocument(post)
            ##Edit ends here
            current = -1
            bool_should_run = True
            while bool_should_run:
                current = document.find(lexeme, current + 1)
                # print(document[current-20:current+len(lexeme)])
                if current != -1 and (not document[current - 1].isalpha()):
                    positionList.append(current)
                elif current == -1:
                    bool_should_run = False
            mydictionary[post] = positionList
            positionList = []
        posIndexObj.write(str(mydictionary))
        mydictionary = {}


    print('Finished! Building Positional Index.')

    return None


#Solves Positional Query
def searchPositionalIndex(lexeme1,lexeme2,k):
    try:
        if not os.path.exists(baseFilePath+'positionalIndex.txt') and not os.path.getsize(baseFilePath + 'positionalIndex.txt') > 0:
            raise FileNotFoundError
    except FileNotFoundError:
        print('catched exception')
        buildPositionalIndex("")

    resultDocs=[]
    k=int(k)
    Stemmer = PorterStemmer()
    lexeme1=Stemmer.stem(lexeme1).lower()
    lexeme2 = Stemmer.stem(lexeme2).lower()
    fileObj = open(baseFilePath+'positionalIndex.txt', 'r')
    totalLexicons = int(fileObj.readline())
    str1=""
    str2=""
    for i in range(0, totalLexicons):
        if i==2450:
            print('here')
        lexeme = fileObj.readline()
        lexeme = lexeme.rstrip('\n')
        posting = fileObj.readline()
        posting = set(eval(posting.rstrip('\n')))
        position=fileObj.readline()
        position=dict(eval(position.rstrip('\n')))

        if lexeme==lexeme1:
            posting1=posting
            position1=position
            str1=lexeme
        elif lexeme==lexeme2:
            posting2=posting
            position2=position
            str2 = lexeme

    if str1==lexeme1 and str2==lexeme2 and str1!=str2:
        res = posting1 & posting2
        # deleteing items from dictionary
        position1new = {}
        position2new = {}
        for docid in res:
            if docid in position1:
                position1new[docid] = position1[docid]
        for docid in res:
            if docid in position2:
                position2new[docid] = position2[docid]

        positionsList = []
        for dID in res:
            tFO = open(baseFilePath+'Stemmed/speech_' + str(dID) + '.txt', 'r')
            text = tFO.read()
            p1 = position1new[dID]
            p2 = position2new[dID]
            next = False
            for a in range(len(p1)):
                if not next:
                    for b in range(len(p2)):
                        if not next:
                            substrRange = ""
                            # if p1[a] <= p2[b] and not text[p1[a] + len(lexeme1)].isalpha():
                            if p1[a] <= p2[b]:
                                substrRange = text[p1[a]:p2[b] + len(lexeme2)]
                                # print(substrRange)
                            else:
                                substrRange = text[p2[b]:p1[a] + len(lexeme1)]
                                #print(substrRange)
                            words = re.sub('[^a-zA-Z]', ' ', substrRange).split()
                            if len(words) <= k + 2 and len(words)>0 and str(words[0]).startswith(str(lexeme1)) and str(words[-1]).startswith(str(lexeme2)):
                                positionsList.append(p1[a])
                                resultDocs.append(dID)
                                next = True

        #print(positionsList)
    return resultDocs


