import MySQLdb as mysql  
from config import * 


dbCon = mysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
dbCursor = dbCon.cursor()

