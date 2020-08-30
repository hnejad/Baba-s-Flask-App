import mysql.connector
from queries.query1 import getQuery1
from queries.query2 import getQuery2

query1 = getQuery1()
query2 = getQuery2()

queries = [query1, query2]

def getQueries():
    return queries