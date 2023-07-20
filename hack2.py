import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import qg as qg
import mysql.connector
from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)


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
	print "=======Answer for your question======",
	print "\n",
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
	return myresult
	for x in myresult:
		for col in x:
			print(col)
			print(' ')
	print ('\n')

@app.route('/generatedata', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        query = request.form['query']
        return process(query)

@app.route('/test')
def handle_get():
    return "test"

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=5858)
