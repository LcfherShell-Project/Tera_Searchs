import os, sys, re, logging, requests, time , requests, asyncio, psutil
from datetime import datetime, timedelta, date
from random import randint
try:
    from Tera_Search.config.config import Datetime_Now
    from Tera_Search.libraries.url2S import Duck2Engine as engineer
    from Tera_Search.libraries.proxys import google_proxy, https_proxy, http_proxy, random
    from Tera_Search.libraries.security import ScanHeaders, AESCipher
    from Tera_Search.libraries.malware_scanning import Malware_Scann
except:
    from config.config import Datetime_Now
    from libraries.url2S import Duck2Engine as engineer
    from libraries.proxys import google_proxy, https_proxy, http_proxy, random
    from libraries.security import ScanHeaders, AESCipher
    from libraries.malware_scanning import Malware_Scann

import logging

from flask import Flask, redirect, url_for, render_template, session, request, jsonify, json, flash, abort, send_file, make_response, current_app, g
from flask_mail import Mail, Message

from sqlalchemy import Column, create_engine, MetaData, Table, text
from sqlalchemy.types import String, DateTime, Integer, Text
from sqlalchemy import Table, Column, create_engine, select, insert, update, delete, join
from datetime import datetime, timedelta, date

try:
	# python2
	from urlparse import urlparse
except:
    # python3
    from urllib.parse import urlparse

#tera_search table "id num"
_home_path_ , filename = os.path.split(os.path.abspath(__file__).replace("\\", "/"))
scann = Malware_Scann(_home_path_)

async def scanner_tools(paths):
    await asyncio.sleep(0)
    return scann.main(paths.replace("\\", "/"))

create_files = ''
def set_proxy(procotol, ip, port):
    dirs = _home_path_
    files = dirs.replace("\\", "/")+"/data.json"
    with open(files, "r+") as jsonFile:
        data = json.load(jsonFile)
        data["proxy"][0] = procotol+"://"+ip+":"+str(port)
        #proxies = {self.schema: f'{self.schema}://{proxy_address}'}
        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile)
        jsonFile.truncate()

def read_proxy(lens):
    dirs = _home_path_
    files = dirs.replace("\\", "/")+"/data.json"
    with open(files, "r+") as jsonFile:
        data = json.load(jsonFile)
        data = data["proxy"][lens]
    return data


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False



point_index = 0


aescipser = AESCipher("Tera_Search")

key_ = os.urandom(58)

####Enginer

engine = engineer()


###DISABLE LOGGING
log = logging.getLogger('werkzeug')
log.disabled = True
app = Flask(__name__)
app.config.update(dict( 
    SECRET_KEY = key_,
    SECURITY_PASSWORD_SALT = os.urandom(128),
    PERMANENT_SESSION_LIFETIME = timedelta(days=2),
    SEND_FILE_MAX_AGE_DEFAULT=43200,
    DATABASE_ENG = f"{_home_path_}/tera_search.db",
    MAIL_SERVER='smtp.office365.com',
    MAIL_PORT=587,
    MAIL_USE_TLS =True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME = 'ramstungga@outlook.co.id',
    MAIL_PASSWORD = "indonesia2393",
    Flask_Engine = engine #,
    #Flask_MalwareScan= asyncio.run(scanner_tools(_home_path_))
    ))



mail = Mail(app)
database = create_engine(f"sqlite+pysqlite:///{app.config['DATABASE_ENG']}", future=True, echo=False)


metadata = MetaData()
Tera_Search = Table('Tera_Search', metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('keyword', Text(), unique=False),
                 Column('search_result', Text(), unique=False),
                 Column('datetimes', Integer())
)

Keyword = Table('Keyword', metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('keyword', Text(), unique=False))

Tera_History = Table('Tera_History', metadata, 
                 Column('id', Integer(), primary_key=True), 
                 Column('history_url', Text()),
                 Column('datetimes', Integer())
                 )

def loads(data):
	#q=dongeng&u=default&r=default&t=None&x=120
	#searchs, user_agent='default', region=None,time=None, max_results=600

	penth = []

	for x in data.keys():
		if x == 'q' or x == 'search':
			penth.append(data[x])

		if x == 'u' or x == 'user':
			penth.append(data[x])

		if x == 'r' or x == "region":
			if data[x] == "None": 
				penth.append('us')
			else:
				penth.append(data[x])

		if x == "t" or x == "tout":
			if data[x] == "None": 
				penth.append(None)
			else:
				penth.append(int(data[x]))

		if x == "x" or x == "ximum":
			penth.append(int(data[x]))


	return penth


print("---------Scan Cache History--------")
try:
    stmt = select(Tera_Search)
    with database.connect() as conn:
        result_db = conn.execute(stmt)
        result_db = result_db.all()

    result_files_db = [files_json[2] for files_json in result_db]
    file_cache_dir = next(os.walk(f'{_home_path_}/history'), (None, None, []))[2]
    cache_row = 0
    for file in file_cache_dir:
        if f'{_home_path_}/history/{file}' in result_files_db:
            cache_row += 1
        else:
            try:
                os.remove(f'{_home_path_}/history/{file}')
            except:
                os.unlink(f'{_home_path_}/history/{file}')
        time.sleep(0.2)
    print(f"Total Cache: {cache_row}")
    if cache_row == 0:
        with database.connect() as conn:
            conn.execute(text("DELETE FROM Tera_Search"))
            conn.commit()

    print("---------------Finish--------------")
except:
	file_cache_dir = next(os.walk(f'{_home_path_}/history'), (None, None, []))[2]
	for file in file_cache_dir:
		try:
			os.remove(f'{_home_path_}/history/{file}')
		except:
			os.unlink(f'{_home_path_}/history/{file}')
		time.sleep(0.2)
	with database.connect() as conn:
		conn.execute(text("DELETE FROM Tera_Search"))
		conn.commit()
	with database.connect() as connt:
		connt.execute(text("DELETE FROM Keyword"))
		connt.commit()

@app.before_request
def before_request():
   g.request_start_time = time.time()
   g.request_time = lambda: "%.5f" % (time.time() - g.request_start_time)

@app.route('/v1/<token>/openurls', methods=['GET', 'POST'])
def openurls(token=None):
    if token == None:
        return "Failed Token"

    data = request.args.to_dict()
    urls = data['urls']
    try:
        target = ScanHeaders(urls)
        response = make_response(render_template('security.html', urls=urls, sessions=target.score, popup=target.scan_WindowPop() ))
        response.status_code = 200
    except:
        response = make_response(render_template('404.html', sessions=urls))
        response.status_code = 404
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; www.duckduck.com'
    #response.headers['Content-Security-Policy'] = 'policy'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/v1/proxy', methods=['GET', 'POST'])
def proxy():
    data = request.args.to_dict()
    https = https_proxy()
    http = http_proxy()
    data_json = {"https":https, "http":http}
    data_json = data_json

    try:
        if data['p']:
            return read_proxy(int(data['p']))
    except:
        if data['procotol'] and data['len']:
            xxx = data_json[data['procotol']][int(data['len'])]
            data_json = {data['procotol']: f"{data['procotol']}://{xxx['ip']}:{xxx['port']}"}
            return jsonify(data_json)


@app.route('/v1/get', methods=['GET', 'POST'])
def search_get():
    get_post = request.args.to_dict()
    proxies_data = r"{}".format(get_post['proxies'].replace("'", "\""))
    my_dict = json.loads(proxies_data)
    #print(my_dict['keys'])
    return ''

#q=dongeng&u=default&r=default&t=None&x=120
@app.route('/v1/post', methods=['GET', 'POST'])
def search_post():
    global create_files

    get_post = request.args.to_dict()

    data = loads(get_post)
    engine.region(data[2])

    datenow = date.today().strftime('%Y%m%d')

    keyword_ = f'{str(data[0])}'
    try:
        try:
            proxies_data = r"{}".format(get_post['proxies'].replace("'", "\""))
            my_dict = json.loads(proxies_data)
            urls = str(request.host_url)+f"v1/proxy?procotol={my_dict['keys']}&len={randint(0, 10)}"
            r = requests.get(urls)
            proxies = r.json()
        except:
            proxies_data = r"{}"
            proxies = json.loads(proxies_data)

        engine.searchs(data[0], user_agent=data[1], time=data[3], max_results=data[4], proxy=proxies)
        query = engine.result().json()

        

        ##JOIN
        j = Tera_Search.join(Keyword,
                        Tera_Search.c.keyword == Keyword.c.keyword)
        
        stmt = select(Tera_Search).select_from(j).order_by(Tera_Search.c.keyword, Tera_Search.c.search_result).where(Tera_Search.c.keyword.contains(keyword_) )
        resultx = []
        with database.connect() as conn:
            resultx = conn.execute(stmt).all()
        conn.close()

        #insert_data = str(json.dumps(query))
        create_files = f"{_home_path_}/history/{ ''.join(re.findall('[a-zA-Z]+', aescipser.encrypt(data[0]).decode('UTF-8') ))  }__{date.today().strftime('%Y%m%d')}.json"
        if len(resultx) != 0:

            #stmt = update(Tera_Search).values(search_result=f"{create_files}").where(Tera_Search.c.keyword.contains(keyword_))
            stmt = select(Tera_Search).where(Tera_Search.c.keyword.contains(keyword_))
            with database.connect() as connt:
                resultx = connt.execute(stmt)
                resultx = resultx.all()

            with open(resultx[0][2], 'w') as f:
                json.dump(query, f, indent=2)
            connt.close()

        else:
            stmt = select(Tera_Search).where(Tera_Search.c.keyword.contains(keyword_))
            with database.connect() as connt:
                resultx = connt.execute(stmt)
                resultx = resultx.all()
            data_query = [x[1] for x in resultx]
            if keyword_ in data_query:
                pass
            else:
                stmt = insert(Keyword).values(keyword=f'{data[0]}')
                with database.connect() as connt:
                    connt.execute(stmt)
                    connt.commit()

            stmt = insert(Tera_Search).values( keyword=keyword_, search_result=create_files, datetimes=Datetime_Now(1) )
            with database.connect() as conn:
                conn.execute(stmt)
                conn.commit()

            with open(create_files, 'w') as f:
                json.dump(query, f, indent=2)

        
    except:
        try:
            resultx = []
            query = ''

            stmt = select(Tera_Search).where(Tera_Search.c.keyword.contains(keyword_))
            with database.connect() as connt:
                resultx = connt.execute(stmt)
                resultx = resultx.all()
            connt.close()
            filenames = resultx[0][2]
            if os.path.isfile(filenames):
                with open(filenames) as f:
                    query = json.load(f)


        except:
            query = {'result': [{'title': "<h3>ERROR 408 REQUEST TIMEOUT</h3>", 'href':'', 'body': 'Your browser did\'t send a complete request in time'}]}


    response = make_response(jsonify(query))
    response.headers['X-Ratelimit-Limit'] = 700
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Max-Age'] = 43200
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, x-requested-with")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST")
    response.status_code = 200
    return response

#########################################
@app.route('/', methods=['GET', 'POST'])
@app.route('/<data>', methods=['GET', 'POST'])
def index(data=None):
    global point_index, create_files
    result = []
    if point_index == 0:

        result_db = []
        datenow = date.today().strftime('%Y%m%d')
        stmt = select(Tera_Search).where(Tera_Search.c.datetimes < int(datenow) )
        with database.connect() as conn:
            result_db = conn.execute(stmt)
            result_db = result_db.all()

        if len(result_db) != 0:
            stmt = delete(Tera_Search).where(Tera_Search.c.datetimes < int(datenow) )
            with database.connect() as conn:
                conn.execute(stmt)
            for delete_JSONfile in result_db:
                if os.path.exists(delete_JSONfile[2]):
                    os.remove(delete_JSONfile[2])
    #


    point_index +=1

    response = make_response(render_template('index.html', sessions=None))
    response.status_code = 200

    #response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'

    response.headers['Strict-Transport-Security'] = 'max-age=31536000; www.duckduck.com'
    
    #response.headers['Content-Security-Policy'] = 'policy'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers.add("Access-Control-Allow-Origin", "*")
    #response.set_cookie('userID', sessions)
    return response

@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/<data>', methods=['GET', 'POST'])
def dashboard(data=None):
    response = make_response(render_template('index.html', sessions=None))
    response.status_code = 200

    #response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'

    response.headers['Strict-Transport-Security'] = 'max-age=31536000; www.duckduck.com'
    
    #response.headers['Content-Security-Policy'] = 'policy'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers.add("Access-Control-Allow-Origin", "*")
    #response.set_cookie('userID', sessions)
    return response



#id 
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







if __name__ == '__main__':
    try:
        app.run(debug=True)
    except:
        print("App Status: Exit")