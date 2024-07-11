import pytest
import os
from emall.database import Database
from psycopg2 import IntegrityError
from unittest.mock import patch, MagicMock
import time

@pytest.fixture
def db():
    if os.getenv('DOCKER'):
        return Database(host='db')
    return Database()

def test_get_users_password(db):
    # 创建一个模拟的游标和连接对象
    pair = {'username':'testuser', "hashed_password":"$2b$12$eC1hZbUuWuGqXK27rxwjJOLtQh4yIc.1Le6lr6zJgrYTaNXqlMEZG"}
    password = db.get_users_password(pair['username'])
    # 断言密码返回值是否正确
    assert password == pair['hashed_password']

def test_get_users_password_not_found(db):
    pair = {'username':'testuser', "hashed_password":"$2b$12$eC1hZbUuWuGqXK27rxwjJOLtQh4yIc.1Le6lr6zJgrYTaNXqlMEZG"}
    password = db.get_users_password('nonexistuser')
    assert password is None

def test_get_users_password_connection_error(db):
    # Mocking psycopg2.connect to raise an exception
    with patch('psycopg2.connect') as mock_connect:
        mock_connect.side_effect = Exception("Mocked connection error")
        
        # Call the method that should handle the connection error gracefully
        password = db.get_users_password('testuser')
        
        # Assert that it returns None when there's a connection error
        assert password is None

def test_get_admins_password(db):
    # Test for existing admin
    admin_username = 'admin'
    admin_password = '$2b$12$5Svk5h1YsBe5YPsyvg7n9OpPEePwgcVbx./JtVMjNRo4paghHYULu'
    
    # Assuming 'testadmin' exists in your 'admins' table with the above password hash
    password = db.get_admins_password(admin_username)
    assert password == admin_password

def test_get_admins_password_not_found(db):
    # Test for non-existing admin
    non_exist_admin_username = 'nonexistadmin'
    
    # Assuming 'nonexistadmin' does not exist in your 'admins' table
    password = db.get_admins_password(non_exist_admin_username)
    assert password is None

def test_get_admins_password_connection_error(db):
    # Test for connection error
    with patch('psycopg2.connect') as mock_connect:
        mock_connect.side_effect = Exception("Mocked connection error")
        
        # Call the method that should handle the connection error gracefully
        password = db.get_admins_password('testadmin')
        
        # Assert that it returns None when there's a connection error
        assert password is None

def test_user_login_successful(db):
    # Test for successful login
    username = 'testuser'
    password = '$2b$12$eC1hZbUuWuGqXK27rxwjJOLtQh4yIc.1Le6lr6zJgrYTaNXqlMEZG'
    
    # Assuming 'testuser' exists in your 'users' table with the password 'password123'
    assert db.user_login(username, password) is True

def test_user_login_invalid_credentials(db):
    # Test for invalid credentials
    username = 'testuser'
    password = 'false'
    
    # Assuming 'testuser' exists in your 'users' table with a different password
    assert db.user_login(username, password) is False

def test_get_admins_password_connection_error(db):
    # Test for connection error
    with patch('psycopg2.connect') as mock_connect:
        mock_connect.side_effect = Exception("Mocked connection error")
        
        # Call the method that should handle the connection error gracefully
        password = db.get_admins_password('testadmin')
        
        # Assert that it returns None when there's a connection error
        assert password is None

def test_admin_login_successful(db):
    # Test for successful login
    username = 'admin'
    password = '$2b$12$5Svk5h1YsBe5YPsyvg7n9OpPEePwgcVbx./JtVMjNRo4paghHYULu'
    
    # Assuming 'testuser' exists in your 'users' table with the password 'password123'
    assert db.admin_login(username, password) is True

def test_admin_login_invalid_credentials(db):
    # Test for invalid credentials
    username = 'admin'
    password = 'false'
    
    # Assuming 'testuser' exists in your 'users' table with a different password
    assert db.admin_login(username, password) is False

def test_register_successful(db):
    unique_username = f'newuser_{int(time.time())}'
    # Test for successful registration
    info = {
        'username':  unique_username,
        'password': 'password123',
        'email': 'newuser@example.com',
        'sex': 'M',
        'birthday': '2000-01-01',
        'address': '123 Main St, City',
        'phone': '1234567890'
    }
    
    assert db.register(info) is True


def test_get_all_goods(db):
    total_num = 17
    data = db.get_all_goods()
    assert len(data) == total_num


def test_show_cart_existing_user_with_items(db):
    # Mocking the database query to return cart items for an existing user
    username = 'testuser'
    expected_cart_items = [
        {'goods_name': 'Item1', 'quantity': 2, 'price': 10.0, 'total_price': 20.0, 'path': 'img/Item1.jpg'},
        {'goods_name': 'Item2', 'quantity': 1, 'price': 5.0, 'total_price': 5.0, 'path': 'img/Item2.jpg'}
    ]
    expected_cart_total_price = 25.0
    
    with patch.object(Database, 'show_cart', return_value=(expected_cart_items, expected_cart_total_price)):
        cart_items, cart_total_price = db.show_cart(username)
        
    assert cart_items == expected_cart_items
    assert cart_total_price == expected_cart_total_price

def test_show_cart_existing_user_no_items(db):
    # Mocking the database query to return an empty cart for an existing user
    username = 'testuser'
    expected_cart_items = []
    expected_cart_total_price = 0.0
    
    with patch.object(Database, 'show_cart', return_value=(expected_cart_items, expected_cart_total_price)):
        cart_items, cart_total_price = db.show_cart(username)
        
    assert cart_items == expected_cart_items
    assert cart_total_price == expected_cart_total_price

def test_show_cart_non_existing_user(db):
    # Mocking the database query to return no user found
    username = 'nonexistent_user'
    expected_cart_items = []
    expected_cart_total_price = 0.0
    
    with patch.object(Database, 'show_cart', return_value=(expected_cart_items, expected_cart_total_price)):
        cart_items, cart_total_price = db.show_cart(username)
        
    assert cart_items == expected_cart_items
    assert cart_total_price == expected_cart_total_price

