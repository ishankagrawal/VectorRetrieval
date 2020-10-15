import sys,getopt
import Trie
#import json
import pickle
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import math
english_stops = set(stopwords.words('english'))
tokenizer = RegexpTokenizer("[\w']+")
queryfile = ''
cutoff = 10
resultfile = ''
indexfile = ''
dictfile = ''
offsetlist = {}

print(sys.argv[1:])
opts, args = getopt.getopt(sys.argv[1:],"",["query=","cutoff=","output=","index=","dict="])
print(opts)
for opt,arg in opts:
	if(opt=="--query"):
		queryfile = arg
		print("lol")
	elif(opt=="--cutoff"):
		cutoff = int(arg)
	elif(opt=="--output"):
		resultfile = arg
	elif(opt=="--index"):
		indexfile = arg
	elif(opt=="--dict"):
		dictfile = arg

f = open(indexfile,"rb")
querylist = []
def tdfidf(freq,n,df):
    return (math.log2(1+freq)*math.log2(1 + (n/df)))
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
                #offsetlist[lastbyte] = int(s[2])
                #lastbyte = curbyte

            else:
                f.seek(int(s[0]),0)
        res = pickle.load(f)

   
    
    
    return (root,res)
def getdocs(query,doclist,root):
    res = {}
    for dociter in doclist:
        res[dociter] = 0
    

    l = tokenizer.tokenize(query)
    qvec = {}
    n = len(doclist)
    for w in l:
        word = w.lower()
        if(word not in english_stops):
            if(word in qvec):
                qvec[word]+=1
            else:
                qvec[word]=1
    for word in qvec:
        trieval = root.search(word)
        if(trieval):
            offset = trieval[1]
            print(offset)
            f.seek(offset,0)

            
            posting = pickle.load(f)
            
            for dociter in posting[0]:
                res[dociter]+= math.log(1+qvec[word])*tdfidf(posting[0][dociter],n,len(posting[0]))
    return res


root,doclist = generateTrie(dictfile)
#print(getdocs("officers",doclist,root))

print(getdocs("news",doclist,root))












