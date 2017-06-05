import sqlite3
import csv
import argparse
from random import shuffle

argparser = argparse.ArgumentParser(description='Import flashcards into database.')
argparser.add_argument('input_file', action="store", help='File to be imported')
argparser.add_argument('-user_id', action="store", dest="id", type=int, default=1)

args = argparser.parse_args()
sqlite_file = 'data-dev.sqlite'
import_file = args.input_file
user_id = args.id

file = open(import_file, 'r')

items =  list(csv.reader(file))
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

#get last collection and flashcard id
last_collection = 0
last_id = 0
for row in c.execute("SELECT rowid, * FROM flashcard ORDER BY id"):
	last_collection = row[6]
	last_id = row[0]

c.execute("INSERT INTO flashcardcollection VALUES('" + str(int(last_collection)+1) +"', 'Japanese', '1000-01-01 00:00:00', " + str(int(last_collection)+1) + ")")

indexes = range(len(items))

num_per_scheduler = int(round(len(items)/3))
schedulers = ([1]*num_per_scheduler) + ([2]*num_per_scheduler) + ([3]*(len(items)-(2*num_per_scheduler)))
shuffle(schedulers)

randomised = {}
for i in range(len(indexes)):
	randomised[i] = schedulers[i]
print randomised

for i in range(len(items)):
	index = i+last_id
	row = "'" + str(index+1) + "','" + str(items[i][1]) + "','<p>" + str(items[i][1]) + "</p>','" + str(items[i][0]) + "','<p>" + str(items[i][0]) + "</p>','" + str(int(last_collection)+1) + "', '', '', '', '', '','" + str(randomised[i]) + "'," 
	print row
	c.execute("INSERT INTO flashcard VALUES(" + row + ")")

conn.commit()
