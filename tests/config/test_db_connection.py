import os
from db_connection import DATABASE_CONFIG

def test_database_config():
    expected_config = {
        "host": "127.0.0.1",
        "port": 3306,
        "database": "test_db",
        "user": "test_user",
        "password": "test_password",
    }

    assert DATABASE_CONFIG == expected_config

def test_default_port():
    os.environ.pop("DB_PORT", None)
    from db_connection import DATABASE_CONFIG as default_config

    assert default_config["port"] == 3307
