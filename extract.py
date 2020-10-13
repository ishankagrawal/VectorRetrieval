import sys
import pickle
'''class TrieNode:  
    def __init__(self): 
        self.children = [None]*26
        
        self.offset = None
        self.df = None  
        self.endtag = -1

class Trie:
    def __init__(self): 
		self.root = TrieNode()
    def insert(self,key,of,freq): 
        cur = self.root 
        length = len(key) 
        for level in range(length): 
            index = ord(key[level]) - ord('a')
            if not cur.children[index]: 
                cur.children[index] = TrieNode()
            cur = cur.children[index] 
        cur.offset = of
        cur.df = freq
        cur.isEnd = True


  
    def getWords(self, key):
    	res = {} 
        cur = self.root 
        length = len(key) 
        for lvl in range(length):
        	if(key.isalpha()):
        		index = ord(key[lvl]) - ord('a')
        		if cur.children[index]:
        			cur = cur.children[index]
        if(cur.isEnd):
        	res.add(key)
'''



dictfile = open(sys.argv[1]+".dict","rb")
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

