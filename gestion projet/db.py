import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_projet",
        cursorclass=pymysql.cursors.DictCursor
    )
