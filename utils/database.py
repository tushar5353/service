from service.utils.config import config

from sqlalchemy import create_engine, text


config_obj = Config()
config = config_obj.get_config("environment")
db_config = config["db"]

def get_mysql_engine():
    mysql_config = db_config["mysql"]
    DATABASE_URL = f"mysql+mysqlconnector://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['dbname']}"

    engine = create_engine(DATABASE_URL)
    return engine

def make_migrations():
    migration_scripts = config_obj.get_config("db_migrations")
    engine = get_mysql_engine()
    conn = engine.connect()
    for table, statement in migration_scripts.items():
        logging.info(f"Creating Table :: {table}")
        conn.execute(text(statement))
