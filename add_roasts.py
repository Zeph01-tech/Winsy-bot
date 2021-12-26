import sqlite3

conn = sqlite3.connect('./Winsy_/Winsy.db')

roasts_list = ["It's better to let someone think you are an Idiot than to open your mouth and prove it.", "Is your ass jealous of the amount of shit that just came out of your mouth?", "Two wrongs don't make a right, take your parents as an example.", "If I wanted to kill myself I'd climb your ego and jump to your IQ.", "You must have been born on a highway because that's where most accidents happen.", "You sound reasonable. It must be time to up my medication!", "You're so ugly, when your mom dropped you off at school she got a fine for littering.", "I don't think you are stupid. You just have a bad luck when thinking."]

type = 'Normal'

def main(type, roast):
    for one in roast:
        c = conn.cursor()
        c.execute("""INSERT INTO roasts (type, roast) VALUES (?, ?)""", [type, one])
        conn.commit()

main(type=type, roast=roasts_list)