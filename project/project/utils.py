from project import db_handler
import random

def reset_room(room_uid):
    db_handler.clear_cards_in_play(room_uid)
    db_handler.load_cards_in_play(room_uid)


def deal_card(room_uid, player_uid, game_board_location):
    card_uids = db_handler.draw_game_board_location_top_card(room_uid, game_board_location)
    card_uid = random.choice(card_uids)
    db_handler.update_card_location(room_uid, card_uid, None, player_uid)


def transfer_card(entity_type1,entity_type2,entity_uid1,entity_uid2):
    if entity_type1 not in ['card','player','location']:
        pass #throws err
    if entity_type2 not in ['card','player','location']:
        pass #throws err
    else:
        pass #do stuff