__author__ = 'lgan'

from dbInterface import *

name_hash = {}

sys.stdout = open("remove_dup.txt" , "w")

for person in table_person.data:
    if person['pid'] <= 752:
        continue
    if name_hash.has_key(person['name']):
        print "DELETE FROM `mydb_track_person` WHERE pid = " , person['pid'] , ';'
        print "DELETE FROM `mydb_album_person` WHERE pid = " , person['pid'] , ';'
        print "DELETE FROM `mydb_person` WHERE pid = " , person['pid'] , ';'
    name_hash[person['name']] = 1
