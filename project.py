import sqlite3

from flask import Flask, request, render_template, url_for


def connect():
    conn = sqlite3.connect('dbtmp.db')
    return conn


def disconnect(conn):
    conn.close()


app = Flask(__name__)


# @app.route('/')
# def home():
#     return "HI"

@app.route('/')
def home():
    return render_template('search.html')


@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        con = connect()
        a = request.form.get('name')
        sql = ""
        if a != "" and str(int(float(a)))==a and 135571 >= int(float(a)) > 0 :
            sql = "select athlete_info.ID as ID,Name,Sex,Age,Height,Weight,Team,NOC,Games,City,Sport,Event,Medal from athlete_info,event_info,game_info where athlete_info.ID= " + a+" and athlete_info.ID=event_info.ID and event_info.GameID=game_info.GameID;"
        cursor = con.execute(sql)
        lis = []
        if cursor == lis:
            return "NOT Found"
        return render_template('search.html', data=cursor)


if __name__ == '__main__':
    app.run()
