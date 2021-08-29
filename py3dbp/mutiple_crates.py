import operator

from py3dbp import Packer, Bin, Item
# import Dataset as Dataset
import json
from py3dbp import visualize as vis2
from py3dbp.constants import RotationType, Axis


# def packing():
#     next_items
# Dataset.test_example()
def Mul_packing():
    packer = Packer()
    Box_Quantity = []
    next_items = {}

    container = {}
    count = 0
    Count = 0
    with open('../input.json', 'r') as outfile:
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
        print(len(packages))
        boxes = data[p_ind]['boxes']
        serial_box = data[p_ind]['Box Serials']
        print(len(boxes))
        total_value = data[p_ind]['total value']
        box_count = data[p_ind]['number']
        boxes_Id = []
        boxes_Serial = []

        # for i in range(len(truck_dimension)):

        packer.add_bin(Bin('large-2-box', 2, truck_dimension[0], truck_dimension[2], truck_dimension[1], 700000.0))
        for each in boxes:
            Box_Quantity.append(each[4])

        # for i in range(0, len(packages)):
        #     # print(each)
        #     # print(serial_box[i][0])
        #     # print(packages[i][2])
        #     packer.add_item(Item(packages[i][2], serial_box[i][0], packages[i][3], packages[i][5], packages[i][4], 2))
        #     boxes_Id.append(packages[i][2])
        #     boxes_Serial.append(serial_box[i][0])
    ColorPair = {}
    count = 0
    color_index, Color_Id = vis2.draw(pieces=packages, title="True Solution Packing")
    print(Color_Id)
    # exit(0)
    for each in Color_Id:
        print(each)

        index = boxes_Id.index(each)
        count += 1
        color = Color_Id[each]
        # print(boxes_Serial[index])
        ColorPair[count] = {boxes_Serial[index]: color}

    for quantity in Box_Quantity:
        for i in range(0, quantity):
            packer.add_item(
                Item(packages[Box_Quantity.index(quantity)][2], serial_box[Box_Quantity.index(quantity)][0], packages[Box_Quantity.index(quantity)][3],
                     packages[Box_Quantity.index(quantity)][5], packages[Box_Quantity.index(quantity)][4], 2))
            boxes_Id.append(packages[Box_Quantity.index(quantity)][2])
            boxes_Serial.append(serial_box[Box_Quantity.index(quantity)][0])

        print(boxes_Id,boxes_Serial)
        packer.pack()
        next_items = {}
        results = []
        finalresult = []
        layout = {}

        # print(ColorPair)
        # exit()
        # print(len(color_index[0]),len(color_index[2]))

        for b in packer.bins:
            print(":::::::::::", b.string())

            print("FITTED ITEMS:")
            for item in b.items:
                print("====> ", item.string())
                if item.rotation_type == RotationType.RT_WHD:
                    results.append(
                        [int(item.Id), float(item.position[0]), float(item.position[2]), float(item.position[1]),
                         float(item.width),
                         float(item.depth), float(item.height), item.name])

                else:
                    results.append(
                        [int(item.Id), float(item.position[0]), float(item.position[2]), float(item.position[1]),
                         float(item.depth),
                         float(item.width), float(item.height), item.name])
            finalresult.append(results)

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
            for each in finalresult:
                # print(each)
                sorted_result = sorted(each, key=operator.itemgetter(3))
                print(sorted_result,len(sorted_result))
                exit()
                ## print result level by level
                f = open("output_{}.txt".format('input_example1'), "a")
                f.write(
                    "Here is the lists of boxes:Figure {} # of box: {}, \n {}".format(Count + 1, len(each), ColorPair))
                f.write(str(each))
                f.write("\n")

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
                            f.close()
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
                          title="Figure {},# of boxes: {},{} ".format(Count + 1, len(each), ColorPair))
                # vis2.draw(each, color_index,truck_dimension,
                #           title="Figure {} levels: {},# of boxes: {},{} ".format(Count + 1, Count, count, ColorPair))

            # for each in sorted_result:

        packer.items = []
        packer.bins = []




        # for i in list(next_items.keys()):
        #     # print()
        #     packer.add_item(
        #         Item(next_items[i]['Id'], next_items[i]['name'], next_items[i]['width'], next_items[i]['height'],
        #              next_items[i]['depth'],
        #              next_items[i]['weight']))
        # packer.add_bin(Bin('large-2-box', 2, truck_dimension[0], truck_dimension[2], truck_dimension[1], 7000.0))
        # print(len(packer.items))
        # print(len(packer.unfitted_items))
        # print(len(packer.bins))
        # Count += 1


Mul_packing()
#
