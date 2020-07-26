drop table if exists players cascade;
create table players(
	username VARCHAR(64)  not null,
  	passcode VARCHAR(64) not null,
  	display_name VARCHAR(64) not null,
  	player_uid uuid PRIMARY KEY,
	login_id int,
	FOREIGN KEY (login_id) REFERENCES auth_user(id) on delete restrict
);
drop table if exists rooms cascade;
create table rooms(
	room_name VARCHAR(64) not null,
	room_passcode varchar(64),
	room_uid uuid PRIMARY KEY,
    template_uid uuid,
    active_player_uid uuid,
    FOREIGN KEY (active_player_uid) REFERENCES players (player_uid) on delete set null,
    FOREIGN KEY (template_uid) REFERENCES game_templates (template_uid) on delete set null
);
drop table if exists room_players;
create table room_players(
	player_uid uuid,
	room_uid uuid,
	PRIMARY KEY (player_uid, room_uid),
	FOREIGN KEY (player_uid) REFERENCES players (player_uid) on delete cascade,
	FOREIGN KEY (room_uid) REFERENCES rooms (room_uid) on delete cascade
);
drop table if exists game_templates cascade;
create table game_templates(
	template_name VARCHAR(64)  not null,
	template_uid uuid PRIMARY KEY
);
drop table if exists game_template_decks;
create table game_template_decks(
	game_board_location_x int,
	game_board_location_y int,
	deck_uid uuid,
	template_uid uuid,
	PRIMARY KEY(game_board_location_x, game_board_location_y, template_uid),
	FOREIGN KEY (template_uid) REFERENCES game_templates (template_uid) on delete cascade,
	FOREIGN KEY(deck_uid) REFERENCES decks (deck_uid) on delete restrict
);
--media stored in media/uuid.png
--make a job to crawl that directory and load this table
drop table if exists media_files cascade;
create table media_files(
	media_uid uuid PRIMARY KEY,
	media_dimensions point not null
);
drop table if exists cards cascade;
create table cards(
	card_name varchar(64),
	card_uid uuid PRIMARY KEY,
	media_uuid uuid,
	media_class varchar(64),
	creation_timestamp timestamp default now(),
	FOREIGN KEY (media_uuid) REFERENCES media_files (media_uid) on delete set null
);
drop table if exists decks cascade;
create table decks(
	deck_name varchar(64),
	deck_uid uuid PRIMARY KEY,
	media_uid uuid,
	FOREIGN KEY (media_uid) REFERENCES media_files (media_uid) on delete set null
);

drop table if exists deck_cards cascade;
create table deck_cards(
	deck_uid uuid,
	card_uid uuid,
	PRIMARY KEY (deck_uid,card_uid),
	FOREIGN KEY (deck_uid) REFERENCES decks (deck_uid) on delete  cascade,
	FOREIGN KEY (card_uid) REFERENCES cards (card_uid) on delete  cascade
);
drop table if exists cards_in_play;
create table cards_in_play(
	room_uid uuid,
	game_board_location_x int,
	game_board_location_y int,
	order_index int,
	player_uid uuid,
	card_uid uuid,
	revealed boolean,
	FOREIGN KEY (room_uid) REFERENCES rooms (room_uid) on delete  cascade,
	FOREIGN KEY (card_uid) REFERENCES cards (card_uid) on delete  cascade,
	PRIMARY KEY (room_uid, card_uid)
);
drop table if exists play_log;
create table play_log(
    message uuid PRIMARY KEY,
    room_uid uuid,
    message varchar(255),
    creation_timestamp timestamp,
    FOREIGN KEY (room_uid) REFERENCES rooms (room_uid) on delete  cascade
);
