import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import qg as qg
import mysql.connector

def process(query):
	query=query.lower()
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
	print ("=======Answer for your question======")
	print ("\n")
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="root",
		database="vistapoint",
		port="1026"
	)
	mycursor = mydb.cursor()
	mycursor.execute(sqlQuery)
	myresult = mycursor.fetchall()
	for x in myresult:
		for col in x:
			print(col)
			print(' ')
	print ('\n')
while True:
	#1) count all active alarms
	#2) list all active alarms
	#3) list all alarms with type tunnel
	#4) count all logs related to orchestration tasks
	#5) count all the appliance with status normal
	#6) list all the appliance with status normal
	query = raw_input("Please enter your question: ")
	process(query)
