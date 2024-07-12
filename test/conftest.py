import pytest
import os
import sys
from emall.app import create_app
from emall.database import Database
import redis

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['LIVESERVER_PORT'] = 5000  # 指定测试服务器的端口
    return app

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def redis_client():
    client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)
    yield client
    client.flushdb()  # 清理测试数据
