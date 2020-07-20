from tkinter import *
from Main import *
from threading import *
import os
from pathlib import Path
#Takes Query from GUI and passes it for further processing


def searcher(event):

    baseFilePath=pathBar.get("1.0",END).rstrip('\n')
    if len(baseFilePath)>0:
        input = searchBar.get("1.0", END)
        print(input)
        query = input
        newQuery = queryPostProcessing(query)  # Parses the query to remove brackets
        newQuery = evaluator(newQuery)  # Infix to Postfix
        print(isPositionalQuery(newQuery))
        print(baseFilePath)
        try:
            if not os.path.exists(baseFilePath + 'invertedIndex.txt') and not os.path.getsize(
                    baseFilePath + 'invertedIndex.txt') > 0:
                raise FileNotFoundError
        except FileNotFoundError:
            print('catched exception')
            buildInvertedIndex(event)

        if not isPositionalQuery(newQuery):
            res = processBooleanQuery(newQuery)  # Solves boolean query
        else:
            positionalType = checkPositionalQuery(newQuery)
            if positionalType == 1:
                res = searchPositionalIndex(newQuery[0], newQuery[1], 0)
            if positionalType == 2:
                res = searchPositionalIndex(newQuery[0], newQuery[1], newQuery[-1][-1])
            if positionalType == 3:
                res = searchPositionalIndex(newQuery[0], newQuery[1], newQuery[3][-1])
        resultBar.delete("1.0", END)
        resultBar.insert(END, str(res))
    return None
root = Tk()
title=Label(root,text='Information Retrieval System',font='Helvetica 12 bold',fg="Blue")
title.grid(row=0,column=0,sticky=N)

labelPath=Label(root,text='BaseFilePath',font='Helvetica 10 bold')
labelPath.grid(row=1,column=0,sticky=W)
pathBar=Text(root,height=1,width=20)
pathBar.grid(row=2,column=0,sticky=W)


labelQuery=Label(root,text='Query',font='Helvetica 10 bold')
labelQuery.grid(row=3,column=0,sticky=W)

searchBar=Text(root,height=3,width=30)
searchBar.grid(row=4,sticky=W)

btnSearch=Button(root,text="Search",fg="red")
btnSearch.grid(row=4,column=1)
btnSearch.bind('<Button-1>',searcher)

btnInvIndex=Button(root,text="Build Inverted Index",fg="red")
btnInvIndex.grid(row=5,column=1,sticky=E)
btnInvIndex.bind('<Button-1>',buildInvertedIndex)

btnPosIndex=Button(root,text="Build Positional Index",fg="red")
btnPosIndex.grid(row=6,column=1,sticky=E)
btnPosIndex.bind('<Button-1>',buildPositionalIndex)

labelResult=Label(root,text='Result',font='Helvetica 10 bold')
labelResult.grid(row=5,column=0,sticky=N)

resultBar=Text(root,height=5,width=30)
resultBar.grid(row=6,column=0,sticky=W)


root.mainloop()
