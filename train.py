# -*- coding: UTF-8 –*-

import sys
import re
from decimal import *
from dbInterface import *
from progress import *
from tagdict import tag_dictionary
from tagdict import category_list

getcontext().prec = 5

'''
To split word brute-forcely:
Example: 流行歌曲 -> {流行,流行歌,流行歌曲,行歌,行歌曲,歌曲}
'''


def update_progress(progress):
    print '\r[{0}] {1}%'.format('#' * (progress / 10), progress)


def splitWord(w):
    wList = []
    l = len(w)
    for i in range(l - 1):
        j = i + 1
        while j < l:
            temp = w[i:j + 1]
            wList.append(temp)
            j += 1
    return wList


current_val = 0
total_val = len(table_album.data)

for row in table_album.data:
    break
    aid = row['aid']
    tag_result = table_album_tag.find_all_by_col('aid', aid)
    current_val += 1
    progress_refresh('updating tag vectors', current_val, total_val)
    tid_list = []
    tag_list = []

    for tag_row in tag_result:
        tid_list.append(tag_row['tid'])

    for tid in tid_list:
        tag = table_tag.find_one_by_col('tid', tid)
        tag_list.append((tid, tag['name']))

    vector_album = dict.fromkeys(category_list, Decimal('0'))

    for tag_pair in tag_list:

        vec = dict.fromkeys(category_list, Decimal('0'))
        tid = tag_pair[0]
        tag = tag_pair[1].lower().strip()
        pc = re.compile(u'[\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\x80-\xff]+')
        pe = re.compile(u'[a-zA-Z0-9]+')
        m = pc.findall(tag)
        rest = ''.join(pe.findall(tag))
        tag = ''.join(m).strip()
        sList = splitWord(tag)
        sList.append(rest)

        if sList is not None:
            for s in sList:
                for cat in category_list:
                    if s in tag_dictionary[cat]:
                        vec[cat] += Decimal(1)
        vector_album = {key: vector_album[key] + vec[key] for key in category_list}
    if len(tag_list) > 0:
        vector_album = {key: vector_album[key] / len(tag_list) for key in category_list}

    for idx, tid in enumerate(tid_list):

        row_tag_vector = table_tag_vector.find(tid, category_list)

        tag = tag_list[idx][1]

        m = pc.findall(tag)
        rest = ''.join(pe.findall(tag))
        tag = ''.join(m).strip()
        sList = splitWord(tag)
        sList.append(rest)
        selfVec = dict.fromkeys(category_list, Decimal('0'))
        if sList is not None:
            for s in sList:
                for cat in category_list:
                    if s in tag_dictionary[cat]:
                        selfVec[cat] += Decimal(1.5)

        vec = {key: Decimal('0.00000') for key in category_list} if row_tag_vector is None else {
            key: Decimal(row_tag_vector[key]) for key in category_list}

        vec = {key: vector_album[key] + vec[key] + selfVec[key] for key in category_list}

        maxv = max(vec.values())
        minv = min(vec.values())

        if maxv - minv > 0:
            vec = {key: Decimal(1000.0) * (vec[key] - minv) / (maxv - minv) for key in category_list}

        tag_vector_row = dict(zip(table_tag_vector.columns,
                                  [int(tid) if i == table_tag_vector.pk else "{:.5f}".format(Decimal(vec[i])) for i
                                   in table_tag_vector.columns]))

        if table_tag_vector.find(tid) is None:
            table_tag_vector.insert(tag_vector_row)
        else:
            table_tag_vector.update(tag_vector_row)
print ''
current_val = 0
for row in table_album.data:
    aid = row['aid']
    tag_result = table_album_tag.find_all_by_col('aid', aid)
    vector_album = dict.fromkeys(category_list, Decimal('0'))
    break
    current_val += 1
    progress_refresh('updating album vectors', current_val, total_val)
    for tag in tag_result:
        tid = tag['tid']
        row_tag_vector = table_tag_vector.find(tid)
        vec = {key: Decimal('0.00000') for key in category_list} if row_tag_vector is None else {
            key: Decimal(row_tag_vector[key]) for key in category_list}
        vector_album = {key: vector_album[key] + vec[key] for key in category_list}

    maxv = max(vector_album.values())
    minv = min(vector_album.values())

    if maxv - minv > 0:
        vector_album = {key: Decimal(1000.0) * (vector_album[key] - minv) / (maxv - minv) for key in category_list}

    album_vector_row = dict(zip(table_album_vector.columns,
                                [int(aid) if i == table_album_vector.pk else "{:.5f}".format(Decimal(vector_album[i])) for i
                                 in table_album_vector.columns]))
    if table_album_vector.find(aid) is None:
        table_album_vector.insert(album_vector_row)
    else:
        table_album_vector.update(album_vector_row)
print ''
current_val = 0
total_val = len(table_person.data)
for row in table_person.data:

    pid = row['pid']
    dbCursor.execute("SELECT DISTINCT " + ','.join(
            ['AV.' + col  for col in table_album_vector.columns]) + " FROM `mydb_album_vector` AV INNER JOIN `mydb_track_person` AP ON AP.aid = AV.aid WHERE AP.pid = " + str(pid))
    album_result = dbCursor.fetchall()
    current_val += 1
    progress_refresh('updating person vectors', current_val, total_val)

    vector_person = dict.fromkeys(category_list, Decimal('0'))

    for album_vector in album_result:

        album_vector = dict(zip(table_album_vector.columns, album_vector))
        vec = {key: Decimal(album_vector[key]) for key in category_list}
        vector_person = {key: vector_person[key] + vec[key] for key in category_list}

    maxv = max(vector_person.values())
    minv = min(vector_person.values())

    if maxv - minv > 0:
        vector_person = {key: Decimal(1000.0) * (vector_person[key] - minv) / (maxv - minv) for key in category_list}

    person_vector_row = dict(zip(table_person_vector.columns,
                                [int(pid) if i == table_person_vector.pk else "{:.5f}".format(Decimal(vector_person[i])) for i
                                 in table_person_vector.columns]))



    if table_person_vector.find(pid) is None:
        table_person_vector.insert(person_vector_row)
    else:
        table_person_vector.update(person_vector_row)
print ''
table_tag_vector.sql_save()
print ''
table_album_vector.sql_save()
print ''
table_person_vector.sql_save()

dbCon.commit()
dbCursor.close()
dbCon.close()
