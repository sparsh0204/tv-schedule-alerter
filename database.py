import mysql.connector
import config

def createscheduledbconnection():
    ''' function to connect to imdb database and tvdata table which saves the schedule of previously searched tv shows '''
    mydb = mysql.connector.connect(host=config.DATABASE_HOST,user=config.DATABASE_USER,passwd=config.DATABASE_PASSWORD)
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("create database if not exists imdb;")
    mydb = mysql.connector.connect(host=config.DATABASE_HOST,user=config.DATABASE_USER,passwd=config.DATABASE_PASSWORD,database='imdb')
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("create table if not exists tvdata (title VARCHAR(200),detail VARCHAR(255),ddate VARCHAR(100),code INT);")
    return mycursor, mydb

def createuserdbconnection():
    ''' function to connect to userdata table and userinput table which consists of data input by users '''
    mydb = mysql.connector.connect(host=config.DATABASE_HOST,user=config.DATABASE_USER,passwd=config.DATABASE_PASSWORD)
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("create database if not exists userdata;")
    mydb = mysql.connector.connect(host=config.DATABASE_HOST,user=config.DATABASE_USER,passwd=config.DATABASE_PASSWORD,database='userdata')
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("create table if not exists userinput (email VARCHAR(200),tvseries MEDIUMTEXT);")
    return mycursor, mydb
