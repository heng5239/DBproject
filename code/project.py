import sqlite3

from flask import Flask, request, render_template


def connect():
    conn = sqlite3.connect('DBproject_new.db')
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
        if name != "" and '"' not in name :
            sql = "SELECT ID,Name,Sex,Height,Weight FROM athlete_info WHERE Name LIKE \"%" + name + "%\";"
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
              "WHERE event_info.ID = " + id + " AND event_info.Gameid = game_info.Gameid AND sport_info.Event " \
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
              "event_info, athlete_info,sport_info WHERE event_info.Event = sport_info.Event AND Gameid = "+gameid+" AND Team = \"" + team_name + "\" AND event_info.ID = athlete_info.ID; "
        cursor = con.execute(sql)
        return render_template('team_search.html', games=game, teams=team, data=cursor)


@app.route('/insert')
def insert():
    return render_template('insert.html')


@app.route('/new_athlete', methods=['POST', 'GET'])
def new_athlete():
    if request.method == 'GET':
        return render_template('new_athlete.html', comment='')
    elif request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        height = request.form.get('height')
        weight = request.form.get('weight')
        if name == '':
            comment = 'Name cannot be empty'
        elif '"' in name:
            comment = 'Don\'t input ".'
        elif sex != 'M' and sex != 'F':
            comment = 'Sex should be "M" or "F"'
        elif not height.isdigit() and height != 'NA':
            comment = 'Height should be a positive integer or "NA"'
        elif int(height) == 0:
            comment = 'Height should be a positive integer or "NA"'
        elif not weight.isdigit() and weight != 'NA':
            comment = 'Weight should be a positive integer or "NA"'
        elif int(weight) == 0:
            comment = 'Weight should be a positive integer or "NA"'
        else:
            con = connect()
            sql = "SELECT MAX(ID) FROM athlete_info"
            cursor = con.execute(sql)
            row = cursor.fetchone()
            id = row[0] + 1
            sql = "INSERT INTO athlete_info (ID, Name, Sex, Height, Weight) VALUES ( " + str(
                id) + ", \"" + name + "\", \"" + sex + "\", \"" + height + "\" ,\"" + weight + "\");"
            con.execute(sql)
            con.commit()
            comment = 'Successfully'
        return render_template('new_athlete.html', comment=comment)


@app.route('/new_game', methods=['POST', 'GET'])
def new_game():
    if request.method == 'GET':
        return render_template('new_game.html', comment='')
    elif request.method == 'POST':
        game = request.form.get('game')
        city = request.form.get('city')
        if game == '':
            comment = 'Game cannot be empty'
        elif len(game) != 11:
            comment = 'Game should be "XXXX Winter" or "XXXX Summer"'
        elif not game[0:4].isdigit():
            comment = 'Year should be an integer'
        elif game[5:11] != 'Summer' and game[5:11] != 'Winter':
            comment = 'Season should be Summer or Winter'
        elif int(game[0:4]) <= 2019:
            comment = 'Year should greater than 2019'
        elif city == '':
            comment = 'City cannot be empty'
        elif '"' in city:
            comment = 'Don\'t input ".'
        else:
            con = connect()
            sql = "INSERT INTO game_info (Games, City) VALUES (\"" + game + "\", \"" + city + "\");"
            con.execute(sql)
            con.commit()
            comment = 'Successfully'
        return render_template('new_game.html', comment=comment)


@app.route('/new_event', methods=['POST', 'GET'])
def new_event():
    con = connect()
    sql = "SELECT Gameid, Games FROM game_info"
    games = con.execute(sql)
    if request.method == 'GET':
        return render_template('new_event.html', comment='', games=games)
    elif request.method == 'POST':
        game = request.form.get('game')
        id = request.form.get('id')
        age = request.form.get('age')
        team = request.form.get('team')
        noc = request.form.get('noc')
        sport = request.form.get('sport')
        event = request.form.get('event')
        medal = request.form.get('medal')
        sql = "SELECT MAX(ID) FROM athlete_info"
        cursor = con.execute(sql)
        row = cursor.fetchone()
        maxid = row[0]
        if id == '' or team == '' or noc == '' or sport == '' or event == '':
            comment = 'Some columns are empty '
        elif not id.isdigit():
            comment = "ID should be an integer between 1 and " + str(maxid) + "."
        elif int(id) < 1 or int(id) > maxid:
            comment = "ID should be an integer between 1 and " + str(maxid) + "."
        elif not age.isdigit():
            comment = "Age should be an positive integer."
        elif int(age) <= 0:
            comment = "Age should be an positive integer."
        elif event[0:len(sport)] != sport:
            comment = "IF your sport is " + sport + ", your event should be '" + sport + "%'."
        elif not noc.isalpha() or len(noc) != 3:
            comment = 'NOC should be 3-letter code.'
        elif medal != 'Gold' and medal != 'Silver' and medal != 'Bronze' and medal != 'NA':
            comment = 'Medal should be Gold or Silver or Bronze or NA .'
        else:
            sql = "SELECT * FROM athlete_info WHERE ID = " + id + ";"
            cursor = con.execute(sql)
            if not cursor:
                comment = "Athlete doesn't exist"
            else:
                if medal == '':
                    medal = 'NA'
                if age == '':
                    age = 'NA'
                sql = "INSERT INTO event_info VALUES (" + id + ", \"" + age + "\", \"" + team + "\", \"" + noc + "\", " \
                                                                                                                 "\"" \
                      + game + "\", \"" + event + "\", \"" + medal + "\"); "
                con.execute(sql)
                con.commit()
                sql = "SELECT COUNT(*) FROM sport_info WHERE Event=\"" + event + "\" AND Sport=\"" + sport + "\" ;"
                cursor = con.execute(sql)
                row = cursor.fetchone()
                num = row[0]
                if num == 0:
                    sql = "INSERT INTO sport_info VALUES (\"" + event + "\", \"" + sport + "\");"
                    cursor = con.execute(sql)
                    con.commit()
                    comment = 'Successfully, new event'
                else:
                    comment = 'Successfully'
        return render_template('new_event.html', comment=comment, games=games)


@app.route('/score_search', methods=['POST', 'GET'])
def score_search():
    con = connect()
    sql = "SELECT * FROM game_info"
    game = con.execute(sql)
    if request.method == 'GET':
        return render_template('score.html', games=game)
    elif request.method == 'POST':
        gameid = request.form.get('game')
        sql = "SELECT NOC,SUM(Gold) AS Gold,SUM(Silver) AS Silver,SUM(Bronze) AS Bronze,SUM(pt)AS score FROM(SELECT " \
              "NOC,COUNT(*)  AS Gold,0 AS Silver,0 AS Bronze,3*COUNT(*) AS pt FROM(SELECT NOC,Event FROM (SELECT NOC," \
              "Event FROM event_info WHERE Medal='Gold' and Gameid=" + gameid + ") GROUP BY NOC,Event) GROUP BY NOC " \
                                                                                "UNION SELECT NOC,0  AS Gold," \
                                                                                "COUNT(*) AS Silver,0 AS Bronze," \
                                                                                "2*COUNT(*) AS pt FROM(SELECT NOC," \
                                                                                "Event FROM  (SELECT NOC,Event FROM " \
                                                                                "event_info WHERE Medal='Silver' and " \
                                                                                "Gameid=" + gameid + ") GROUP BY NOC," \
                                                                                                     "Event)GROUP BY " \
                                                                                                     "NOC UNION " \
                                                                                                     "SELECT NOC," \
                                                                                                     "0  AS Gold," \
                                                                                                     "0 AS Silver," \
                                                                                                     "COUNT(*) AS " \
                                                                                                     "Bronze," \
                                                                                                     "COUNT(*)AS pt " \
                                                                                                     "FROM(SELECT " \
                                                                                                     "NOC,Event FROM " \
                                                                                                     "(SELECT NOC," \
                                                                                                     "Event FROM " \
                                                                                                     "event_info " \
                                                                                                     "WHERE " \
                                                                                                     "Medal='Bronze' " \
                                                                                                     "and Gameid=" + \
              gameid + ") GROUP BY NOC,Event) GROUP BY NOC)GROUP BY NOC ORDER BY score DESC; "

        cursor = con.execute(sql)
        return render_template('score.html', data=cursor, games=game)


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
