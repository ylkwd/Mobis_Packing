import operator
import sys
from py3dbp import Packer, Bin, Item
# import Dataset as Dataset
import json
from py3dbp import visualize as vis2
from py3dbp.constants import RotationType, Axis
import os
import datetime


# def packing():
#     next_items
# Dataset.test_example()
def Mul_packing():
    packer = Packer()
    Box_Quantity = []
    ColorPair = {}
    next_items = {}
    boxes_sorted =[]
    packages_sorted =[]
    container = {}
    count = 0
    Count = 0
    filename = 'input'
    with open('{}.json'.format(filename), 'r') as outfile:
        data = json.load(outfile)
    # with open('input_example1.json', 'r') as outfile:
    #     data = json.load(outfile)
    # container  = Dataset.test_example()
    # # container = dataset
    # print(container)
    # exit()
    problem_indices = list(data.keys())
    for p_ind in problem_indices:
        truck_dimension = data[p_ind]['truck dimension']
        packages = data[p_ind]['solution']
        print(packages)
        boxes = data[p_ind]['boxes']
        serial_box = data[p_ind]['Box Serials']
        print(boxes)

        total_value = data[p_ind]['total value']
        box_count = data[p_ind]['number']
        boxes_Id = []
        boxes_Serial = []

        # for i in range(len(truck_dimension)):

        packer.add_bin(Bin('large-2-box', 2, truck_dimension[0], truck_dimension[2], truck_dimension[1], 700000.0))
        # print(truck_dimension)
        # exit()
        for each in boxes:
            Box_Quantity.append(each[4])
        print(Box_Quantity)
        # exit()
        for j in range (0,len(Box_Quantity)):
            # for quantity in Box_Quantity:
            #     print(Box_Quantity.index(quantity))
            for i in range(0, Box_Quantity[j]):
                # print(each)
                # print(serial_box[i][0])
                # print(packages[i][2])
                packer.add_item(Item(packages[j][2], serial_box[j][0], packages[j][3], packages[j][5], packages[j][4], 2))
                boxes_Id.append(packages[j][2])
                boxes_Serial.append(serial_box[j][0])
        # exit()
    # print(boxes_Serial)
    # print(len(boxes_Serial))
    # exit()

    color_index, Color_Id = vis2.draw(pieces=packages, title="True Solution Packing")
    # for each in Color_Id:
    #     print(each)
    #
    #     # index = Color_Id.index(each)
    #     color = Color_Id[each]
    #     # print(boxes_Serial[index])
    #     ColorPair[count + 1] = {serial_box[count][0]: color}
    #     count += 1
    # packer.add_item(Item('Box', box[2], box[3], box[5], box[4], 2))
    cratevolume = float(truck_dimension[0] * truck_dimension[1] * truck_dimension[2])
    total_packed =0

    # Create a folder to save output files
    current_time = datetime.datetime.now()  # Get current time
    folder_name = current_time.strftime("%Y-%m-%d %H%M%S")  # Format time into folder name
    os.makedirs(folder_name, exist_ok=True)  # Make folder

    while len(packer.items) > 0:
        packer.pack()
        next_items = {}
        results = []
        finalresult = {}
        layout = []
        # layout = {}
        # ColorPair = {}
        boxesvolume =0
        count =0
        # color_index, Color_Id = vis2.draw(pieces=packages, title="True Solution Packing")
        # for each in Color_Id:
        #     # print(each)
        #
        #     index = boxes_Id.index(each)
        #     count +=1
        #     color = Color_Id[each]
        #     print(boxes_Serial[index])
        #     ColorPair[count] = {boxes_Serial[index]:color}
        # print(ColorPair)
        # exit()
        # print(len(color_index[0]),len(color_index[2]))



        for b in packer.bins:
            print(":::::::::::", b.string())

            print("FITTED ITEMS:")
            for item in b.items:
                print("====> ", item.string())
                boxesvolume += float(item.width * item.depth * item.height)
                if item.rotation_type == RotationType.RT_WHD:
                    results.append(
                        [int(item.Id), float(item.position[0]), float(item.position[2]), float(item.position[1]), float(item.width),
                         float(item.depth), float(item.height),item.name])

                else:
                    results.append(
                        [int(item.Id),float(item.position[0]), float(item.position[2]), float(item.position[1]), float(item.depth),
                         float(item.width), float(item.height),item.name])

            layout.append(results)

            # with open('output.json'.format(file_count=Count), 'a') as outfile:
            #     json.dump(finalresult, outfile)
            # print(results)
            # print(finalresult)
            # print(color_index)

            print("UNFITTED ITEMS:")
            # exit(0)
            count = 0
            for item in b.unfitted_items:
                print("====> ", item.string())

                # print(item.name,int(item.width),type(item.width))
                next_items[count] = {'Id': item.Id, 'name': item.name, 'width': int(item.width),
                                     'height': int(item.height),
                                     "depth": int(item.depth), "weight": int(item.weight)}
                count += 1

            packer.unfitted_items = []
            print(count)
            print("***************************************************")
            print("***************************************************")

            for each in layout:
                print(each)
                sorted_result = sorted(each, key=operator.itemgetter(3))
                # print(sorted_result,len(sorted_result))
                # exit()
                ## print result level by level
                crate_no = 'Crate ' + str(Count+1)
                box_quantity = 'Number of boxes: ' + str(len(each))
                total_packed += len(each)


                # Create txt output file for each crate
                with open(os.path.join(folder_name, 'Crate ' + str(Count+1) + '.txt'), 'w') as f:
                    [f.write(crate_no + '    ' + box_quantity + '\n')]
                    [f.write('----------------------------------------------------------------\n')]
                    [f.write('|Serial Number|     COORDINATES     |     DIMENSION     |  ID  |\n')]
                    [f.write(f'| {line[7]} | {line[1]} | {line[2]} | {line[3]} | {line[4]} | {line[5]} | {line[6]} | {line[0]}\n') for line in
                     each]
                    [f.write(f'Total Number of Boxes Packed: {total_packed}')]

                # f = open("output_{}.txt".format(filename), "a")
                # f.write("Here is the lists of boxes:Figure {} # of box: {},# of total packed box: {} \n ".format(
                #     Count + 1, len(each), total_packed))
                # f.write(str(each))
                # f.write("\n")
                # f.write("\n")


                # finalresult[Count] = {'Crate dimension': truck_dimension, 'Color index': color_index[1],
                #                       'volume percent': boxesvolume / cratevolume * 100.0,
                #                       'box quantity': len(sorted_result), 'box layout': sorted_result}
                #####Write results in file######
                # with open('{}output_Mutiple{}.json'.format(filename, Count + 1), 'w') as outfile:
                #     json.dump(finalresult, outfile)

                for i in range(0, len(sorted_result)):
                    # print(i)
                    if i >= 1:
                        if sorted_result[i][3] == sorted_result[i - 1][3]:
                            layout_box.append(sorted_result[i])
                            count += 1
                        else:
                            # vis2.draw(layout_box, color_index, title="Figure {},level {}, # of box: {},{} ".format(Count + 1, level + 1, count,ColorPair))
                            # f = open("output_{}.txt".format('input_example1'), "a")
                            # f.write("Here is the lists of boxes:Figure {}, Level: {}, # of box: {}, \n {}".format(Count + 1, level + 1, count,ColorPair))
                            # for each in layout_box:
                            #     f.write(str(each))
                            #     f.write("\n")
                            # f.close()
                            level += 1
                            layout_box.append(sorted_result[i])
                            count += 1
                            # layout_box = []
                    else:
                        layout_box = []
                        level = 0
                        count = 1
                        layout_box.append(sorted_result[i])
                #
                vis2.draw(each, color_index, truck_dimension,
                          title="Figure {},# of boxes: {},volume percent:{}, {} "
                          .format(Count + 1, len(each), boxesvolume / cratevolume * 100.0, ColorPair))
                # ####
            # for each in sorted_result:

        packer.items = []
        packer.bins = []
        for i in list(next_items.keys()):
            # print()
            packer.add_item(
                Item(next_items[i]['Id'], next_items[i]['name'], next_items[i]['width'], next_items[i]['height'],
                     next_items[i]['depth'],
                     next_items[i]['weight']))
        packer.add_bin(Bin('large-2-box', 2, truck_dimension[0], truck_dimension[2], truck_dimension[1], 7000.0))
        print(len(packer.items))
        print(len(packer.unfitted_items))
        print(len(packer.bins))
        Count += 1

def start():
    Mul_packing()

if __name__ == "__main__":
    start()
    # conn.close()
