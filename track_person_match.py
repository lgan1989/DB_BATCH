# -*- coding: UTF-8 –*-

from dbInterface import *
import urllib
import xml.etree.ElementTree as ET
import time
from logger import *

logger_path = "log/track_person_match_log.txt"
updater_path = "log/track_artist_update_suggestion.txt"

logger = Logger(logger_path)
updater = Logger(updater_path)

def track_person_match(tid_list):

    query_url = 'http://musicbrainz.org/ws/2/artist/?query=artist:'

    name_hash = {}
    not_found_hash = {}
    c = 0

    for person in table_person.data:
        not_found_hash[person['name']] = person

    for tid in tid_list:
        c += 1

        print 'track_person_match progress:', c, '/', len(tid_list)
        tid = int(tid[0])

        track = table_track.find(tid, None)
        artist = track['artist']

        try:
            if '/' in artist:
                artist_list = artist.split('/')

                for artist in artist_list:
                    artist = artist.strip()
                    if artist in name_hash.keys():
                        dbCursor.execute(
                            "INSERT IGNORE INTO `mydb_track_person` (pid , tid , aid) values (%s , %s , %s)",
                            (name_hash[artist],
                             track['tid'], track['album']))
                        continue
                    query = query_url + artist.encode('utf-8')

                    result = urllib.urlopen(query).read()
                    time.sleep(1)
                    tree = ET.fromstring(result)
                    result_list = tree[0]
                    mbid = None
                    u_artist = artist.encode('utf-8')
                    best_match = ''
                    found = False
                    for item in result_list:
                        for child in item:
                            if 'name' in child.tag:
                                name = child.text.strip().encode('utf-8')
                                if best_match == '':
                                    best_match = name
                                if name == u_artist or name.upper() == u_artist.upper():

                                    mbid = item.attrib['id']
                                    if table_person.find_one_by_col('mbid', mbid, None) is not None:
                                        found = True
                            if 'alias-list' in child.tag:
                                for alia in child:
                                    alis = alia.text.strip().encode('utf-8')
                                    if best_match == '':
                                        best_match = alis
                                    if alis == u_artist or alis.upper() == u_artist.upper():
                                        mbid = item.attrib['id']
                                        if table_person.find_one_by_col('mbid', mbid, None) is not None:
                                            found = True
                            if found is True:
                                break
                        if found is True:
                            break

                    if mbid is not None:
                        ret = table_person.find_one_by_col('mbid', mbid, None)
                        if ret is not None:
                            name_hash[artist] = ret['pid']
                            dbCursor.execute(
                                "INSERT IGNORE INTO `mydb_track_person` (pid , tid , aid) values (%s , %s , %s)",
                                (ret['pid'],
                                 track['tid'], track['album']))
                        else:
                            logger.log("failed[mbid not found]:" + str(track['tid']))
                            if best_match != "":
                                updater.log(
                                    "UPDATE mydb_track SET artist = '" + str(track['artist'].encode('utf-8')).replace(
                                        u_artist, best_match.replace("'", "\\'")) + "' WHERE tid = " + str(
                                        track['tid']) + "; #" + str(track['artist'].encode('utf-8')))
                    else:

                        if artist in not_found_hash.keys():
                            ret = not_found_hash[artist]
                            name_hash[artist] = ret['pid']
                            dbCursor.execute(
                                "INSERT IGNORE INTO `mydb_track_person` (pid , tid , aid) values (%s , %s , %s)",
                                (ret['pid'],
                                 track['tid'], track['album']))
                        else:
                            logger.log("failed[not found]:" + str(track['tid']))
                            if best_match != "":
                                updater.log(
                                    "UPDATE mydb_track SET artist = '" + str(track['artist'].encode('utf-8')).replace(
                                        u_artist, best_match.replace("'", "\\'")) + "' WHERE tid = " + str(
                                        track['tid']) + "; #" + str(track['artist'].encode('utf-8')))
            else:
                artist = artist.strip()
                if artist in name_hash.keys():
                    dbCursor.execute("INSERT IGNORE INTO `mydb_track_person` (pid , tid , aid) values (%s , %s , %s)",
                                     (name_hash[artist],
                                      track['tid'], track['album']))
                    continue
                query = query_url + artist.encode('utf-8')

                result = urllib.urlopen(query).read()
                time.sleep(1)
                tree = ET.fromstring(result)
                result_list = tree[0]
                mbid = None
                u_artist = artist.encode('utf-8')
                best_match = ''
                found = False
                for item in result_list:
                    for child in item:
                        if 'name' in child.tag:

                            name = child.text.encode('utf-8')
                            if best_match == '':
                                best_match = name

                            if name == u_artist or name.upper() == u_artist.upper():
                                mbid = item.attrib['id']
                                if table_person.find_one_by_col('mbid', mbid, None) is not None:
                                    found = True
                        if 'alias-list' in child.tag:
                            for alia in child:
                                alis = alia.text.encode('utf-8')
                                if best_match == '':
                                    best_match = alis
                                if alis == u_artist or alis.upper() == u_artist.upper():
                                    mbid = item.attrib['id']
                                    if table_person.find_one_by_col('mbid', mbid, None) is not None:
                                        found = True
                        if found is True:
                            break
                    if found is True:
                        break

                if mbid is not None:
                    ret = table_person.find_one_by_col('mbid', mbid, None)
                    if ret is not None:
                        name_hash[artist] = ret['pid']
                        dbCursor.execute(
                            "INSERT IGNORE INTO `mydb_track_person` (pid , tid , aid) values (%s , %s , %s)",
                            (ret['pid'],
                             track['tid'], track['album']))
                    else:
                        logger.log("failed[mbid not found]:" + str(track['tid']))
                        if best_match != "":
                            updater.log(
                                "UPDATE mydb_track SET artist = '" + str(track['artist'].encode('utf-8')).replace(
                                    u_artist, best_match.replace("'", "\\'")) + "' WHERE tid = " + str(
                                    track['tid']) + "; #" + str(track['artist'].encode('utf-8')))
                else:
                    if artist in not_found_hash.keys():
                        ret = not_found_hash[artist]
                        name_hash[artist] = ret['pid']
                        dbCursor.execute(
                            "INSERT IGNORE INTO `mydb_track_person` (pid , tid , aid) values (%s , %s , %s)",
                            (ret['pid'],
                             track['tid'], track['album']))
                    else:
                        logger.log("failed[not found]:" + str(track['tid']))
                        if best_match != "":
                            updater.log(
                                "UPDATE mydb_track SET artist = '" + str(track['artist'].encode('utf-8')).replace(
                                    u_artist, best_match.replace("'", "\\'")) + "' WHERE tid = " + str(
                                    track['tid']) + "; #" + str(track['artist'].encode('utf-8')))
        except:
            logger.log("failed:" + str(track['tid']))
            raise




