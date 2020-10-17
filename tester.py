import sys
import os
import xml.etree.ElementTree as ET 
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import nltk.data
import re
import json
from bs4 import BeautifulSoup,NavigableString
from nltk.stem import PorterStemmer 
ps = PorterStemmer()


import math

tokenizer = RegexpTokenizer("[\w']+")
def tdfidf(freq,n,word,vocab):
	return (math.log2(1+freq)*math.log2(1 + (n/len(vocab[word][0]))))**2





english_stops = set(stopwords.words('english'))

abspath = sys.argv[1]
dlist = os.listdir(abspath)
dociter = 0
doclist = {}


vocab = {}

numtags = 0
filelim = 0
print("Generating index: It may take a few minutes...")
for filename in dlist:
	filelim+=1
	
	with open(abspath + "/" + filename,'r') as f:
		soup = BeautifulSoup(f, 'html.parser')
	
	
	for tag in soup.find_all('doc'):
		
		dociter+=1
		u = tag.find('docno')
		doclist[dociter] = [u.text.split()[0]]
		for t in tag.find_all('text'):
		
		

			if(tag!=None):
				numtags+=1
			
			l = tokenizer.tokenize(t.text)
			

			for w in l:
				word = ps.stem(w.lower())
				if(word[0]==" "):
					print(word)
				if(word[-1] == "'"):

					if(len(word)>1 and word[-2]=="'"):
						word = word[:-2]
					else:
						word = word[:-1]
				if(word not in english_stops):
					if(word in vocab):
						if(dociter in vocab[word][0]):
							
							vocab[word][0][dociter]+=1
						else:
							vocab[word][0][dociter]=1
							
												
					else:
						

						vocab[word] = [{dociter:1}]

			
			'''for noun in tag.find_all(['person','organization','location']):
				if(noun.name=='location'):
					curnoun = noun.text.lower()
					if(curnoun in vocab and len(vocab[curnoun])==1):
						vocab[curnoun].append(1)
					else:
						vocab[curnoun] = [{dociter:1},1]
				elif(noun.name=='person' ):
					curnoun = noun.text.lower()
					if(curnoun in vocab and len(vocab[curnoun])==1):
						vocab[curnoun].append(2)
					else:
						vocab[curnoun] = [{dociter:1},2]
				elif(noun.name=='organization'):
					curnoun = noun.text.lower()
					if(curnoun in vocab and len(vocab[curnoun])==1):
						vocab[curnoun].append(3)
					else:
						vocab[curnoun] = [{dociter:1},3]
			'''

						
			#taglist = t.contents
			
			
			""" MERGE QUAERIES TBDL
			p=0
			while(p<len(taglist)):
				if(not isinstance(taglist[p],NavigableString)):
					curword = ""
					if(taglist[p].name=="person"):
						

						while(p<len(taglist) and (not isinstance(taglist[p],NavigableString)) and taglist[p].name=="person"):
							curword += taglist[p].text.lower()
							p+=1

						if(curword not in vocab):
							vocab[curword] = [{dociter,1},1]
						else:
							if len(vocab[curword])==1:
								vocab[curword].append(1) 
					elif(taglist[p].name=="location"):
						
						while(p<len(taglist) and (not isinstance(taglist[p],NavigableString)) and taglist[p].name=="location"):
							curword += taglist[p].text.lower()
							p+=1
						if(curword not in vocab):
							vocab[curword] = [{dociter,1},2]
						else:
							if len(vocab[curword])==1:
								vocab[curword].append(2) 
					elif(taglist[p].name=="organization"):
						
						while(p<len(taglist) and (not isinstance(taglist[p],NavigableString)) and taglist[p].name=="organization"):
							curword += taglist[p].text.lower()
							p+=1
						print(curword)
						if(curword not in vocab):
							vocab[curword] = [{dociter,1},3]
						else:
							if len(vocab[curword])==1:
								vocab[curword].append(3) 

				else:
					p+=1
			"""

		
	print(filelim)

total = len(doclist)
for word in vocab:
	for doc in vocab[word][0]:
		if(len(doclist[doc])>1):
			doclist[doc][1]+=tdfidf(vocab[word][0][doc],total,word,vocab)
		else:
			doclist[doc].append(tdfidf(vocab[word][0][doc],total,word,vocab))





		

	



lastbyte = 0
lasttell = 0

dictfile =  open(sys.argv[2] + '.dict', mode='w')
indexfile =  open(sys.argv[2] + '.idx', mode='wb')
'''
for word in vocab:
	dictfile.write(bytes((word + " " + str(len(vocab[word][0]))).encode()))
	indexfile.write(bytes(str(vocab[word]).encode()))

	dictfile.write(bytes((" " + str(indexfile.tell()-lastbyte) + "").encode()))
	lastbyte = indexfile.tell()
'''

for word in vocab:
	if(word ==''):
		continue

	dictfile.write(word + " " + str(len(vocab[word][0])) + " ")
	
	indexfile.write(json.dumps(vocab[word]).encode())
	#pickle.dump(vocab[word],indexfile)
	dictfile.write(str(indexfile.tell() - lasttell) + "\n")
	lasttell = indexfile.tell()
	
	
	

dictfile.write(str(indexfile.tell()))
indexfile.write(json.dumps(doclist).encode())
#pickle.dump(doclist,indexfile)
dictfile.close()
indexfile.close()







	

	
	





		
		

	


	

		

	



		
			