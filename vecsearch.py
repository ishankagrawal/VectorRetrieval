import sys,getopt
import Trie
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import math
ps = PorterStemmer()
tokenizer = RegexpTokenizer("\w+")
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
                offsetlist[lastbyte] = int(s[2])
                lastbyte = curbyte

            else:
                
                f.seek(int(s[0]),0)
        res = json.loads(f.read())

   
    
    
    return (root,res)
def getdocs(query,doclist,root):
    n = len(doclist)

    res = {}
    for dociter in doclist:
        res[dociter] = 0
    
    qvec = {}
    qnorm = 0
    t = query.split()

    temp = []
    for word in t:
        if(word[-1] == '*'):
            oflist = root.searchprefix(word.lower())
            qnorm+=1
            
            for offset in oflist:
                f.seek(offset,0)
                posting = json.loads(f.read(offsetlist[offset]))
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
        qnorm += qvec[word]**2
        trieval = root.search(word)
        if(trieval):
            offset = trieval[1]
            
            
            f.seek(offset,0)

            
            posting = json.loads(f.read(offsetlist[offset]))
            
            for dociter in posting[0]:
                res[dociter]+= math.log2(1+qvec[word])*tdfidf(posting[0][dociter],n,len(posting[0]))

    '''for dociter in doclist:
            if(len(doclist[dociter])==2):
                res[dociter] = res[dociter]/math.sqrt((qnorm*doclist[dociter][1]))
   '''
    return res

print("Importing Dictionary: Please wait...")

root,doclist = generateTrie(dictfile)

print("Generating result file: Please wait...")


'''with open(dictfile,"r") as d:
    for line in d:
        s = line.split()
        print(s[0])
        
        f.seek(curbyte,0)
        p = json.loads(f.read(offsetlist[curbyte]))
        curbyte+=int(s[2])'''
        


qlist = parseQ(queryfile)
qiter = 51

with open(resultfile,"w") as rf:
	for q in qlist:
		ab = 1
		docs = getdocs(q,doclist,root)
		topk = sorted(docs,key = lambda item: -docs[item])[:cutoff]
		for dociter in topk:

			rf.write(str(qiter) + " Q0" + " " + doclist[dociter][0] + " " + str(ab) + " " + str(docs[dociter]) + " STANDARD" + '\n')
			ab+=1
		qiter+=1

f.close()





    















