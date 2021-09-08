# import sqlite3

# conn = sqlite3.connect('Winsy.db')

# def main():
#     c = conn.cursor()
#     c.execute("""SELECT Ctr FROM ctr""")
#     rep = c.fetchone()
#     print(rep[-1])
# main()

def func(num):
    if num == +1:
        print("Increased")

    elif num == -1:
        print("Decreased")

func(-1)