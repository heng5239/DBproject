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
    return render_template('search.html')


@app.route('/ID', methods=['POST'])
def submitid():
    if request.method == 'POST':
        con = connect()
        a = request.form.get('ID')
        sql = ""
        if a != "" and str(int(float(a))) == a and 135571 >= int(float(a)) > 0:
            sql = "select athlete_info2.ID as ID,Name,Sex,Age,Height,Weight,Team,NOC,Games,City,Event,Medal from (" \
                  "select * from athlete_info where ID= " + a + ")as athlete_info2,(select * from event_info where " \
                                                                "ID=" + a + ")as event_info2,game_info where  " \
                                                                            "event_info2.GameID=game_info.GameID; "

        cursor = con.execute(sql)
        return render_template('search.html', data=cursor)


@app.route('/Name', methods=['POST'])
def submitname():
    if request.method == 'POST':
        con = connect()
        b = request.form.get('Name')
        sql = ""
        if b != "":
            sql = "select athlete_info2.ID as ID,Name,Sex,Age,Height,Weight,Team,NOC,Games,City,Event,Medal from (" \
                  "select * from athlete_info where Name= '" + b + "')as athlete_info2,event_info,game_info where " \
                                                                   "athlete_info2.ID=event_info.ID and " \
                                                                   "event_info.GameID=game_info.GameID; "
        cursor = con.execute(sql)
        return render_template('search.html', data=cursor)


if __name__ == '__main__':
    app.run()
