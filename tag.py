# -*- coding: UTF-8 –*-

from progress import *
from dbInterface import *
import sys
import re
import operator

reload(sys)
sys.setdefaultencoding('utf8')


tag_set = {}

p = re.compile(u'[0-9a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\x80-\xff]+')
size = len(table_tag.data)

for idx, row in enumerate(table_tag.data):
    tag = row['name']

    progress_refresh(idx, size)
    m = p.findall(tag)
    if m != None:
        for x in m:
            tag = x.lower().strip()
            tag = tag.encode('utf-8')
            if len(tag) < 2:
                continue
            if tag_set.has_key(tag):
                tag_set[tag] = tag_set[tag] + 1
            else:
                tag_set[tag] = 1

tag_set = sorted(tag_set.iteritems(), key=operator.itemgetter(1) , reverse = True)
sys.stdout = open("tagset.txt" , "w")

for tag in tag_set:
    print tag[0]