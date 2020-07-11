select NOC,sum(Gold) as Gold,sum(Silver) as Silver,sum(Bronze) as Bronze,sum(pt)as score
from(select NOC,count(*)  as Gold,0 as Silver,0 as Bronze,3*count(*) as pt
from(select NOC,Event
from  (select NOC,GameID,Medal,Event from event_info where Medal='Gold')as event_info2,(select GameID from game_info where Games='2016 Summer' )as game_info2
where event_info2.GameID=game_info2.GameID
group by NOC,Event)
group by NOC
union
select NOC,0  as Gold,count(*) as Silver,0 as Bronze,2*count(*) as pt
from(select NOC,Event
from  (select NOC,GameID,Medal,Event from event_info where Medal='Silver')as event_info2,(select GameID from game_info where Games='2016 Summer' )as game_info2
where event_info2.GameID=game_info2.GameID
group by NOC,Event)
group by NOC
union
select NOC,0  as Gold,0 as Silver,count(*) as Bronze,count(*) as pt
from(select NOC,Event
from  (select NOC,GameID,Medal,Event from event_info where Medal='Bronze')as event_info2,(select GameID from game_info where Games='2016 Summer' )as game_info2
where event_info2.GameID=game_info2.GameID
group by NOC,Event)
group by NOC)
group by NOC
order by score desc;
