import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection()

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except sqlite3.Error as e:
            print(e)
            return None

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)

    def insert_hotel(self, hotel):
        sql = ''' INSERT INTO hotels(city, name, cleanliness, room, service, location, value, safety, comfort, transportation, noise)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, hotel)
        self.conn.commit()
        return cur.lastrowid

    def select_all_hotels(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM hotels")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def select_hotels_by_city(self, city):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM hotels WHERE city=?", (city,))
        rows = cur.fetchall()
        if rows is None:
            return []
        return rows

    def close_connection(self):
        if self.conn:
            self.conn.close()
