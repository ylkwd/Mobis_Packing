"""
This function is used to create the data-set
"""

import json
import random
import boxes as bx

import mysql.connector
from mysql.connector import errorcode
import datetime

MIN_BOXES = 10
MAX_BOXES = 36
MIN_VALUE = 50
MAX_VALUE = 500
MAX_TRUCK_LEN = 600
MIN_TRUCK_LEN = 50
MAX_TRUCK_WID = 600
MIN_TRUCK_WID = 50
MAX_TRUCK_HT = 600
MIN_TRUCK_HT = 50

truck_dim = [[random.randint(MIN_TRUCK_LEN, MAX_TRUCK_LEN), random.randint(MIN_TRUCK_WID, MAX_TRUCK_WID),
              random.randint(MIN_TRUCK_HT, MAX_TRUCK_HT)] for _ in range(5)]
NUM_BOXES = [
    [random.randint(MIN_BOXES, MAX_BOXES), random.randint(MIN_BOXES, MAX_BOXES), random.randint(MIN_BOXES, MAX_BOXES),
     random.randint(MIN_BOXES, MAX_BOXES), random.randint(MIN_BOXES, MAX_BOXES)] for _ in range(5)]
dataset = {}
i = 0
for cont, counts in zip(truck_dim, NUM_BOXES):
    for number in counts:
        # print(counts)
        # print(number,cont)
        packages = bx.generateboxes([[0, 0, 0] + cont], number)
        boxes = []
        total_value = 0
        # print(packages)
        for each in packages:
            # print(each)
            l, w, h = each[3:]
            vol = l * w * h
            value = random.randint(MIN_VALUE, MAX_VALUE)
            total_value += value
            boxes.append([l, w, h, vol, value])
        dataset[i] = {'truck dimension': cont, 'number': number, 'boxes': boxes, 'solution': packages,
                      'total value': total_value}
        i += 1

# conn = connect_database()
# print(select_data(conn))
# print(type(dataset))

# print(truck_dim)
# print(NUM_BOXES)
# print(cont)
# print(counts)

# with open('input.json', 'w') as outfile:
#     json.dump(dataset, outfile)


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

def select_data(conn,Id):
    now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    table_name = "box"
    
    mycursor = conn.cursor(dictionary=True)
    sql = """SELECT * from {table_name} where Id={Id}"""
    # value = (data_list[0], data_list[1], data_list[2],
    #          data_list[3], data_list[4])
    try:
        mycursor.execute(sql.format(table_name="data", Id =Id))
        # result = mycursor.fetchall()
        result = mycursor
        # print(type(result))
        return result
        # print("\n" + table_name + " inserted " + now)
    except mysql.connector.Error as err:
        print(err)


def dataset(result):
    dataset = {}
    i = 0
    for cont, counts in zip(truck_dim, NUM_BOXES):
        for number in counts:
            packages = bx.generateboxes([[0, 0, 0] + cont], number)
            boxes = []
            total_value = 0
            # print(packages)
            for each in packages:
                # print(each)
                l, w, h = each[3:]
                vol = l * w * h
                value = random.randint(MIN_VALUE, MAX_VALUE)
                total_value += value
                boxes.append([l, w, h, vol, value])

            dataset[i] = {'truck dimension': cont, 'number': number, 'boxes': boxes, 'solution': packages,
                        'total value': total_value}
            i += 1


# conn = connect_database()
# container = [2260,1320,1100]
# boxes = []
# i =0
# Con = "yes"
# while(Con =="yes"):

#     NumId = input("Enter id:")
#     # Count = input("Enter Quantity: ")
#     result = select_data(conn,NumId)
#     for row in result:
        
#         # SerialNum = row['SerialNumber']
#         l = float(row['Length'])
#         w = float(row['Width'])
#         h = float(row['Height'])
#         vol = l * w * h
#         weight = float(row['Weight'])
#         boxes.append([l,w,h,vol,weight])
    
#     dataset[i] = {'truck dimension': container, 'number': number, 'boxes': boxes, 'solution': packages,
#                         'total value': total_value}
#         # print("{SerialNumber}, {Length}, {Width}, {Height}, {Weight}".format(**row))
#     print(boxes)
#     Con = input("yes or no: ")

# print(type(dataset))
