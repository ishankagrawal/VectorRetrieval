import sys
import pickle
class TrieNode:  
	def __init__(self): 
		self.children = [None]*36
		
		self.offset = None
		self.df = None  
		self.isEnd = False

class trie:
	def __init__(self): 
		self.root = TrieNode()
	
	def insert(self,key,of,freq): 
		cur = self.root 
		
		level = 0
		while(level<len(key)):
			index = -1
			if(key[level].isalpha()):
				index = ord(key[level]) - ord('a')
			elif(key[level].isdigit()) :
				
				index = int(key[level]) + 26
			if(index>=0):
				if not cur.children[index]: 
					cur.children[index] = TrieNode()
				cur = cur.children[index]
				
			level+=1 
		cur.offset = of
		cur.df = freq
		cur.isEnd = True


	def search(self,key):
		res = ""
		cur = self.root
		
		level = 0
		while(level<len(key)):
			index = -1
			if(key[level].isalpha()):
				index = ord(key[level]) - ord('a')
			elif(key[level].isdigit()) :
				index = int(key[level]) + 26
			if(index>=0):
				if(cur.children[index]): 
					cur = cur.children[index]
					res+=key[level]
				else:
					return None
			level+=1

		if(cur.isEnd):
			return [cur.df,cur.offset]
		return None
	def searchprefix(self,key):
		res = []
		cur = self.root
		
		level = 0
		while(level<len(key)):
			index = -1
			if(key[level].isalpha()):
				index = ord(key[level]) - ord('a')
			elif(key[level].isdigit()) :
				index = int(key[level]) + 26
			if(index>=0):
				if(cur.children[index]): 
					cur = cur.children[index]
				else:
					return res
					
			level+=1

		self.generate(cur,res)
		return res
		
	def generate(self,cur,res):

		if(cur):
			if(cur.isEnd):
				res.append(cur.offset)
			for child in cur.children:
				self.generate(child,res)








		 

			







'''dictfile = open(sys.argv[1]+".dict","rb")
indexfile = open(sys.argv[1] + ".idx","rb")

vocab = {}
curbyte = 0
lim = 0
for line in dictfile:
	lim+=1
	s = line.split()

	vocab[s[0].decode()] = [int(s[1].decode()),int(s[2].decode()) + curbyte]
	curbyte += int(s[2].decode())
	
	if(lim>10):
		break





dictfile.close()
indexfile.close()
'''

