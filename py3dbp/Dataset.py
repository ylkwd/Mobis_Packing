import random
import mysql.connector
from mysql.connector import errorcode
import datetime
import json


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


def select_data(conn, Id, table_name):
    now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    # table_name = "box"

    mycursor = conn.cursor(dictionary=True)
    sql = """SELECT * from {table_name} where Id={Id}"""
    # value = (data_list[0], data_list[1], data_list[2],
    #          data_list[3], data_list[4])
    try:
        mycursor.execute(sql.format(table_name=table_name, Id=Id))
        # result = mycursor.fetchall()
        result = mycursor
        # print(type(result))
        # print(result)
        return result

        # print("\n" + table_name + " inserted " + now)
    except mysql.connector.Error as err:
        print(err)


def select_Box_serial(conn, SerialNumber):
    now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    table_name = "box"
    id = '{}'.format(SerialNumber)
    # print(type(id))
    mycursor = conn.cursor(dictionary=True)
    sql = """SELECT * from {table_name} where (SerialNumber = '{SerialNumber}')"""
    # value = (data_list[0], data_list[1], data_list[2],
    #          data_list[3], data_list[4])
    try:
        mycursor.execute(sql.format(table_name=table_name, SerialNumber=id))
        # result = mycursor.fetchall()
        result = mycursor
        # print(type(result))
        # print(result)
        return result
        # print("\n" + table_name + " inserted " + now)
    except mysql.connector.Error as err:
        print(err)


def select_Crate_serial(conn, SerialNumber):
    now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    table_name = "container"
    id = '{}'.format(SerialNumber)
    # print(type(id))
    mycursor = conn.cursor(dictionary=True)
    sql = """SELECT * from {table_name} where (SerialNumber = '{SerialNumber}')"""
    # value = (data_list[0], data_list[1], data_list[2],
    #          data_list[3], data_list[4])
    try:
        mycursor.execute(sql.format(table_name=table_name, SerialNumber=id))
        # result = mycursor.fetchall()
        result = mycursor
        # print(type(result))
        # print(result)
        return result
        # print("\n" + table_name + " inserted " + now)
    except mysql.connector.Error as err:
        print(err)


def select_all_crate(conn):
    now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    table_name = "container"
    # id = '{}'.format(SerialNumber)
    # print(type(id))
    mycursor = conn.cursor(dictionary=True)
    sql = """SELECT * from {table_name} """
    # value = (data_list[0], data_list[1], data_list[2],
    #          data_list[3], data_list[4])
    try:
        mycursor.execute(sql.format(table_name=table_name))
        # result = mycursor.fetchall()
        result = mycursor
        # print(type(result))
        # print(result)
        return result
        # print("\n" + table_name + " inserted " + now)
    except mysql.connector.Error as err:
        print(err)


def select_all_box(conn):
    now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    table_name = "box"
    # id = '{}'.format(SerialNumber)
    # print(type(id))
    mycursor = conn.cursor(dictionary=True)
    sql = """SELECT * from {table_name}"""
    # value = (data_list[0], data_list[1], data_list[2],
    #          data_list[3], data_list[4])
    try:
        mycursor.execute(sql.format(table_name=table_name))
        # result = mycursor.fetchall()
        result = mycursor
        # print(type(result))
        print(result)
        return result
        # print("\n" + table_name + " inserted " + now)
    except mysql.connector.Error as err:
        print(err)


# def dataset(result):
#     dataset = {}
#     i = 0
#     for cont, counts in zip(truck_dim, NUM_BOXES):
#         for number in counts:
#             packages = bx.generateboxes([[0, 0, 0] + cont], number)
#             boxes = []
#             total_value = 0
#             # print(packages)
#             for each in packages:
#                 # print(each)
#                 l, w, h = each[3:]
#                 vol = l * w * h
#                 value = random.randint(MIN_VALUE, MAX_VALUE)
#                 total_value += value
#                 boxes.append([l, w, h, vol, value])

#             dataset[i] = {'truck dimension': cont, 'number': number, 'boxes': boxes, 'solution': packages,
#                         'total value': total_value}
#             i += 1

def Packing_Prepare(conn, Container, Boxes):
    # conn = connect_database()
    ContainerId = Container[0]
    container = []
    i = 0
    ConResult = select_data(conn, ContainerId, "container")
    for row in ConResult:
        container = [float(row['Length']), float(row['Width']), float(row['Height'])]
    print(container)
    boxes = []
    number = 0
    total_value = 0
    dataset = {}
    solution = []
    for each in Boxes:
        print(type(each[0]))
        BoxeId = int(each[0])
        # exit(0)
        result = select_data(conn, BoxeId, "box")
        for row in result:
            id = row['Id']
            # SerialNum = row['SerialNumber']
            l = float(row['Length'])
            w = float(row['Width'])
            h = float(row['Height'])
            vol = l * w * h
            weight = float(row['Weight'])
            value = 10
            total_value += value
            # total_value += weight
            boxes.append([l, w, h, vol, value])
            solution.append([0, 0, id, l, w, h])

    number = len(Boxes)
    dataset[i] = {'truck dimension': container, 'number': number, 'boxes': boxes, 'solution': solution,
                  'total value': total_value}
    # print(dataset)
    with open('input.json', 'w') as outfile:
        json.dump(dataset, outfile)
    return dataset


def test_example():
    conn = connect_database()
    container = [1320, 1130, 1230]
    boxes = []
    i = 0
    Con = "yes"
    number = 0
    total_value = 0
    dataset = {}
    solution = []
    # while(number<=47):
    while (Con == "yes"):

        NumId = input("Enter id:")
        # NumId = random.randint(151,1000)
        # NumId = 939
        Count = input("Enter Quantity: ")
        for j in range(0, int(Count)):
            result = select_data(conn, NumId, "box")

            for row in result:
                id = row['Id']
                # SerialNum = row['SerialNumber']
                l = float(row['Length'])
                w = float(row['Width'])
                h = float(row['Height'])
                vol = l * w * h
                weight = float(row['Weight'])
                value = 10
                total_value += value
                # total_value += weight
                boxes.append([l, w, h, vol, value])
                solution.append([0, 0, id, l, w, h])

            j += 1

        number += int(Count)
        # print(boxes)
        # number +=1
        # number = len(boxes)
        Con = input("yes or no: ")
        print(len(boxes), len(solution))
    # print(boxes,number)
    dataset[i] = {'truck dimension': container, 'number': number, 'boxes': boxes, 'solution': solution,
                  'total value': total_value}
    # print("{SerialNumber}, {Length}, {Width}, {Height}, {Weight}".format(**row))

    with open('input.json', 'w') as outfile:
        json.dump(dataset, outfile)

    print(dataset)
    # return dataset

conn = connect_database()
# result = select_Box_serial(conn, '13270-08001')
#
# # result= select_data(conn,25)
#
# for row in result:
#     print(row)
# # test_example()

# conn = connect_database()
# result = select_all_crate(conn)
# boxresult = select_all_box(conn)

# ressult = Packing_Prepare(conn,[1],[14,14,14])
# test_example()