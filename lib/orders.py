import os
import logging

from service.utils import database

# Initialize the logger
logger = logging.getLogger(os.environ["RUN_TYPE"])

def new(user_id, product, quantity):
    engine = database.get_mysql_engine()
    conn = engine.connection()
    query = f"INSERT INTO orders(user_id, product, quantity) values ({user_id}, '{product}', {quantity})"
    logger.info(query)
    conn.execute(query)
