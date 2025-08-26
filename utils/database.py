import os
import logging

from service.utils.config import Config

import mysql.connector

config_obj = Config()
config = config_obj.get_config("environment")
db_config = config["db"]

# Initialize the logger
logger = logging.getLogger(os.environ["RUN_TYPE"])

def get_mysql_conn():
    mysql_config = db_config["mysql"]
    conn = mysql.connector.connect(
    user=mysql_config['user'],
    password=mysql_config['password'],
    host=mysql_config['host'],
    database=mysql_config['dbname']
    )
    return conn

def execute_statement(statement):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute(statement)
    conn.commit()

def make_migrations():
    migration_scripts = config_obj.get_config("db_migrations")
    for table, statement in migration_scripts.items():
        logger.info(f"Creating Table :: {table}")
        execute_statement(statement)

def fetch_info(statement):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute(statement)
    return cursor.fetchall()
