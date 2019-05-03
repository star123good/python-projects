import json
import csv
import re
import gc
from textblob import TextBlob
import os
import psutil
import time
import random
import string
from random_word import RandomWords
import mysql.connector
r = RandomWords()
list1 = r.get_random_words()

random_strings = []
random_strings_two = []

mydb = mysql.connector.connect(
  host="206.189.43.198",
  user="supauser",
  passwd="BoomBo3!",
  database="MODEL",
  autocommit=True
)

mycursor = mydb.cursor(buffered=True)

'''1000 random strings to be generated in two arrays as this will be the processed data to be used in main function.
Template of real data, there is no need to optimise this.'''
for i in list1:
    random_strings.append(i)

for m in range(1000):
    random_strings.append(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)))

for n in range(1000):
    random_strings_two.append(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)))

def test_function(x):
    return "MODEL OUTPUT"

random_strings = list(set(random_strings))
'''Assume there are 20,000 rows in a csv file, represented by the "variable" below.'''
# for n in range(20000):
def process_one(n):
    '''with open('input.csv', mode='r') as employee_file:'''
    '''assume each row read from csv'''
    '''each row consists of a string and two integers'''
    variable = [random_strings[m], random.randint(0, 100), random.randint(0, 100)]
    # print(variable)
    memory = []

    blob = TextBlob(variable[0])
    plurals = [word.pluralize() for word in blob.words]
    plurals = " ".join(plurals)
    plurals = plurals.upper()

    memory.append(plurals)

    blob = TextBlob(variable[0])
    plurals = [word.singularize() for word in blob.words]
    plurals = " ".join(plurals)
    plurals = plurals.upper()

    memory.append(plurals)

    blob = TextBlob(variable[0])
    plurals = [word.lemmatize() for word in blob.words]
    plurals = " ".join(plurals)
    plurals = plurals.upper()

    memory.append(plurals)

    memory = list(set(memory))


    for r in memory:
        for s in random_strings:
            model = []
            for t in random_strings_two:
                string_to_write = r + " " + s + " " + t
                model.append(string_to_write)
            
            final_result = test_function(model)
            '''assume final_result will write to a csv file'''

    return n