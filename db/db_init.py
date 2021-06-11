import sqlite3
import os

db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/carbgenius.db'
conn = sqlite3.connect(db_abs_path)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS cg_users")
c.execute("DROP TABLE IF EXISTS cg_restaurants")
c.execute("DROP TABLE IF EXISTS cg_food_items")
c.execute("DROP TABLE IF EXISTS cg_pictures")
c.execute("DROP TABLE IF EXISTS cg_feedback")

c.execute("""CREATE TABLE cg_users(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id            TEXT,
                    user_name            TEXT
)""")

c.execute("""CREATE TABLE cg_restaurants(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    longitude           REAL,
                    latitude           REAL,
                    chain_name    TEXT,
                    restaurant_name    TEXT
)""")

c.execute("""CREATE TABLE cg_food_items(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    restaurant_id     INTEGER,
                    item_name           TEXT,
                    item_group     TEXT,
                    carbs           INTEGER,
                    protein     INTEGER,
                    fat  INTEGER
)""")

c.execute("""CREATE TABLE cg_pictures(
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id     INTEGER,
                    request_timestamp     TEXT,
                    request_long     REAL,
                    request_lat     REAL,
                    item_group     TEXT,
                    picture_name   TEXT,
                    picture_path   TEXT
)""")

c.execute("""CREATE TABLE cg_feedback(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    title            TEXT,
                    feedback            TEXT
)""")

users = [
    ("user1", "user 1"),
    ("user2", "user 2"),
    ("user3", "user 3")
]
c.executemany("INSERT INTO cg_users (user_id,user_name) VALUES (?,?)", users)

restaurants = [
    (-88.255859, 42.217388, "McDonald's", "McDonald's"),
    (-88.257700, 42.218470, "Wendy's", "Wendy's"),
    (-88.255310, 42.217060, "Taco Bell", "Taco Bell")
]
c.executemany("INSERT INTO cg_restaurants (longitude,latitude, chain_name, restaurant_name) VALUES (?,?,?,?)", restaurants)

items = [
    (1, "Burger", "Burgers", 34),
    (2, "Burger", "Burgers", 45),
    (3, "Taco", "Tacos", 24)
]
c.executemany("INSERT INTO cg_food_items (restaurant_id,item_name, item_group, carbs) VALUES (?,?,?,?)", items)

conn.commit()
conn.close()

print("Database is created and initialized.")
print("You can see the tables with the show_tables.py script.")
