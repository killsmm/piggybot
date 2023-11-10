from discord.ext import tasks
from datetime import datetime
import os
import sqlite3
class Scheduler:
    def __init__(self, report_time:datetime = datetime(2001,1,1,7,30,0), db_path:str = "schedule.db"):
        self.report_time : datetime = report_time
        self.db_path : str = db_path
        if not os.path.isfile(self.db_path):
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''CREATE TABLE tasks
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          target_date TEXT,
                          task_info TEXT)''')
            conn.commit()
            conn.close()
            
    def change_report_time(self, new_time:datetime):
        self.report_time = new_time

    def schedule_task(self, target_date : datetime, task_info : str):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO tasks (target_date, task_info) VALUES (?,?)", (target_date.strftime("%Y-%m-%d"), task_info))
        conn.commit()
        conn.close()
    
    def dump_tasks(self, date:datetime = None) -> 'list[dict]':
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        if date is None:
            c.execute("SELECT * FROM tasks")
        else:
            c.execute("SELECT * FROM tasks WHERE target_date = ?", (date.strftime("%Y-%m-%d"),))
        tmp = c.fetchall()
        task_list = [{"id":t[0], "date":t[1], "info":t[2]} for t in tmp]
        conn.close()
        return task_list
    
    def delete_task(self, task_id:int):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

    def get_task(self, task_id:int) -> dict:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        tmp = c.fetchone()
        task = {"id":tmp[0], "date":tmp[1], "info":tmp[2]}
        conn.close()
        return task
    
    def print_tasks(self):
        tasks = self.dump_tasks()
        for task in tasks:
            print(task["id"], task["date"], task["info"])