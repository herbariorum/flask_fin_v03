import json
import sqlite3

connection = sqlite3.connect('finance.db')
cursor = connection.cursor()
cursor.execute('Create Table if not exists cidades (id Text, cidade TEXT)')
traffic = json.load(open('json_cidades/TO.json'))
columns = ['id', 'cidade']
for row in traffic:
	keys = tuple(row[c] for c in columns)
	cursor.execute('insert into cidades values(? , ?)', keys)
	# print(f'{row["cidade"]} data inserted Succefully')
connection.commit()
connection.close()
