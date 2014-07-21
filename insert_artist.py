# -*- coding: UTF-8 –*-

from dbInterface import *
import urllib
import json
import xml.etree.ElementTree as ET
import time
from logger import *



insert_album_log = Logger("log/album_insert_log.txt")
insert_track_log = Logger("log/track_insert_log.txt")
insert_log = None
mbid_hash = {}

# 1). To get avatar from last.fm
# 2). To get mbid from MZ
# 3). insert into database


def process_last_fm(artist_name):
    global insert_log
    url = base_last_fm_url + artist_name
    try:
        json_data = urllib.urlopen(url).read()
        if json_data is None:
            return None

        artist = json.loads(json_data)
        if artist.has_key('artist') is False:
            return None
        artist = artist['artist']
        avatar = artist['image'][2]['#text'].strip()
        return avatar

    except Exception, e:
        insert_log.log('Error when insert ' + artist_name + ' :' + e.message)


def process_mz(artist_name, avatar):
    global insert_log
    mz_query = base_mz_url + artist_name
    result = urllib.urlopen(mz_query).read()
    time.sleep(1)
    tree = ET.fromstring(result)
    artist_list = tree[0]
    found = False
    try:
        for artist in artist_list:
            for child in artist:
                if 'name' in child.tag:
                    name = child.text.encode('utf-8')
                    if name == artist_name or name.upper() == artist_name.upper():
                        person_row = {'pid': None, 'dbid': None, 'mbid': artist.attrib['id'], 'name': name,
                                      'avatar': avatar, 'favourite': None}

                        if mbid_hash.has_key(artist.attrib['id']) is False:
                            table_person.insert(person_row)
                            insert_log.log('Insert successfully: ' + artist_name + ' - ' + artist.attrib['id'])
                            found = True
                            mbid_hash[artist.attrib['id']] = 1
                            break
                        else:
                            insert_log.log('Found duplication when insert ' + artist_name)
                            return

                if 'alias-list' in child.tag:
                    for alia in child:
                        alis = alia.text.encode('utf-8')
                        if alis == artist_name or alis.upper() == artist_name.upper():
                            person_row = {'pid': None, 'dbid': None, 'mbid': artist.attrib['id'], 'name': name,
                                          'avatar': avatar, 'favourite': None}
                            if mbid_hash.has_key(artist.attrib['id']) is False:
                                table_person.insert(person_row)
                                insert_log.log('Insert successfully: ' + artist_name + ' - ' + artist.attrib['id'])
                                found = True
                                mbid_hash[artist.attrib['id']] = 1
                                break
                            else:
                                insert_log.log('Found duplication when insert ' + artist_name)
                                return

            if found is True:
                break
        if found is False:
            person_row = {'pid': None, 'dbid': None, 'mbid': None, 'name': artist_name,
                          'avatar': avatar, 'favourite': None}
            table_person.insert(person_row)

            insert_log.log('Insert successfully: ' + artist_name + ' - ' + '[no mbid found]')

    except Exception, e:
        insert_log.log('Error when insert ' + artist_name + ' :' + e.message)


def insert_artist(type, list_file): #0: track , 1: album

    global insert_log

    name_hash = {}

    id_list = open(list_file , 'r')

    for person in table_person.data:
        mbid_hash[person['mbid']] = 1
        name_hash[person['name']] = 1

    table = table_track if type == 0 else table_album
    column = 'artist' if type == 0 else 'author'

    insert_log = insert_track_log if type == 0 else insert_album_log
    c = 0


    for id in id_list:

        id = int(id.strip())

        line = table.find(id, None)
        line = line[column].encode('utf-8')
        c += 1
        print table.table_name, ' insert progress:', c

        if '/' in line:
            name_list = line.split('/')
        else:
            name_list = [line]

        for name in name_list:
            name = name.replace("%", "")
            name = name.strip()
            if name == '':
                continue
            if name_hash.has_key(name):
                continue
            name_hash[name] = 1
            ret = process_last_fm(name)
            process_mz(name, ret)

    table_person.sql_save()







