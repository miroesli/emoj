import psycopg2
import datetime
import time
import uuid
# allows use of .to_dict on any object
class NiceObject(object):
    def __str__(self):
        return str(self.__dict__)

    def to_dict(self):
        d = self.__dict__.copy()
        for k in list(d.keys()):
            if type(d[k]) == datetime.date:
                d[k] = d[k].strftime("%Y-%m-%d")
            if type(d[k]) == datetime.datetime:
                try:
                    d[k] = int(time.mktime(d[k].timetuple()))
                except OverflowError:
                    d[k] = 0
            elif type(d[k]) == datetime.time:
                d[k] = d[k].strftime("%H:%M:%S")
            elif isinstance(d[k], NiceObject):
                d[k] = d[k].to_dict()
            elif isinstance(d[k], list) and len(d[k]) > 0 and hasattr(d[k][0], "to_dict"):
                d[k] = [x.to_dict() for x in d[k]]
            elif k == "password":
                d[k] = ''
        return d


#todo add error handling
def get_conn():
    return psycopg2.connect("dbname='project' user='toggleme' password='ss'")


class DBClassDeck(NiceObject):
    def __init__(self, deck_name, game_board_location, deck_uid, template_uid):
        self.deck_name = deck_name
        self.game_board = game_board_location
        self.deck_uid = deck_uid
        self.template_uid = template_uid


def get_template_decks(template_uuid):
    conn = get_conn()
    with conn.cursor() as curs:
        #don't use select *, copy order from dbclass
        query = """select deck_name, game_board_location, deck_uid, template_uid from decks where template_uuid = %s"""
        curs.execute(query,[template_uuid])
        # *i just places all things into the function individiaully in order
        return [DBClassDeck(*i) for i in curs]


def get_cards():
    conn = get_conn()
    with conn.cursor() as curs:
        # don't use select *, copy order from dbclass
        query = """select card_name, card_uid, media_uuid, media_class from cards"""
        curs.execute(query)
        # *i just places all things into the function individually in order
        return [DBClassDeck(*i) for i in curs]


def insert_card(card_name, media_uuid, media_class):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """insert into cards(card_name, card_uid, media_uuid, media_class) values(%s, uuid_generate_v4(), %s, %s)"""
        curs.execute(query, [card_name, media_uuid, media_class])
    conn.commit()
