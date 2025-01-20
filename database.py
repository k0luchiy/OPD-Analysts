import mysql.connector
import configparser
import datetime

class DB():
    def __init__(self):
        self.connection = None
        config = configparser.ConfigParser()
        config.read("./database_config.ini")
        database_config = config["ONLINEDB"]

        self.connection = mysql.connector.connect(**database_config)
        #self.connection = mysql.connector.connect(host="127.0.0.1", user="root", password="31415926", port=80, database="OPD_Analysts")
        
    def query(self, sql, args):
        cursor = self.connection.cursor()
        cursor.execute(sql, args)
        return cursor

    def insert(self,sql,args):
        cursor = self.query(sql, args)
        id = cursor.lastrowid
        self.connection.commit()
        cursor.close()
        return id

    def insertmany(self,sql,args):
        cursor = self.connection.cursor()
        cursor.executemany(sql, args)
        rowcount = cursor.rowcount
        self.connection.commit()
        cursor.close()
        return rowcount

    def update(self,sql,args):
        cursor = self.query(sql, args)
        rowcount = cursor.rowcount
        self.connection.commit()
        cursor.close()
        return rowcount

    def fetch(self, sql, args):
        rows = []
        cursor = self.query(sql, args)
        if cursor.with_rows:
            rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetchone(self, sql, args):
        row = None
        cursor = self.query(sql, args)
        if cursor.with_rows:
            row = cursor.fetchone()
        cursor.close()
        return row

    def __del__(self):
        if self.connection != None:
            self.connection.close()

    def create_user(self, userId, username):
        creationTime = datetime.datetime.now()
        query = "Insert into Users(UserId, Username, createdAt) values(%s, %s, %s);"
        return self.insert(query, (userId, username, creationTime))

    def insert_response(self, userId, prompt, response):
        creationTime = datetime.datetime.now()
        query = "Insert into AiResponse(UserId, userPrompt, Response, createdAt) values(%s, %s, %s, %s);"
        return self.insert(query, (userId, prompt, response, creationTime))
    
    def insert_rating(self, userId, responseId, rating, review):
        query = "Insert into Reviews(UserId, AiResponseId, Rating, Review) values(%s, %s, %s, %s);"
        return self.insert(query, (userId, responseId, rating, review))
    