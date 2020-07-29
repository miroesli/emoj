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


# todo add error handling
def get_conn():
    return psycopg2.connect("dbname='project' user='toggleme' password='ss'")


class DBClassPOINT(NiceObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class DBClassTemplate(NiceObject):
    def __init__(self,template_name, template_uid):
        self.template_name = template_name
        self.template_uid = template_uid


class DBClassDeck(NiceObject):
    def __init__(self, deck_name, deck_uid, template_uid, game_board_location_x, game_board_location_y):
        self.deck_name = deck_name
        self.game_board_location = DBClassPOINT(game_board_location_x, game_board_location_y)
        self.deck_uid = deck_uid
        self.template_uid = template_uid


class DBClassCard(NiceObject):
    def __init__(self, card_name, card_uid, media_uuid, media_class, creation_timestamp, order_index=None, revealed=None):
        self.card_name = card_name
        self.card_uid = card_uid
        self.media_uuid = media_uuid
        self.media_class = media_class
        self.creation_timestamp = creation_timestamp
        if order_index is not None:
            self.order_index = order_index
        if revealed is not None:
            self.revealed = revealed


class DBClassPlayer(NiceObject):
    def __init__(self, username, display_name, player_uid):
        self.username = username
        self.display_name = display_name
        self.player_uid = player_uid


class DBClassRoom(NiceObject):
    def __init__(self, room_name, room_uid, template_uid, active_player_uid):
        self.room_name = room_name
        self.room_uid = room_uid
        self.template_uid = template_uid
        self.active_player_uid = active_player_uid

# notes on db function things
# please include order by clause and all items selected(no select *) to future proof
# if setting up a new entity make a DBClassMyNewEntity and make it's __init__ take all of the db values
# use *i to take all of the select parameters(in the order they are in at the select)

# player functions
def get_player(player_uid, room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """select username, display_name, p.player_uid::varchar from 
                   players p join room_players rp on p.player_uid = rp.player_uid 
                   where p.player_uid=%s and room_uid=%s"""
        curs.execute(query,[player_uid, room_uid])
        for i in curs:
            return DBClassPlayer(*i)


def get_player_by_username(username):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """select username, display_name, player_uid::varchar from players where username=%s"""
        curs.execute(query, [username])
        for i in curs:
            return DBClassPlayer(*i)


def get_players():
    conn = get_conn()
    with conn.cursor() as curs:
        query = """select username, display_name, player_uid::varchar from players order by player_uid"""
        curs.execute(query)
        # *i just places all things into the function individually in order
        return [DBClassPlayer(*i) for i in curs]


def insert_room_player(room_uid, player_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """insert into room_players(room_uid, player_uid) values(%s, %s)"""
        curs.execute(query, [room_uid, player_uid])
    conn.commit()


def get_room_players(room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """select username, display_name, p.player_uid::varchar from 
                   players p join room_players r on p.player_uid = r.player_uid
                   where room_uid = %s"""
        curs.execute(query, [room_uid])
        # *i just places all things into the function individually in order
        return [DBClassPlayer(*i) for i in curs]

# cards functions


def get_card(card_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """ select card_name, card_uid::varchar, media_uuid::varchar, media_class, creation_timestamp 
                    from cards where card_uid =%s order by creation_timestamp """
        curs.execute(query, [card_uid])
        # *i just places all things into the function individually in order
        for i in curs:
            return DBClassCard(*i)


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


def get_room_card(card_uid, room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """ select card_name, c.card_uid::varchar, media_uuid::varchar, media_class, creation_timestamp,p.order_index, p.revealed from
                        cards c join cards_in_play p on c.card_uid = p.card_uid and p.room_uid = %s
                        where c.card_uid =%s
                        order by creation_timestamp"""
        curs.execute(query, [room_uid, card_uid])
        # *i just places all things into the function individually in order
        for i in curs:
            return DBClassCard(*i)


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


def insert_card_into_deck(deck_uid, card_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """insert into deck_cards(deck_uid, card_uid) values(%s, %s)"""
        curs.execute(query, [deck_uid, card_uid])
    conn.commit()


# room functions

def get_room(room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """select room_name, room_uid::varchar, template_uid::varchar, active_player_uid::varchar from rooms where room_uid =%s """
        curs.execute(query, [room_uid])
        for i in curs:
            return DBClassRoom(*i)


def get_rooms():
    conn = get_conn()
    with conn.cursor() as curs:
        query = """select room_name, room_uid::varchar from rooms """
        curs.execute(query)
        return [i for i in curs]



def reset_room_active_player(room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """update rooms set active_player_uid =null where room_uid = %s"""
        curs.execute(query, [room_uid])
    conn.commit()


def clear_cards_in_play(room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """delete from cards_in_play where room_uid =%s"""
        curs.execute(query, [room_uid])
    conn.commit()


def load_cards_in_play(room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """insert into cards_in_play(room_uid,game_board_location_x,game_board_location_y,order_index,player_uid,card_uid,revealed) 
                   select room_uid,0,0,0,NULL,dc.card_uid,false from 
                                rooms r 
                                join game_templates t on r.room_uid=%s and r.template_uid = t.template_uid 
                                join game_template_decks td on td.template_uid = t.template_uid and td.deck_uid is not null
                                join deck_cards dc on td.deck_uid = dc.deck_uid
                                """
        curs.execute(query, [room_uid])
    conn.commit()


#  play area functions
def get_location_cards(room_uid,game_board_location_x, game_board_location_y):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """ select card_name, c.card_uid, media_uuid, media_class, creation_timestamp, order_index, revealed 
                    from cards_in_play cip join cards c on cip.card_uid = c.card_uid 
                    where room_uid =%s and game_board_location_x =%s and game_board_location_y =%s
        """
        curs.execute(query, [room_uid, game_board_location_x, game_board_location_y])
        return [DBClassCard(*i) for i in curs]
# this pulls all of the cards with maximum index, randomize which card we draw in python


def draw_game_board_location_top_card(room_uid, game_board_location_x, game_board_location_y):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """ select card_uid::varchar from cards_in_play where room_uid=%s and game_board_location_x=%s and game_board_location_y=%s
                    and order_index = (select max(order_index) from cards_in_play where room_uid=%s and game_board_location_x=%s and game_board_location_y=%s)"""
        curs.execute(query, [room_uid, game_board_location_x,game_board_location_y, room_uid, game_board_location_x,game_board_location_y])
        return [i[0] for i in curs]


def update_card_location(room_uid, card_uid, game_board_location_x, game_board_location_y, player_uid, revealed=False,idx =0):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """update cards_in_play set game_board_location_x=%s,game_board_location_y=%s, player_uid=%s,revealed=%s, order_index = %s
                   where room_uid = %s and card_uid = %s 
                """
        curs.execute(query, [game_board_location_x,game_board_location_y,player_uid,revealed, idx, room_uid, card_uid])
    conn.commit()


def shuffle_location(room_uid, game_board_location_x, game_board_location_y):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """update cards_in_play set order_index=0, revealed=false
                          where room_uid = %s and game_board_location_x=%s and game_board_location_y=%s
                       """
        curs.execute(query, [room_uid, game_board_location_x, game_board_location_y])
    conn.commit()


def reveal_card(room_uid, player_uid, card_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """update cards_in_play set revealed = true where room_uid=%s and player_uid=%s and card_uid=%s"""
        curs.execute(query,[room_uid, player_uid, card_uid])
    conn.commit()


def pass_turn(room_uid, player_uid, new_player_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """update rooms set active_player_uid=%s where room_uid=%s and active_player_uid=%s or active_player_uid is null"""
        curs.execute(query, [new_player_uid, room_uid, player_uid])
    conn.commit()


def give_card(room_uid, player_uid, new_player_uid, card_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """update cards_in_play set player_uid=%s where room_uid=%s and player_uid=%s and card_uid=%s"""
        curs.execute(query, [new_player_uid, room_uid, player_uid, card_uid])
    conn.commit()


# template functions

def get_room_template(room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """select template_name, r.template_uid::varchar from game_templates gt join rooms r on r.template_uid = gt.template_uid where room_uid=%s"""
        curs.execute(query, [room_uid])
        for i in curs:
            return DBClassTemplate(*i)


def get_all_templates():
    conn = get_conn()
    with conn.cursor() as curs:
        query ="""select template_name, template_uid::varchar from game_templates"""
        curs.execute(query)
        return [DBClassTemplate(*i) for i in curs]


def insert_room(room_name, room_passcode, room_uid, template_uid, active_player_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """insert into rooms (room_name, room_passcode, room_uid, template_uid, active_player_uid)
                    values(%s,%s,%s,%s,%s)"""
        curs.execute(query, [room_name, room_passcode, room_uid, template_uid, active_player_uid])
        conn.commit()


def insert_template(template_name, template_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """insert into game_templates (template_name, template_uid) values(%s,%s)"""
        curs.execute(query, [template_name, template_uid])
        conn.commit()


def insert_template_deck(template_uid, deck_uid, game_board_location_x, game_board_location_y):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """insert into game_template_decks(deck_uid, template_uid, game_board_location_x, game_board_location_y)
                   values (%s,%s,%s,%s) """
        curs.execute(query, [deck_uid, template_uid, game_board_location_x, game_board_location_y])
        conn.commit()


def get_template_decks(template_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """ select null, deck_uid::varchar, template_uid::varchar,game_board_location_x,game_board_location_y
                    from game_template_decks where template_uid = %s"""
        curs.execute(query, [template_uid])
        return [DBClassDeck(*i) for i in curs]


def get_first_deck():
    conn = get_conn()
    with conn.cursor() as curs:
        query = """ select deck_uid::varchar from decks limit 1;"""
        curs.execute(query)
        for i in curs:
            return i[0]


#play log functions

def get_room_log(room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """select message from play_log where room_uid=%s order by creation_timestamp limit 20"""
        curs.execute(query, [room_uid])
        return [i[0] for i in curs]


def log_action(room_uid, message):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """insert into play_log(message_uid, room_uid, message) values(uuid_generate_v4(), %s,%s)"""
        curs.execute(query, [room_uid, message])
    conn.commit()


def clear_log(room_uid):
    conn = get_conn()
    with conn.cursor() as curs:
        query = """delete from play_log where room_uid=%s"""
        curs.execute(query, [ room_uid])
    conn.commit()
