import csv
import json
import sqlite3

connection = sqlite3.connect('finance.db')
cursor = connection.cursor()
# cursor.execute('Create Table if not exists cidades_tables (id Integer primary key AUTOINCREMENT, uf TEXT, nome TEXT)')
traffic = open('json_cidades/cidades.csv')
rows = csv.reader(traffic)
cursor.executemany("INSERT INTO cidades_tables VALUES(null, ?,?)", rows)
connection.commit()
connection.close()