# -*- coding: UTF-8 –*-

import sys
import re
from decimal import *
from dbConnection import *
from progress import *

getcontext().prec = 5

STRUCT_ALBUM = {'name': 'mydb_album',
                'columns': ['aid', 'daid', 'title', 'author', 'cover', 'link', 'fetched'],
                'pk': 'aid'}
STRUCT_ALBUM_TAG = {'name': 'mydb_album_tag',
                    'columns': ['id', 'aid', 'tid', 'count'],
                    'pk': 'id'}
STRUCT_ALBUM_VECTOR = {'name': 'mydb_album_vector',
                       'columns': ['aid', 'anime', 'pop', 'classic', 'acoustic', 'japanese', 'taiwan', 'chinese',
                                   'rock',
                                   'cantonese',
                                   'female', 'male', 'pure', 'english', 'american', 'country'],
                       'pk': 'aid'}
STRUCT_TAG = {'name': 'mydb_tag',
              'columns': ['tid', 'name'],
              'pk': 'tid'}
STRUCT_TAG_VECTOR = {'name': 'mydb_tag_vector',
                     'columns': ['tid', 'anime', 'pop', 'classic', 'acoustic', 'japanese', 'taiwan', 'chinese',
                                 'rock', 'cantonese',
                                 'female', 'male', 'pure', 'english', 'american', 'country'],
                     'pk': 'tid'}

STRUCT_TRACK = {'name': 'mydb_track',
                'columns': ['tid', 'title', 'url', 'artist', 'album', 'played', 'like', 'sid', 'dislike', 'skipped',
                            'lastlistened', 'tagstring'],
                'pk': 'tid'}

STRUCT_PERSON = {'name': 'mydb_person',
                 'columns': ['pid', 'dbid', 'mbid', 'name', 'avatar', 'favourite'],
                 'pk': 'pid'}

STRUCT_PERSON_VECTOR = {'name': 'mydb_person_vector',
                     'columns': ['pid', 'anime', 'pop', 'classic', 'acoustic', 'japanese', 'taiwan', 'chinese',
                                 'rock', 'cantonese',
                                 'female', 'male', 'pure', 'english', 'american', 'country'],
                     'pk': 'pid'}

STRUCT_TRACK_ALBUM = {}

class DBError:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MyDBTable:
    def __init__(self, var_table_name=None, var_columns=[], var_pk=None):
        self.table_name = var_table_name
        self.columns = var_columns
        self.pk = var_pk
        self.cur = dbCon.cursor()
        self.cur.execute('SELECT ' + ','.join(
            ['`' + col + '`' for col in self.columns]) + ' FROM ' + self.table_name + ' ORDER BY ' + self.pk + ' ASC')
        self.data = [dict(zip(self.columns, row)) for row in self.cur.fetchall()]
        self.top_id = self.data[-1][self.pk] if len(self.data) > 0 else 0
        self.size = len(self.data)
        print self.table_name + ' loaded.'

    def sql_save(self):

        current_val = 0
        total_val = len(self.data)
        for val in self.data:
            #progress_refresh('saving to ' + self.table_name, current_val, total_val)
            current_val += 1

            if 'flag_insert' in val and val['flag_insert'] is True:
                self.sql_insert(val)
                val['flag_insert'] = None
            elif 'flag_update' in val and val['flag_update'] is True:
                self.sql_update(val)
                val['flag_update'] = None

    def sql_update(self, var_row={}):
        update_params = ','.join([col + '= %s' for col in self.columns])
        update_values = ['NULL' if var_row[col] is None else var_row[col] for col in self.columns]
        update_values.append(var_row[self.pk])
        dbCursor.execute('update ' + self.table_name + ' set ' + update_params + \
                         ' where ' + self.pk + ' = %s', update_values)


    def sql_insert(self, var_row={}):
        insert_columns = '(' + ','.join(self.columns) + ')'
        insert_params = '(' + ','.join(['%s' for col in self.columns]) + ')'
        insert_values = [var_row[col] for col in self.columns]

        dbCursor.execute('insert into ' + self.table_name + ' ' + insert_columns + " values " + insert_params,
                         insert_values)


    def insert(self, var_row={}):

        if self.pk in var_row:
            if self.find(var_row[self.pk]) is not None:  # duplication occurs
                raise DBError('Primary key duplication occurs when inserting data: ' + var_row.__repr__())
                return

        new_row = dict.fromkeys(self.columns, 0)

        for col in self.columns:
            if col in var_row:
                new_row[col] = var_row[col]
        new_row[self.pk] = var_row[self.pk] if self.pk in var_row and var_row[self.pk] is not None else self.top_id + 1
        new_row['flag_insert'] = True

        self.data.insert(self.size, new_row)
        self.size += 1
        self.top_id = self.top_id + 1


    def update(self, var_row={}):

        if self.pk in var_row:
            if self.find(var_row[self.pk]) is None:  # not found in db
                print var_row[self.pk], self.top_id
                raise DBError('Primary key not found when updating data: ' + var_row.__repr__())
                return
        idx = self.binary_search(var_row[self.pk])
        for col in var_row.keys():
            self.data[idx][col] = var_row[col]
        self.data[idx]['flag_update'] = True

    def find_one_by_col(self, col=None, key=None, columns=None):
        columns = columns if columns is not None else self.columns
        if col in self.columns:
            for row in self.data:
                if row[col] == key:
                    return {i: row[i] for i in columns}
        return None

    def find_all_by_col(self, col=None, key=None, columns=None):
        columns = columns if columns is not None else self.columns
        result_set = []
        if col in self.columns:
            for row in self.data:
                if row[col] == key:
                    ret = {i: row[i] for i in columns}
                    result_set.append(ret)
        return result_set

    def binary_search(self, key=None):
        if key is None:
            return
        low = 0
        key = int(key)
        high = len(self.data) - 1
        while low <= high:

            mid = (low + high) / 2
            val = self.data[mid][self.pk]
            if val < key:
                low = mid + 1
            elif val > key:
                high = mid - 1
            else:
                return mid
        return -1

    def find(self, key=None, columns=None):
        if key is None:
            return None
        columns = columns if columns is not None else self.columns
        idx = self.binary_search(key)
        if idx != -1:
            return {i: self.data[idx][i] for i in columns}
        return None

#
table_album = MyDBTable(STRUCT_ALBUM['name'], STRUCT_ALBUM['columns'], STRUCT_ALBUM['pk'])
table_album_tag = MyDBTable(STRUCT_ALBUM_TAG['name'], STRUCT_ALBUM_TAG['columns'], STRUCT_ALBUM_TAG['pk'])
table_album_vector = MyDBTable(STRUCT_ALBUM_VECTOR['name'], STRUCT_ALBUM_VECTOR['columns'], STRUCT_ALBUM_VECTOR['pk'])
table_tag = MyDBTable(STRUCT_TAG['name'], STRUCT_TAG['columns'], STRUCT_TAG['pk'])
table_tag_vector = MyDBTable(STRUCT_TAG_VECTOR['name'], STRUCT_TAG_VECTOR['columns'], STRUCT_TAG_VECTOR['pk'])
table_track = MyDBTable(STRUCT_TRACK['name'], STRUCT_TRACK['columns'], STRUCT_TRACK['pk'])
table_person = MyDBTable(STRUCT_PERSON['name'], STRUCT_PERSON['columns'], STRUCT_PERSON['pk'])
table_person_vector = MyDBTable(STRUCT_PERSON_VECTOR['name'], STRUCT_PERSON_VECTOR['columns'], STRUCT_PERSON_VECTOR['pk'])

print 'initiation finished'




