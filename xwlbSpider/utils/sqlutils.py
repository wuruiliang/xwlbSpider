import pymysql

mysql_host = '127.0.0.1'
mysql_port = 3306
mysql_user = 'root'
mysql_password = ''
mysql_db = 'xwlb'

def open_connection():
    return pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        passwd=mysql_password,
        db=mysql_db,
        charset='utf8')

def close_connection(connection):
    connection.close()