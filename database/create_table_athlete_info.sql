.mode csv
create table athlete_info(
    ID INTEGER ,
    Name TEXT,
    Sex TEXT,
    Height TEXT,
    Weight TEXT,
    primary key(ID)
);
.import "athlete_info.csv" athlete_info

