.separator ","
.mode csv
create table game_info(
    Gameid INTEGER PRIMARY KEY,
    Games char(11),
    City varchar(25)

);
.import "game_info.csv" game_info
