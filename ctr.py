import sqlite3

conn = sqlite3.connect("Winsy.db")

def main(type):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM roasts WHERE type = ?""", [type])
    response = cursor.fetchall()
    for tuple in response:
        print(tuple)

main('Normal')