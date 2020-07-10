.mode csv
create table event_info(
    ID int ,
    Age char(2),
    Team varchar(50),
    NOC char(3),
    Gameid int,
    Sport varchar(30),
    Event varchar(255),
    Medal varchar(6)

);
.import "event_info.csv" event_info
