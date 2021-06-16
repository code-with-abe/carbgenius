import sqlite3
import os

db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/carbgenius.db'

print("Options: (users, restaurants, food, pictures, feedback, all)")
table = input("Show table: ")

conn = sqlite3.connect(db_abs_path)
c = conn.cursor()


def show_users():
    try:
        users = c.execute("""SELECT
                                c.user_id, c.user_name
                             FROM
                                cg_users AS c
        """)

        print("USERS")
        print("#############")
        for row in users:
            print("user_id:             ", row[0]),
            print("user_name:          ", row[1]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()


def show_restaurants():
    try:
        comments = c.execute("""SELECT
                                c.id,c.restaurant_name, c.longitude,c.latitude
                             FROM
                                cg_restaurants AS c
        """)

        print("RESTAURANTS")
        print("#############")
        for row in comments:
            print("ID:             ", row[0]),
            print("Restaurant:        ", row[1]),
            print("Longitude:           ", row[2]),
            print("Latitude:           ", row[3]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()


def show_feedback():
    try:
        comments = c.execute("""SELECT
                                c.id,c.title, c.feedback
                             FROM
                                cg_feedback AS c
        """)

        print("FEEDBACK")
        print("#############")
        for row in comments:
            print("ID:             ", row[0]),
            print("Title:        ", row[1]),
            print("Feedback:           ", row[2]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()

def show_pictures():
    try:
        comments = c.execute("""SELECT
                                c.id,c.request_timestamp, c.picture_name
                             FROM
                                cg_pictures AS c
        """)

        print("PICTURES")
        print("#############")
        for row in comments:
            print("ID:             ", row[0]),
            print("Timestamp:        ", row[1]),
            print("Picture Name:           ", row[2]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()

if table == "users":
    show_users()
elif table == "restaurants":
    show_restaurants()
elif table == "feedback":
    show_feedback()
elif table == "pictures":
    show_pictures()
elif table == "all":
    show_users()
    show_restaurants()
else:
    print("This option does not exist.")

conn.close()
