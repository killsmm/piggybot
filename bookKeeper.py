import sqlite3


class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    

class BookKeeper:

    def __init__(self, db_name='accounts.db'):
        self.db_name = db_name
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS accounts (username TEXT, password TEXT, balance REAL DEFAULT 0.0, PRIMARY KEY(username))')
        c.execute('CREATE TABLE IF NOT EXISTS transactions (username TEXT, amount REAL, date TEXT, note TEXT, FOREIGN KEY(username) REFERENCES accounts(username))')
        conn.commit()


    def get_account(self, username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE username = ?', (username,))
        account = c.fetchone()
        conn.close()
        return Account(account[0], account[1])
    
    def create_account(self, username, password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('INSERT INTO accounts VALUES (?, ?, ?)', (username, password, 0.0))
        conn.commit()
        conn.close()

    def delete_account(self, username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('DELETE FROM accounts WHERE username = ?', (username,))
        conn.commit()
        conn.close()

    def update_account(self, username, password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('UPDATE accounts SET password = ? WHERE username = ?', (password, username))
        conn.commit()
        conn.close()

    def deposit(self, username, amount, date, note):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('UPDATE accounts SET balance = balance + ? WHERE username = ?', (amount, username))
        c.execute('INSERT INTO transactions VALUES (?, ?, ?, ?)', (username, amount, date, note))
        conn.commit()
        conn.close()

    def withdraw(self, username, amount, date, note):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('UPDATE accounts SET balance = balance - ? WHERE username = ?', (amount, username))
        c.execute('INSERT INTO transactions VALUES (?, ?, ?, ?)', (username, -amount, date, note))
        conn.commit()
        conn.close()
    
    def get_balance(self, username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT balance FROM accounts WHERE username = ?', (username,))
        balance = c.fetchone()[0]
        conn.close()
        return balance