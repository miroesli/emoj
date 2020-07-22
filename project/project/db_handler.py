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
            if not d[k]:
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

class DBClassCard(NiceObject):
    def __init__(self, card_name, card_uid, media_uuid, media_class, creation_timestamp):
        self.card_name = card_name
        self.card_uid = card_uid
        self.media_uuid = media_uuid
        self.media_class = media_class
        self.creation_timestamp = creation_timestamp

class DBClassPlayer(NiceObject):
    def __init__(self, username, display_name, player_uid):
        self.username = username
        self.display_name = display_name
        self.player_uid = player_uid

def get_template_decks(template_uuid):
    conn = get_conn()
    with conn.cursor() as curs:

        query = """ select deck_name, game_board_location, deck_uid::varchar, template_uid::varchar 
                    from game_template_decks where template_uid = %s"""
        curs.execute(query, [template_uuid])
        return [DBClassDeck(*i) for i in curs]

# notes on db function things
# please include order by clause and all items selected(no select *) to future proof
# if setting up a new entity make a DBClassMyNewEntity and make it's __init__ take all of the db values
# use *i to take all of the select parameters(in the order they are in at the select)


def get_players():
    conn = get_conn()
    with conn.cursor() as curs:
        query = """select username, display_name, player_uid::varchar from players"""
        curs.execute(query)
        # *i just places all things into the function individually in order
        return [DBClassPlayer(*i) for i in curs]


def get_room_players(room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """select username, display_name, player_uid::varchar from 
                   players p join room_players r on p.player_uid = r.player_uid
                   where room_uid = %s"""
        curs.execute(query[room_uid])
        # *i just places all things into the function individually in order
        return [DBClassPlayer(*i) for i in curs]


def get_cards():
    conn = get_conn()
    with conn.cursor() as curs:
        query = """select card_name, card_uid::varchar, media_uuid::varchar, media_class, creation_timestamp from cards order by creation_timestamp"""
        curs.execute(query)
        # *i just places all things into the function individually in order
        return [DBClassCard(*i) for i in curs]


def get_player_cards(player_uid, room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """ select card_name, c.card_uid::varchar, media_uuid::varchar, media_class, creation_timestamp from
                    cards c join cards_in_play p on c.card_uid = p.card_uid and p.room_uid = %s
                    where player_uid =%s
                    order by creation_timestamp"""
        curs.execute(query, [room_uid, player_uid])
        # *i just places all things into the function individually in order
        return [DBClassCard(*i) for i in curs]


def get_player_card_revealed(player_uid, room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """ select card_name, c.card_uid::varchar, media_uuid::varchar, media_class, creation_timestamp from
                        cards c join cards_in_play p on c.card_uid = p.card_uid and p.room_uid = %s
                        where player_uid =%s and p  .revealed
                        order by creation_timestamp"""
        curs.execute(query, [room_uid, player_uid])
        # *i just places all things into the function individually in order
        return [DBClassCard(*i) for i in curs]

def get_player_card_count(player_uid, room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """ select count(*) from
                           cards c join cards_in_play p on c.card_uid = p.card_uid and p.room_uid = %s
                           where player_uid =%s"""
        curs.execute(query, [room_uid, player_uid])
        # *i just places all things into the function individually in order
        for i in curs:
            return i[0]


def insert_card(card_name, media_uuid, media_class):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """insert into cards(card_name, card_uid, media_uuid, media_class) values(%s, uuid_generate_v4(), %s, %s)"""
        curs.execute(query, [card_name, media_uuid, media_class])
    conn.commit()
