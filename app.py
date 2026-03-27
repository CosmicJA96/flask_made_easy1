from flask import Flask,g
import sqlite3

DATABASE = 'database.db'

#initialise app
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def home():
    #home page - just the ID, Planet, number of moons, LargestMoon and Image URL
    sql = """
            SELECT Moons.PlanetID,Planets.Name,Moons.NumOfMoons,Moons.LargestMoon,Moons.ImageURL
            FROM Moons
            JOIN Planets ON Planets.PlanetID=Moons.PlanetID;
            """
    results = query_db(sql)
    return str(results)

@app.route("/moons/<int:num>")
def moons(num):
    #show num of moons on that planet
    sql = """
        SELECT * FROM Moons 
        JOIN Planets ON Planets.PlanetID=Moons.PlanetID
        WHERE Moons.NumOfMoons = ?;
        """
    result = query_db(sql,(num,),True)
    return str(result)

if __name__ == "__main__":
    app.run(debug=True)