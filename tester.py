import sys
import os
import xml.etree.ElementTree as ET 
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import nltk.data
import re
import pickle
from bs4 import BeautifulSoup,NavigableString
import tracemalloc
#tracemalloc.start()







stemmer = PorterStemmer()
english_stops = set(stopwords.words('english'))

abspath = sys.argv[1]
dlist = os.listdir(abspath)
dociter = 1
doclist = {}


vocab = {}

numtags = 0
filelim = 0
for filename in dlist:
	filelim+=1
	
	f = open(abspath + "/" + filename,'r')
	soup = BeautifulSoup(f, 'html.parser')
	f.close()
	
	for tag in soup.find_all('doc'):
		doclist[dociter] = tag.docno.string
		dociter+=1
		t = tag.find('text')

		if(tag!=None):
			numtags+=1
		tokenizer = RegexpTokenizer(r"[\w']+")
		l = tokenizer.tokenize(t.text)
		

		for w in l:
			word = w.lower()
			if(word not in english_stops):
				if(word in vocab):
					if(dociter in vocab[word]):
						vocab[word][0][dociter]+=1
					else:
						vocab[word][0][dociter]=1
					
				else:
					

					vocab[word] = [{dociter:1}]
		for noun in tag.find_all(['person','organization','location']):
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

					
		#taglist = t.contents
		
		p = 0
		""" MERGE QUAERIES TBDL
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

	
	#current, peak = tracemalloc.get_traced_memory()
	#print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
	print(dociter)
#tracemalloc.stop()


lastbyte = 0

dictfile =  open(sys.argv[2] + '.dict', mode='w')
indexfile =  open(sys.argv[2] + '.idx', mode='wb')
'''
for word in vocab:
	dictfile.write(bytes((word + " " + str(len(vocab[word][0]))).encode()))
	indexfile.write(bytes(str(vocab[word]).encode()))

	dictfile.write(bytes((" " + str(indexfile.tell()-lastbyte) + "\n").encode()))
	lastbyte = indexfile.tell()
'''

	
for word in vocab:
	dictfile.write((word + " " + str(len(vocab[word][0])) + " "))
	
	pickle.dump(vocab[word],indexfile)
	dictfile.write(str(lastbyte) + "\n")
	lastbyte = indexfile.tell() - lastbyte
dictfile.close()
indexfile.close()







	

	
	





		
		

	


	

		

	



		
			