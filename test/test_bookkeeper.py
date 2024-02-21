import pytest
from ..bookKeeper import *
import os

@pytest.fixture
def bookkeeper():
    #delete account.db file if it exists
    try:
        os.remove('account.db')
    except FileNotFoundError:
        pass
    return BookKeeper()

def test_create_account(bookkeeper):
    bookkeeper.create_account('test', 'password')
    account = bookkeeper.get_account('test')
    assert account.username == 'test'
    assert account.password == 'password'
    bookkeeper.delete_account('test')

def test_delete_account(bookkeeper):
    bookkeeper.create_account('test', 'password')
    bookkeeper.delete_account('test')
    with pytest.raises(TypeError):
        bookkeeper.get_account('test')

def test_update_account(bookkeeper):
    bookkeeper.create_account('test', 'password')
    bookkeeper.update_account('test', 'newpassword')
    account = bookkeeper.get_account('test')
    assert account.password == 'newpassword'
    bookkeeper.delete_account('test')

def test_deposit(bookkeeper):
    bookkeeper.create_account('test', 'password')
    bookkeeper.deposit('test', 100.0, '2020-01-01', 'Initial deposit')
    balance = bookkeeper.get_balance('test')
    assert balance == 100.0
    bookkeeper.delete_account('test')

def test_withdraw(bookkeeper):
    bookkeeper.create_account('test', 'password')
    bookkeeper.deposit('test', 100.0, '2020-01-01', 'Initial deposit')
    bookkeeper.withdraw('test', 50.0, '2020-01-02', 'Withdrawal')
    balance = bookkeeper.get_balance('test')
    assert balance == 50.0
    bookkeeper.delete_account('test')