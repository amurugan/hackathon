import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import qg as qg

# Sample natural language query
query = "How many tunnels are there?"

tokens = nltk.word_tokenize(query)
tagged=nltk.pos_tag(tokens)
keywords=[]
numerals=[]
tags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'RB']
for i in tagged:
		if i[1] in tags:
			keywords.append(i[0])
		elif i[1] == 'CD':
			numerals.append(i[0])
sqlQuery = qg.queryGenerator(tagged,keywords,numerals,tokens)
print(sqlQuery)
