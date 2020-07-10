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
        sql = "SELECT Name,Sex,Height,Weight FROM athlete_info WHERE ID = " + id + ";";
        cursor = con.execute(sql)
        s = cursor.fetchone()
        sql = "SELECT Age,Team,NOC,Games,City,Sport,Event,Medal FROM event_info, game_info WHERE event_info.ID = " + id + " AND event_info.Gameid = game_info.Gameid"
        cursor = con.execute(sql)
        lis = []
        if cursor == lis:
            return "NOT Found"
        return render_template('individual.html', status = s, data=cursor)


if __name__ == '__main__':
    app.run()