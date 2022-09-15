import sqlite3, os, json, requests, random, time
from datetime import timedelta, date
from flask_sqlalchemy import SQLAlchemy

list_files = ["keys.tr", "tera_search.db", "history.db", "proxy.txt"]

def Datetime_Now(datex_s):
	EndDate = date.today() + timedelta(days=datex_s)
	return int(EndDate.strftime('%Y%m%d'))


class cof:
	"""docstring for cof"""
	def __init__(self):
		super(cof, self).__init__()

	def check(self, folder):
		if os.path.isdir(folder):
			try:
				paths = "/".join(folder.split("\\"))
			except:
				paths = folder.replace("\\", "/")
			point  = 0
			for filename in list_files:
				file = "/".join([paths, filename])
				files, exts = os.path.splitext(filename)
				
				if os.path.isfile(file):
					print(filename, "is Ready!")
				else:
					if exts == "db":
						connection = sqlite3.connect(file)
						time.sleep(0.2)
						connection.close()
					else:
						with open(file, 'w') as files:#, buffering=0) as files:
							pass
		else:
			print(0)

class Database_Manage:
	"""docstring for Database_Manage"""
	def __init__(self, sqlite3, name:str):
		super(Database_Manage, self).__init__()
		self.sqlite3 = sqlite3
		if type(name) != str:
			try:
				if name.config['DATABASE']: name = name.config['DATABASE']
			except:
				name = name.config['DB']
		else:
			pass
		self.connect = self.sqlite3.connect(name)
		self.cursor = self.connect.cursor()

	def create_tabel(self, tabel_data:str):
		try:
			self.connect.execute(tabel_data)
		except:
			self.cursor.execute(tabel_data)
		self.close()

	def row(self, data:str, data2:str):
		try:
			self.cursor.execute(data)
		except:
			self.cursor.execute(data, data2)

		get_row = self.cursor.fetchall()
		return get_row, len(get_row)

	def limite_row(self, data:str, data2:str, lenght:int):
		try:
			self.cursor.execute(data)
		except:
			self.cursor.execute(data, data2)

		get_row = self.cursor.fetchmany(lenght)
		return get_row, len(get_row)

	def options(self, data:str, data2:str):
		try:
			execs = self.cursor.execute(data)
		except:
			execs = self.cursor.execute(data, data2)
		try:
			self.cursor.commit()
		except:
			pass
		if data.lower().find("delete") >= 0 or data.lower().find("update") >= 0:
			return execs.rowcount

	def close(self):
		try:
			self.connect.close()
		except:
			self.cursor.close()

#LOAD/READ FILE DATABASE
#database = Database_Manage(sqlite3, "tera_search.db")

#ADD DATA
#database.options("INSERT INTO Tera_Search(search_result, datetimes, keyword) VALUES( ?, ?, ?);", ('Bajingan', 'now', 'bajingan'))

#GET DATA FROM TABLE
#database.row("SELECT * FROM Tera_Search;", '')

#database.row("SELECT * FROM Tera_Search WHERE search_result LIKE '%Baji%'", '')
#database.limite_row("SELECT * FROM Tera_Search WHERE search_result LIKE '%Baji%'", '', 1)

#database.row("SELECT * FROM Tera_Search WHERE search_result=?", 'bajingan')
#database.limite_row("SELECT * FROM Tera_Search WHERE search_result=?", 'bajingan')


#UPDATE
#database.options("UPDATE Tera_Search SET search_result='Hello' WHERE search_result LIKE '%Baji%'", '')
#database.options("UPDATE Tera_Search SET search_result='Hello' WHERE search_result='Bajingan'", '')

#DELETE
#database.options("DELETE FROM Tera_Search WHERE search_result LIKE '%Baji%'", '')
#database.options("DELETE FROM Tera_Search WHERE search_result='Baji'", '')
		

cof = cof()