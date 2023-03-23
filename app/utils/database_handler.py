from sqlalchemy import create_engine, Table, Column, Integer, MetaData, inspect, text
from sqlalchemy_utils import create_database, database_exists, drop_database
import yaml
from cryptography.fernet import Fernet

CONFIG_FILE = r"C:\Users\nadig\Arizona State University\Spring 2023\MFG 598 Engineering Computing With Python\mfg598\mfg_598\megamind_config.yaml"

with open(CONFIG_FILE, "r") as file:
    CONFIG = yaml.safe_load(file)

USER = CONFIG['database_creds']["USER"]
PASSWORD = CONFIG['database_creds']["PASSWORD"]
HOSTNAME = CONFIG['database_creds']['HOSTNAME']
DATABASE = CONFIG['database_creds']['DATABASE']
METADATA = MetaData()
URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE}"


def encrypt_data(key=CONFIG['database_creds']['key'], password = ""):
    if password != "":
        fernet = Fernet(key)
        return {"password": fernet.encrypt(password.encode())}
    else:
        return {404: "Error password not found!"}


def decrypt_data(key = CONFIG['database_creds']['key'], password = ""):
    if password != "":
        fernet = Fernet(key)
        return {"password": fernet.decrypt(password).decode()}
    else:
        return {404: "Error password not found!"}


def get_credentials(username: str = "", first_name: str = "", last_name: str = "") -> tuple:
    engine = create_engine(URL)
    if username == "":
        username = first_name.title() + " " + last_name.title()
        encrypted_api_key, encrypted_secret_key =  engine.connect().execute(f"""SELECT api_key, secret_key FROM USERS WHERE Username = '{username}'""").fetchall()[0]
        api_key = decrypt_data(password=encrypted_api_key)['password']
        secret_key = decrypt_data(password=encrypted_secret_key)['password']
    else:
        encrypted_api_key, encrypted_secret_key =  engine.connect().execute(f"""SELECT api_key, secret_key FROM USERS WHERE Username = '{username}'""").fetchall()[0]
        api_key = decrypt_data(password=encrypted_api_key)['password']
        secret_key = decrypt_data(password=encrypted_secret_key)['password']
    return api_key,secret_key


def add_user(
    first_name: str = "",
    last_name: str = "",
    api_key: str = "",
    secret_key: str = "",
    email: str = "",
    google_auth_key: str = "",
) -> None:
    """Add API key and the secret key for a new user. If the user already exists. Return exception.

    Args:
        first_name (str, optional): First name of the user. Defaults to "".
        last_name (str, optional): Last name of the user. Defaults to "".
        api_key (str, optional): API key of the user.
        secret_key (str, optional): API secret of the user.
    """
    user = first_name + last_name
    user = user.lower()
    user = user.replace(" ", "")
    dict_update = CONFIG
    engine = create_engine(URL)
    encrypted_api_key = encrypt_data(password=api_key)['password'].decode("utf-8")
    encrypted_secret_key = encrypt_data(password=secret_key)['password'].decode("utf-8")
    encrypted_google_auth_key = encrypt_data(password=google_auth_key)['password'].decode("utf-8")
    dict_dump = {
        "username": first_name.title() + " " + last_name.title(),
        "email": email,
        "api_key": api_key,
        "secret_key": secret_key,
        "google_auth_key": google_auth_key,
    }
    if user not in dict_update["trading"]["accounts"]:
        dict_update["trading"]["accounts"][user] = dict_dump
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            yaml.safe_dump(dict_update, file)

        engine.connect().execute(f"""INSERT INTO trading_bot.users (Username, email, api_key, secret_key, google_auth_key)
    VALUES ('{first_name.title() + " " + last_name.title()}', '{email}', '{encrypted_api_key}', '{encrypted_secret_key}', '{encrypted_google_auth_key}');""")
        return {200: "User added!"}
    else:
        return {404: "Error user already present!"}

def update_user(first_name: str = "",
    last_name: str = "",
    api_key: str = "",
    secret_key: str = "",
    email: str = "",
    google_auth_key: str = "",):
    user = first_name.title() + " " + last_name.title()
    encrypted_api_key = encrypt_data(password=api_key)['password'].decode("utf-8")
    encrypted_secret_key = encrypt_data(password=secret_key)['password'].decode("utf-8")
    dict_update = CONFIG
    dict_dump = {
        "username": first_name.title() + " " + last_name.title(),
        "email": email,
        "api_key": api_key,
        "secret_key": secret_key,
        "google_auth_key": google_auth_key,
    }
    if user not in dict_update["trading"]["accounts"]:
        return {404: "Error user not present!"}
    else:
        dict_update["trading"]["accounts"][user] = dict_dump
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            yaml.safe_dump(dict_update, file)
        engine = create_engine(URL)
        engine.connect().execute(f"""UPDATE users SET api_key = '{encrypted_api_key}', secret_key = '{encrypted_secret_key}' WHERE Username = {user};""")
        return {200: "User updated!"}


def delete_user(first_name: str = "", last_name: str = "", user: str = ""):
    engine = create_engine(URL)
    if user == "":
        user = first_name + last_name
        user = user.lower()
        user = user.replace(" ", "")
        user = first_name.title() + " " + last_name.title()
        print(user)
        print(engine.connect().execute(f"""DELETE FROM users WHERE username = '{user}';"""))
        return {200: "User deleted!"}
    else:
        print(user)
        engine.connect().execute(f"""DELETE FROM users WHERE username = '{user}';""")
        return {200: "User deleted!"}


def create_database_function(database: str):
    try:
        engine = create_engine(URL)
        connection = engine.connect()
        if not database_exists(URL+f"/{database}"):
            connection.execute(create_database(URL+f"/{database}"))
            return {"Ok": "Database Created!"}
        else:
            return {"Already Exists!": "Database Already Exists!"}
    except Exception as exception:
        return(None, exception)

def delete_database_function(database: str):
    try:
        engine = create_engine(URL)
        connection = engine.connect()
        if database_exists(URL+f"/{database}"):
            value = connection.execute(drop_database(URL+f"/{database}"))
            if value is None:
                return({"Ok": "Database Deleted!"})
        else:
            return({"Doesn't Exist!": "Database doesn't Exist!"})
    except Exception as exception:
        return(exception)

def create_tables(database: str,*table_names: str):
    try:
        engine = create_engine(URL+f"/{database}", echo= True)
        inspector = inspect(engine)
        if database_exists(URL+f"/{database}"):
            for table_name in table_names:
                if table_name not in inspector.get_table_names():
                    table_name  = Table(
                    f"{table_name}", METADATA,
                    Column("Id", Integer, primary_key = True))
                    table_name.create(bind=engine)
                else:
                    return("Table already exists!")
        else:
            return({"Error!": "Database Does not exist!"})
    except Exception as exception:
        return exception

def delete_tables(database: str, *table_names: str):
    try:
        engine = create_engine(URL+f"/{database}")
        inspector = inspect(engine)
        if database_exists(URL+f"/{database}"):
            for table in table_names:
                if table in inspector.get_table_names():
                    table = Table(f"{table}", MetaData(bind=engine), autoload=True, autoload_with=engine)
                    table.drop(bind = engine)
                else:
                    return("Tables don't exist!")
        else:
            return("database doesn't exist!")
    except Exception as exception:
        return exception

def insert_columns(database: str, table_name: str,  column_name: str, datatype: str, size: str, command: str):
    try:
        engine = create_engine(URL+f"/{database}")
        inpsector = inspect(engine)
        command = str(command)
        command.lower()
        if database_exists(URL+f"/{database}"):
            if table_name in inpsector.get_table_names():
                command = text(f"ALTER TABLE {table_name} ADD {column_name} {datatype}({size}) {command}")
                engine.execute(command)
                return("Successfully inserted columns!")
    except Exception as exception:
        return(exception)
        #         if len(order) > 0 and order == "first":
        #             command = text(f"ALTER TABLE {table_name} ADD {column_name} {datatype}({size}) {order}")
        #         else:
        #             return{"Error":"Invalid order!"}
        #         if len(column) > 0 and order == "after":
        #             command = text(f"ALTER TABLE {table_name} ADD {column_name} {datatype}({size}) {order} {column}")
        #     else:
        #         return {"Error":"Table does not exist!"}
        # else:
        #     return{"Error":"Database does not exist!"}

def delete_columns(database: str, table_name: str, column_name: str):

    try:
        engine = create_engine(URL+f"/{database}")
        inspector = inspect(engine)
        if database_exists(URL+f"/{database}"):
            if table_name in inspector.get_table_names():
                command = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
                engine.execute(command)
            else:
                return{"Error": "Table does not exist!"}
        else:
            return{"Error": "Database does not exist!"}
    except Exception as exception:
        return exception

def modify_column(database: str, table_name: str, column_name: str, command: str):
    try:
        engine = create_engine(URL+f"/{database}")
        inspector = inspect(engine)
        if database_exists(URL+f"{database}"):
            if table_name in inspector.get_table_names():
                    command = f"ALTER TABLE {table_name} MODIFY {column_name} {command}"
                    engine.execute(command)
            else:
                return("table doesn't exist")
        else:
            return("Database doesn't exist")
    except Exception as exception:
        return exception

def inspect_columns(database: str, table, *column: str):
    try:
        engine = create_engine(URL+ f"/{database}")
        inspector = inspect(engine)
        table = Table(f"{table}", MetaData(bind=engine), autoload=True, autoload_with=engine)
        if database_exists(URL+f"/{database}"):
            if table in inspector.get_table_names():
                return engine.execute(f"SHOW COLUMNS IN {table}").fetchall()
            elif table in inspector.get_table_names() and len(column) > 0:
                return engine.execute(f"SELECT * FROM {column}").fetchall()
            else:
                return("Table doesn't Exist!")
        else:
            return("Database doesn't exist")
    except Exception as exception:
        return exception

def query(database: str, table_name: str, filter_condition: str = ""):
    try:
        engine = create_engine(URL+ f"/{database}")
        inspector = inspect(engine)
        table = Table(f"{table_name}", MetaData(bind=engine), autoload=True, autoload_with=engine)
        if database_exists(URL+f"/{database}"):
            if table in inspector.get_table_names():
                return(engine.execute(f"SELECT * FROM {table}").fetchall())
    except Exception as exception:
        return exception

if __name__ == '__main__':
    # create_tables("trading_bot", "users")
    print(add_user("Shantha", "Krishnamurthy", "AKASDWASDASDASD", "ASWQROQW11232345", "shanthahurali", "ASDDWEQ124FDGHTSAWQWERTY"))
    print(update_user("Shantha", "Krishnamurthy", "123455ADAWRWR", "ASDA1324531"))
    # print(get_credentials(username="Shantha Krishnamurthy"))
    # print(delete_user(user="Shantha Krishnamurthy"))


# SELECT `AUTO_INCREMENT`
# FROM  INFORMATION_SCHEMA.TABLES
# WHERE TABLE_SCHEMA = 'trading_bot'
# AND   TABLE_NAME   = 'users';