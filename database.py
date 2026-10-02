import mysql.connector

password=""
database = "python_public_service"
port=3306
def select(q):
	cnx = mysql.connector.connect(user="root", password=password, host="localhost", database=database,port=port)
	cur = cnx.cursor(dictionary=True)
	cur.execute(q)
	result = cur.fetchall()
	cur.close()
	cnx.close()
	return result
def update(q, values):
	cnx = mysql.connector.connect(user="root", password=password, host="localhost", database=database,port=port)
	cur = cnx.cursor(dictionary=True)
	cur.execute(q, values)
	cnx.commit()
	result = cur.rowcount
	cur.close()
	cnx.close()
	return result
def delete(q):
	cnx = mysql.connector.connect(user="root", password=password, host="localhost", database=database,port=port)
	cur = cnx.cursor(dictionary=True)
	cur.execute(q)
	cnx.commit()
	result = cur.rowcount
	cur.close()
	cnx.close()
def insert(q, values):
	cnx = mysql.connector.connect(user="root", password=password, host="localhost", database=database,port=port)
	cur = cnx.cursor(dictionary=True)
	cur.execute(q, values)
	cnx.commit()
	result = cur.lastrowid
	cur.close()
	cnx.close()
	return result