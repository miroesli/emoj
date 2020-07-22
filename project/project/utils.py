from project import db_handler
def reset_room(room_uid):
    db_handler.clear_cards_in_play(room_uid)
    db_handler.load_cards_in_play(room_uid)
