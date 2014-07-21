# -*- coding: UTF-8 –*-

import sys
import os



tag_dictionary = {}
category_list = []

dir = 'classes'

list_dirs = os.listdir(dir)

for files in list_dirs:
    category = files.split('.')[0]
    category_list.append(category)

tag_dictionary = dict.fromkeys(category_list)

for files in list_dirs:
    category = files.split('.')[0]
    tag_dictionary[category] = {}
    fp = open(dir + '/' + files , "r")
    for f in fp:
        tag_dictionary[category][f.strip().decode('utf-8')] = 1



