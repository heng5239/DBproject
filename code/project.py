import sqlite3

from flask import Flask, request, render_template


def connect():
    conn = sqlite3.connect('DBproject3.db')
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
        name = request.form.get('name')
        sql = ""
        if name != "":
            sql = "SELECT ID,Name,Sex,Height,Weight FROM athlete_info WHERE Name LIKE '%" + name + "%';"
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
        i = cursor.fetchone()
        sql = "SELECT Age,Team,NOC,Games,City,Sport,event_info.Event,Medal FROM event_info, game_info, sport_info " \
              "WHERE event_info.ID = "+id+" AND event_info.Gameid = game_info.Gameid AND sport_info.Event " \
                                          "=event_info.Event; "

        cursor = con.execute(sql)
        lis = []
        if cursor == lis:
            return "NOT Found"
        return render_template('individual.html', information=i, data=cursor)


@app.route('/team_search', methods=['POST', 'GET'])
def game_search():
    con = connect()
    sql = "SELECT * FROM game_info"
    game = con.execute(sql)
    sql = "SELECT DISTINCT team FROM event_info ORDER BY team"
    team = con.execute(sql)
    if request.method == 'GET':
        return render_template('team_search.html', games=game, teams=team)
    elif request.method == 'POST':
        gameid = request.form.get('game')
        team_name = request.form.get('team')
        sql = "SELECT athlete_info.ID, Name, Sex, Age, Height, Weight, Sport, event_info.Event, Medal FROM " \
              "event_info, athlete_info,sport_info WHERE event_info.Event = sport_info.Event AND Gameid = "+gameid+" AND Team = '"+team_name+"' AND event_info.ID = athlete_info.ID; "

        cursor = con.execute(sql)
        return render_template('team_search.html', games=game, teams=team, data=cursor)


@app.route('/score_search', methods=['POST', 'GET'])
def score_search():
    con = connect()
    if request.method == 'GET':
        return render_template('score.html')
    elif request.method == 'POST':
        a = request.form.get('Games')
        sql = ""
        if a != "":
            sql = "SELECT NOC,SUM(Gold) AS Gold,SUM(Silver) AS Silver,SUM(Bronze) AS Bronze,SUM(pt)AS score FROM(" \
                  "SELECT NOC,COUNT(*)  AS Gold,0 AS Silver,0 AS Bronze,3*COUNT(*) AS pt FROM(SELECT NOC,Event FROM  " \
                  "(SELECT NOC,GameID,Medal,Event FROM event_info WHERE Medal='Gold')AS event_info2,(SELECT Gameid " \
                  "FROM game_info WHERE Games='" + a + "' )AS game_info2 WHERE event_info2.Gameid=game_info2.Gameid " \
                                                       "GROUP BY NOC,Event) GROUP BY NOC UNION SELECT NOC,0  AS Gold," \
                                                       "COUNT(*) AS Silver,0 AS Bronze," \
                                                       "2*COUNT(*) AS pt FROM(SELECT NOC,Event FROM  (SELECT NOC," \
                                                       "GameID,Medal,Event FROM event_info WHERE " \
                                                       "Medal='Silver')AS event_info2,(SELECT GameID FROM game_info " \
                                                       "WHERE Games='" + a + "' )AS game_info2 " \
                                                                             "WHERE event_info2.Gameid=game_info2" \
                                                                             ".GameID GROUP BY NOC,Event) GROUP BY " \
                                                                             "NOC UNION SELECT NOC,0  AS Gold," \
                                                                             "0 AS Silver," \
                                                                             "COUNT(*) AS Bronze,COUNT(*) AS pt FROM(" \
                                                                             "SELECT NOC,Event FROM  (SELECT NOC," \
                                                                             "GameID,Medal,Event FROM event_info " \
                                                                             "WHERE Medal='Bronze')AS event_info2," \
                                                                             "(SELECT Gameid FROM game_info WHERE " \
                                                                             "Games='" + a + "' )AS game_info2 WHERE " \
                                                                                             "event_info2.Gameid" \
                                                                                             "=game_info2.Gameid " \
                                                                                             "GROUP BY NOC," \
                                                                                             "Event) GROUP BY NOC) " \
                                                                                             "GROUP BY NOC ORDER BY " \
                                                                                             "score DESC; "
        cursor = con.execute(sql)
        return render_template('score.html', data=cursor)


@app.route('/bio_data', methods=['POST', 'GET'])
def bio_data_search():
    con = connect()
    sql = "SELECT * FROM game_info"
    game = con.execute(sql)
    if request.method == 'GET':
        return render_template('bio_data.html', games=game)
    elif request.method == 'POST':
        gameid = request.form.get('game')
        sql = "SELECT Sport,Sex,round(AVG(CAST(Height AS REAL)),2)AS AVGHeight,round(AVG(CAST(Weight AS REAL))," \
              "2)AS AVGWeight FROM  (SELECT DISTINCT ID,Sport FROM event_info, sport_info WHERE sport_info.Event = " \
              "event_info.Event AND Medal!='NA' AND Gameid = " + \
              gameid + ")AS event_info2,athlete_info WHERE  event_info2.ID=athlete_info.ID AND " \
                       "athlete_info.Height!='NA' AND athlete_info.Weight!='NA'  GROUP BY Sport,Sex ORDER BY " \
                       "AVGHeight DESC; "

        cursor = con.execute(sql)
        return render_template('bio_data.html', games=game, data=cursor)


if __name__ == '__main__':
    app.run()
