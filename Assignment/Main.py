import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re
baseFilePath = 'C:/MyFiles/'

def buildInvertedIndex(event):
    print('Building Inverted Index..')


    stopWords = open(baseFilePath + 'Stopword-List.txt', 'r').read()
    stopWords = nltk.word_tokenize(stopWords)

    fileNumber = '0'
    filePath = ''

    Lexicon = []
    postingList = []
    totalDocs = 56
    "totalProcessedDocs=[None]*totalDocs"
    "Document Preprocessing"
    for i in range(totalDocs):
        #print('File number:' + str(i))
        filePath = baseFilePath + 'Trump Speechs/speech_' + str(i) + '.txt'
        fileObj = open(filePath + '', 'r')
        document = fileObj.read()
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

            sentences[j] = newSentence

            processedDocument = ''.join(sentences)


    "Not storing processed Documents to save RAM"
    "Writing lexicons to file"
    Lexicon = list(dict.fromkeys(Lexicon))
    tokenFile = open(baseFilePath + "/tokens.txt", "w")
    tokenFile.write(" ".join(Lexicon))
    "Generating Posting List"

    postingList = []
    for a in range(len(Lexicon)):
        postingList.append([])

    "Building Posting List"
    for i in range(totalDocs):

        filePath = baseFilePath + 'Trump Speechs/speech_' + str(i) + '.txt'
        fileObj = open(filePath + '', 'r')
        document = fileObj.read()
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
            sentences[j] = newSentence

            processedDocument = ''.join(sentences)
        ##checking for word
        tokens = processedDocument.split()
        tokens = list(dict.fromkeys(tokens))
        for a in range(len(Lexicon)):
            "if Lexicon[a] in tokens:"
            if tokens.count(Lexicon[a]) >= 1:
                if i not in postingList[a]:
                    postingList[a].append(i)
    fileObj = open(baseFilePath + '/invertedIndex.txt', 'w')
    myDictionary = {}
    fileObj.write(str(len(Lexicon)))
    fileObj.write('\n')
    for a in range(len(Lexicon)):
        myDictionary[Lexicon[a]] = postingList[a]
        fileObj.write(Lexicon[a])
        fileObj.write('\n')
        fileObj.write(str(postingList[a]))
        fileObj.write('\n')
    print('Finished! Building Inverted Index.')
    return None



#Inverted index is built now following code can be run to load block inverted index

from ReadIndex import *
from ExpressionEvaluation import *
#Converting string representation of list to list

#Parses the query to remove brackets
def queryPostProcessing(query):
    import re
    query = query.split()
    newQuery = []
    # Splitting further if it contains brackets
    for t in query:
        if len(t) >= 3 and t[0] == '(' and t[len(t) - 1] == ')':
            newQuery.append('(')
            newQuery.append(t[1:len(t) - 1])
            newQuery.append(')')
        elif len(t) >= 2 and t[0] == '(':
            newQuery.append('(')
            newQuery.append(t[1:len(t)])
        elif len(t) >= 2 and t[len(t) - 1] == '(':
            newQuery.append(t[0:len(t) - 1])
            newQuery.append('(')

        elif len(t) >= 2 and t[len(t) - 1] == ')':
            newQuery.append(t[0:len(t) - 1])
            newQuery.append(')')
        elif len(t) >= 2 and t[0] == ')':
            newQuery.append(')')
            newQuery.append(t[1:len(t)])
        elif t == '(' or t == ')':
            newQuery.append(t)
        else:
            if t != ' ' or t != '':
                newQuery.append(t)
    # Captializing bool operators
    for a in range(len(newQuery)):
        if isOperator(newQuery[a].upper()):
            newQuery[a] = newQuery[a].upper()
    return newQuery

#Solves boolean query by stack as a DataStructure and parameter passed to this function is postfix expression
def processBooleanQuery(str):
    resStack = []
    queryprocessedStack=[]
    uSet = set()
    for i in range(56):
        uSet.add(i)
    for a in range(len(str)):
        if not isOperator(str[a]):
            queryprocessedStack.append(str[a])
            termPosting = blockSearch(str[a])
            if termPosting == -1:
                termPosting = set()
            else:
                termPosting = set(ast.literal_eval(termPosting))
            resStack.append(termPosting)
        elif str[a] != '(' or str[a] != ')' or str[a] != ' ':

#Search lexeme if present store as set its posting list

# check if previous result is stored otherwise if not present search and store as set its posting list
                if str[a] == 'AND':
                    result=resStack[-1] & resStack[-2]
                    del resStack[-1]
                    del resStack[-1]
                    resStack.append(result)
                if str[a] == 'OR':
                    result = resStack[-1] | resStack[-2]
                    del resStack[-1]
                    del resStack[-1]
                    resStack.append(result)
                if str[a] == 'NOT':
                    result = uSet - resStack[-1]
                    del resStack[-1]
                    resStack.append(result)
    print(resStack)
    return resStack

def checkPositionalQuery(query):
    # Phrase query
    if len(query) == 2:
        return 1
    #Must be positional query
    if len(query)==3:
        if not isOperator(query[0]) and not isOperator(query[1]) and '/' in query[-1]:
            return 2
    if len(query)==4:
        if '/' in query[-1] and isOperator(query[2]) and '/' not in query[2]:
            return 3
    return 0

from PositionalIndex import *


