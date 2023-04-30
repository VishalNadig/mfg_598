from sqlalchemy import create_engine, MetaData
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


def encrypt_data(key: str =CONFIG['database_creds']['key'], password: str = "") -> dict:
    """Encrypt the sensitive credentials such as API key, SECRET key and Google Auth Key.

    Args:
        key (str, optional): The fernet key generated once at the start. Defaults to CONFIG['database_creds']['key'].
        password (str, optional): The password to encrypt. Defaults to "".

    Returns:
        dict: Encrypted credentials dictionary 200 if successful. 404 If the password is wrong.
    """
    if password != "":
        fernet = Fernet(key)
        return {"password": fernet.encrypt(password.encode())}
    else:
        return {404: "Error password not found!"}


def decrypt_data(key: str = CONFIG['database_creds']['key'], password: str = "") -> dict:
    """Decrypt the sensitive credentials to use for API call authentication.

    Args:
        key (str, optional): The fernet key generated once at the start. Defaults to CONFIG['database_creds']['key'].
        password (str, optional): The password to decrypt. Defaults to "".

    Returns:
        dict: Decrypted credentials dictionary 200 if successful. 404 If the password is wrong.
    """
    if password != "":
        fernet = Fernet(key)
        return {"password": fernet.decrypt(password).decode()}
    else:
        return {404: "Error password not found!"}


def get_credentials(username: str = "", first_name: str = "", last_name: str = "") -> tuple:
    """Fetch the use credentials from the database.

    Args:
        username (str, optional): The usename of the user. Defaults to "".
        first_name (str, optional): The first name of the user. Pass this argument in case the username of the user is not known. Defaults to "".
        last_name (str, optional): The last name of the user. Pass this argument in case the username of the user is not known. Defaults to "".

    Returns:
        tuple: Returns the tuple of decrypted API key and secret key of the user for API calls authentication.
        Exception: Returns an exception in case the code execution fails.
    """
    try:
        engine = create_engine(URL)

        if first_name.title() + " " + last_name.title() in engine.connect().execute("SELECT USERNAME FROM TRADING_BOT.USERS;").fetchall()[0][0]:
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
        else:
            return {404: "User Not Found!"}
    except Exception:
        return Exception


def add_user(
    first_name: str = "",
    last_name: str = "",
    api_key: str = "",
    secret_key: str = "",
    email: str = "",
    google_auth_key: str = "",
) -> dict:
    """Add API key and the secret key for a new user. If the user already exists. Return exception.

    Args:
        first_name (str, optional): First name of the user. Defaults to "".
        last_name (str, optional): Last name of the user. Defaults to "".
        api_key (str, optional): API key of the user. Defaults to "".
        secret_key (str, optional): API secret of the user. Defaults to "".
        email (str, optional): Email of the user. Defaults to "".
        google_auth_key (str, optional): The google auth key of the user. Defaults to "".

    Returns:
        dict: Returns the tuple of decrypted API key and secret key of the user for API calls authentication.
        Exception: Returns exception if failure due to unknown reasons.
    """
    user = first_name.title() + " " + last_name.title()
    engine = create_engine(URL)
    connection = engine.connect()
    encrypted_api_key = encrypt_data(password=api_key)['password'].decode("utf-8")
    encrypted_secret_key = encrypt_data(password=secret_key)['password'].decode("utf-8")
    encrypted_google_auth_key = encrypt_data(password=google_auth_key)['password'].decode("utf-8")
    try:
        if connection.execute(f""" SELECT Username from Users where Username = '{user}';""").fetchone() is not None:
            if user not in connection.execute(f""" SELECT Username from Users where Username = '{user}';""").fetchone()[0]:
                engine.connect().execute(f"""INSERT INTO trading_bot.users (Username, email, api_key, secret_key, google_auth_key)
        VALUES ('{first_name.title() + " " + last_name.title()}', '{email}', '{encrypted_api_key}', '{encrypted_secret_key}', '{encrypted_google_auth_key}');""")
                return {200: "User added!"}
            else:
                return {404: "Error user already present!"}
        else:
            engine.connect().execute(f"""INSERT INTO trading_bot.users (Username, email, api_key, secret_key, google_auth_key)
        VALUES ('{first_name.title() + " " + last_name.title()}', '{email}', '{encrypted_api_key}', '{encrypted_secret_key}', '{encrypted_google_auth_key}');""")
            return {200: "User added!"}
    except Exception:
        return Exception

def update_user(username: str = "",
    first_name: str = "",
    last_name: str = "",
    api_key: str = "",
    secret_key: str = "",
    email: str = "",
    google_auth_key: str = "",) -> dict:
    """Update the user credentials in the database.

    Args:
        username (str, optional): The username of the user. Defaults to "".
        first_name (str, optional): The first name of the user Pass this argument if the username of the user is not known. Defaults to "".
        last_name (str, optional): The last name of the users. Pass this argument if the username of the user is not known. Defaults to "".
        api_key (str, optional): The API key of the user. Defaults to "".
        secret_key (str, optional): The secret key of the user. Defaults to "".
        email (str, optional): The email ID of the user. Defaults to "".
        google_auth_key (str, optional): The google auth key of the user. Defaults to "".

    Returns:
        dict: 200 if updating the credentials was successful. 404 if the update failed or the user was not found.
    """
    engine = create_engine(URL)
    connection = engine.connect()
    if username == "":
        user = first_name.title() + " " + last_name.title()
    else:
        user = username
    encrypted_api_key = encrypt_data(password=api_key)['password'].decode("utf-8")
    encrypted_secret_key = encrypt_data(password=secret_key)['password'].decode("utf-8")
    print(encrypt_data(password=google_auth_key)['password'].decode("utf-8"))
    encrypted_google_auth_key = encrypt_data(password=google_auth_key)['password'].decode("utf-8")
    if user == connection.execute(f"""SELECT Username from USERS WHERE Username = '{user}'""").fetchone()[0]:
        if encrypted_api_key != "" and encrypted_secret_key != "" and encrypted_google_auth_key != "" and email != "":
            connection.execute(f"""UPDATE users SET api_key = '{encrypted_api_key}', secret_key = '{encrypted_secret_key}', google_auth_key = '{encrypted_google_auth_key}', email = '{email}' WHERE Username = '{user}';""")
            return {200: "User Updated"}
        elif encrypted_api_key != "" and encrypted_api_key != connection.execute(f""" SELECT API_KEY FROM USERS WHERE Username = '{user}' """).fetchone()[0]:
            connection.execute(f"""UPDATE users SET api_key = '{encrypted_api_key}' WHERE Username = '{user}';""")
            return {200: "User api_key Updated!"}
        elif encrypted_secret_key != "" and encrypted_secret_key != connection.execute(f""" SELECT SECRET_KEY FROM USERS WHERE Username = '{user}' """).fetchone()[0]:
            connection.execute(f"""UPDATE users SET secret_key = '{encrypted_secret_key}' WHERE Username = '{user}';""")
            return {200: "User secret_key Updated!"}
        elif encrypted_google_auth_key != "" and encrypted_google_auth_key != connection.execute(f"""SELECT GOOGLE_AUTH_KEY FROM USERS WHERE Username = '{user}'""").fetchone()[0]:
            connection.execute(f"""UPDATE users SET google_auth_key = '{encrypted_google_auth_key}' WHERE Username = '{user}';""")
            return {200: "User google_auth_key Updated!"}
        elif email != "" and email != connection.execute(f"""SELECT ENAUL FROM USERS WHERE Username = {user}""").fetchone()[0]:
            connection.execute(f"""UPDATE users SET email = '{email}' WHERE Username = '{user}';""")
            return {200: "User email Updated!"}
        else:
            return {400: "User Already Present!"}
    else:
        return {404: "User not Found!"}


def delete_user(username: str = "", first_name: str = "", last_name: str = "") -> dict:
    """Delete a user from the database.

    Args:
        username (str, optional): The username of the user. Defaults to "".
        first_name (str, optional): The first name of the user Pass this argument if the username of the user is not known. Defaults to "".
        last_name (str, optional): The last name of the users. Pass this argument if the username of the user is not known. Defaults to "".

    Returns:
        dict: 200 if deleting the user was successful. 404 if the delete failed or the user was not found.
    """
    engine = create_engine(URL)
    if username == "":
        user = first_name.title() + " " + last_name.title()
        print(engine.connect().execute(f"""DELETE FROM users WHERE username = '{user}';"""))
        max_id = engine.connect().execute(f"""SELECT MAX(Id) FROM users;""").fetchone()[0]
        if max_id is not None:

            engine.connect().execute(f"""ALTER TABLE USERS AUTO_INCREMENT={max_id};""")
        else:
            engine.connect().execute(f"""ALTER TABLE USERS AUTO_INCREMENT=1;""")
        return {200: "User deleted!"}
    else:
        engine.connect().execute(f"""DELETE FROM users WHERE username = '{username}';""")
        max_id = engine.connect().execute(f"""SELECT MAX(Id) FROM users;""").fetchone()[0]
        if max_id is not None:

            engine.connect().execute(f"""ALTER TABLE USERS AUTO_INCREMENT={max_id};""")
        else:
            engine.connect().execute(f"""ALTER TABLE USERS AUTO_INCREMENT=1;""")
        engine.connect().execute(f"""ALTER TABLE USERS AUTO_INCREMENT=1;""")
        return {200: "User deleted!"}


if __name__ == '__main__':
#     print(add_user("Vishal", "Nadig", "", "", "", ""))
#     print(get_credentials("Vishal Nadig"))
#     print(update_user(first_name="Vishal", last_name="Nadig", api_key="123455ADAWRWR", secret_key="ASDA1324531", email="nadigvishal", google_auth_key="ASDTWERTEWTWET123123123123"))
#     print(delete_user(username="Vishal Nadig"))
#     print(add_user("Vishal", "Nadig", "", "", "nadigvishal", ""))
#     print(get_credentials("Vishal Nadig"))

#  SELECT `AUTO_INCREMENT`
# FROM  INFORMATION_SCHEMA.TABLES
# WHERE TABLE_SCHEMA = 'trading_bot'
# AND   TABLE_NAME   = 'users';
