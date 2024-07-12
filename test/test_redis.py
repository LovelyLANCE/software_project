import pytest
import redis

def test_redis_connection(redis_client):
    try:
        redis_client.ping()
    except redis.ConnectionError:
        pytest.fail("Unable to connect to Redis")
