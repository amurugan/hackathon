import nltk
# --------------------------------------------------------------------
# Enable Below code to download nltk moduesl and commet back again
# --------------------------------------------------------------------
# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# --------------------------------------------------------------------

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import qg as qg
import mysql.connector
from OpenSSL import SSL
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def process(query):
    query = query.lower()
    tokens = nltk.word_tokenize(query)
    tagged = nltk.pos_tag(tokens)
    keywords = []
    numerals = []
    tags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'RB']
    for i in tagged:
        if i[1] in tags:
            keywords.append(i[0])
        elif i[1] == 'CD':
            numerals.append(i[0])
    sqlQuery = qg.queryGenerator(tagged, keywords, numerals, tokens)
    print("=======Answer for your question======")
    print("\n")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="vistapoint_99_99_99",  # vistapoint
        port="1026"
    )
    mycursor = mydb.cursor()
    mycursor.execute(sqlQuery)
    myresult = mycursor.fetchall()
    return myresult


@app.route('/generatedata', methods=['POST'])
# @cross_origin(origins=['localhost'])
def handle_post():
    if request.method == 'POST':
        query = request.form['query']
        return process(query)


@app.route('/test')
# @cross_origin(origins=['localhost'])
def handle_get():
    return "test"

@app.route('/nlp_query', methods=['POST'])
# @cross_origin(origins=['localhost'])
def handel_nlp_query():
	if request.method == 'POST':
		query = request.form['query']
		return process(query)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5858, ssl_context='adhoc')
