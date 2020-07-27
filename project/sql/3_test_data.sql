\set EmilyUid 36df8b1c-cc52-11ea-b508-784f437b7506
\set MishaUid 36e08c92-cc52-11ea-b508-784f437b7506
\set OlegUid 36e17922-cc52-11ea-b508-784f437b7506
\set JuanUid 36e25108-cc52-11ea-b508-784f437b7506

insert into auth_user(username, password, first_name, last_name, email, is_staff, is_active, date_joined, is_superuser, id) values('Emily', 'pbkdf2_sha256$180000$uFhfTbCWjzNU$5gL3NJwmjN3S61Ua8XYGVj/tjo9zFcmJtCcLgihLxC8=', '', '', '', 't', 't', '2020-07-24 01:36:44.606188+00', 't', 1);
insert into auth_user(username, password, first_name, last_name, email, is_staff, is_active, date_joined, is_superuser, id) values('Misha', 'pbkdf2_sha256$180000$SygKBhSylTLZ$rE+MWcqSXQq50dnjgQCVhq1O5VouqDybAjnHIMuCKng=', '', '', '', 't', 't', '2020-07-24 01:36:44.606188+00','t', 2);
insert into auth_user(username, password, first_name, last_name, email, is_staff, is_active, date_joined, is_superuser, id) values('Oleg', 'pbkdf2_sha256$180000$tFyRw2QHFGeV$wrNDYC5BBZeJLcng6FcSF8yP3PxL8h/ufllnQB63lCI=', '', '', '', 't', 't', '2020-07-24 01:36:44.606188+00','t', 3);
insert into auth_user(username, password, first_name, last_name, email, is_staff, is_active, date_joined, is_superuser, id) values('Juan', 'pbkdf2_sha256$180000$yfsv7fdPJoZH$baV6YAFjL9GhOesvwjbcDUUCTBkm1k3vV9VKwU1pcg0=', '', '', '', 't', 't', '2020-07-24 01:36:44.606188+00','t', 4);

insert into players(username, passcode, display_name, player_uid, login_id) values('Emily','ylimy','Emily',:'EmilyUid', 1);
insert into players(username, passcode, display_name, player_uid, login_id) values('Misha','ahsim','Misha', :'MishaUid',2 );
insert into players(username, passcode, display_name, player_uid, login_id) values('Oleg','gelo','Oleg', :'OlegUid',3);
insert into players(username, passcode, display_name, player_uid, login_id) values('Juan','nauj','Juan', :'JuanUid',4);

\set TemplateUid 36e3531e-cc52-11ea-b508-784f437b7506

\set RoomUid 36e37bb4-cc52-11ea-b508-784f437b7506

\set DeckUid 36e3a5a8-cc52-11ea-b508-784f437b7506

insert into game_templates(template_name, template_uid) values('Awesome Game', :'TemplateUid');

insert into rooms(room_name, room_passcode, room_uid, template_uid) values('Awesome Room', '', :'RoomUid', :'TemplateUid');

insert into decks(deck_name, deck_uid) values('Awesome Deck', :'DeckUid');

insert into room_players(player_uid, room_uid) values (:'EmilyUid', :'RoomUid');
insert into room_players(player_uid, room_uid) values (:'MishaUid', :'RoomUid');
insert into room_players(player_uid, room_uid) values (:'OlegUid', :'RoomUid');
insert into room_players(player_uid, room_uid) values (:'JuanUid', :'RoomUid');

insert into game_template_decks(game_board_location_x, game_board_location_y, deck_uid, template_uid) values (0,0, :'DeckUid', :'TemplateUid');
