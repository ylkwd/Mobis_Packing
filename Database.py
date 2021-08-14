import mysql.connector
from mysql.connector import errorcode
import datetime


def connect_database():
    try:
        cnx = mysql.connector.connect(user='root',
                                      password='123456',
                                      database='mobis',
                                      host='127.0.0.1',
                                      auth_plugin='mysql_native_password')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("error")
            print(err)
    else:
        print("connected")
        return cnx


def create_table_cur(conn,table_name):

    mycursor = conn.cursor()
    mycursor.execute("DROP TABLE IF EXISTS {table_name}".format(table_name=table_name))
    sql = """CREATE TABLE IF NOT EXISTS {table_name} (Id INT AUTO_INCREMENT PRIMARY KEY,
        SerialNumber VARCHAR(255),
        Length VARCHAR(255),
        Width VARCHAR(255),
        Height VARCHAR(255),
        Weight VARCHAR(255))"""
    mycursor.execute(sql.format(table_name=table_name))
    # mycursor.execute(
    #     )
    # mycursor.execute("CREATE TABLE customers")
    print("Table is created")


def insert_data(conn, data_list):
    now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    table_name = "box"
    mycursor = conn.cursor()
    sql = """INSERT INTO {table_name}
            (SerialNumber, Length, Width, Height, Weight)
             VALUES (%s, %s, %s, %s, %s)"""
    value = (data_list[0], data_list[1], data_list[2],
             data_list[3], data_list[4])
    try:
        mycursor.execute(sql.format(table_name=table_name), value)
        conn.commit()

        # print("\n" + table_name + " inserted " + now)
    except mysql.connector.Error as err:
        print(err)
        print("Message", err.msg)


def select_data(conn):
    now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    table_name = "box"
    mycursor = conn.cursor(dictionary=True)
    sql = """SELECT * from {table_name}"""
    # value = (data_list[0], data_list[1], data_list[2],
    #          data_list[3], data_list[4])
    try:
        mycursor.execute(sql.format(table_name=table_name))
        # result = mycursor.fetchall()
        result = mycursor
        # print(type(result))
        return result
        # print("\n" + table_name + " inserted " + now)
    except mysql.connector.Error as err:
        print(err)
        print("Message", err.msg)

def select_all_crate(conn):
    now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    table_name = "container"
    mycursor = conn.cursor(dictionary=True)
    sql = """SELECT * from {table_name}"""
    # value = (data_list[0], data_list[1], data_list[2],
    #          data_list[3], data_list[4])
    try:
        mycursor.execute(sql.format(table_name=table_name))
        # result = mycursor.fetchall()
        result = mycursor
        # print(type(result))
        return result
        # print("\n" + table_name + " inserted " + now)
    except mysql.connector.Error as err:
        print(err)
        print("Message", err.msg)

def close_connection(conn):
    conn.close()

# conn = connect_database()
# create_table_cur(conn,"data")
# # select_data(conn)
#
# # for row in select_data(conn):
# #     print(row, '\n')
# print(select_data(conn))
# # print(conn)
