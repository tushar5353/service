import os
import logging

from fastapi import HTTPException

from service.utils import database

# Initialize the logger
logger = logging.getLogger(os.environ["RUN_TYPE"])

def new(user_id, product, quantity):
    """
    Function to keep record for new orders
    """
    check_user_query = f"SELECT 1 from mydb.users where id={user_id}"
    info = database.fetch_info(check_user_query)
    if not len(info):
        raise HTTPException(status_code=5111, detail="User Not Found")
    query = f"INSERT INTO orders(user_id, product, quantity) values ({user_id}, '{product}', {quantity})"
    logger.info(query)
    database.execute_statement(query)
