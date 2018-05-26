import json
import MySQLdb
import MySQLdb.cursors
from functools import wraps
import flask
app = flask.Flask(__name__, static_folder='static', static_url_path='')


def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = flask.request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args,**kwargs)) + ')'
            return flask.current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)
    return decorated_function



@app.route('/')
@app.route('/index')
def index():
    return '''
<html>
    <head>
        <title>Final Project</title>
    </head>
    <body>
        <h1>Thanks for the Extension!</h1>
        You're the bomb... 4real
    </body>
</html>'''


@app.route('/Player/<player_name>')
def Player(player_name):
    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='Simon4710',
                           db='NBA_DATA',
                           cursorclass = MySQLdb.cursors.DictCursor)
    c = conn.cursor()
    c.execute('SELECT * FROM Player WHERE PlayerName=%s;', [player_name])
    if c.rowcount > 0:
        rs = c.fetchall()
        return flask.render_template('NBA.html', player_name=player_name, data=[r for r in rs])
    else:
        return flask.render_template('NBA.html', player_name=player_name)


@app.route('/PlayerShooting/<player_name>')
def PlayerShooting(player_name):
    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='Simon4710',
                           db='NBA_DATA',
                           cursorclass = MySQLdb.cursors.DictCursor)
    c = conn.cursor()
    c.execute('SELECT Year, Games, Minutes, TruePer, ThreePer, FTPer, ShotPer FROM Player JOIN Stats ON Player.StatsID = Stats.StatsID WHERE PlayerName=%s;', [player_name])
    if c.rowcount > 0:
        rs = c.fetchall()
        return flask.render_template('NBA2.html', player_name=player_name, data=[r for r in rs])
    else:
        return flask.render_template('NBA2.html', player_name=player_name)


@app.route('/PlayerTeam/<player_name>')
def PlayerTeam(player_name):
    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='Simon4710',
                           db='NBA_DATA',
                           cursorclass = MySQLdb.cursors.DictCursor)
    c = conn.cursor()
    c.execute('SELECT Year, PlayerName, Age, YearsExp, Height, Weight, Salary, TeamName FROM Player JOIN Team ON Player.TeamID = Team.TeamID WHERE PlayerName=%s;', [player_name])
    if c.rowcount > 0:
        rs = c.fetchall()
        return flask.render_template('NBA3.html', player_name=player_name, data=[r for r in rs])
    else:
        return flask.render_template('NBA3.html', player_name=player_name)


@app.route('/json/Player/<player_name>')
@support_jsonp
def json_Player(player_name):
    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='Simon4710',
                           db='NBA_DATA',
                           cursorclass = MySQLdb.cursors.DictCursor)
    c = conn.cursor()
    c.execute('SELECT * FROM Player WHERE PlayerName LIKE %s;', [player_name])
    result_list = []
    if c.rowcount > 0:
        rs = c.fetchall()
        result_list = [r for r in rs]
    s = json.dumps({'Player': result_list})
    return s


@app.route('/json/PlayerTeam/<player_name>')
@support_jsonp
def json_PlayerTeam(player_name):
    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='Simon4710',
                           db='NBA_DATA',
                           cursorclass = MySQLdb.cursors.DictCursor)
    c = conn.cursor()
    c.execute('SELECT Year, PlayerName, Age, YearsExp, Height, Weight, Salary, TeamName FROM Player JOIN Team ON Player.TeamID = Team.TeamID WHERE PlayerName=%s;', [player_name])
    result_list = []
    if c.rowcount > 0:
        rs = c.fetchall()
        result_list = [r for r in rs]
    s = json.dumps({'PlayerTeam': result_list})
    return s


@app.route('/json/PlayerShooting/<player_name>')
@support_jsonp
def json_PlayerShooting(player_name):
    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='Simon4710',
                           db='NBA_DATA',
                           cursorclass = MySQLdb.cursors.DictCursor)
    c = conn.cursor()
    c.execute('SELECT Year, Games, Minutes, TruePer, ThreePer, FTPer, ShotPer FROM Player JOIN Stats ON Player.StatsID = Stats.StatsID WHERE PlayerName=%s;', [player_name])
    result_list = []
    if c.rowcount > 0:
        rs = c.fetchall()
        result_list = [r for r in rs]
    s = json.dumps({'PlayerShooting': result_list})
    return s


#Done
@app.route('/xml/Player/<player_name>')
def xml_player(player_name):
    conn = MySQLdb.connect(host = 'localhost',
                           user='root',
                           passwd='Simon4710',
                           db='NBA_DATA',
                           cursorclass = MySQLdb.cursors.DictCursor)
    c = conn.cursor()
    c.execute('SELECT PlayerName, Year, Age, YearsExp, Height, Weight, Salary FROM Player WHERE PlayerName = %s;', [player_name])
    result_list = []
    if c.rowcount > 0:
        rs = c.fetchall()
        result_list = [r for r in rs]
        s = '<?xml version="1.0" encoding="UTF-8" ?>\n<Players>\n'
        for row in result_list:
            s += '<Player>'
            s += '<PlayerName>{}</PlayerName><Year>{}</Year><Age>{}</Age><YearsExp>{}</YearsExp><Height>{}</Height><Weight>{}</Weight><Salary>{}</Salary>'.format(row['PlayerName'],row['Year'],row['Age'],row['YearsExp'],row['Height'],row['Weight'],row['Salary'])
            s += '</Player>'
            s += '</Players>'
        return s


if __name__ == '__main__':
    app.run()
