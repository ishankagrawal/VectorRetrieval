#!/usr/bin/python3
import sys
import os
import nltk
import math
from nltk.tokenize import RegexpTokenizer

from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer 
ps = PorterStemmer()
abspath = sys.argv[1]



english_stops = {'very', 'with', "should", "'ve","'s", 'in', 'the', 'on', 'to', 'down', 'ain', 'their', 'ours', 'shouldn', 'you', 'needn', 'any', 'out', 'll', 'are', 'be', 'had', "mightn't", 'him', "you've", 'doing', 'what', 'off', 'that', 'whom', 'hers', 'when', 'been', "you're", 'didn', 'she', 'ourselves', 'while', 'her', 'because', 'your', 'yours', 't', 'once', 'being', 'why', 'aren', 'mightn', 'those', 'over', 'now',  'how', 'do', 'above', 'wasn', "couldn't", 'yourselves', 'these', 'is', "didn't", 'won', 'having', 's', 'but', 've', 'm', 'its', 'couldn', 'who', 'don',   'doesn', 'nor', 'this', 'of', 'few', 'or', 'haven', "weren't", 'at', 'am', 'have', 'they', 'myself', "doesn't", 'then', 'itself', 'than', 'most', "you'd", 'did', 'we', 'will', 'were', "mustn't", 'shan', 'he', 'd', 'it', 'such', 're', 'my', "that'll", 'mustn', 'can', 'does', 'if', 'me', 'again', "shan't", 'theirs', 'here', 'under', 'themselves', 'through', 'between', 'where', "don't", "needn't", "wouldn't", 'no', "she's", 'hadn', 'some', "it's", 'other', 'his', "haven't", 'isn', 'not', "aren't", 'which', 'against', "wasn't", 'y', 'as', 'weren', 'same', 'wouldn', 'them', "hasn't", 'himself', 'about', 'and', 'from', 'more', 'during', 'own', 'after', 'a', 'there', 'hasn', 'so', 'o', "shouldn't", 'all', 'yourself', 'an', 'just', 'for', 'herself', 'should', 'i', 'below', 'has', 'was', 'into', 'ma', 'by', 'before', 'both', 'too', 'each', "won't", 'our', 'until', 'further', 'up', 'only'}
print(english_stops)


def tdfidf(freq,n,word,vocab):
	return ((1+math.log2(freq))*math.log2(1 + (n/len(vocab[word][0]))))**2
def dictencode(d):
	last = 0
	reslist = []
	for dociter in d[0]:

		reslist.append(str(dociter-last) + ":" + str(d[0][dociter]))
		last = dociter
	s1 = ','.join(reslist)
	last = 0
	reslist = []
	if(len(d)>1):
		for dociter in d[1]:
			reslist.append(str(dociter-last) + ":" + str(d[1][dociter]))
			last = dociter
	s2 = ','.join(reslist)
	return s1 + " " + s2

def encoder(d):
	reslist = []
	for dociter in d:


		reslist.append(d[dociter][0] + ',' + str(int(d[dociter][1])))
	return " ".join(reslist)




def generateidx(abspath,english_stops):
	tokenizer = RegexpTokenizer("[\w]+")
	
	dlist = os.listdir(abspath)
	dociter = 0
	doclist = {}


	vocab = {}


	filelim = 0
	for filename in dlist:
		filelim+=1
		
		with open(abspath + "/" + filename,'r') as f:
			soup = BeautifulSoup(f, 'html.parser')
		
		
		for tag in soup.find_all('doc'):
			
			dociter+=1
			doclist[dociter] = [tag.find('docno').text.split()[0],0]
			for t in tag.find_all('text'):
			
			

				
					
				
				

				
				

				for word in map(ps.stem,map(str.lower,tokenizer.tokenize(t.text))):
					


					'''if(word[-1] == "'"):

						if(len(word)>1 and word[-2]=="'"):
							word = word[:-2]
						else:
							word = word[:-1]'''
					if(word not in english_stops):

						if(word in vocab):
							if(dociter in vocab[word][0]):
								
								vocab[word][0][dociter]+=1
							else:
								vocab[word][0][dociter]=1
								
													
						else:
							

							vocab[word] = [{dociter:1}]
				persons = tag.find_all('person')
				for person in persons:
					l = tokenizer.tokenize(person.text)
					for w in l:
						word = w.lower()
						if(word in vocab):
							if(len(vocab[word])==1):
								vocab[word].append({dociter:1})
							else:
								vocab[word][1][dociter] = 1
				locations = tag.find_all('location')
				for loc in locations:
					l = tokenizer.tokenize(loc.text)
					for w in l:
						word = w.lower()
						if(word in vocab):
							if(len(vocab[word])==1):
								vocab[word].append({dociter:2})
							else:
								vocab[word][1][dociter] = 2
				orgs = tag.find_all('organization')
				for org in orgs:
					l = tokenizer.tokenize(org.text)
					for w in l:
						word = w.lower()
						if(word in vocab):
							if(len(vocab[word])==1):
								vocab[word].append({dociter:3})
							else:
								vocab[word][1][dociter] = 3
		print(filelim)
		if(filelim>5):
			break






	return (vocab,doclist)




print("Generating index: It may take a few minutes...")
vocab,doclist = generateidx(abspath,english_stops)





total = len(doclist)
for word in vocab:
	for doc in vocab[word][0]:
			doclist[doc][1]+=tdfidf(vocab[word][0][doc],total,word,vocab)
			



lastbyte = 0
lasttell = 0

dictfile =  open(sys.argv[2] + '.dict', mode='w')
indexfile =  open(sys.argv[2] + '.idx', mode='w')

for word in vocab:
	if(word ==''):
		continue

	dictfile.write(word + " " + str(len(vocab[word][0])) + " ")
	
	indexfile.write(dictencode(vocab[word]))
	
	dictfile.write(str(indexfile.tell() - lasttell) + "\n")
	lasttell = indexfile.tell()
	
	
	

dictfile.write(str(indexfile.tell()))
indexfile.write(encoder(doclist))

dictfile.close()
indexfile.close()







	

	
	





		
		

	


	

		

	



		
			