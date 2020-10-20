#!/usr/bin/python
import sys,getopt
import Trie
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk
import math
def decoder(s):
    cur = 1
    dlist = {}
    for item in s.split():
        dlist[str(cur)] = [item.split(",")[0],int(item.split(",")[1])*4]
        cur+=1
    return dlist
def dictdecode(s):
    
    d = s.split()
    cur = 0
    d1 = {}
    d2 = {}
    for dictitem in d[0].split(','):
        d1[str(cur+int(dictitem.split(':')[0]))] = int(dictitem.split(':')[1])
        cur = cur+int(dictitem.split(':')[0])
    cur = 0
    if(len(d)>1):
        for dictitem in d[1].split(','):
            d2[str(cur+int(dictitem.split(':')[0]))] = int(dictitem.split(':')[1])
            cur = cur+int(dictitem.split(':')[0])
    return [d1,d2]





    
ps = PorterStemmer()
tokenizer = RegexpTokenizer("[\w']+")
english_stops = set(stopwords.words('english'))
queryfile = ''
cutoff = 10
resultfile = ''
indexfile = ''
dictfile = ''
offsetlist = {}


opts, args = getopt.getopt(sys.argv[1:],"",["query=","cutoff=","output=","index=","dict="])

for opt,arg in opts:
    if(opt=="--query"):
        queryfile = arg
        
    elif(opt=="--cutoff"):
        cutoff = int(arg)
    elif(opt=="--output"):
        resultfile = arg
    elif(opt=="--index"):
        indexfile = arg
    elif(opt=="--dict"):
        dictfile = arg

f = open(indexfile,"r")
querylist = []
mapnouns = {"P:":1 , "L:":2 , "O:":3}
def tdfidf(freq,n,df):
    return ((1+math.log2(freq))*math.log2(1 + (n/df)))
def parseQ(queryfile):
    res = []
    with open(queryfile,"r") as qf:
        for line in qf:
            if(line.startswith("<title>")):
                res.append(line[14:-1])
    return res
def generateTrie(dictfile):
    lim = 0
    root = Trie.trie()
    curbyte = 0
    lastbyte = 0
    
    with open(dictfile,"r") as d:
        for line in d:
            
            s = line.split()
            if(len(s)>2):
                
                root.insert(s[0],curbyte,int(s[1]))

                curbyte += int(s[2])
                offsetlist[lastbyte] = int(s[2])
                lastbyte = curbyte

            else:
                
                f.seek(int(s[0]),0)
        res = decoder(f.read())

   
    
    
    return (root,res)
def getdocs(query,doclist,root):
    n = len(doclist)

    res = {}
    for dociter in doclist:
        res[dociter] = 0
    
    qvec = {}
    qnorm = 0
    qfull = query.split()
    t = []
    for word in qfull:
        if(len(word)>=2 and word[1] == ":"):
            if(word[0]=='N'):
                qfull.append("L:" + word[2:])
                qfull.append("O:" + word[2:])
                qfull.append("P:" + word[2:])
                continue
            if(word[-1] == '*'):
                oflist = root.searchprefix(word[2:].lower())
                
                
                for offset in oflist:
                    f.seek(offset,0)
                    posting = dictdecode(f.read(offsetlist[offset]))
                    if(len(posting)>1):
                        for dociter in posting[1]:
                            if(posting[1][dociter]==mapnouns[word[:2]]):
                                res[dociter]+=tdfidf(posting[1][dociter],n,len(posting[1]))
            else:
                qnorm+=1
                trieval = root.search(word[2:].lower())
                if(trieval):
                    offset = trieval[1]

                    
                    
                    f.seek(offset,0)

                    
                    posting = dictdecode(f.read(offsetlist[offset]))
                    if(len(posting)>1):
                        for dociter in posting[1]:
                            if(posting[1][dociter] == mapnouns[word[:2]]):
                                res[dociter]+= tdfidf(posting[1][dociter],n,len(posting[1]))







        else:
                t.append(word)  






    temp = []
    for word in t:
        if(word[-1] == '*'):
            oflist = root.searchprefix(word.lower())
            
            
            for offset in oflist:
                f.seek(offset,0)
                posting = dictdecode(f.read(offsetlist[offset]))

                for dociter in posting[0]:
                    res[dociter]+=tdfidf(posting[0][dociter],n,len(posting[0]))
            #Apply sqrt here if not work

        else:
            temp.append(word)


 

    l = tokenizer.tokenize(' '.join(temp))
    print(l)
    for w in l:

        word = ps.stem(w.lower())
        if(word not in english_stops):
            if(word in qvec):
                qvec[word]+=1
            else:
                qvec[word]=1
    for word in qvec:

        
        trieval = root.search(word)
        if(trieval):
            offset = trieval[1]
            
            
            f.seek(offset,0)

            
            posting = dictdecode(f.read(offsetlist[offset]))
            
           
            for dociter in posting[0]:
                    res[dociter]+= (1+math.log2(qvec[word]))*tdfidf(posting[0][dociter],n,len(posting[0]))
                


    for dociter in doclist:
            if(len(doclist[dociter])==2):
                res[dociter] = res[dociter]/math.sqrt(doclist[dociter][1])
   
    return res

print("Importing Dictionary: Please wait...")

root,doclist = generateTrie(dictfile)
print(len(doclist))

print("Generating result file: Please wait...")

        


qlist = parseQ(queryfile)
qiter = 51


with open(resultfile,"w") as rf:
    for q in qlist:
        ab = 1
        docs = getdocs(q,doclist,root)
        print(qiter)
        topk = sorted(docs,key = lambda item: -docs[item])[:cutoff]
        for dociter in topk:

            rf.write(str(qiter) + " Q0" + " " + doclist[dociter][0] + " " + str(ab) + " " + str(docs[dociter]) + " STANDARD" + '\n')
            ab+=1
        qiter+=1


'''
docs  = getdocs("U.S.",doclist,root)

tptp = sorted(docs,key = lambda item: -docs[item])[:cutoff]

for lplp in tptp:
    print(doclist[lplp])
for lplp in tptp:
    print(docs[lplp])

f.close()
'''







    















