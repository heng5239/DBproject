import sqlite3

from flask import Flask, request, render_template, url_for


def connect():
    conn = sqlite3.connect('DBproject.db')
    return conn


def disconnect(conn):
    conn.close()


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/name_search', methods=['POST', 'GET'])
def name_search():
    if request.method == 'GET':
        return render_template('name.html')
    elif request.method == 'POST':
        con = connect()
        a = request.form.get('name')
        sql = ""
        if a != "":
            sql = "SELECT ID,Name,Sex,Height,Weight FROM athlete_info WHERE Name LIKE '%" + a + "%';"
        cursor = con.execute(sql)
        lis = []
        if cursor == lis:
            return "NOT Found"
        return render_template('name.html', data=cursor)


@app.route('/individual_page', methods=['POST'])
def individual():

    if request.method == 'POST':
        con = connect()
        id = request.form.get('ID')
        sql = "SELECT Name,Sex,Height,Weight FROM athlete_info WHERE ID = " + id + ";"
        cursor = con.execute(sql)
        s = cursor.fetchone()
        sql = "SELECT Age,Team,NOC,Games,City,Sport,Event,Medal FROM event_info, game_info WHERE event_info.ID = " + id + " AND event_info.Gameid = game_info.Gameid"
        cursor = con.execute(sql)
        lis = []
        if cursor == lis:
            return "NOT Found"
        return render_template('individual.html', status=s, data=cursor)


@app.route('/score_search', methods=['POST', 'GET'])
def score_search():
    if request.method == 'GET':
        return render_template('score.html')
    elif request.method == 'POST':
        con = connect()
        a = request.form.get('Games')
        sql = ""
        if a != "":
            sql = "select NOC,sum(Gold) as Gold,sum(Silver) as Silver,sum(Bronze) as Bronze,sum(pt)as score from(" \
                  "select NOC,count(*)  as Gold,0 as Silver,0 as Bronze,3*count(*) as pt from  (select NOC,GameID," \
                  "Medal from event_info where Medal='Gold')as event_info2,(select GameID from game_info where " \
                  "Games='"+a+"' )as game_info2 where event_info2.GameID=game_info2.GameID group by NOC union select " \
                              "NOC,0 as Gold,count(*) as Silver,0 as Bronze,2*count(*) as pt from  (select NOC," \
                              "GameID,Medal from event_info where Medal='Silver')as event_info2,(select GameID from " \
                              "game_info where Games='"+a+"' )as game_info2 where " \
                                                          "event_info2.GameID=game_info2.GameID group by NOC union " \
                                                          "select NOC,0 as Gold,0 as Silver,count(*) as Bronze," \
                                                          "count(*) as pt from  (select NOC,GameID,Medal from " \
                                                          "event_info where Medal='Bronze')as event_info2," \
                                                          "(select GameID from game_info where Games='"+a+"' )as " \
                                                                                                          "game_info2 " \
                                                                                                          "where " \
                                                                                                          "event_info2.GameID=game_info2.GameID group by NOC) group by NOC order by score desc; "
        cursor = con.execute(sql)
        lis = []
        if cursor == lis:
            return "NOT Found"
        return render_template('score.html', data=cursor)


if __name__ == '__main__':
    app.run()
