from flask import *
from database import*

import random 



agent=Blueprint('agent',__name__)

@agent.route('/agent_home')
def agent_home():
	return render_template('agent_home.html')


# @agent.route('/get_text', methods=['POST'])
# def get_text(): 
#     out = None  # Initialize out to None

#     if 'sub' in request.form:   
#         malayalam_text = request.form['malayalam_text']
#         out = checknews(malayalam_text)
#         print(out)
    
#     return render_template('get_malayalam.html', out=out)  # Pass out to the template

 
# @agent.route('/get_malayalam_text', methods=['POST'])
# def get_malayalam_text():
#     malayalam_text = request.json
#     # Perform your news checking logic here (replace this with your actual logic)
#     out = checknews(malayalam_text['title'] + ' ' + malayalam_text['details'])

#     # Return the result as JSON
#     return jsonify({'message': out})


@agent.route('/agentnewsadd',methods=['get','post'])
def agentnewsadd():
    	
	data={}
	aid=session['agent_id']
	if 'submit' in request.form:
		tit=request.form['title']
		details=request.form['details']
		category = request.form['category']
		
		print(tit)
		print(details)
		
		
		q = "INSERT INTO `news` VALUES (NULL, %s, %s, %s,CURDATE(),%s)"
		values = (aid, tit,details,category)
		insert(q, values)


	if 'action' in request.args:
		action=request.args['action']
		news_id=request.args['nid']
	
	else:
		action=None

	if action=='delete':
		q="delete from news where news_id='%s'"%(news_id)
		delete(q)
		return redirect(url_for('agent.agentnewsadd'))

	if action=='update':
		q="SELECT * from news WHERE news_id='%s'"%(news_id)
		res=select(q)
		data['upd']=res

	if 'update' in request.form:
		tit=request.form['title']
		details=request.form['details']
		category = request.form['category']
		# q="UPDATE `news` SET `title` ='%s' ,`details`='%s' WHERE `news_id`='%s'"%(tit,details,news_id)
		# update(q)

		q = "UPDATE `news` SET `title` = %s, `details` = %s,`category` = %s WHERE `news_id` = %s"
		values = (tit, details, category, news_id)
		update(q, values)

		return redirect(url_for('agent.agentnewsadd'))

	q="SELECT * FROM news WHERE  `agent_id`='%s' ORDER BY `news_id` DESC"%(aid)
	data['view']=select(q)

	return render_template('agentnewsadd.html',data=data)
