# -*- coding: UTF-8 –*-

import sys
from pprint import pprint
from dbInterface import *
import urllib
import json
import xml.etree.ElementTree as ET
import time

f = open("name_list.txt", "r")

base_url = 'http://localhost:8080/bethello/index/getAvatar/'

stdout = sys.stdout

mbid_hash = {}

person_list = table_person.data

query_url = 'http://musicbrainz.org/ws/2/artist/?query=artist:'

f_ret= open("mbid_match.txt" , "r")
c = 0

for data in f_ret:
    if '[NOT MATCHED]' in data:
        continue
    data = data.strip().split(';')
    try:
        dbCursor.execute('UPDATE `mydb_person` SET mbid = %s WHERE pid = %s' , (data[1] , data[0]))
    except:

        print data[0]
        pass
        #dbCursor.execute('DELETE FROM `mydb_person` WHERE pid = %s' , data[0])

dbCon.commit()
dbCursor.close()
dbCon.close()

exit()

for person in person_list:
    c += 1
    print c
    if person['mbid'] is not None or person['dbid'] is not None:
        continue
    query = query_url + person['name'].encode('utf-8')
    result = urllib.urlopen(query).read()
    time.sleep(1)
    tree = ET.fromstring(result)
    artist_list = tree[0]
    found = False

    for artist in artist_list:
        for child in artist:
            if 'name' in child.tag:
                name = child.text.encode('utf-8')
                if name == person['name'].encode('utf-8'):

                    f_ret.write( str(person['pid']) + ';' +artist.attrib['id'] + ';' + name + '\n')
                    found = True
                    break
            if 'alias-list' in child.tag:
                for alia in child:
                    alis = alia.text.encode('utf-8')
                    if alis == person['name'].encode('utf-8'):

                        f_ret.write( str(person['pid']) + ';' +artist.attrib['id'] + ';' + alis + '\n')
                        found = True
                        break
        if found is False:

            f_ret.write( str(person['pid']) + ';' + artist.attrib['id'] + ';' + person['name'].encode('utf-8') +  '[NOT MATCHED]\n')
            break
        if found is True:
            break




