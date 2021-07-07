import csv
import MySQLdb

mydb = MySQLdb.connect(host = 'localhost', user='root', passwd='1234', db='mangoPeace')
cursor = mydb.cursor()

def csv_to_mysql():
    file = open("users/mangodata.csv", mode="r")
    print(file)
    csv.re

csv_to_mysql()