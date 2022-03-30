import sqlite3


class SQbanshik:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def banshik_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_human(self, user_id, full_name, amount=0, bath=''):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, full_name, amount, bath) VALUES (?,?,?,?)",
                                       (user_id, full_name, amount, bath))

    def get_amount(self):
        items = self.cursor.execute("SELECT rowid, full_name, amount FROM users").fetchall()
        for _ in items:
            cash_people = f"{items[0]} \n {items[1]} \n {items[2]} \n {items[3]} \n {items[4]} \n "\
                     f"{items[5]} \n {items[6]} \n {items[7]} \n {items[8]} \n {items[9]}"
            return cash_people

    def get_bath(self):
        items = self.cursor.execute("SELECT rowid, full_name, bath FROM users").fetchall()
        for _ in items:
            people_go = f"{items[0]} \n {items[1]} \n {items[2]} \n {items[3]} \n {items[4]} \n "\
                     f"{items[5]} \n {items[6]} \n {items[7]} \n {items[8]} \n {items[9]}"
            return people_go

    def get_kubyshka(self):
        items = self.cursor.execute("SELECT money FROM kubyshkas").fetchone()[0]
        return items

    def add_kubyshka(self, money):
        return self.cursor.execute("UPDATE kubyshkas SET money = money + ?", (money,))

    def delete_kubyshka(self, money):
        return self.cursor.execute("UPDATE kubyshkas SET money = money - ?", (money,))

    def update_bath(self, bath, user_id):
        return self.cursor.execute("UPDATE users SET bath = ? WHERE user_id = ?", (bath, user_id))

    def update_everyone_bath_house(self, bath):
        return self.cursor.execute("UPDATE users SET bath = ?", (bath,))

    def update_amount(self, amount, user_id):
        return self.cursor.execute("UPDATE users SET amount = ? WHERE user_id = ?", (amount, user_id))

    def update_everyone_amount(self, amount):
        return self.cursor.execute("UPDATE users SET amount = ?", (amount,))

    def close(self):
        self.connection.close()
