import os
import logging

from service.utils import database

# Initialize the logger
logger = logging.getLogger(os.environ["RUN_TYPE"])

def add(user_name, email):
    engine = database.get_mysql_engine()
    conn = engine.connection()
    query = f"INSERT INTO USERS(name, email) values ('{user_name}', '{email}')"
    logger.info(query)
    conn.execute(query)

