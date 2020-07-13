.mode csv
create table game_info(
    Gameid INTEGER PRIMARY KEY,
    Games TEXT,
    City TEXT

);
.import "game_info.csv" game_info
