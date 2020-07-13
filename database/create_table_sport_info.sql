.mode csv
create table sport_info(
    Event TEXT PRIMARY KEY,
    Sport TEXT
);
.import "sport_info.csv" sport_info
