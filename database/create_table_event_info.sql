.mode csv
create table event_info(
    ID INTEGER ,
    Age TEXT,
    Team TEXT,
    NOC TEXT,
    Gameid INTEGER,
    Event TEXT,
    Medal TEXT

);
.import "event_info.csv" event_info
