from flask import *
from database import*


public=Blueprint('public',__name__)



@public.route('/')
def home():
	return render_template('indexs.html')

@public.route('/userregistration',methods=['post','get'])	
def userregistration():
	if "user" in request.form:
		f=request.form['fname']
		l=request.form['lname']
		p=request.form['place']
		ph=request.form['phone']
		e=request.form['email']
		
		u=request.form['uname']
		pw=request.form['pwd']
		
		q="select * from login where username='%s' or password='%s'"%(u,pw)
		res=select(q)
		if res:
			flash('already exist')

		else:
			q="insert into login values(null,'%s','%s','user')"%(u,pw)
			id=insert(q,None)
			q="insert into user values(null,'%s','%s','%s','%s','%s','%s')"%(id,f,l,p,ph,e)
			insert(q,None)
			flash('inserted successfully')
			return redirect(url_for('public.userregistration'))
		
	return render_template('userregistration.html')


@public.route('/newsagentreg',methods=['post','get'])	
def newsagentreg():
	if "agent" in request.form:
		f=request.form['fname']
		l=request.form['lname']
		p=request.form['place']
		ph=request.form['phone']
		e=request.form['email']
		
		u=request.form['uname']
		pw=request.form['pwd']
		
		q="select * from login where username='%s' or password='%s'"%(u,pw)
		res=select(q)
		if res:
			flash('already exist')

		else:
			q="insert into login values(null,'%s','%s','agent')"%(u,pw)
			id=insert(q,None)
			q="insert into agent values(null,'%s','%s','%s','%s','%s','%s')"%(id,f,l,p,ph,e)
			insert(q,None)
			flash('inserted successfully')
			return redirect(url_for('public.newsagentreg'))
		
	return render_template('newsagentreg.html')

@public.route('/login',methods=['post','get'])	
def login():
	if "login" in request.form:
		u=request.form['uname']
		pw=request.form['pwd']
		
		q="select * from login where username='%s' and password='%s'"%(u,pw)
		res=select(q)
		if res:
			session['login_id']=res[0]['login_id']
			lid=session['login_id']
			
			
			if res[0]['usertype']=="agent":
				q="select * from agent where login_id='%s'"%(lid)
				res=select(q)
				if res:
					session['agent_id']=res[0]['agent_id']
					# aid=session['agent_id']
				return redirect(url_for('agent.agent_home'))

			elif res[0]['usertype']=="user":
				q="select * from user where login_id='%s'"%(lid)
				res=select(q)
				if res:
					session['user_id']=res[0]['user_id']
					# uid=session['user_id']
					
				return redirect(url_for('user.user_home'))

		else:
			flash('invalid username and password')

	return render_template('login.html')	
