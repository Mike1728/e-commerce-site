from flask import Flask, jsonify, request, render_template, session, url_for, g
import sqlite3
app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY']= 'Thisisasecret!'

def connect_db():
    sql = sqlite3.connect('D:\Mike_vscode\sqlite-tools-win32-x86-3310100\data.db')
    sql.row_factory = sqlite3.Row
    sql.commit()
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
    

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return '<h1>Hello!!! World!!!</h1>'

@app.route('/home', methods=['POST','GET'],defaults={'name' : 'default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return render_template('home.html', name=name, display = False, mylist=['one', 'two'], Listofdictionaries=[{'name' : 'Ankit'}, {'name' : 'Divya'}])

@app.route('/json')
def json():
    return jsonify({'key' : 'value', 'listkey' : [1,2,3]})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are on the query page!</h1>'.format(name,location)

@app.route('/theform')
def theform():
    return render_template('form.html')

@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    return '<h1>Hello {}. You are from {}. You have submitted the form successfully!</h1>'.format(name,location)

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1>The ID is {}. The name is {}. The location is {}.</h1>'.format(results[0]['id'], results[0]['name'], results[0]['location'])

if __name__ == '__main__':
    app.run(debug=True)