import sqlite3
import os

conn = sqlite3.connect("Winsy.db")

list = os.listdir()
id = 123
images = []
rick_check = []

def check_rick_func(user_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM faces WHERE user_id = ?""", [user_id])
    response = cursor.fetchall()
    if len(response) == 0:
        return False

    else:
        return True

for file in list:
    if ".jpg" in file:
        if file != 'temp.jpg':
            images.append(file)

    elif "temp.gif" in file:
        check = check_rick_func(id)
        if check == True:
            continue
        else:
            images.append(file)

def main():
    for image in images:
        bytes = get_bytes(image)
        add_image(id, bytes)

def get_bytes(image):
    with open(image, 'rb') as f:
        bytes = f.read()
    return bytes

def add_image(user_id, image):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO faces (user_id, image) VALUES (?, ?)""", [user_id, image])
    conn.commit()

main()