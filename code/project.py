import sqlite3

from flask import Flask, request, render_template, url_for


def connect():
    conn = sqlite3.connect('..\database\DBproject.db')
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
        sql = "SELECT Name,Sex,Height,Weight FROM athlete_info WHERE ID = " + id + ";";
        cursor = con.execute(sql)
        i = cursor.fetchone()
        sql = "SELECT Age,Team,NOC,Games,City,Sport,Event,Medal FROM event_info, game_info WHERE event_info.ID = " + id + " AND event_info.Gameid = game_info.Gameid"
        cursor = con.execute(sql)
        lis = []
        if cursor == lis:
            return "NOT Found"
        return render_template('individual.html', information = i, data=cursor)

@app.route('/team_search', methods=['POST', 'GET'])
def game_search():
    con = connect()
    sql = "SELECT * FROM game_info"
    game = con.execute(sql)
    sql = "SELECT DISTINCT team FROM event_info ORDER BY team"
    team = con.execute(sql)
    if request.method == 'GET':
        return render_template('team_search.html', games = game, teams = team)
    elif request.method == 'POST':
        gameid = request.form.get('game')
        team_name = request.form.get('team')
        sql = "SELECT athlete_info.ID, Name, Sex, Age, Height, Weight, Sport, Event, Medal  FROM event_info, athlete_info WHERE Gameid = " + gameid + " AND Team = '" + team_name + "' AND event_info.ID = athlete_info.ID;"
        cursor = con.execute(sql)
        return render_template('team_search.html', games = game, teams = team, data = cursor)

@app.route('/insert')
def insert():
    return render_template('insert.html')

@app.route('/new_athlete', methods=['POST', 'GET'])
def new_athlete():
    if request.method == 'GET':
        return render_template('new_athlete.html', comment = '')
    elif request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        height = request.form.get('height')
        weight = request.form.get('weight')
        if name == '':
            comment = 'Name cannot be empty'
        elif sex != 'M' and sex != 'F':
            comment = 'Sex should be "M" or "F"'
        else:
            if height == '':
                height = 'NA'
            if weight == '':
                weight = 'NA'
            con = connect()
            sql = "SELECT MAX(ID) FROM athlete_info"
            cursor = con.execute(sql)
            row = cursor.fetchone()
            id = row[0] + 1
            sql = "INSERT INTO athlete_info (ID, Name, Sex, Height, Weight) VALUES ( " + str(id) + ", '" + name + "', '" + sex + "', '" + height + "' ,'" + weight + "');"
            con.execute(sql)
            con.commit()
            comment = 'Successfully'
        return render_template('new_athlete.html', comment = comment)

@app.route('/new_game', methods=['POST', 'GET'])
def new_game():
    if request.method == 'GET':
        return render_template('new_game.html', comment = '')
    elif request.method == 'POST':
        game = request.form.get('game')
        city = request.form.get('city')
        if game == '':
            comment = 'Game cannot be empty'
        elif city == '':
            comment = 'City cannot be empty'
        else:
            con = connect()
            sql = "INSERT INTO game_info (Games, City) VALUES ('" + game + "', '" + city + "');"
            con.execute(sql)
            con.commit()
            comment = 'Successfully'
        return render_template('new_game.html', comment = comment)

@app.route('/new_event', methods=['POST', 'GET'])
def new_event():
    con = connect()
    sql = "SELECT Gameid, Games FROM game_info"
    games = con.execute(sql)
    if request.method == 'GET':
        return render_template('new_event.html', comment = '', games = games)
    elif request.method == 'POST':
        game = request.form.get('game')
        id = request.form.get('id')
        age = request.form.get('age')
        team = request.form.get('team')
        noc = request.form.get('noc')
        sport = request.form.get('sport')
        event = request.form.get('event')
        medal = request.form.get('medal')
        if id == '' or team =='' or noc == '' or sport == '' or event == '':
            comment = 'Some columns are empty '
        else:
            sql = "SELECT * FROM athlete_info WHERE ID = " + id + ";"
            cursor = con.execute(sql)
            if cursor == []:
                comment = "Athlete doesn't exist"
            else:
                if medal == '':
                    medal = 'NA'
                if age == '':
                    age = 'NA'
                sql = "INSERT INTO event_info VALUES (" + id + ", '" + age + "', '" + team + "', '" + noc + "', " + game + ", '" + sport + "', '" + event + "', '" + medal + "');"
                con.execute(sql)
                con.commit()
                comment = 'Successfully'
        return render_template('new_event.html', comment = comment, games = games)
if __name__ == '__main__':
    app.run()