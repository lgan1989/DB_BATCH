__author__ = 'lgan'

from dbInterface import dbCursor, dbCon
from album_person_match import album_person_match, logger_path as album_logger_path
from track_person_match import track_person_match, logger_path as track_logger_path
from check_not_found_artists import check_not_found, aid_retry_list_path, tid_retry_list_path
from insert_artist import insert_artist
from update_person_avatar import update_person_avatar

# 1). Find out albums and tracks that haven't been matched
# 2). Run album_person_match.py and track_person_match.py, output aid_retry_list.txt and tid_retry_list.txt
# 3). Run album_insert_artist.py and track_insert_artist.py
# 4). Run album_person_math.py and track_person_match.py


def match():
    dbCursor.execute("SELECT aid FROM `mydb_album`  Album WHERE Album.aid NOT IN (SELECT aid FROM `mydb_album_person`)")

    aid_list = dbCursor.fetchall()
    album_person_match(aid_list)

    dbCursor.execute("SELECT tid FROM `mydb_track`  Track WHERE Track.tid NOT IN (SELECT tid FROM `mydb_track_person`)")

    tid_list = dbCursor.fetchall()
    track_person_match(tid_list)

    check_not_found(album_logger_path, aid_retry_list_path)
    check_not_found(track_logger_path, tid_retry_list_path)


def insert():
    insert_artist(0, tid_retry_list_path)
    insert_artist(1, aid_retry_list_path)


#match()
#insert()
#dbCon.commit()
#match()
update_person_avatar()

dbCon.commit()
dbCursor.close()
dbCon.close()
