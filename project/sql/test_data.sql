\set EmilyUid 36df8b1c-cc52-11ea-b508-784f437b7506
\set MishaUid 36e08c92-cc52-11ea-b508-784f437b7506
\set OlegUid 36e17922-cc52-11ea-b508-784f437b7506
\set JuanUid 36e25108-cc52-11ea-b508-784f437b7506

insert into players(username, passcode, display_name, player_uid) values('Emily','ylimy','Emily', :'EmilyUid');
insert into players(username, passcode, display_name, player_uid) values('Misha','ahsim','Misha', :'MishaUid');
insert into players(username, passcode, display_name, player_uid) values('Oleg','gelo','Oleg', :'OlegUid');
insert into players(username, passcode, display_name, player_uid) values('Juan','nauj','Juan', :'JuanUid');

\set TemplateUid 36e3531e-cc52-11ea-b508-784f437b7506

\set RoomUid 36e37bb4-cc52-11ea-b508-784f437b7506

\set DeckUid 36e3a5a8-cc52-11ea-b508-784f437b7506

insert into game_templates(template_name, template_uid) values('Awesome Game', :'TemplateUid');

insert into rooms(room_name, room_passcode, room_uid, template_uid) values('Awesome Room', '', :'RoomUid', :'TemplateUid');

insert into decks(deck_name, deck_uid) values('Awesome Deck', :'DeckUid');

insert into room_players(player_uuid, room_uid) values (:'EmilyUid', :'RoomUid');
insert into room_players(player_uuid, room_uid) values (:'MishaUid', :'RoomUid');
insert into room_players(player_uuid, room_uid) values (:'OlegUid', :'RoomUid');
insert into room_players(player_uuid, room_uid) values (:'JuanUid', :'RoomUid');

insert into game_template_decks(game_board_location_x, game_board_location_y, deck_uid, template_uid) values (0,0, :'DeckUid', :'TemplateUid');
