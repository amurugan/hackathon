from nltk.corpus import stopwords

relationList={
	#key		value
	'alarm' : 'appliancealarm',
	'alarms' : 'appliancealarm',
	'log' : 'actionlog',
	'appliance' : 'neconfig2'
}

attributeList={
	#Table=Alarm
	#key			value
	'id':			['appliancealarm.id'],
	'type':		['appliancealarm.type'],
	#Table=logs
	'id':			['actionlog.ID'],
    'tasks' : ['actionlog.name'],
	#neconfig
	'status' : ['neconfig2.config_data']
}

tableAttributeList={
	#attribute		relation
	'appliancealarm.id':	'appliancealarm',
	'appliancealarm.type':	'appliancealarm',
	'actionlog.ID' : 'actionlog',
	'actionlog.name' : 'actionlog',
	"neconfig2.config_data" : 'neconfig2'
}

aggregateFunction = {
	'many' : 'count',
	'count' : 'count'
}

primaryKey = {
	'tunnel' : 'tunnel.id',
	'alarm' : 'alarm.id'
}

alaramTypes = {
	"tunnel" : 'TUN' 
}


def queryGenerator(tagged,keywords,numerals,query):
	table = []
	attribute = []
	special = []
	
	#Create table[] , attribute[], special[]
	for word in tagged:
		if word[0] in relationList:
			table.append(relationList[word[0]])
		elif word[0] in attributeList:
			for temp in attributeList[word[0]]:
				attribute.append(temp)
		elif word[0] not in numerals:
			special.append(word[0])
	for attr in attribute:
		if tableAttributeList[attr] not in table:
			table.append(tableAttributeList[attr])
	table = list(set(table))
	#if no attribute is found, all attibutes to be selected	
	if(len(attribute)==0):
		attribute.append('*')
	else:
		attribute = list(set(attribute))
		
	#print(table)
	#print(attribute)
	#print(special)
	
	
	#join condition if >1 tables
	joinCond = ''
	
	#if(len(table)>1):
	#	joinCond = primaryKey[table[0]]+'='+primaryKey[table[1]]
	
	boolean = ['or','and']
	booleanDict = {}
	
	#Numeral processing and relational operation
	relOpn={'greater than' : '>', 'less than': '<' , 'more than' : '>'}
	numAttrList={}
	numOp={}
	for num in numerals:
		#relational operation for each numeral
		numIndex=query.index(num)
		if (numIndex+1)<len(query) and query[numIndex+1] in boolean:
			booleanDict[num] = query[numIndex+1]
		temp = ' '.join([query[numIndex-2], query[numIndex-1]]).lower()
		temp.strip(' ')
		if temp in relOpn:
			numOp[num]=relOpn[temp]
		else:
			numOp[num]='='
		
		#attribute for each numeral
		for i in range(1,5):
			identified=False
			if numIndex-i>-1 :
				if query[numIndex-i] in attributeList:
					print(query[numIndex-i])
					numAttrList[num]=attributeList[query[numIndex-i]]
					identified=True
			if identified==True:
				break		
	#print('relational operation for each numeral')
	#print(numOp)
	#print('num attribute list')
	#print(numAttrList)
	
	#mysql code for numerical condition
	numCond=[]
	for item in numAttrList:
		temp=numAttrList[item][0]+numOp[item]+item
		if item in booleanDict:
			temp = temp + ' ' + booleanDict[item]
		numCond.append(temp)
	#print('Numeral conditions')
	#print(numCond)
	
	stopw = ['need','i', 'many','with', 'fetch','give','all','find','related', 'display','greater','less','more','than','list', 'show','select', 'out', 'number','select',',','get','retrieve','print','tell','having','whose','details'] + stopwords.words('english')
	stopw.remove('up')
	stopw.remove('down')
	#condition list for non numeric attributes
	condList = {}
	for item in special:
		if item not in stopw:
			itemIndex = query.index(item)
			if (itemIndex+1)<len(query) and query[itemIndex+1] in boolean:
				booleanDict[item] = query[itemIndex+1]		
			identified = False
			for i in range(1,3):	
				if(itemIndex-i>=0):
					if query[itemIndex-i] in attributeList:
						if item not in condList:
							condList[item] = attributeList[query[itemIndex-i]]
				if(itemIndex+i<len(query)):
					if query[itemIndex+i] in attributeList:
						if item not in condList:
							condList[item] = attributeList[query[itemIndex+i]]
	
	#print('Condition list')
	#print(condList)
	
	#where clause involving 'and' and 'or' with numeral and string attributes
	whereClause = []
	operation = ' ';
	for item in condList:
		temp = ''
		if(len(condList[item])>1):
			temp += ' ( '
			for attr in condList[item]:
				temp = temp+attr+'="'+item+'" or '
			temp = temp[:len(temp)-3]
			temp += ' ) '
			if item in booleanDict:
				temp = temp + ' ' + booleanDict[item]
			whereClause.append(temp)
			
		else:
			if condList[item][0] == 'appliancealarm.type' :
				temp = condList[item][0]+'="'+alaramTypes[item]+'"'
			else:
				temp = condList[item][0]+'="'+item+'"'
			if item in booleanDict:
				temp = temp + ' ' + booleanDict[item]
			if condList[item][0] == 'appliancealarm.type' :
				whereClause.append(condList[item][0]+'="'+alaramTypes[item]+'"')
			else:
				whereClause.append(condList[item][0]+' like "%'+item+'%"')
			
	try :
		if 'and' in query:
			operation = ' and '
		if 'or' in query:
			operation = ' or '
	except ValueError :
		operation = ''
	#print('Where Clause List ')
	#print(whereClause)
	
	selectAll = ['all', 'details','records','record','detail']
	for word in selectAll:
		if word in query:
			if 'appliancealarm' in table:
				attribute = ['DESCRIPTION']
			elif 'neconfig2' in table:
				attribute = ["json_extract(config_data, '$.hostName') as hostname"]
			else:
				attribute = ['*']

	for word in aggregateFunction:
		if word in query:	
			attribute = [aggregateFunction[word] + '(*)']
	
	execQuery='SELECT '
	
	#inserting attributes
	for index in range(0,len(attribute)-1):
		execQuery+=attribute[index]+', '
	execQuery+=attribute[len(attribute)-1]
	execQuery+=' FROM '
	
	#inserting tables
	for index in range(0,len(table)-1):
		execQuery+=table[index]+', '
	execQuery+=table[len(table)-1]
	
	if(len(joinCond)>0 or len(whereClause)>0):
		execQuery+=' WHERE '
	
	if len(joinCond)>0:
		execQuery+=joinCond + ' and '
		
	execQuery+= operation.join(whereClause) 
	if len(numCond)>0:
		execQuery+=joinCond + ' and '
	execQuery+= operation.join(numCond) 

	if 'neconfig2' in table:
		execQuery+= ' and ' + " resource_base like '%systemInfo%'"
	execQuery+=';'
	#print('Final Query')
	#print(execQuery)
	return execQuery
