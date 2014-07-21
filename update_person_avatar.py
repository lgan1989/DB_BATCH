__author__ = 'lgan'

from dbInterface import *
import urllib
import json
from logger import Logger

update_person_avatar_logger = Logger("log/update_person_avatar_log.txt")

def process_last_fm(artist_name):
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
    except:

        pass


def update_person_avatar():
    c = 0
    for person in table_person.data:
        c += 1
        try:
            print 'update artist avatar progress:', c, '/', table_person.size
            if person['avatar'] is None or person['avatar'].strip() == '':
                ret = process_last_fm(person['name'].encode('utf-8'))
                person['avatar'] = ret
                table_person.update(person)
        except:
            update_person_avatar_logger.log("Error when trying to update person with pid :" + str(person['pid']))
    table_person.sql_save()
