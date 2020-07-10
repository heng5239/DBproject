.mode csv
create table athlete_info(
    ID int ,
    Name varchar(108),
    Sex char(1),
    Height varchar(3),
    Weight varchar(16),
    primary key(ID)
);
.import "athlete_info.csv" athlete_info

