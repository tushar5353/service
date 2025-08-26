import os
import logging

from service.utils import database

# Initialize the logger
logger = logging.getLogger(os.environ["RUN_TYPE"])

def add(user_name, email):
    """
    Function to add a new user

    :param user_name: `str` - Name of user
    :param email: `str` - email for a user
    """
    query = f"INSERT INTO USERS(name, email) values ('{user_name}', '{email}')"
    logger.info(query)
    database.execute_statement(query)

