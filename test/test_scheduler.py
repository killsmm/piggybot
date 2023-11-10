import datetime
import pytest

import sys

from ..scheduler import Scheduler
import os


@pytest.fixture
def sched():
    if os.path.isfile("schedule.db"):
        os.remove("schedule.db")
    
    return Scheduler()

    

def test_init(sched):
    assert sched.report_time.hour == 7
    assert sched.report_time.minute == 30
    assert sched.report_time.second == 0
    assert sched.report_time.microsecond == 0
    assert sched.db_path == "schedule.db"


def test_change_report_time(sched):
    new_time = datetime.datetime(2001,1,1,7,31,0)
    sched.change_report_time(new_time)
    assert sched.report_time.hour == 7
    assert sched.report_time.minute == 31
    assert sched.report_time.second == 0
    assert sched.report_time.microsecond == 0

def test_schedule_task(sched):
    target_date = datetime.datetime(2021,1,1,7,30,0)
    task_info = "test task"
    sched.schedule_task(target_date, task_info)
    tasks = sched.dump_tasks()
    assert tasks[0]["date"] == "2021-01-01"
    assert tasks[0]["info"] == "test task"

def test_dump_tasks(sched):
    target_date = datetime.datetime(2021,1,1,7,30,0)
    task_info = "test task"
    sched.schedule_task(target_date, task_info)
    tasks = sched.dump_tasks()
    assert tasks[0]["date"] == "2021-01-01"
    assert tasks[0]["info"] == "test task"
    tasks = sched.dump_tasks(datetime.datetime(2021,1,1,0,0,0))
    assert tasks[0]["date"] == "2021-01-01"
    assert tasks[0]["info"] == "test task"
    tasks = sched.dump_tasks(datetime.datetime(2021,1,2,0,0,0))
    assert len(tasks) == 0

def test_delete_task(sched):
    target_date = datetime.datetime(2021,1,1,7,30,0)
    task_info = "test task"
    sched.schedule_task(target_date, task_info)
    tasks = sched.dump_tasks()
    assert len(tasks) == 1
    sched.delete_task(tasks[0]["id"])
    tasks = sched.dump_tasks()
    assert len(tasks) == 0

def test_get_task(sched):
    target_date = datetime.datetime(2021,1,1,7,30,0)
    task_info = "test task"
    sched.schedule_task(target_date, task_info)
    task = sched.get_task(1)
    assert task["date"] == "2021-01-01"
    assert task["info"] == "test task"

def test_print_tasks(sched, capsys):
    target_date = datetime.datetime(2021,1,1,7,30,0)
    task_info = "test task"
    sched.schedule_task(target_date, task_info)
    sched.print_tasks()
    captured = capsys.readouterr()
    assert captured.out == "1 2021-01-01 test task\n"